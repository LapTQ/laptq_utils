PATH__DIR__LABEL__INPUT = "/home/laptq/laptq_utils/outputs/fs26/helper--extract--detection"
POSTFIX__DIR__LABEL__INPUT = "--PRED--DATA--None--MODEL--dfine_x_obj2coco--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--only-person--conf-0.4--filter-size--JSON"

PATH__DIR__LABEL__OUTPUT = "/home/laptq/laptq_utils/outputs/fs26/helper--extract--detection"
POSTFIX__DIR__LABEL__OUTPUT = "--PRED--DATA--None--MODEL--dfine_x_obj2coco--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--only-person--conf-0.4--filter-size--filter-nms--JSON"

# -----
import os
import glob

MAP__SUBPATH_DIR__TO__ = {
    p[len(PATH__DIR__LABEL__INPUT) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL__INPUT}/*/*.mp4"
    )
    if os.path.isdir(p)
} | {
    p[len(PATH__DIR__LABEL__INPUT) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL__INPUT}/*.mp4"
    )
    if os.path.isdir(p)
}


# =============================================================
import multiprocessing as mp
import os
import shutil
from multiprocessing import Pool

from laptq_pyutils.helper import helper__filter__detection__result__by__nms

# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__lbl__input']}")

    # Call the python function directly
    helper__filter__detection__result__by__nms(**kwargs)

    print(f"{TAG__PASSED} Done processing: {kwargs['path__dir__lbl__input']}")

    # Verification Logic
    num__lbl__input = len(os.listdir(kwargs["path__dir__lbl__input"]))
    num__lbl__output = len(os.listdir(kwargs["path__dir__lbl__output"]))

    if num__lbl__output != num__lbl__input:
        print(
            f"{TAG__FAILED} Number of labels mismatched: {kwargs['path__dir__lbl__input']}"
        )
        print(f"    [+] {num__lbl__input} old labels")
        print(f"    [+] {num__lbl__output} new labels")
        exit(1)
    else:
        print(
            f"{TAG__PASSED} {num__lbl__input} old labels == {num__lbl__output} target labels: {kwargs['path__dir__lbl__input']}"
        )


ls_kwargs = []

for subpath__dir in MAP__SUBPATH_DIR__TO__:
    path__dir__lbl__input = (
        f"{PATH__DIR__LABEL__INPUT}/{subpath__dir}/labels{POSTFIX__DIR__LABEL__INPUT}"
    )
    path__dir__lbl__output = (
        f"{PATH__DIR__LABEL__OUTPUT}/{subpath__dir}/labels{POSTFIX__DIR__LABEL__OUTPUT}"
    )

    # Clean and create output directory
    if os.path.exists(path__dir__lbl__output):
        shutil.rmtree(path__dir__lbl__output)
    os.makedirs(path__dir__lbl__output)

    kwargs = dict(
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__lbl__output=path__dir__lbl__output,
        iou__mode="miniou", # iou miniou
        thresh=0.9,
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(15) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
