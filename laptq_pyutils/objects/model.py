import sys
from abc import ABC, abstractmethod
import numpy as np
from PIL import Image
import cv2
import torch
import os
from tqdm import tqdm
from copy import deepcopy
import torchvision.transforms as T
import torch

# import tensorrt as trt
# import pycuda.driver as cuda
# import pycuda.autoinit

from laptq_pyutils.objects import ListAligner
from laptq_pyutils.ops import (
    box_normalized__to__box_pixels,
    xcycwh__to__x1y1x2y2,
)


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
        list__name_keypoints = kwargs["list__name_keypoints"]
        persist = kwargs["persist"]
        task = kwargs["task"]
        thresh__conf__keypoints__min = kwargs["thresh__conf__keypoints__min"]

        _args = {
            "source": img__bgr,
            "imgsz": imgsz,
            "conf": thresh__conf__min,
            "iou": thresh__iou,
            "verbose": False,
            "thresh__conf__keypoints__min": thresh__conf__keypoints__min,
        }
        if task == "track":
            _func = self.model.track
            _args.update({"persist": persist})
        else:
            _func = self.model.predict

        result_ultralytics = _func(**_args)[0].cpu().numpy()

        boxes = result_ultralytics.boxes
        keypoints = result_ultralytics.keypoints
        keypoints = (
            keypoints
            if keypoints is not None and keypoints.xyn.shape != (1, 0, 2)
            else [None] * len(boxes)
        )
        track_ids = (
            boxes.id
            if hasattr(boxes, "id") and boxes.id is not None
            else [None] * len(boxes)
        )

        dict__result = {
            "list__obj__id_class": [],
            "list__obj__box_xcycwhn": [],
            "list__obj__box_conf": [],
            "list__obj__kpts_xyn": [],
            "list__obj__kpts_conf": [],
            "list__obj__id_track": [],
        }

        for i_b, (id_track, box, kpts) in enumerate(zip(track_ids, boxes, keypoints)):
            id_track = int(id_track) if id_track is not None else None
            id_class = int(box.cls)
            b_xcn, b_ycn, b_wn, b_hn = box.xywhn[0].tolist()
            b_conf = float(box.conf)

            if kpts is None:
                kpts_xyn = None
                kpts_conf = None
            else:
                kpts_xyn = kpts.xyn[0].tolist()
                kpts_conf = kpts.conf[0].tolist()

            if task == "pose":
                assert len(list__name_keypoints) == len(
                    kpts_xyn
                ), f"len(list__name_keypoints)={len(list__name_keypoints)} != len(kpts_xyn)={len(kpts_xyn)}"

            dict__result["list__obj__id_class"].append(id_class)
            dict__result["list__obj__box_xcycwhn"].append([b_xcn, b_ycn, b_wn, b_hn])
            dict__result["list__obj__box_conf"].append(b_conf)
            dict__result["list__obj__kpts_xyn"].append(
                {name: [kpts_xyn[i]][0] for i, name in enumerate(list__name_keypoints)}
                if kpts_xyn is not None
                else None
            )
            dict__result["list__obj__kpts_conf"].append(
                {name: [kpts_conf[i]][0] for i, name in enumerate(list__name_keypoints)}
                if kpts_conf is not None
                else None
            )
            dict__result["list__obj__id_track"].append(id_track)

        return dict__result


class YOLOv5CompatDetectPredictor(BaseModel):

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

        return dict__result


class DFinePredictor(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        dfine_dir = kwargs["dfine_dir"]
        path__file__config = kwargs["path__file__config"]
        path__file__model = kwargs["path__file__model"]
        self.device = kwargs["device"]

        sys.path.append(dfine_dir)

        import torch.nn as nn
        from src.core import YAMLConfig

        # Load config
        # If path__file__config is not provided, we might interpret path__file__model as containing config info or
        # we might need to look for it. D-FINE usually needs a config.
        # The inference script uses -c (config) and -r (resume/weights).
        # We need both.
        if path__file__config is None:
            raise ValueError("D-FINE requires path__file__config")

        self.cfg = YAMLConfig(path__file__config, resume=path__file__model)

        if "HGNetv2" in self.cfg.yaml_cfg:
            self.cfg.yaml_cfg["HGNetv2"]["pretrained"] = False

        checkpoint = torch.load(
            path__file__model, map_location="cpu", weights_only=True
        )
        if "ema" in checkpoint:
            state = checkpoint["ema"]["module"]
        else:
            state = checkpoint["model"]

        self.cfg.model.load_state_dict(state)

        class Model(nn.Module):
            def __init__(self, cfg):
                super().__init__()
                self.model = cfg.model.deploy()
                self.postprocessor = cfg.postprocessor.deploy()

            def forward(self, images, orig_target_sizes):
                outputs = self.model(images)
                outputs = self.postprocessor(outputs, orig_target_sizes)
                return outputs

        self.model = Model(self.cfg).to(self.device)
        self.model.eval()

    def predict(self, **kwargs):

        img__bgr = kwargs["img__bgr"]
        imgsz = kwargs["imgsz"]
        thresh__conf__min = kwargs["thresh__conf__min"]

        # D-FINE preprocessing
        # It converts BGR to RGB (PIL) then resize then tensor
        # We can do it with cv2/numpy/torch

        H, W = img__bgr.shape[:2]
        img__rgb = cv2.cvtColor(img__bgr, cv2.COLOR_BGR2RGB)
        img__pil = Image.fromarray(img__rgb)

        transforms = T.Compose(
            [
                T.Resize((imgsz, imgsz)),
                T.ToTensor(),
            ]
        )

        im_data = transforms(img__pil).unsqueeze(0).to(self.device)
        orig_size = torch.tensor([[W, H]]).to(self.device)

        with torch.no_grad():
            output = self.model(im_data, orig_size)

        labels, boxes, scores = output

        # labels, boxes, scores are batched? yes, [batch_size, num_det, ...]
        # We have batch size 1

        labels = labels[0]  # [N]
        boxes = boxes[0]  # [N, 4] (x1, y1, x2, y2)
        scores = scores[0]  # [N]

        mask = scores > thresh__conf__min

        labels = labels[mask]
        boxes = boxes[mask]
        scores = scores[mask]

        list_aligner__result = ListAligner(
            list__key=[
                "list__obj__id_class",
                "list__obj__box_xcycwhn",
                "list__obj__box_conf",
            ]
        )

        if len(scores) > 0:
            labels = labels.cpu().numpy().tolist()
            boxes = boxes.cpu().numpy().tolist()
            scores = scores.cpu().numpy().tolist()

            for lbl, box, score in zip(labels, boxes, scores):
                x1, y1, x2, y2 = box
                w = x2 - x1
                h = y2 - y1
                xc = x1 + w / 2
                yc = y1 + h / 2

                xcn = xc / W
                ycn = yc / H
                wn = w / W
                hn = h / H

                list_aligner__result.extend(
                    {
                        "list__obj__id_class": [int(lbl)],
                        "list__obj__box_xcycwhn": [[xcn, ycn, wn, hn]],
                        "list__obj__box_conf": [float(score)],
                    }
                )

        dict__result = list_aligner__result.item()

        return dict__result


class TensorRTPredictor:

    def __init__(self, model_path, max_dynmic_shape):
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

            if max_dynmic_shape is not None and ts_name in max_dynmic_shape:
                ts_shape = max_dynmic_shape[ts_name]

            for s in ts_shape:
                assert (
                    s > 0
                ), f"TensorRT shape dimension for {ts_name} must be greater than 0, got {s}"
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
            self.context.set_input_shape(
                self.io_bindings[name]["name"], inputs[name].shape
            )

        self.context.execute_v2(self.allocations)

        for name in outputs:
            cuda.memcpy_dtoh(outputs[name], self.io_bindings[name]["allocation"])

        return outputs


class ONNXPredictor:

    def __init__(self, **kwargs):
        import onnxruntime as ort
        import onnx

        model_path = kwargs["model_path"]
        enable_CUDAExecutionProvider = kwargs["enable_CUDAExecutionProvider"]
        enable_CPUExecutionProvider = kwargs["enable_CPUExecutionProvider"]

        providers = []
        if enable_CUDAExecutionProvider:
            providers.append("CUDAExecutionProvider")
        if enable_CPUExecutionProvider:
            providers.append("CPUExecutionProvider")

        self.model = onnx.load(model_path)
        self.session = ort.InferenceSession(
            model_path,
            providers=providers,
        )

        onnx.checker.check_model(self.model)

    def predict(self, inputs, output_names):
        inputs = {name: np.array(inputs[name], dtype=np.float32) for name in inputs}
        outputs = self.session.run(output_names, inputs)
        return {name: outputs[i] for i, name in enumerate(output_names)}


class CLIPFeatureExtractor(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            import clip
        except:
            raise ImportError(
                "Please install clip by `pip install git+https://github.com/openai/CLIP.git`"
            )

        model = kwargs["model"]
        device = kwargs["device"]

        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        self.device = device

    def predict(self, **kwargs):
        img__bgr = kwargs["img__bgr"]

        img__pil = Image.fromarray(cv2.cvtColor(img__bgr, cv2.COLOR_BGR2RGB))
        input_ = self.preprocess(img__pil).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_feature = self.model.encode_image(input_)[0]

        image_feature = image_feature.cpu().numpy()

        return {"image_feature": image_feature}


class Midas(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        model = kwargs["model"]
        device = kwargs["device"]

        assert model in [
            "MiDaS_small",
            "DPT_Hybrid",
            "DPT_Large",
        ], f"Unsupported model: {model}"

        self.model = torch.hub.load("intel-isl/MiDaS", model)
        self.model.to(device)
        self.model.eval()

        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        if model == "DPT_Large" or model == "DPT_Hybrid":
            self.transform = midas_transforms.dpt_transform
        else:
            self.transform = midas_transforms.small_transform

        self.device = device

    def predict(self, **kwargs):

        img__bgr = kwargs["img__bgr"]

        img__rgb = cv2.cvtColor(img__bgr, cv2.COLOR_BGR2RGB)

        input_batch = self.transform(img__rgb).to(self.device)
        preds = self.model(input_batch)

        depth_map = preds[0].detach().cpu().numpy()
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())

        depth_map = cv2.resize(
            depth_map,
            (img__bgr.shape[1], img__bgr.shape[0]),
            interpolation=cv2.INTER_CUBIC,
        )

        return {
            "depth_map": depth_map,
        }


def batch_inference_topdown(model, list_img, list_bboxes, bbox_format="xyxy"):
    """Inference multiple images with a top-down pose estimator.

    Args:
        model (nn.Module): The top-down pose estimator
        list_img (List[np.ndarray]): List of loaded images to inference
        list_bboxes (List[np.ndarray]): List of bboxes for each image.
            Each element is an array of shape (N, 4) for N objects in that image
        bbox_format (str): The bbox format indicator. Options are ``'xywh'``
            and ``'xyxy'``. Defaults to ``'xyxy'``

    Returns:
        List[List[PoseDataSample]]: The inference results for each image.
    """
    from mmpose.structures.bbox import bbox_xywh2xyxy
    from mmpose.structures import PoseDataSample
    from mmengine.dataset import Compose, pseudo_collate
    from mmengine.registry import init_default_scope
    import torch

    scope = model.cfg.get("default_scope", "mmpose")
    if scope is not None:
        init_default_scope(scope)
    pipeline = Compose(model.cfg.test_dataloader.dataset.pipeline)

    assert bbox_format in {"xyxy", "xywh"}, f'Invalid bbox_format "{bbox_format}".'

    # Construct batch data samples for all images and all bboxes
    data_list = []
    frame_bbox_counts = []

    for img, bboxes in zip(list_img, list_bboxes):
        if bboxes is None or len(bboxes) == 0:
            # Get bbox from the image size
            h, w = img.shape[:2]
            bboxes = np.array([[0, 0, w, h]], dtype=np.float32)
        else:
            if isinstance(bboxes, list):
                bboxes = np.array(bboxes)

            if bbox_format == "xywh":
                bboxes = bbox_xywh2xyxy(bboxes)

        frame_bbox_counts.append(len(bboxes))

        for bbox in bboxes:
            data_info = dict(img=img)
            data_info["bbox"] = bbox[None]  # shape (1, 4)
            data_info["bbox_score"] = np.ones(1, dtype=np.float32)  # shape (1,)
            data_info.update(model.dataset_meta)
            data_list.append(pipeline(data_info))

    if data_list:
        # Collate data list into a batch
        batch = pseudo_collate(data_list)
        with torch.no_grad():
            results = model.test_step(batch)
    else:
        results = []

    # Split results back into per-image lists
    list_results = []
    start_idx = 0
    for count in frame_bbox_counts:
        list_results.append(results[start_idx : start_idx + count])
        start_idx += count

    return list_results


class RTMPosePredictor:
    def __init__(self, **kwargs):
        from mmpose.apis import init_model

        path__file__config = kwargs["path__file__config"]
        path__file__model = kwargs["path__file__model"]
        device = kwargs["device"]

        self.pose_estimator = init_model(path__file__config, path__file__model, device)

    def predict_batch(self, **kwargs):
        list_img__bgr = kwargs["list_img__bgr"]
        list_dict__result = kwargs["list_dict__result"]
        list__name_keypoints = kwargs["list__name_keypoints"]

        # Collect all bboxes for each frame
        list_bboxes = []

        for img__bgr, dict__result in zip(list_img__bgr, list_dict__result):
            H, W = img__bgr.shape[:2]

            list__obj__box_xcycwhn = np.array(
                dict__result["list__obj__box_xcycwhn"]
            ).reshape(-1, 4)
            list__obj__box_x1y1x2y2 = box_normalized__to__box_pixels(
                xcycwh__to__x1y1x2y2(list__obj__box_xcycwhn), (W, H)
            )

            list_bboxes.append(list__obj__box_x1y1x2y2)

        # Batch inference on all images
        list_poses = batch_inference_topdown(
            self.pose_estimator,
            list_img__bgr,
            list_bboxes,
            bbox_format="xyxy",
        )

        # Store keypoints per frame for return value
        list_list_keypoints = []

        # Process results for each frame
        for frame_idx, (
            img__bgr,
            dict__result,
            list__obj__box_x1y1x2y2,
            poses,
        ) in enumerate(zip(list_img__bgr, list_dict__result, list_bboxes, list_poses)):
            H, W = img__bgr.shape[:2]

            list_keypoints = []
            for pose in poses:
                keypoints = pose.get("pred_instances").get("keypoints")[0]
                scores = (
                    pose.get("pred_instances").get("keypoint_scores")[0].reshape(-1, 1)
                )
                pose_result = np.concatenate((keypoints, scores), axis=1)
                # print(keypoints.shape, scores.shape, pose_result.shape)
                list_keypoints.append(pose_result)

            list__obj__kpts_xyn = []
            list__obj__kpts_conf = []
            if (
                len(list__obj__box_x1y1x2y2) > 0
            ):  # the inference function returns at-least 1 pose even if no boxes is provided
                for i_obj, kpts in enumerate(list_keypoints):
                    kpts_xyn = kpts[:, :2] / [W, H]
                    kpts_conf = kpts[:, 2]
                    list__obj__kpts_xyn.append(
                        {
                            name: kpt.tolist()
                            for name, kpt in zip(list__name_keypoints, kpts_xyn)
                        }
                    )
                    list__obj__kpts_conf.append(
                        {
                            name: conf.item()
                            for name, conf in zip(list__name_keypoints, kpts_conf)
                        }
                    )

            dict__result["list__obj__kpts_xyn"] = list__obj__kpts_xyn
            dict__result["list__obj__kpts_conf"] = list__obj__kpts_conf
            list_list_keypoints.append(list_keypoints)

        # Return single list if input was single image, otherwise return list of lists
        if len(list_img__bgr) == 1:
            return list_list_keypoints[0]
        else:
            return list_list_keypoints


class MajorVoteActionPredictor:
    def __init__(self, **kwargs):
        self.ls__dict__result__not_voted = []
        self.ls__dict__result__voted = []

    def append(self, **kwargs):
        dict__result = kwargs["dict__result"]
        self.ls__dict__result__not_voted.append(deepcopy(dict__result))
        self.ls__dict__result__voted.append(dict__result)  # to write in-place

    def predict(self, **kwargs):
        idx = kwargs["idx"]
        step_size = kwargs["step_size"]
        left_window = kwargs["left_window"]
        right_window = kwargs["right_window"]
        ls__id_action__prioritized = kwargs["ls__id_action__prioritized"]
        min_votes_threshold = kwargs["min_votes_threshold"]
        unconfirmed__id_action = kwargs["unconfirmed__id_action"]

        dict__result__not_voted = self.ls__dict__result__not_voted[idx]
        dict__result__voted = self.ls__dict__result__voted[idx]

        list__obj__id_track = dict__result__not_voted["list__obj__id_track"]

        list__obj__action_status__voted = dict__result__voted[
            "list__obj__action_status"
        ]
        list__obj__action_conf__voted = dict__result__voted["list__obj__action_conf"]

        # # debug
        # print("Before voting:", list__obj__action_status__in, list__obj__action_conf__in)

        # For each object in the current frame
        for i_obj, id_track in enumerate(list__obj__id_track):

            # Get window bounds
            window_start = max(0, idx - left_window * step_size)
            window_end = min(
                len(self.ls__dict__result__not_voted) - 1,
                idx + right_window * step_size,
            )

            # Collect votes and confidence values for this track within the window
            votes = {id_action: 0 for id_action in ls__id_action__prioritized}
            conf_values = {id_action: [] for id_action in ls__id_action__prioritized}

            for i_w in range(window_start, window_end + 1, step_size):
                w__dict__result__input = self.ls__dict__result__not_voted[i_w]

                w__list__obj__id_track = w__dict__result__input["list__obj__id_track"]

                if id_track in w__list__obj__id_track:
                    track_idx = w__list__obj__id_track.index(id_track)

                    # Get action status for this track in this window frame
                    for id_action in ls__id_action__prioritized:
                        if (
                            w__dict__result__input["list__obj__action_status"][
                                id_action
                            ][track_idx]
                            is True
                        ):
                            votes[id_action] += 1
                            conf = w__dict__result__input["list__obj__action_conf"][
                                id_action
                            ][track_idx]
                            if conf is not None:
                                conf_values[id_action].append(conf)

            # # debug
            # print(votes)

            # Determine majority action
            max_votes = max(votes.values())
            if max_votes > 0:  # If we have any votes
                # In case of a tie, prioritize
                for id_action in ls__id_action__prioritized:
                    if votes[id_action] == max_votes:
                        if max_votes >= min_votes_threshold:
                            majority_action = id_action
                        else:
                            majority_action = unconfirmed__id_action
                        break

                # Update action status
                for id_action in ls__id_action__prioritized:
                    list__obj__action_status__voted[id_action][i_obj] = (
                        majority_action == id_action
                    )

                # Update confidence values based on majority class
                for id_action in ls__id_action__prioritized:
                    if len(conf_values[id_action]):
                        list__obj__action_conf__voted[id_action][i_obj] = float(
                            np.mean(conf_values[id_action])
                        )
                    else:
                        list__obj__action_conf__voted[id_action][i_obj] = None
