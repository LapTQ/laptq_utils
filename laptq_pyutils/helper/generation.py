from laptq_pyutils.log import load_logger
from laptq_pyutils.image_processing import handler__paste
from laptq_pyutils.ops import (
    x1y1wh__to__x1y1x2y2,
    box__leftiou,
    box_normalized__to__box_pixels,
    xcycwh__to__x1y1x2y2,
    x1y1x2y2__to__polygon,
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
        list__paste_candidate__x1y1wh = []
        list__paste_candidate__idx_crop = []
        list__paste_candidate__idx_obj = []
        for i_obj, img__obj__box_x1y1x2y2 in enumerate(list__img__obj__box_x1y1x2y2):
            img__obj__x1, img__obj__y1, img__obj__x2, img__obj__y2 = (
                img__obj__box_x1y1x2y2
            )
            for i_crop, crop__img in enumerate(list__crop__img):
                crop__H, crop__W = crop__img.shape[:2]
                _list__paste__x1 = np.linspace(
                    img__obj__x1 - crop__W + 1,
                    img__obj__x2,
                    num__steps,
                    dtype=np.int32,
                )
                _list__paste__y1 = np.linspace(
                    img__obj__y1 - crop__H + 1,
                    img__obj__y2,
                    num__steps,
                    dtype=np.int32,
                )
                _x, _y = np.meshgrid(_list__paste__x1, _list__paste__y1)
                _list__paste__x1y1 = np.vstack([_x.ravel(), _y.ravel()]).T
                _list__paste__x1y1wh = np.concatenate(
                    [
                        _list__paste__x1y1,
                        np.ones((_list__paste__x1y1.shape[0], 1), dtype=np.int32)
                        * crop__W,
                        np.ones((_list__paste__x1y1.shape[0], 1), dtype=np.int32)
                        * crop__H,
                    ],
                    axis=1,
                )
                list__paste_candidate__x1y1wh.extend(_list__paste__x1y1wh.tolist())
                list__paste_candidate__idx_crop.extend(
                    [i_crop] * len(_list__paste__x1y1wh)
                )
                list__paste_candidate__idx_obj.extend(
                    [i_obj] * len(_list__paste__x1y1wh)
                )
        list__paste_candidate__x1y1x2y2 = x1y1wh__to__x1y1x2y2(
            np.array(list__paste_candidate__x1y1wh).reshape(-1, 4)
        )

        # calculate ratio of source label being occluded, using leftiou
        mat__leftiou = box__leftiou(
            list__img__obj__box_x1y1x2y2,
            list__paste_candidate__x1y1x2y2,
        )
        list__idx_paste = np.where(
            np.any(mat__leftiou >= thresh__leftiou__min, axis=0)
            & np.all(mat__leftiou <= thresh__leftiou__max, axis=0)
        )[0]

        _dict__idx = {}
        for idx__paste in list__idx_paste:
            i__obj = list__paste_candidate__idx_obj[idx__paste]
            _dict__idx.setdefault(i__obj, []).append(idx__paste)
        list__to_paste = random.choices(
            [True, False], weights=[prob, 1 - prob], k=len(list__img__obj__box_xcycwhn)
        )

        img__out = img.copy()
        for i__obj, to_paste in enumerate(list__to_paste):
            if i__obj not in _dict__idx:
                continue
            if not to_paste:
                continue
            idx__paste = random.choice(_dict__idx[i__obj])
            i__crop = list__paste_candidate__idx_crop[idx__paste]
            crop__img = list__crop__img[i__crop]
            crop__mask = list__crop__mask[i__crop]
            paste__x1, paste__y1, paste__w, paste__h = list__paste_candidate__x1y1wh[
                idx__paste
            ]
            center = (paste__x1 + paste__w // 2, paste__y1 + paste__h // 2)

            img__out = handler__paste(
                method=method,
                img=img__out,
                crop=crop__img,
                mask=crop__mask,
                center=center,
                flags=flags,
            )

        path__file__img__output = os.path.join(path__dir__img__output, name__file__img)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)
        cv2.imwrite(path__file__img__output, img__out)
        os.system(
            "cp '{}' '{}'".format(path__file__lbl__input, path__file__lbl__output)
        )


def helper__paste__seg_crops__over__background(**kwargs):

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
    num = kwargs["num"]
    roi__polygonn = kwargs["roi__polygonn"]
    margin__xn = kwargs["margin__xn"]
    margin__yn = kwargs["margin__yn"]
    seed = kwargs["seed"]
    method = kwargs["method"]
    flags = kwargs["flags"]

    if seed is not None:
        random.seed(seed)

    os.makedirs(path__dir__img__output, exist_ok=True)
    os.makedirs(path__dir__lbl__output, exist_ok=True)

    roi__polygonn = np.array(roi__polygonn).reshape(-1, 2)

    # get crop list
    list__crop__img = []
    list__crop__mask = []
    list__crop__wh = []
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
        list__crop__wh.append((crop__img.shape[1], crop__img.shape[0]))
    list__crop__wh = np.array(list__crop__wh).reshape(-1, 2)

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

        margin__x = int(margin__xn * img__W)
        margin__y = int(margin__yn * img__H)

        # top-left of pasted object will not be placed in the avoided regions
        list__to_avoid__box_x1y1x2y2 = (
            list__img__obj__box_x1y1x2y2
            + [-margin__x, -margin__y, margin__x, margin__y]
        ).reshape(-1, 1, 4) + np.concatenate(
            [-list__crop__wh, np.zeros_like(list__crop__wh)], axis=1
        )
        list__to_avoid__box_x1y1x2y2 = np.stack(
            [
                list__to_avoid__box_x1y1x2y2[:, :, 0].min(axis=1),
                list__to_avoid__box_x1y1x2y2[:, :, 1].min(axis=1),
                list__to_avoid__box_x1y1x2y2[:, :, 2].min(axis=1),
                list__to_avoid__box_x1y1x2y2[:, :, 3].min(axis=1),
            ],
            axis=1,
        )
        list__to_avoid__box_polygon = x1y1x2y2__to__polygon(
            list__to_avoid__box_x1y1x2y2
        )

        roi__polygon = (roi__polygonn * [img__W, img__H]).astype(int)

        mask__img = np.zeros((img__H, img__W), dtype=np.uint8)
        mask__img = cv2.fillPoly(mask__img, [roi__polygon], 255)
        for polygon in list__to_avoid__box_polygon:
            polygon = polygon.reshape(-1, 1, 2)
            cv2.fillPoly(mask__img, [polygon], 0)

        list__paste_y1x1 = random.choices(np.argwhere(mask__img == 255), k=num)
        list__idx__crop = random.choices(range(len(list__crop__img)), k=num)

        img__out = img.copy()
        for (py1, px1), idx__crop in zip(list__paste_y1x1, list__idx__crop):
            crop__img = list__crop__img[idx__crop]
            crop__mask = list__crop__mask[idx__crop]

            xc = px1 + crop__img.shape[1] // 2
            yc = py1 + crop__img.shape[0] // 2
            center = (xc, yc)

            img__out = handler__paste(
                method=method,
                img=img__out,
                crop=crop__img,
                mask=crop__mask,
                center=center,
                flags=flags,
            )

        path__file__img__output = os.path.join(path__dir__img__output, name__file__img)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)
        cv2.imwrite(path__file__img__output, img__out)
        os.system(
            "cp '{}' '{}'".format(path__file__lbl__input, path__file__lbl__output)
        )
