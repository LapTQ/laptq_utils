PATH__DIR__MEDIA = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fs26"
# PATH__DIR__MEDIA = "/home/laptq/laptq-fs26-shoplifting-detection/data/test-videos"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/SkateFormer/fs26/v206--satudora_veo3_awlrecord--r2.4-0xauto-1x1--satudora-filter-roi-conf--only-normal-satudora--veo3-all--1s-15frames--split-17-class--12-kpts"
# PATH__DIR__LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--add--action-frame-txt--to--json"
POSTFIX__DIR__LABEL = ""

NUM__MAX__IMG__TO__VISUALIZE = None
IS_OK__LBL_NOT_FOUND = False

OUTPUT_AS = "imgdir"  # imgdir, video

PATH__DIR__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--draw/fs26/v201--satudora_veo3_awlrecord--r1.25-0xauto-1x1--satudora-filter-roi-conf--only-normal-satudora--veo3-all--1s-15frames--split-17-class--v2"

# Define the map of subpaths
MAP__SUBPATH_DIR__TO__ = {
    "shoplifting-25min.mp4": 30,
    # "r9_25min_rotate.mp4": 15,
}
# -----
# import os
# import glob

# MAP__SUBPATH_DIR__TO__ = {
#     p[len(PATH__DIR__LABEL) + 1 :]: None
#     for p in glob.glob(
#         f"{PATH__DIR__LABEL}/crops--single-person--shoplifting-awlrecord-videos/day1/cuongdh--Basket_carry_by_hand--Back_pant_pocket--front--standing.mp4/*"
#     )
#     if os.path.isdir(p)
# }

# =============================================================
import os
import subprocess
from laptq_pyutils.helper import helper__draw__imgdir, helper__draw__video
from multiprocessing import Pool
import multiprocessing as mp
import shutil


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    # =============== imgdir ==============
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__img']}")
    helper__draw__imgdir(**kwargs)
    print(f"{TAG__PASSED} Done: {kwargs['path__dir__img']}")

    # ================ video ================
    # print(f"{TAG__INFO} Processing: {kwargs['path__file__video']}")
    # helper__draw__video(**kwargs)
    # print(f"{TAG__PASSED} Done: {kwargs['path__file__video']}")


ls_kwargs = []


def lambda__id_frame__from(x):
    return x.split(".")[0]


# Iterate over the subpaths
for subpath in MAP__SUBPATH_DIR__TO__:
    path__dir__img = f"{PATH__DIR__MEDIA}/{subpath}/images{POSTFIX__DIR__IMAGE}"
    path__file__video = f"{PATH__DIR__MEDIA}/{subpath}"
    path__dir__lbl = f"{PATH__DIR__LABEL}/{subpath}/labels{POSTFIX__DIR__LABEL}"
    path__dir__output = f"{PATH__DIR__OUTPUT}/{subpath}/vis{POSTFIX__DIR__LABEL}"
    path__file__output = f"{PATH__DIR__OUTPUT}/{subpath}"

    if os.path.exists(path__dir__output) and OUTPUT_AS == "imgdir":
        os.system(f"rm -rf {path__dir__output}")
    if os.path.exists(path__file__output) and OUTPUT_AS == "video":
        os.system(f"rm -rf {path__file__output}")

    fps = MAP__SUBPATH_DIR__TO__[subpath]

    kwargs = dict(
        path__dir__img=path__dir__img,
        path__file__video=path__file__video,
        path__dir__lbl=path__dir__lbl,
        output_as=OUTPUT_AS,
        path__dir__output=path__dir__output,
        path__file__output=path__file__output,
        num__workers=10,
        num__max__img=NUM__MAX__IMG__TO__VISUALIZE,
        seed=42,
        to_draw__id_frame=False,
        id_frame__from="filename",
        lambda__id_frame__from=lambda__id_frame__from,
        fps=fps,
        fourcc="mp4v",
        num__pad__0=9,
        to_draw__id_track=True,
        to_draw__box_x1y1whn=True,
        to_draw__box_polygon=False,
        to_draw__box_conf=False,
        to_draw__id_class=False,
        to_draw__name_class=False,
        to_draw__pose=False,
        to_draw__connected_keypoints=False,
        to_draw__id_action=False,
        to_draw__name_action=True,
        to_draw__action_conf=False,
        to_draw__keypoints_displacement=False,
        to_draw__keypoints_speed=False,
        to_draw__event_info=False,
        fontScale=1,
        thickness=2,
        box_color_by="id__track",
        displacement_key="list__obj__kpts_displacement_average",
        speed_key="list__obj__kpts_speed_relative",
        is_ok__lbl_not_exist=IS_OK__LBL_NOT_FOUND,
        list__keypoints_same_color=[
            ["left_eye", "right_eye", "left_ear", "right_ear"],
            ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
            ["left_elbow", "right_elbow", "left_wrist", "right_wrist"],
            ["left_knee", "right_knee", "left_ankle", "right_ankle"],
        ],
        list__keypoints_edge=[
            ["nose", "left_eye"],
            ["nose", "right_eye"],
            ["left_eye", "left_ear"],
            ["right_eye", "right_ear"],
            ["left_shoulder", "right_shoulder"],
            ["left_hip", "right_hip"],
            ["left_shoulder", "left_hip"],
            ["right_shoulder", "right_hip"],
            ["left_shoulder", "left_elbow"],
            ["right_shoulder", "right_elbow"],
            ["left_elbow", "left_wrist"],
            ["right_elbow", "right_wrist"],
            ["left_hip", "left_knee"],
            ["right_hip", "right_knee"],
            ["left_knee", "left_ankle"],
            ["right_knee", "right_ankle"],
        ],
        list__edges_same_color=[
            [
                ["nose", "left_eye"],
                ["nose", "right_eye"],
                ["left_eye", "left_ear"],
                ["right_eye", "right_ear"],
            ],
            [
                ["left_shoulder", "right_shoulder"],
                ["left_hip", "right_hip"],
                ["left_shoulder", "left_hip"],
                ["right_shoulder", "right_hip"],
            ],
            [
                ["left_shoulder", "left_elbow"],
                ["right_shoulder", "right_elbow"],
                ["left_elbow", "left_wrist"],
                ["right_elbow", "right_wrist"],
            ],
            [
                ["left_hip", "left_knee"],
                ["right_hip", "right_knee"],
                ["left_knee", "left_ankle"],
                ["right_knee", "right_ankle"],
            ],
        ],
        list__keypoints_to_exclude=[],
        # list__keypoints_to_include=[
        #     "left_shoulder",
        #     "right_shoulder",
        #     "left_elbow",
        #     "right_elbow",
        #     "left_wrist",
        #     "right_wrist",
        # ],
        list__keypoints_to_include=[
            # "nose",
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
        # list__keypoints_to_include=[
        #     "nose",
        #     "left_eye",
        #     "right_eye",
        #     "left_ear",
        #     "right_ear",
        #     "left_shoulder",
        #     "right_shoulder",
        #     "left_elbow",
        #     "right_elbow",
        #     "left_wrist",
        #     "right_wrist",
        #     "left_hip",
        #     "right_hip",
        #     "left_knee",
        #     "right_knee",
        #     "left_ankle",
        #     "right_ankle",
        # ],
        map__id_class__to__name_class=None,
        map__id_action__to__name_action={
            # "0": "",
            # "1": "SHOPLIFTING",
            # "unk": "",
            #
            # "0": "falling",
            # "1": "kicking",
            # "2": "punching",
            # "3": "pushing",
            # "4": "sitting_down",
            # "5": "standing_up",
            # "6": "walking",
            # "7": "standing",
            # "unk": "",
            #
            # "0": "falling",
            # "1": "violence",
            # "2": "violence",
            # "3": "violence",
            # "4": "",
            # "5": "",
            # "6": "",
            # "7": "",
            # "unk": "",
            #
            # "A043": "falling",
            # "A024": "kicking",
            # "A051": "kicking",
            # "A100": "kicking backward",
            # "A102": "side kicking",
            # "A050": "punching",
            # "A052": "pushing",
            # "A008": "sitting_down",
            # "A009": "standing_up",
            # "A059": "walking",
            # "A060": "walking",
            #
            "0": "dung",
            "1": "dung day",
            "2": "ngoi",
            "3": "ngoi xuong",
            "4": "di lai",
            "5": "dua tay vao nguoi",
            "6": "rut tay khoi tui",
            "7": "rut tay khoi nguoi",
            "8": "dua tay ra truoc",
            "9": "tuong tac phia truoc",
            "10": "tay cam vat the",
            "11": "rut tay ve",
            "12": "GIAU -> TUI QUAN",
            "13": "GIAU -> TUI AO/XACH",
            "14": "GIAU -> TUI trong GIO",
            "15": "GIAU -> CO AO",
            "16": "GIAU -> GIAY",
            "unk": "",
        },
    )

    ls_kwargs.append(kwargs)


# ============ sequential =============
for kwargs in ls_kwargs:
    run_wrapper(kwargs)
# ============ multi-process run ============
# with Pool(10) as p:
#     p.map(run_wrapper, ls_kwargs)
# ===================================
