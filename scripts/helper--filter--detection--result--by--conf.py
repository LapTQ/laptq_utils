PATH__DIR__LABEL__INPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--filter--detection--result--by--roi/fs26/satudora"
POSTFIX__DIR__LABEL__INPUT = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--filter-roi--all-keypoints--JSON"

PATH__DIR__LABEL__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--filter--detection--result--by--conf/fs26/satudora"
POSTFIX__DIR__LABEL__OUTPUT = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--filter-roi--filter-conf-0.4--all-keypoints--JSON"

MAP__SUBPATH_DIR__TO__ = {
    "R3_2025_05_15_23_40_32_rotate.mp4": None,
    "R4_2025_05_15_23_40_32_rotate.mp4": None,
    "R7_2025_05_15_23_40_32_rotate.mp4": None,
    "R8_2025_05_15_23_40_32_rotate.mp4": None,
    "R9_2025_05_15_23_40_32_rotate.mp4": None,
    "R10_2025_05_15_23_40_32_rotate.mp4": None,
}


# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__filter__detection__result__by__conf
from multiprocessing import Pool
import multiprocessing as mp


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__lbl__input']}")
    helper__filter__detection__result__by__conf(**kwargs)
    print(f"{TAG__PASSED} Done: {kwargs['path__dir__lbl__input']}")

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

    if os.path.exists(path__dir__lbl__output):
        shutil.rmtree(path__dir__lbl__output)
    os.makedirs(path__dir__lbl__output)

    kwargs = dict(
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__lbl__output=path__dir__lbl__output,
        map__id_class__to__thresh_conf={0: 0.4},
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(15) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
