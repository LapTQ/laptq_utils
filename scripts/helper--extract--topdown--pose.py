# RTMPose runs OK with:
# nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
# torch                    2.0.0+cu118
# torchaudio               2.0.1+cu118
# torchvision              0.15.1+cu118
# mmcv                     2.0.1
# mmdet                    3.3.0
# mmengine                 0.10.7
# mmpose                   1.3.2
# pip uninstall mmcv-full && mim uninstall mmpose mmdet mmcv mmengine && mim install mmengine && mim install --trusted-host download.openmmlab.com mmcv==2.0.1 && mim install --trusted-host download.openmmlab.com mmdet==3.3.0 && mim install --trusted-host download.openmmlab.com mmpose==1.3.2 && pip install numpy==1.26.4

PATHD_MEDIA = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fs26"
# PATHD_MEDIA = "/mnt/ssd2/shared_workspace/cuongdh/FSPRJ26/data/250516/rotate"
# PATHD_MEDIA='/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/prj54'
POSTFIX_IMAGE = ""

PATHD_LABEL_INPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics/fs26"
# PATHD_LABEL_INPUT='/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics/prj54'
POSTFIX_LABEL_INPUT = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"

PATH__FILE__MODEL = "/home/laptq/laptq-fs26-shoplifting-detection/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.pth"
PATH__FILE__CONFIG = "/home/laptq/laptq-fs26-shoplifting-detection/submodules/laptq_utils/backlog/rtmpose-m_8xb256-420e_body8-256x192.py"

PATHD_LABEL_OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics/fs26"
# PATHD_LABEL_OUTPUT='/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/prj54'
POSTFIX_LABEL_OUTPUT = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--RTMPose--JSON"

DEVICES = ["cuda:0", "cuda:2", "cuda:3", "cuda:4", "cuda:5"]

# Define the map of subpaths
# MAP__SUBPATH_DIR__TO__ = {
#     # "shoplifting-25min.mp4": None,
#     # "r9_25min_rotate.mp4": None,
#     "R3_2025_05_15_23_40_32_rotate.mp4": None,
#     "R4_2025_05_15_23_40_32_rotate.mp4": None,
#     "R9_2025_05_15_23_40_32_rotate.mp4": None,
#     "R7_2025_05_15_23_40_32_rotate.mp4": None,
#     "R8_2025_05_15_23_40_32_rotate.mp4": None,
#     "R10_2025_05_15_23_40_32_rotate.mp4": None,
# }
#
# -----
import os
import glob

MAP__SUBPATH_DIR__TO__ = {
    p[len(PATHD_MEDIA) + 1 :]: None
    for p in glob.glob(f"{PATHD_MEDIA}/gen-*-20260520/*/*/*.mp4")
    if os.path.isdir(p)
}

# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import (
    helper__extract__topdown__pose__imgdir,
    helper__extract__topdown__pose__video,
)
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
    helper__extract__topdown__pose__imgdir(**kwargs)
    print(f"{TAG__PASSED} Done: {kwargs['path__dir__img']}")
    # print(f"{TAG__INFO} Processing: {kwargs['path__file__video']}")
    # helper__extract__topdown__pose__video(**kwargs)
    # print(f"{TAG__PASSED} Done: {kwargs['path__file__video']}")

    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()


ls_kwargs = []

for i_m, subpath__media in enumerate(MAP__SUBPATH_DIR__TO__):
    path__dir__img__input = f"{PATHD_MEDIA}/{subpath__media}/images{POSTFIX_IMAGE}"
    path__file__video = f"{PATHD_MEDIA}/{subpath__media}"
    path__dir__lbl__input = (
        f"{PATHD_LABEL_INPUT}/{subpath__media}/labels{POSTFIX_LABEL_INPUT}"
    )
    path__dir__lbl__output = (
        f"{PATHD_LABEL_OUTPUT}/{subpath__media}/labels{POSTFIX_LABEL_OUTPUT}"
    )

    if os.path.exists(path__dir__lbl__output):
        shutil.rmtree(path__dir__lbl__output)
    os.makedirs(path__dir__lbl__output)

    kwargs = dict(
        path__dir__img=path__dir__img__input,
        path__file__video=path__file__video,
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__lbl__output=path__dir__lbl__output,
        path__file__model=PATH__FILE__MODEL,
        path__file__config=PATH__FILE__CONFIG,
        device=DEVICES[i_m % len(DEVICES)],
        batch_size=16,
        is_ok__lbl_not_exist=False,
        num__pad__0=9,
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
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(15) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
