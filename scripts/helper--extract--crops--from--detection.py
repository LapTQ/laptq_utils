# Define paths and postfixes
PATH__DIR__IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fs26"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/fs26"
POSTFIX__DIR__LABEL = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--RTMPose--JSON"
# POSTFIX__DIR__LABEL = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--RTMPose--JSON"

PATH__DIR__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--crops--from--detection/fs26"
POSTFIX__DIR__OUTPUT = ""

# Define the map of subpaths
# MAP__SUBPATH_VIDEO__TO__ = {
#     "shoplifting-25min.mp4": None,
#     "r9_25min_rotate.mp4": None,
# }
# -----
import os
import glob

MAP__SUBPATH_VIDEO__TO__ = {
    p[len(PATH__DIR__LABEL) + 1 :]: None
    for p in glob.glob(f"{PATH__DIR__LABEL}/shoplifting-awlrecord-videos/*/*.mp4")
    if os.path.isdir(p)
}

# =============================================================
import os
import subprocess
from laptq_pyutils.helper import helper__extract__crops__from__detection
from multiprocessing import Pool
import multiprocessing as mp


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__img__input']}")

    helper__extract__crops__from__detection(**kwargs)

    print(f"{TAG__PASSED} Done: {kwargs['path__dir__img__input']}")


ls_kwargs = []

# Iterate over the subpaths
for subpath__dir in MAP__SUBPATH_VIDEO__TO__:
    path__dir__img__input = (
        f"{PATH__DIR__IMAGE}/{subpath__dir}/images{POSTFIX__DIR__IMAGE}"
    )
    path__dir__lbl__input = (
        f"{PATH__DIR__LABEL}/{subpath__dir}/labels{POSTFIX__DIR__LABEL}"
    )
    path__dir__crop__img__output = (
        f"{PATH__DIR__OUTPUT}/{subpath__dir}/{{}}/images{POSTFIX__DIR__OUTPUT}"
    )
    path__dir__crop__lbl__output = (
        f"{PATH__DIR__OUTPUT}/{subpath__dir}/{{}}/labels{POSTFIX__DIR__OUTPUT}"
    )

    # Remove existing directories if they exist
    if os.path.exists(path__dir__crop__img__output):
        os.rmdir(path__dir__crop__img__output)
    if os.path.exists(path__dir__crop__lbl__output):
        os.rmdir(path__dir__crop__lbl__output)

    # Create directories if they don't contain "{}"
    if "{}" not in path__dir__crop__img__output:
        os.makedirs(path__dir__crop__img__output, exist_ok=True)
    if "{}" not in path__dir__crop__lbl__output:
        os.makedirs(path__dir__crop__lbl__output, exist_ok=True)

    kwargs = dict(
        path__dir__img__input=path__dir__img__input,
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__crop__img__output=path__dir__crop__img__output,
        path__dir__crop__lbl__output=path__dir__crop__lbl__output,
        is_ok__lbl_not_exist=False,
        num__pad__0=6,
        to_resize_box__wrt__pose=True,
        to_shift__coords__wrt__box=True,
        to_save__img=True,
        split_by="id__track",  # "id__track" # if not None, please add a "/{}" before /images and /labels assuming there's an /images and /labels in path__dir__crop__img__output and path__dir__crop__lbl__output
    )

    ls_kwargs.append(kwargs)


# ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ multi-process run ============
# mp.set_start_method("spawn", force=True)

with Pool(10) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
