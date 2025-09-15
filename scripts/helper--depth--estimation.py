# Define paths and postfixes
PATH__DIR__IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fs26"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/fs26"
POSTFIX__DIR__LABEL = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"

PATH__DIR__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--depth--estimation/fs26/midas"
POSTFIX__DIR__OUTPUT = ""

# Define the map of subpaths
MAP__SUBPATH_VIDEO__TO__ = {
    "shoplifting-25min.mp4": None,
    "r9_25min_rotate.mp4": None,
}
# -----
# import os
# import glob

# MAP__SUBPATH_VIDEO__TO__ = {
#     p[len(PATH__DIR__IMAGE) + 1 :]: None
#     for p in glob.glob(f"{PATH__DIR__IMAGE}/*/*/*/*")
#     if os.path.isdir(p)
# }

# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__depth__estimation


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"

# Iterate over the subpaths
for subpath__dir in MAP__SUBPATH_VIDEO__TO__:
    path__dir__img__input = (
        f"{PATH__DIR__IMAGE}/{subpath__dir}/images{POSTFIX__DIR__IMAGE}"
    )
    path__dir__lbl__input = (
        f"{PATH__DIR__LABEL}/{subpath__dir}/labels{POSTFIX__DIR__LABEL}"
    )
    path__dir__np__output = (
        f"{PATH__DIR__OUTPUT}/{subpath__dir}/depths{POSTFIX__DIR__OUTPUT}"
    )
    path__dir__img__output = (
        f"{PATH__DIR__OUTPUT}/{subpath__dir}/depths--img{POSTFIX__DIR__OUTPUT}"
    )

    # Remove existing directories if they exist
    if os.path.exists(path__dir__np__output):
        shutil.rmtree(path__dir__np__output)
    if os.path.exists(path__dir__img__output):
        shutil.rmtree(path__dir__img__output)

    # Call the helper function
    helper__depth__estimation(
        path__dir__img__input=path__dir__img__input,
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__np__output=path__dir__np__output,
        to_save__img=True,
        path__dir__img__output=path__dir__img__output,
        is_ok__lbl_not_exist=False,
        model="MiDaS_small",  # MiDaS_small, DPT_Hybrid, DPT_Large
        device="cuda:5",
    )

    print(f"{TAG__INFO} Done: {subpath__dir}")
