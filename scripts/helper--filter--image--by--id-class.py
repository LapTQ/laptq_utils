# actually, I just remove the label files. So you should create symblink to image corresponding to the accepted labels
PATH__DIR__LABEL__INPUT = "/home/laptq/laptq_utils/outputs/fs26/helper--extract--detection"
POSTFIX__DIR__LABEL__INPUT = "--PRED--DATA--None--MODEL--dfine_x_obj2coco--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--only-person--conf-0.4--filter-size--filter-nms--JSON"

PATH__DIR__LABEL__OUTPUT = "/home/laptq/laptq_utils/outputs/fs26/helper--extract--detection"
POSTFIX__DIR__LABEL__OUTPUT = "--PRED--DATA--None--MODEL--dfine_x_obj2coco--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--only-person--conf-0.4--filter-size--filter-nms--contain-person--JSON"

# Define the map of subpaths
# MAP__SUBPATH_DIR__TO__ = {
#     "shoplifting-25min.mp4": None,
#     "r9_25min_rotate.mp4": None,
# }
# -----
import os
import glob

MAP__SUBPATH_DIR__TO__ = {
    p[len(PATH__DIR__LABEL__INPUT) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL__INPUT}/*/*/*.mp4"
    )
    if os.path.isdir(p)
}


# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__filter__image__by__id_class
from multiprocessing import Pool
import multiprocessing as mp


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__lbl__input']}")
    helper__filter__image__by__id_class(**kwargs)

    if not os.path.exists(kwargs["path__dir__lbl__output"]):
        print(
            f"{TAG__FAILED} The output {kwargs['path__dir__lbl__output']} not existed"
        )
        exit(1)
    else:
        # Optional: Count files similar to your sample if needed
        num__lbl__output = len(os.listdir(kwargs["path__dir__lbl__output"]))
        print(
            f"{TAG__PASSED} Done: Output generated with {num__lbl__output} labels: {kwargs['path__dir__lbl__output']}"
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
        list__id_class__to_include_any=[0],
        list__id_class__to_include_all=None,
        list__id_class__to_exclude=[],
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(15) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================