TO_USE_SHAPE_FROM_ = "imgsz"  # 'img' or 'imgsz'

PATHD_IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images"
POSTFIXD_IMAGE = ""
# or get filenames from labels
IMGSZ = (640, 360)  # (W, H)
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
    "nturgb+d_skeletons/S030C002P085R001A100.skeleton": None,
    "nturgb+d_skeletons/S020C003P044R001A100.skeleton": None,
    "nturgb+d_skeletons/S028C001P041R002A100.skeleton": None,
    "nturgb+d_skeletons/S030C001P044R001A100.skeleton": None,
    "nturgb+d_skeletons/S018C002P008R001A100.skeleton": None,
    "nturgb+d_skeletons/S031C001P101R001A100.skeleton": None,
    "nturgb+d_skeletons/S021C003P057R001A100.skeleton": None,
    "nturgb+d_skeletons/S029C003P048R002A100.skeleton": None,
    "nturgb+d_skeletons/S020C001P043R002A100.skeleton": None,
    "nturgb+d_skeletons/S018C003P045R002A100.skeleton": None,
    "nturgb+d_skeletons/S020C002P008R002A100.skeleton": None,
    "nturgb+d_skeletons/S019C001P051R002A100.skeleton": None,
    "nturgb+d_skeletons/S021C001P059R001A100.skeleton": None,
    "nturgb+d_skeletons/S021C003P059R001A100.skeleton": None,
    "nturgb+d_skeletons/S027C003P043R002A100.skeleton": None,
    "nturgb+d_skeletons/S027C001P086R002A100.skeleton": None,
    "nturgb+d_skeletons/S023C001P064R002A100.skeleton": None,
    "nturgb+d_skeletons/S020C003P052R002A100.skeleton": None,
    "nturgb+d_skeletons/S023C001P058R001A100.skeleton": None,
    "nturgb+d_skeletons/S029C002P067R001A100.skeleton": None,
    "nturgb+d_skeletons/S020C002P053R001A100.skeleton": None,
    "nturgb+d_skeletons/S025C002P066R001A100.skeleton": None,
    "nturgb+d_skeletons/S028C001P008R001A100.skeleton": None,
    "nturgb+d_skeletons/S024C001P067R001A102.skeleton": None,
    "nturgb+d_skeletons/S032C001P102R001A102.skeleton": None,
    "nturgb+d_skeletons/S031C001P042R002A102.skeleton": None,
    "nturgb+d_skeletons/S029C002P067R001A102.skeleton": None,
    "nturgb+d_skeletons/S025C002P059R002A102.skeleton": None,
    "nturgb+d_skeletons/S023C001P066R002A102.skeleton": None,
    "nturgb+d_skeletons/S030C001P094R002A102.skeleton": None,
    "nturgb+d_skeletons/S023C002P055R001A102.skeleton": None,
    "nturgb+d_skeletons/S028C003P070R002A102.skeleton": None,
    "nturgb+d_skeletons/S030C003P088R002A102.skeleton": None,
    "nturgb+d_skeletons/S024C003P061R002A102.skeleton": None,
    "nturgb+d_skeletons/S026C002P008R001A102.skeleton": None,
    "nturgb+d_skeletons/S019C003P050R001A102.skeleton": None,
    "nturgb+d_skeletons/S024C003P064R002A102.skeleton": None,
    "nturgb+d_skeletons/S032C001P104R002A102.skeleton": None,
    "nturgb+d_skeletons/S025C003P058R002A102.skeleton": None,
    "nturgb+d_skeletons/S024C002P060R001A102.skeleton": None,
    "nturgb+d_skeletons/S019C003P046R001A102.skeleton": None,
    "nturgb+d_skeletons/S029C003P008R001A102.skeleton": None,
    "nturgb+d_skeletons/S023C002P066R002A102.skeleton": None,
    "nturgb+d_skeletons/S026C003P050R002A102.skeleton": None,
    "nturgb+d_skeletons/S031C003P067R002A102.skeleton": None,
    "nturgb+d_skeletons/S026C003P071R002A102.skeleton": None,
    "nturgb+d_skeletons/S030C003P096R001A102.skeleton": None,
    "nturgb+d_skeletons/S032C003P043R001A102.skeleton": None,
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
