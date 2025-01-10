LIST__METHOD__PASTING = ["PASTE__SIMPLE", "PASTE__CV2_SEAMLESS_CLONE"]


def paste__simple(**kwargs):

    import cv2
    import numpy as np

    img = kwargs["img"]
    crop = kwargs["crop"]
    mask = kwargs["mask"]
    center = kwargs["center"]

    img = img.copy()
    crop__H, crop__W = crop.shape[:2]
    roi__xc, roi__yc = center

    roi__x1, roi__y1 = roi__xc - crop__W // 2, roi__yc - crop__H // 2

    roi__img = img[roi__y1 : roi__y1 + crop__H, roi__x1 : roi__x1 + crop__W]
    roi__img[np.where(mask)] = crop[np.where(mask)]
    img[roi__y1 : roi__y1 + crop__H, roi__x1 : roi__x1 + crop__W] = roi__img

    return img


def paste__cv2_seamlessClone(**kwargs):

    import cv2

    img = kwargs["img"]
    crop = kwargs["crop"]
    mask = kwargs["mask"]
    center = kwargs["center"]
    flags = kwargs["flags"]

    assert flags in [
        cv2.NORMAL_CLONE,
        cv2.MIXED_CLONE,
        cv2.MONOCHROME_TRANSFER,
    ], "Invalid flags: {}. Supported flags: {}".format(
        flags, [cv2.NORMAL_CLONE, cv2.MIXED_CLONE, cv2.MONOCHROME_TRANSFER]
    )

    img = cv2.seamlessClone(
        src=crop,
        dst=img,
        mask=mask,
        p=center,
        flags=flags,
    )

    return img


def handler__paste(**kwargs):

    method = kwargs["method"]
    img = kwargs["img"]
    crop = kwargs["crop"]
    mask = kwargs["mask"]
    center = kwargs["center"]
    flags = kwargs["flags"]

    assert (
        method in LIST__METHOD__PASTING
    ), "Invalid method: {}. Supported methods: {}".format(method, LIST__METHOD__PASTING)
    if method == "PASTE__SIMPLE":
        img = paste__simple(
            img=img,
            crop=crop,
            mask=mask,
            center=center,
        )
    elif method == "PASTE__CV2_SEAMLESS_CLONE":
        flags = eval(kwargs["flags"])
        img = paste__cv2_seamlessClone(
            img=img,
            crop=crop,
            mask=mask,
            center=center,
            flags=flags,
        )

    return img
