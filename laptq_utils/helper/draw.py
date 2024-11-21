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
