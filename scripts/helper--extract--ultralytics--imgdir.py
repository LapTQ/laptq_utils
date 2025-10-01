PATH__DIR__IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fs26"
POSTFIX__DIR__IMAGE = ""

TO_USE__YOLOv5_COMPAT = False
PATH__FILE__MODEL = "yolov8x-pose.pt"
# PATH__FILE__MODEL='/home/laptq/laptq-fs26-shoplifting-detection/runs/bag-detection/yolov8s--640/train/weights/best.pt'
ID__DATA = None
# ID__DATA='bag-detection'
ID__MODEL = "yolov8x-pose"
# ID__MODEL='yolov8s'
# ID__TRAIN='train'
ID__TRAIN = "exp"

IMGSZ = 640
# IMGSZ=960
THRESH__CONF__MIN = 0.1
# THRESH__CONF__MIN=0.01
THRESH__IOU = 0.45
ID__PREDICT = f"imgsz-{IMGSZ}--conf-{THRESH__CONF__MIN}--iou-{THRESH__IOU}"

DEVICE = "cuda:0"

PATH__DIR__LABEL__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/fs26"
# PATH__DIR__LABEL__OUTPUT='/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/prj54'
POSTFIX__DIR__LABEL__OUTPUT = f"--PRED--DATA--{ID__DATA}--MODEL--{ID__MODEL}--TRAIN--{ID__TRAIN}--PREDICT--{ID__PREDICT}--all-keypoints--JSON"
# POSTFIX__DIR__LABEL__OUTPUT=f"--PRED--DATA--{ID__DATA}--MODEL--{ID__MODEL}--TRAIN--{ID__TRAIN}--PREDICT--{ID__PREDICT}--JSON"

# Define the map of subpaths
# MAP__SUBPATH_DIR__TO__ = {
#     "shoplifting-25min.mp4": None,
#     "r9_25min_rotate.mp4": None,
# }
# -----
import os
import glob

MAP__SUBPATH_DIR__TO__ = {
    p[len(PATH__DIR__IMAGE) + 1 :]: None
    for p in glob.glob(f"{PATH__DIR__IMAGE}/shoplifting-awljp-demo-videos/demo_room/*.mp4")
    if os.path.isdir(p)
}

# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__extract__ultralytics__imgdir
from multiprocessing import Pool
import multiprocessing as mp
import torch
import gc


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__img']}")

    helper__extract__ultralytics__imgdir(**kwargs)

    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

    print(f"{TAG__PASSED} Done: {kwargs['path__dir__img']}")



ls_kwargs = []

for subpath__dir in MAP__SUBPATH_DIR__TO__:
    path__dir__img__input = (
        f"{PATH__DIR__IMAGE}/{subpath__dir}/images{POSTFIX__DIR__IMAGE}"
    )
    path__dir__lbl__output = (
        f"{PATH__DIR__LABEL__OUTPUT}/{subpath__dir}/labels{POSTFIX__DIR__LABEL__OUTPUT}"
    )

    if os.path.exists(path__dir__lbl__output):
        shutil.rmtree(path__dir__lbl__output)
    os.makedirs(path__dir__lbl__output)

    kwargs = dict(
        path__dir__img=path__dir__img__input,
        path__dir__output=path__dir__lbl__output,
        path__file__model=PATH__FILE__MODEL,
        device=DEVICE,
        imgsz=IMGSZ,
        thresh__conf__min=THRESH__CONF__MIN,
        thresh__iou=THRESH__IOU,
        to_use__yolov5_compat=TO_USE__YOLOv5_COMPAT,
        task="track",
        persist=True,
        list__name_keypoints=[
            "nose",
            "left_eye",
            "right_eye",
            "left_ear",
            "right_ear",
            "left_shoulder",
            "right_shoulder",
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist",
            "left_hip",
            "right_hip",
            "left_knee",
            "right_knee",
            "left_ankle",
            "right_ankle",
        ],
        thresh__conf__keypoints__min=0.0,
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(15) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
