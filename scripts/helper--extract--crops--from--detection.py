# Define paths and postfixes
PATH__DIR__IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/sample_frames_by_skipping/full"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir"
POSTFIX__DIR__LABEL = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--RTMPose--JSON"

PATH__DIR__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--crops--from--detection"
POSTFIX__DIR__OUTPUT = ""

# Define the map of subpaths
MAP__SUBPATH_VIDEO__TO__ = {
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (1).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (2).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (3).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (4).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (5).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (6).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (7).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (8).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (9).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (10).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (11).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (12).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (13).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (14).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (15).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (16).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (17).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (18).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (19).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (20).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (21).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (22).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (23).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (24).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (25).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (26).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (27).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (28).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (29).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (30).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (31).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (32).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (33).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (34).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (35).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (36).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (37).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (38).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (39).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (40).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (41).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (42).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (43).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (44).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (45).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (46).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (47).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (48).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (49).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (50).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (51).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (52).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (53).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (54).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (55).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (56).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (57).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (58).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (59).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (60).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (61).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (62).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (63).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (64).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (65).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (66).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (67).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (68).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (69).avi": None,
    "fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (70).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (1).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (2).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (3).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (4).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (5).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (6).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (7).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (8).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (9).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (10).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (11).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (12).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (13).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (14).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (15).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (16).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (17).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (18).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (19).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (20).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (21).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (22).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (23).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (24).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (25).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (26).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (27).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (28).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (29).avi": None,
    "fall_violence/train/fall/Le2i/Home_01/Videos/video (30).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (31).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (32).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (33).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (34).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (35).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (36).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (37).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (38).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (39).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (40).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (41).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (42).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (43).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (44).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (45).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (46).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (47).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (48).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (49).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (50).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (51).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (52).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (53).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (54).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (55).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (56).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (57).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (58).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (59).avi": None,
    "fall_violence/train/fall/Le2i/Home_02/Videos/video (60).avi": None,
}
# import sys

# sys.path.append("/home/laptq/laptq-fs26-shoplifting-detection/data")
# from fall_violence_subpaths import MAP__SUBPATHF__TO__ as MAP__SUBPATH_VIDEO__TO__

# =============================================================
import os
import subprocess
from laptq_pyutils.helper import helper__extract__crops__from__detection


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

    # Call the helper function
    helper__extract__crops__from__detection(
        path__dir__img__input=path__dir__img__input,
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__crop__img__output=path__dir__crop__img__output,
        path__dir__crop__lbl__output=path__dir__crop__lbl__output,
        is_ok__lbl_not_exist=False,
        num__pad__0=6,
        to_resize_box__wrt__pose=True,
        to_shift__coords__wrt__box=True,
        to_save__img=False,
        split_by="id__track",  # "id__track" # if not None, please add a "/{}" before /images and /labels assuming there's an /images and /labels in path__dir__crop__img__output and path__dir__crop__lbl__output
    )

    print(f"{TAG__INFO} Done: {subpath__dir}")
