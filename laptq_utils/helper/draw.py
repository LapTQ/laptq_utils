from laptq_utils import *

import os
import numpy as np
from tqdm import tqdm
import cv2
import yaml
import random


def helper__visualize__detection(**kwargs):
    import warnings

    warnings.filterwarnings("ignore")

    path__dir__img = kwargs["path__dir__img"]
    path__dir__label = kwargs["path__dir__label"]
    path__dir__output = kwargs["path__dir__output"]
    path__file__class_id_to_label = kwargs["path__file__class_id_to_label"]
    num__max__img = kwargs["num__max__img"]

    os.makedirs(path__dir__output, exist_ok=True)

    with open(path__file__class_id_to_label, "r") as f:
        class_id_to_label = yaml.safe_load(f)
        kwargs["class_id_to_label"] = class_id_to_label

    list__name__img__all = os.listdir(path__dir__img)
    if num__max__img is not None:
        num_img = min(num__max__img, len(list__name__img__all))
        list__name__img = random.sample(list__name__img__all, num_img)
    else:
        list__name__img = list__name__img__all
        num_img = len(list__name__img__all)
    i_img = 0
    pbar = tqdm(total=num_img)
    while True:
        if i_img >= len(list__name__img):
            break
        name__img = list__name__img[i_img]
        i_img += 1
        path__img = os.path.join(path__dir__img, name__img)

        fname = os.path.splitext(name__img)[0]
        name__label = fname + ".txt"
        path__label = os.path.join(path__dir__label, name__label)

        # add further images if one of the sampled images are skipped
        if not os.path.exists(path__label):
            if num__max__img is not None:
                while True:
                    name_img_replaced = random.choice(list__name__img__all)
                    if name_img_replaced in list__name__img:
                        continue
                    list__name__img.append(name_img_replaced)
                    break
            continue

        img = cv2.imread(path__img)
        labels = np.loadtxt(path__label, dtype=np.float32, delimiter=" ", ndmin=2)

        # assume YOLO format
        boxes_x1y1whn = []
        class_ids = []
        for label in labels:
            id_class, xcn, ycn, wn, hn = label
            x1n, y1n = xcn - wn / 2, ycn - hn / 2
            class_ids.append(int(id_class))
            boxes_x1y1whn.append([x1n, y1n, wn, hn])

        img_visualized = visualize_frame(
            data={
                "frame_img": img,
                "boxes_x1y1whn": boxes_x1y1whn,
                "track_ids": [-1] * len(boxes_x1y1whn),
                "class_ids": class_ids,
            },
            **kwargs
        )

        path__img__output = os.path.join(path__dir__output, name__img)
        cv2.imwrite(path__img__output, img_visualized)
        pbar.update(1)



# class LoaderVideo:

#     def __init__(self, **kwargs):
#         path__file = kwargs['path__file']


def min_box_iou(a, b):
    """
    calculate the ratio between intersection area and the smaller box.
    @a: array of first bounding box in format [xmin, ymin, xmax, ymax]
    @b: array of second bounding boxes in format [xmin, ymin, xmax, ymax]
    @return: area of (a and b)/ min( area of a, area of b)
    """
    w_intsec = np.maximum(0, (np.minimum(a[2], b[2]) - np.maximum(a[0], b[0])))
    h_intsec = np.maximum(0, (np.minimum(a[3], b[3]) - np.maximum(a[1], b[1])))
    s_intsec = w_intsec * h_intsec
    s_a = (a[2] - a[0]) * (a[3] - a[1])
    s_b = (b[2] - b[0]) * (b[3] - b[1])
    return float(s_intsec) / (np.minimum(s_a, s_b))


def helper__predict__yolo__detect(**kwargs):
    path__file__input = kwargs["path__file__input"]
    cls_loader = kwargs["cls_loader"]
    path__file__output = kwargs["path__file__output"]
    path__file__checkpoint = kwargs["path__file__checkpoint"]
    device = kwargs["device"]
    imgsz = kwargs["imgsz"]
    thresh__conf_min = kwargs["thresh__conf_min"]
    list__conf = kwargs["list__conf"]
    to__filterby__miniou = kwargs["to__filterby__miniou"]
    thresh__miniou = kwargs["thresh__miniou"]
    path__file__class_id_to_label = kwargs["path__file__class_id_to_label"]

    with open(path__file__class_id_to_label, "r") as f:
        class_id_to_label = yaml.safe_load(f)
        kwargs["class_id_to_label"] = class_id_to_label

    from ultralytics import YOLO

    model = YOLO(path__file__checkpoint).to(device)

    assert len(list__conf) == len(model.names)

    os.makedirs(os.path.split(path__file__output)[0], exist_ok=True)

    cap = cv2.VideoCapture(path__file__input)
    writer = cv2.VideoWriter(
        path__file__output,
        cv2.VideoWriter_fourcc(*"mp4v"),
        cap.get(cv2.CAP_PROP_FPS),
        (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        ),
    )

    # loader = eval(cls_loader)(**kwargs)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i_f in tqdm(range(n_frames)):
        ret, frame = cap.read()
        if not ret:
            break
        results = (
            model.predict(
                source=frame,
                imgsz=imgsz,
                conf=thresh__conf_min,
                verbose=False,
            )[0]
            .cpu()
            .numpy()
        )

        boxes = results.boxes

        collecting_param = {
            "list__id_class": [],
            "list__conf": [],
            "list__xcycwhn": [],
            "list__x1y1x2y2n": [],
            "list__x1y1whn": [],
        }
        for i_b, box in enumerate(boxes):
            id_class = int(box.cls)
            xcn, ycn, wn, hn = box.xywhn[0].tolist()
            conf = float(box.conf)

            # filter by conf threshold
            if conf < list__conf[id_class]:
                continue

            x1n = xcn - wn / 2
            y1n = ycn - hn / 2
            x2n = x1n + wn
            y2n = y1n + hn

            collecting_param["list__id_class"].append(id_class)
            collecting_param["list__conf"].append(conf)
            collecting_param["list__xcycwhn"].append([xcn, ycn, wn, hn])
            collecting_param["list__x1y1x2y2n"].append([x1n, y1n, x2n, y2n])
            collecting_param["list__x1y1whn"].append([x1n, y1n, wn, hn])

        if to__filterby__miniou:
            list__index__to_remove = []
            for i_b1, (x1y1x2y2n__b1, xcycwhn__b1, id_class__b1) in enumerate(
                zip(
                    collecting_param["list__x1y1x2y2n"],
                    collecting_param["list__xcycwhn"],
                    collecting_param["list__id_class"],
                )
            ):
                for i_b2, (x1y1x2y2n__b2, xcycwhn__b2, id_class__b2) in enumerate(
                    zip(
                        collecting_param["list__x1y1x2y2n"],
                        collecting_param["list__xcycwhn"],
                        collecting_param["list__id_class"],
                    )
                ):
                    if i_b1 == i_b2:
                        continue

                    # only apply if same class
                    if id_class__b1 != id_class__b2:
                        continue

                    if min_box_iou(x1y1x2y2n__b1, x1y1x2y2n__b2) > thresh__miniou:
                        _, __, wn__b1, hn__b1 = xcycwhn__b1
                        _, __, wn__b2, hn__b2 = xcycwhn__b2
                        area__b1 = wn__b1 * hn__b1
                        area__b2 = wn__b2 * hn__b2
                        if area__b1 > area__b2:
                            list__index__to_remove.append(i_b2)
                        else:
                            list__index__to_remove.append(i_b1)

            list__index__to_keep = [
                _
                for _ in range(len(collecting_param["list__id_class"]))
                if _ not in list__index__to_remove
            ]
            for key in collecting_param:
                collecting_param[key] = [
                    collecting_param[key][_] for _ in list__index__to_keep
                ]

        img_visualized = visualize_frame(
            data={
                "frame_img": frame,
                "boxes_x1y1whn": collecting_param["list__x1y1whn"],
                "track_ids": [-1] * len(collecting_param["list__x1y1whn"]),
                "class_ids": collecting_param["list__id_class"],
                "boxes_conf": collecting_param["list__conf"],
            },
            **kwargs
        )

        writer.write(img_visualized)

    writer.release()
    cap.release()
