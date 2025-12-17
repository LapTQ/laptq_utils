from laptq_pyutils.ops import xcycwh__to__x1y1x2y2, box_normalized__to__box_pixels
from laptq_pyutils.objects import Midas


def helper__depth__estimation(**kwargs):

    import json
    from tqdm import tqdm
    import os
    import numpy as np
    import cv2

    path__dir__img__input = kwargs["path__dir__img__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__np__output = kwargs["path__dir__np__output"]
    to_save__img = kwargs["to_save__img"]
    path__dir__img__output = kwargs["path__dir__img__output"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]

    os.makedirs(path__dir__img__output, exist_ok=True)

    model = Midas(**kwargs)

    for namef_img in tqdm(
        sorted(os.listdir(path__dir__img__input)), desc="Processing images"
    ):
        pathf_img = os.path.join(path__dir__img__input, namef_img)

        namef_lbl = namef_img.rsplit(".", 1)[0] + ".json"
        pathf_lbl = os.path.join(path__dir__lbl__input, namef_lbl)

        if not os.path.exists(pathf_lbl):
            if is_ok__lbl_not_exist:
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {pathf_lbl}")

        # Load image and label
        img_bgr = cv2.imread(pathf_img)
        with open(pathf_lbl, "r") as f:
            dict__result = json.load(f)

        H, W = img_bgr.shape[:2]

        list__obj__box_xcycwhn = np.array(
            dict__result["list__obj__box_xcycwhn"]
        ).reshape(-1, 4)
        list__obj__box_x1y1x2y2 = box_normalized__to__box_pixels(
            xcycwh__to__x1y1x2y2(list__obj__box_xcycwhn), (W, H)
        )

        for i_obj, box in enumerate(list__obj__box_x1y1x2y2):
            x1, y1, x2, y2 = box
            crop_bgr = img_bgr[y1:y2, x1:x2]

            _ = model.predict(img__bgr=crop_bgr)
            depth_map = _["depth_map"]

            pathd_output_np = os.path.join(path__dir__np__output, namef_img)
            os.makedirs(pathd_output_np, exist_ok=True)

            np.save(os.path.join(pathd_output_np, f"{i_obj}.npy"), depth_map)

            if to_save__img:
                depth_map_img = (depth_map * 255).astype(np.uint8)

                pathd_output_img = os.path.join(path__dir__img__output, namef_img)
                os.makedirs(pathd_output_img, exist_ok=True)

                cv2.imwrite(
                    os.path.join(pathd_output_img, f"{i_obj}.jpg"), depth_map_img
                )
