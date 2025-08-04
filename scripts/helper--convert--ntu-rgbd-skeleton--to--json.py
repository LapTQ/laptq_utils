PATHD_LBL_INPUT = "/home/laptq/laptq-fs26-shoplifting-detection/data"
PATHD_LBL_OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--ntu-rgbd-skeleton--to--json"

# ============================
# MAP__SUBPATHF__TO__ = {
# }
import sys

sys.path.append("/home/laptq/laptq-fs26-shoplifting-detection/data")
from fall_violence_subpaths import MAP__SUBPATHF__TO__

# ============================


# ======================================================
import os
import json
import numpy as np
from pprint import pprint
from tqdm import tqdm
from laptq_pyutils.objects import ListAligner


def read__ntu_grbd_skeleton__file(pathf):
    f = open(pathf, "r")
    datas = f.readlines()
    f.close()

    nframe = int(datas[0][:-1])
    cursor = 0
    ret_data = []
    for frame in range(nframe):
        frame_data = {}
        cursor += 1
        bodycount = int(datas[cursor][:-1])
        for body in range(bodycount):
            cursor += 1
            bodyinfo = datas[cursor][:-1].split(" ")
            id_track = int(bodyinfo[0])
            frame_data[id_track] = {"skel_body": [], "rgb_body": [], "depth_body": []}
            cursor += 1

            njoints = int(datas[cursor][:-1])
            for joint in range(njoints):
                cursor += 1
                jointinfo = datas[cursor][:-1].split(" ")
                jointinfo = np.array(list(map(float, jointinfo))).tolist()
                frame_data[id_track]["skel_body"].append(jointinfo[:3])
                frame_data[id_track]["depth_body"].append(jointinfo[3:5])
                frame_data[id_track]["rgb_body"].append(jointinfo[5:7])
        ret_data.append(frame_data)
    return ret_data


def helper__convert__ntu_rgbd_skeleton__to__json(**kwargs):
    pathf_lbl_input = kwargs["pathf_lbl_input"]
    pathd_lbl_output = kwargs["pathd_lbl_output"]
    map__name_keypoint__to__id_keypoint = kwargs["map__name_keypoint__to__id_keypoint"]
    num__pad__0 = kwargs["num__pad__0"]

    os.makedirs(pathd_lbl_output, exist_ok=True)

    data = read__ntu_grbd_skeleton__file(pathf_lbl_input)

    id_action = os.path.basename(pathf_lbl_input).split(".")[0][-4:]
    for id_frame, frame_data in tqdm(enumerate(data)):
        dict__result = {
            "list__obj__id_class": [],
            "list__obj__box_xcycwhn": [],
            "list__obj__box_conf": [],
            "list__obj__kpts_xyn": [],
            "list__obj__kpts_conf": [],
            "list__obj__id_track": [],
            "list__obj__action_conf": {id_action: []},
            "list__obj__action_status": {id_action: []},
        }
        for id_track, person_data in frame_data.items():

            kpts_xyn = {}
            for (
                name_keypoint,
                id_keypoint,
            ) in map__name_keypoint__to__id_keypoint.items():
                k_x, k_y = person_data["rgb_body"][id_keypoint][:2]
                kxn = k_x / 1920
                kyn = k_y / 1080
                kpts_xyn[name_keypoint] = [kxn, kyn]

            b_x1n, b_y1n, b_x2n, b_y2n = 1e9, 1e9, -1e9, -1e9
            for k_x, k_y in person_data["rgb_body"]:
                k_xn = k_x / 1920
                k_yn = k_y / 1080
                b_x1n = min(b_x1n, k_xn)
                b_y1n = min(b_y1n, k_yn)
                b_x2n = max(b_x2n, k_xn)
                b_y2n = max(b_y2n, k_yn)
            b_xcn = (b_x1n + b_x2n) / 2
            b_ycn = (b_y1n + b_y2n) / 2
            b_wn = b_x2n - b_x1n
            b_hn = b_y2n - b_y1n

            dict__result["list__obj__id_class"].append(0)
            dict__result["list__obj__box_xcycwhn"].append([b_xcn, b_ycn, b_wn, b_hn])
            dict__result["list__obj__box_conf"].append(1.0)
            dict__result["list__obj__kpts_xyn"].append(kpts_xyn)
            dict__result["list__obj__kpts_conf"].append({k: 1.0 for k in kpts_xyn})
            dict__result["list__obj__id_track"].append(id_track)
            dict__result["list__obj__action_conf"][id_action].append(1.0)
            dict__result["list__obj__action_status"][id_action].append(True)

        pathf_lbl_output = os.path.join(
            pathd_lbl_output, f"{id_frame:0{num__pad__0}}.json"
        )
        with open(pathf_lbl_output, "w") as f:
            json.dump(dict__result, f, indent=4)


if __name__ == "__main__":

    for subpathf in MAP__SUBPATHF__TO__:
        pathf_lbl_input = os.path.join(PATHD_LBL_INPUT, subpathf)
        pathd_lbl_output = os.path.join(PATHD_LBL_OUTPUT, subpathf, "labels")
        os.system("rm -rf {}".format(pathd_lbl_output))
        helper__convert__ntu_rgbd_skeleton__to__json(
            pathf_lbl_input=pathf_lbl_input,
            pathd_lbl_output=pathd_lbl_output,
            map__name_keypoint__to__id_keypoint={  # note that the index of keypoints in drawn picture is 1-based, so we must -1 to get the 0-based index
                "nose": 3,
                "left_eye": 3,
                "right_eye": 3,
                "left_ear": 3,
                "right_ear": 3,
                "left_shoulder": 4,
                "right_shoulder": 8,
                "left_elbow": 5,
                "right_elbow": 9,
                "left_wrist": 6,
                "right_wrist": 10,
                "left_hip": 12,
                "right_hip": 16,
                "left_knee": 13,
                "right_knee": 17,
                "left_ankle": 14,
                "right_ankle": 18,
            },
            num__pad__0=9,
        )
