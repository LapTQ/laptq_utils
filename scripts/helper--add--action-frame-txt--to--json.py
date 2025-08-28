# Currently, this script expects:
# - the input JSON file is in the output of `helper--extract--ultralytics--imgdir.sh`, not the output of `helper--extract--crops--from--detection.sh`
# - the action frame file is the list of action frames for each track ID, which is selected by picking (e.g., using yazi) from the output of `helper--extract--crops--from--detection.sh`
# - the output JSON file is will be of the same format as the input JSON file

import os
import time
import copy
import torch
import pickle
import numpy as np
from shutil import copyfile
from tqdm import tqdm
import datetime
import random
import csv
import json
import cv2
import sys
import glob

# ===========================================================

PATHD_LBL_INPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/fs26"
POSTFIX_LBL_INPUT = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"

MAP__SUBPTHD__TO__DICT_PATHF_ACTION_FRAMES = {
    # ====== fs26 ======
    "shoplifting-25min.mp4": {
        "1": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--customer-video/shoplifting-frames.txt"
    },
    # "r9_25min_rotate.mp4": {
    #     "1": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--satudora/shoplifting-frames.txt"
    # },
    # ====== prj54 ======
    # p[len(PATHD_LBL_INPUT) + 1 :]: {
    #     "fall_down": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--fall-violence/fall_down-frames.txt",
    #     "lying_down": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--fall-violence/lying_down-frames.txt",
    #     "sitting": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--fall-violence/sitting-frames.txt",
    #     "sitting_down": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--fall-violence/sitting_down-frames.txt",
    #     "standing": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--fall-violence/standing-frames.txt",
    #     "standing_up": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--fall-violence/standing_up-frames.txt",
    #     "walking": "/home/laptq/laptq-fs26-shoplifting-detection/data/crops--single-person--fall-violence/walking-frames.txt",
    # }
    # for p in glob.glob(f"{PATHD_LBL_INPUT}/*/*/*/*/*/*.avi")
    # if os.path.isdir(p)
    # ===================
}


def parse_action_frame(line):
    *subpathd, id_track, _, crop_name = line.strip().split("/")
    subpathd = "/".join(subpathd)
    id_track = int(id_track)
    id_frame = int(crop_name.split("--")[0])
    return {
        "subpathd": subpathd,
        "id_track": id_track,
        "id_frame": id_frame,
    }


# fs26, when only shoplifting-frames.txt is available, normal-frames.txt is not available
def process_condition(**kwargs):
    id_action = kwargs["id_action"]
    condition = kwargs["condition"]
    dict_result = kwargs["dict_result"]

    assert id_action == "1"

    for other_id_action in ["0"]:
        if other_id_action not in dict_result["list__obj__action_conf"]:
            dict_result["list__obj__action_conf"][other_id_action] = []
            dict_result["list__obj__action_status"][other_id_action] = []

    if condition is True:
        dict_result["list__obj__action_conf"]["0"].append(0.0)
        dict_result["list__obj__action_conf"]["1"].append(1.0)
        dict_result["list__obj__action_status"]["0"].append(False)
        dict_result["list__obj__action_status"]["1"].append(True)
    else:
        dict_result["list__obj__action_conf"]["0"].append(1.0)
        dict_result["list__obj__action_conf"]["1"].append(0.0)
        dict_result["list__obj__action_status"]["0"].append(True)
        dict_result["list__obj__action_status"]["1"].append(False)


# # general, when .txt for all actions are available
# def process_condition(**kwargs):
#     id_action = kwargs["id_action"]
#     condition = kwargs["condition"]
#     dict_result = kwargs["dict_result"]

#     if condition is True:
#         dict_result["list__obj__action_conf"][id_action].append(1.0)
#         dict_result["list__obj__action_status"][id_action].append(True)
#     else:
#         dict_result["list__obj__action_conf"][id_action].append(0.0)
#         dict_result["list__obj__action_status"][id_action].append(False)


PATHD_LBL_OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/data/ground-truth/fs26"
POSTFIX_LBL_OUTPUT = ""

# ===========================================================


def load_action_frames(pathf_action_frames):
    """Load action frames from a text file and organize them by subpath directory."""
    action_frames = {}
    with open(pathf_action_frames, "r") as f:
        data = f.readlines()
        for line in data:
            _ = parse_action_frame(line)
            subpathd = _["subpathd"]
            id_track = _["id_track"]
            id_frame = _["id_frame"]

            if subpathd not in action_frames:
                action_frames[subpathd] = []

            action_frames[subpathd].append((id_track, id_frame))

    return action_frames


def add__action_frame_txt__to__json(**kwargs):
    pathd_lbl_input = kwargs["pathd_lbl_input"]
    subpathd = kwargs["subpathd"]
    map__id_action__to__pathf_action_frames = kwargs[
        "map__id_action__to__pathf_action_frames"
    ]
    pathd_lbl_output = kwargs["pathd_lbl_output"]

    # load action frames, organized by dict of subpath -> id_action -> list of (id_track, id_frame)
    map__id_action__to__ls_frame = {}
    for id_action in map__id_action__to__pathf_action_frames:
        pathf_action_frames = map__id_action__to__pathf_action_frames[id_action]
        map__id_action__to__ls_frame[id_action] = load_action_frames(
            pathf_action_frames
        ).get(subpathd, [])

    for namef_lbl in tqdm(sorted(os.listdir(pathd_lbl_input))):
        pathf_lbl = os.path.join(pathd_lbl_input, namef_lbl)

        # load cached pose prediction from YOLO
        with open(pathf_lbl, "r") as f:
            dict_result = json.load(f)

        id_frame = int(os.path.splitext(namef_lbl)[0])

        list__obj__box_xcycwhn = dict_result["list__obj__box_xcycwhn"]
        list__obj__id_track = dict_result.get(
            "list__obj__id_track", [None] * len(list__obj__box_xcycwhn)
        )

        dict_result["list__obj__action_conf"] = {
            id_action: [] for id_action in map__id_action__to__ls_frame
        }
        dict_result["list__obj__action_status"] = {
            id_action: [] for id_action in map__id_action__to__ls_frame
        }
        for i_obj, id_track in enumerate(list__obj__id_track):

            for id_action in map__id_action__to__ls_frame:
                ls__action_frames = map__id_action__to__ls_frame[id_action]
                process_condition(
                    id_action=id_action,
                    condition=(id_track, id_frame) in ls__action_frames,
                    dict_result=dict_result,
                )

        os.makedirs(pathd_lbl_output, exist_ok=True)
        pathf_lbl_output = os.path.join(pathd_lbl_output, namef_lbl)
        with open(pathf_lbl_output, "w") as f:
            json.dump(dict_result, f, indent=4)


if __name__ == "__main__":

    for subpathd in MAP__SUBPTHD__TO__DICT_PATHF_ACTION_FRAMES:
        pathd_lbl_input = os.path.join(
            PATHD_LBL_INPUT, subpathd, "labels{}".format(POSTFIX_LBL_INPUT)
        )
        pathd_lbl_output = os.path.join(
            PATHD_LBL_OUTPUT, subpathd, "labels{}".format(POSTFIX_LBL_OUTPUT)
        )
        map__id_action__to__pathf_action_frames = (
            MAP__SUBPTHD__TO__DICT_PATHF_ACTION_FRAMES[subpathd]
        )

        add__action_frame_txt__to__json(
            pathd_lbl_input=pathd_lbl_input,
            subpathd=subpathd,
            map__id_action__to__pathf_action_frames=map__id_action__to__pathf_action_frames,
            pathd_lbl_output=pathd_lbl_output,
        )

        print(f"[DONE] {subpathd}")
