from laptq_pyutils.log import load_logger
from laptq_pyutils.image_processing import (
    LIST__METHOD__PASTING,
    paste__simple,
    paste__cv2_seamlessClone,
)
from laptq_pyutils.ops import (
    x1y1wh__to__x1y1x2y2,
    box__leftiou,
    box_normalized__to__box_pixels,
    xcycwh__to__x1y1x2y2,
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
    thresh__leftiou__min = kwargs["thresh__leftiou__min"]
    thresh__leftiou__max = kwargs["thresh__leftiou__max"]
    num__steps = kwargs["num__steps"]

    if seed is not None:
        random.seed(seed)

    os.makedirs(path__dir__img__output, exist_ok=True)
    os.makedirs(path__dir__lbl__output, exist_ok=True)

    # get crop list
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

    # iterate through images
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

        # get bounding boxes
        list__img__obj__box_xcycwhn = np.array(
            dict__result__img["list__obj__box_xcycwhn"]
        ).reshape(-1, 4)
        list__img__obj__box_xcycwh = box_normalized__to__box_pixels(
            list__img__obj__box_xcycwhn, (img__W, img__H)
        )
        list__img__obj__box_x1y1x2y2 = xcycwh__to__x1y1x2y2(list__img__obj__box_xcycwh)

        # calculate candidate positions to paste crops
        list__roi_candidate__x1y1wh = []
        list__roi_candidate__idx_crop = []
        list__roi_candidate__idx_obj = []
        for i_obj, img__obj__box_x1y1x2y2 in enumerate(list__img__obj__box_x1y1x2y2):
            img__obj__x1, img__obj__y1, img__obj__x2, img__obj__y2 = (
                img__obj__box_x1y1x2y2
            )
            for i_crop, crop__img in enumerate(list__crop__img):
                crop__H, crop__W = crop__img.shape[:2]
                _list__roi__x1 = np.linspace(
                    img__obj__x1 - crop__W + 1,
                    img__obj__x2,
                    num__steps,
                    dtype=np.int32,
                )
                _list__roi__y1 = np.linspace(
                    img__obj__y1 - crop__H + 1,
                    img__obj__y2,
                    num__steps,
                    dtype=np.int32,
                )
                _x, _y = np.meshgrid(_list__roi__x1, _list__roi__y1)
                _list__roi__x1y1 = np.vstack([_x.ravel(), _y.ravel()]).T
                _list__roi__x1y1wh = np.concatenate(
                    [
                        _list__roi__x1y1,
                        np.ones((_list__roi__x1y1.shape[0], 1), dtype=np.int32)
                        * crop__W,
                        np.ones((_list__roi__x1y1.shape[0], 1), dtype=np.int32)
                        * crop__H,
                    ],
                    axis=1,
                )
                list__roi_candidate__x1y1wh.extend(_list__roi__x1y1wh.tolist())
                list__roi_candidate__idx_crop.extend([i_crop] * len(_list__roi__x1y1wh))
                list__roi_candidate__idx_obj.extend([i_obj] * len(_list__roi__x1y1wh))
        list__roi_candidate__x1y1x2y2 = x1y1wh__to__x1y1x2y2(
            np.array(list__roi_candidate__x1y1wh).reshape(-1, 4)
        )

        # calculate ratio of source label being occluded, using leftiou
        mat__leftiou = box__leftiou(
            list__img__obj__box_x1y1x2y2,
            list__roi_candidate__x1y1x2y2,
        )
        list__idx_roi = np.where(
            np.any(mat__leftiou >= thresh__leftiou__min, axis=0)
            & np.all(mat__leftiou <= thresh__leftiou__max, axis=0)
        )[0]

        _dict__idx = {}
        for idx__roi in list__idx_roi:
            i__obj = list__roi_candidate__idx_obj[idx__roi]
            _dict__idx.setdefault(i__obj, []).append(idx__roi)
        list__to_paste = random.choices(
            [True, False], weights=[prob, 1 - prob], k=len(list__img__obj__box_xcycwhn)
        )

        for i__obj, to_paste in enumerate(list__to_paste):
            if i__obj not in _dict__idx:
                continue
            if not to_paste:
                continue
            idx__roi = random.choice(_dict__idx[i__obj])
            i__crop = list__roi_candidate__idx_crop[idx__roi]
            crop__img = list__crop__img[i__crop]
            crop__mask = list__crop__mask[i__crop]
            roi__x1, roi__y1, roi__w, roi__h = list__roi_candidate__x1y1wh[idx__roi]
            center = (roi__x1 + roi__w // 2, roi__y1 + roi__h // 2)

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
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)
        cv2.imwrite(path__file__img__output, img)
        os.system(
            "cp '{}' '{}'".format(path__file__lbl__input, path__file__lbl__output)
        )
