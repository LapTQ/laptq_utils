TO_USE_SHAPE_FROM_ = "imgsz"  # 'img' or 'imgsz'

PATHD_IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images"
POSTFIXD_IMAGE = ""
# or get filenames from labels
IMGSZ = (960, 540)  # (W, H)
# PATHD_LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--crops--from--detection"
PATHD_LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--ntu-rgbd-skeleton--to--json"
POSTFIXD_LABEL = ""

PATHD_OUTPUT = (
    "/home/laptq/laptq-fs26-shoplifting-detection/outputs/generate_background_images"
)
POSTFIX_OUTPUT = ""

TO_USE__SOFTLINK = True

MAP_SUBPATHD_TO = {
    # "shoplifting-1min_anonymized.mp4": None,
    # "R3_2025_05_15_23_40_32_rotate.mp4": None,
    # "R7_2025_05_15_23_40_32_rotate.mp4/10729": None,
    # "nturgb+d_skeletons/S011C001P015R001A024.skeleton": None,
    "nturgb+d_skeletons/S001C001P006R002A051.skeleton": None,
}


import os
from PIL import Image
import numpy as np
import cv2
from tqdm import tqdm


def generate_background_images(**kwargs):
    path__dir__img = kwargs["path__dir__img"]
    path__dir__output = kwargs["path__dir__output"]
    to_use__softlink = kwargs["to_use__softlink"]
    to_use_shape_from_ = kwargs["to_use_shape_from_"]
    imgsz = kwargs["imgsz"]
    path__dir__lbl = kwargs["path__dir__lbl"]

    assert to_use_shape_from_ in ["img", "imgsz"]

    is__1st_image__created = False
    pathf__1st_img__output = None
    pool = (
        sorted(os.listdir(path__dir__img))
        if to_use_shape_from_ == "img"
        else sorted(os.listdir(path__dir__lbl))
    )
    for namef_input in tqdm(pool):
        if to_use_shape_from_ == "img":
            namef_img_input = namef_input
            pathf_img_input = os.path.join(path__dir__img, namef_input)
            W, H = Image.open(pathf_img_input).size
        else:
            namef_img_input = namef_input.replace(".json", ".jpg")
            W, H = imgsz

        img_bg = np.full(
            (H, W, 3),
            # (255, 229, 204),
            (25, 25, 25),
            dtype=np.uint8,
        )

        pathf_img_output = os.path.join(path__dir__output, namef_img_input)
        if not is__1st_image__created:
            cv2.imwrite(pathf_img_output, img_bg)
            is__1st_image__created = True
            pathf__1st_img__output = pathf_img_output
            continue

        if to_use__softlink:
            os.system("ln -sf {} {}".format(pathf__1st_img__output, pathf_img_output))
        else:
            cv2.imwrite(pathf_img_output, img_bg)


for subpathd in MAP_SUBPATHD_TO:
    pathd_img = os.path.join(PATHD_IMAGE, subpathd, "images{}".format(POSTFIXD_IMAGE))
    pathd_output = os.path.join(
        PATHD_OUTPUT, subpathd, "images{}".format(POSTFIX_OUTPUT)
    )
    pathd_lbl = os.path.join(PATHD_LABEL, subpathd, "labels{}".format(POSTFIXD_LABEL))

    if os.path.exists(pathd_output):
        os.system("rm -rf {}".format(pathd_output))
    os.makedirs(pathd_output, exist_ok=True)

    generate_background_images(
        path__dir__img=pathd_img,
        path__dir__output=pathd_output,
        to_use__softlink=TO_USE__SOFTLINK,
        to_use_shape_from_="imgsz",
        imgsz=IMGSZ,
        path__dir__lbl=pathd_lbl,
    )

    print("Done: {}".format(subpathd))
