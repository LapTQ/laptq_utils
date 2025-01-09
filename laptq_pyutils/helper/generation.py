from laptq_pyutils.log import load_logger
from laptq_pyutils.image_processing import (
    LIST__METHOD__PASTING,
    paste__simple,
    paste__cv2_seamlessClone,
)


LOGGER = load_logger()


def helper__paste__seg_crops__over__det_boxes(**kwargs):

    import os
    import cv2
    import numpy as np
    from tqdm import tqdm
    import json
    import random

    path__dir__img__input = kwargs["path__dir__img__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__crop__img__input = kwargs["path__dir__crop__img__input"]
    path__dir__crop__mask__input = kwargs["path__dir__crop__mask__input"]
    path__dir__crop__lbl__input = kwargs["path__dir__crop__lbl__input"]
    path__dir__img__output = kwargs["path__dir__img__output"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    prob = kwargs["prob"]
    seed = kwargs["seed"]
    method = kwargs["method"]
    flags = kwargs["flags"]

    if seed is not None:
        random.seed(seed)

    os.makedirs(path__dir__img__output, exist_ok=True)
    os.makedirs(path__dir__lbl__output, exist_ok=True)

    list__crop__img = []
    list__crop__mask = []
    for name__file__crop__img in tqdm(sorted(os.listdir(path__dir__crop__img__input))):
        path__file__crop__img = os.path.join(
            path__dir__crop__img__input, name__file__crop__img
        )
        path__file__crop__mask = os.path.join(
            path__dir__crop__mask__input, name__file__crop__img
        )
        crop__img = cv2.imread(path__file__crop__img)
        crop__mask = cv2.imread(path__file__crop__mask, cv2.IMREAD_GRAYSCALE)
        if len(np.unique(crop__mask)) == 2:
            LOGGER.warning("Mask is not binary")
            _, crop__mask = cv2.threshold(crop__mask, 127, 255, cv2.THRESH_BINARY)
        list__crop__img.append(crop__img)
        list__crop__mask.append(crop__mask)

    for name__file__img in tqdm(sorted(os.listdir(path__dir__img__input))):
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__img__input = os.path.join(path__dir__img__input, name__file__img)
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)

        if not os.path.exists(path__file__lbl__input):
            if not is_ok__lbl_not_exist:
                raise FileNotFoundError(
                    "File not found: {}".format(path__file__lbl__input)
                )
            else:
                continue

        img = cv2.imread(path__file__img__input)
        img__H, img__W = img.shape[:2]
        with open(path__file__lbl__input, "r") as f:
            dict__result__img = json.load(f)

        list__img__obj__box_xcycwhn = dict__result__img["list__obj__box_xcycwhn"]
        list__to_paste = random.choices(
            [True, False], weights=[prob, 1 - prob], k=len(list__img__obj__box_xcycwhn)
        )

        for i_obj, (obj__box_xcycwhn, to_paste) in enumerate(
            zip(list__img__obj__box_xcycwhn, list__to_paste)
        ):
            if not to_paste:
                continue

            obj__xcn, obj__ycn, obj__wn, obj__hn = obj__box_xcycwhn
            obj__xc, obj__yc, obj__w, obj__h = (
                int(obj__xcn * img__W),
                int(obj__ycn * img__H),
                int(obj__wn * img__W),
                int(obj__hn * img__H),
            )
            obj__x1, obj__y1 = obj__xc - obj__w // 2, obj__yc - obj__h // 2
            obj__x2, obj__y2 = obj__x1 + obj__w, obj__y1 + obj__h
            
            # center = (obj__xc, obj__yc)
            center = random.choice([(obj__x1, obj__y1), (obj__x1, obj__y2), (obj__x2, obj__y2), (obj__x2, obj__y1)])

            idx__crop = random.randint(0, len(list__crop__img) - 1)
            crop__img = list__crop__img[idx__crop]
            crop__mask = list__crop__mask[idx__crop]

            assert (
                method in LIST__METHOD__PASTING
            ), "Invalid method: {}. Supported methods: {}".format(
                method, LIST__METHOD__PASTING
            )
            if method == "PASTE__SIMPLE":
                img = paste__simple(
                    img=img,
                    crop=crop__img,
                    mask=crop__mask,
                    center=center,
                )
            elif method == "PASTE__CV2_SEAMLESS_CLONE":
                flags = eval(kwargs["flags"])
                img = paste__cv2_seamlessClone(
                    img=img,
                    crop=crop__img,
                    mask=crop__mask,
                    center=center,
                    flags=flags,
                )

        path__file__img__output = os.path.join(path__dir__img__output, name__file__img)
        cv2.imwrite(path__file__img__output, img)
