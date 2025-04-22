from abc import ABC, abstractmethod
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

from laptq_pyutils.objects import ListAligner


class BaseModel(ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def predict(self, **kwargs):
        pass


class UltralyticsPredictor(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from ultralytics import YOLO

        self.path__file__model = kwargs["path__file__model"]
        self.device = kwargs["device"]

        self.model = YOLO(self.path__file__model).to(self.device)

    def predict(self, **kwargs):

        img__bgr = kwargs["img__bgr"]
        imgsz = kwargs["imgsz"]
        thresh__conf__min = kwargs["thresh__conf__min"]
        thresh__iou = kwargs["thresh__iou"]

        result_ultralytics = (
            self.model.predict(
                source=img__bgr,
                imgsz=imgsz,
                conf=thresh__conf__min,
                iou=thresh__iou,
                verbose=False,
            )[0]
            .cpu()
            .numpy()
        )

        boxes = result_ultralytics.boxes

        list_aligner__result = ListAligner(
            list__key=[
                "list__obj__id_class",
                "list__obj__box_xcycwhn",
                "list__obj__box_conf",
            ]
        )

        for i_b, box in enumerate(boxes):
            id_class = int(box.cls)
            xcn, ycn, wn, hn = box.xywhn[0].tolist()
            conf = float(box.conf)

            list_aligner__result.extend(
                {
                    "list__obj__id_class": [id_class],
                    "list__obj__box_xcycwhn": [[xcn, ycn, wn, hn]],
                    "list__obj__box_conf": [conf],
                }
            )

        dict__result = list_aligner__result.item()

        return {
            "dict__result": dict__result,
        }


class YOLOv5CompatPredictor(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        import torch

        self.path__file__model = kwargs["path__file__model"]
        self.device = kwargs["device"]

        self.model = torch.hub.load(
            repo_or_dir="ultralytics/yolov5",
            model="custom",  # e.g., 'yolov5n', 'yolov5x6', or 'custom'
            path=self.path__file__model,
            device=self.device,
        )

    def predict(self, **kwargs):

        import cv2

        img__bgr = kwargs["img__bgr"]
        imgsz = kwargs["imgsz"]
        thresh__conf__min = kwargs["thresh__conf__min"]
        thresh__iou = kwargs["thresh__iou"]

        assert hasattr(self.model, "conf"), "self.model does not have attribute conf"
        assert hasattr(self.model, "iou"), "self.model does not have attribute iou"

        self.model.conf = thresh__conf__min
        self.model.iou = thresh__iou

        img__rgb = cv2.cvtColor(img__bgr, cv2.COLOR_BGR2RGB)
        imH, imW = img__bgr.shape[:2]

        result_ultralytics = self.model(img__rgb, size=imgsz).pandas().xyxy[0]

        list_aligner__result = ListAligner(
            list__key=[
                "list__obj__id_class",
                "list__obj__box_xcycwhn",
                "list__obj__box_conf",
            ]
        )

        for i_b, box in result_ultralytics.iterrows():
            id_class = int(box["class"])
            x1, y1, x2, y2 = box[["xmin", "ymin", "xmax", "ymax"]].tolist()
            conf = float(box["confidence"])

            xc = (x1 + x2) / 2
            yc = (y1 + y2) / 2
            w = x2 - x1
            h = y2 - y1

            xcn = xc / imW
            ycn = yc / imH
            wn = w / imW
            hn = h / imH

            list_aligner__result.extend(
                {
                    "list__obj__id_class": [id_class],
                    "list__obj__box_xcycwhn": [[xcn, ycn, wn, hn]],
                    "list__obj__box_conf": [conf],
                }
            )

        dict__result = list_aligner__result.item()

        return {
            "dict__result": dict__result,
        }


class TensorRTPredictor:

    def __init__(self, model_path):
        self.logger = trt.Logger(trt.Logger.INFO)

        with open(model_path, "rb") as f, trt.Runtime(self.logger) as runtime:
            self.model = runtime.deserialize_cuda_engine(f.read())
        self.context = self.model.create_execution_context()

        self.io_bindings = {}
        self.allocations = []
        for i_ts in range(self.model.num_io_tensors):
            ts_name = self.model.get_tensor_name(i_ts)
            ts_dtype = self.model.get_tensor_dtype(ts_name)
            ts_shape = self.model.get_tensor_shape(ts_name)
            ts_size = np.dtype(trt.nptype(ts_dtype)).itemsize
            for s in ts_shape:
                ts_size *= s
            allocation = cuda.mem_alloc(ts_size)
            binding = {
                "index": i_ts,
                "name": ts_name,
                "dtype": np.dtype(trt.nptype(ts_dtype)),
                "shape": list(ts_shape),
                "allocation": allocation,
            }
            self.allocations.append(allocation)
            self.io_bindings[ts_name] = binding

    def predict(self, inputs, output_names):
        """
        Parameters
        ----------
        inputs : dict
            Dictionary of input names and their corresponding value (numpy arrays).
        output_names : list
            List of output names to be returned.

        Returns
        -------
        outputs : dict
            Dictionary of output names and their corresponding value (numpy arrays).
        """

        inputs = {
            name: np.array(inputs[name], dtype=self.io_bindings[name]["dtype"])
            for name in inputs
        }
        outputs = {
            name: np.zeros(
                self.io_bindings[name]["shape"], dtype=self.io_bindings[name]["dtype"]
            )
            for name in output_names
        }

        for name in inputs:
            cuda.memcpy_htod(
                self.io_bindings[name]["allocation"], np.ascontiguousarray(inputs[name])
            )
        self.context.execute_v2(self.allocations)
        for name in outputs:
            cuda.memcpy_dtoh(outputs[name], self.io_bindings[name]["allocation"])
        return outputs
