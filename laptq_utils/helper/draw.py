from laptq_utils import *

import os
import numpy as np
from tqdm import tqdm
import cv2
import yaml


def helper__visualize__detection(**kwargs):
    import warnings

    warnings.filterwarnings("ignore")

    path__dir__img = kwargs["path__dir__img"]
    path__dir__annot = kwargs["path__dir__annot"]
    path__dir__output = kwargs["path__dir__output"]
    path__file__class_id_to_label = kwargs["path__file__class_id_to_label"]

    os.makedirs(path__dir__output, exist_ok=True)

    with open(path__file__class_id_to_label, "r") as f:
        class_id_to_label = yaml.safe_load(f)
        kwargs["class_id_to_label"] = class_id_to_label

    for name__img in tqdm(os.listdir(path__dir__img)):
        path__img = os.path.join(path__dir__img, name__img)

        fname = os.path.splitext(name__img)[0]
        name__annot = fname + ".txt"
        path__annot = os.path.join(path__dir__annot, name__annot)

        if not os.path.exists(path__annot):
            continue

        img = cv2.imread(path__img)
        labels = np.loadtxt(path__annot, dtype=np.float32, delimiter=" ", ndmin=2)

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
