from laptq_pyutils.log import load_logger
from laptq_pyutils.image_processing import (
    LIST__METHOD__PASTING,
    paste__simple,
    paste__cv2_seamlessClone,
)
from laptq_pyutils.ops import x1y1wh__to__x1y1x2y2, box__iou__left


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

        list__img__obj__box_xcycwhn = dict__result__img["list__obj__box_xcycwhn"]
        list__to_paste = random.choices(
            [True, False], weights=[prob, 1 - prob], k=len(list__img__obj__box_xcycwhn)
        )

        # consider each box
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

            # select a crop to paste
            idx__crop = random.randint(0, len(list__crop__img) - 1)
            crop__img = list__crop__img[idx__crop]
            crop__mask = list__crop__mask[idx__crop]

            # calculate a good position to paste
            crop__H, crop__W = crop__img.shape[:2]
            _list__x1 = np.arange(-crop__W + 1, img__W)
            _list__y1 = np.arange(-crop__H + 1, img__H)
            _list__x1, _list__y1 = np.meshgrid(_list__x1, _list__y1)
            _list__x1y1 = np.vstack([_list__x1.ravel(), _list__y1.ravel()]).T
            list__roi_candidate__x1y1wh = np.concatenate(
                [
                    _list__x1y1,
                    np.ones((_list__x1y1.shape[0], 1), dtype=np.int32) * crop__W,
                    np.ones((_list__x1y1.shape[0], 1), dtype=np.int32) * crop__H,
                ],
                axis=1,
            ).reshape(-1, 4)
            list__roi_candidate__x1y1x2y2 = x1y1wh__to__x1y1x2y2(
                list__roi_candidate__x1y1wh
            )
            mat__iou = box__iou__left(
                np.array([[obj__x1, obj__y1, obj__x2, obj__y2]]),
                list__roi_candidate__x1y1x2y2,
            )
            list__idx = np.where(
                (mat__iou >= thresh__leftiou__min) & (mat__iou <= thresh__leftiou__max)
            )[1]
            if len(list__idx) == 0:
                continue
            idx_center = random.choice(list__idx)
            roi__x1, roi__y1, roi__w, roi__h = list__roi_candidate__x1y1wh[idx_center]
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
