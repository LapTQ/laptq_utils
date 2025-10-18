PATH__DIR__IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--crops--from--detection/fs26"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--crops--from--detection/fs26"
POSTFIX__DIR__LABEL = ""

NUM__MAX__IMG__TO__VISUALIZE = None
IS_OK__LBL_NOT_FOUND = False

PATH__DIR__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--crops--from--detection/fs26"

PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS = (
    "/home/laptq/laptq-fs26-shoplifting-detection/src/configs/class_name.yaml"
)
PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION = (
    "/home/laptq/laptq-fs26-shoplifting-detection/src/configs/action_names.yaml"
)

# Define the map of subpaths
# MAP__SUBPATH_DIR__TO__ = {
#     "shoplifting-25min.mp4": None,
#     "r9_25min_rotate.mp4": None,
# }
# -----
import os
import glob

MAP__SUBPATH_DIR__TO__ = {
    p[len(PATH__DIR__LABEL) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL}/shoplifting-gen-videos/veo3/v1/A_fixedposition_surveillance_202509261747_bh.mp4/*"
    )
    if os.path.isdir(p)
}

# =============================================================
import os
import subprocess
from laptq_pyutils.helper import helper__draw__imgdir
from multiprocessing import Pool
import multiprocessing as mp
import shutil


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__img']}")

    helper__draw__imgdir(**kwargs)

    num__lbl = len(os.listdir(kwargs["path__dir__lbl"]))
    num__img_vis = len(os.listdir(kwargs["path__dir__output"]))
    if (
        NUM__MAX__IMG__TO__VISUALIZE is not None
        and num__lbl > NUM__MAX__IMG__TO__VISUALIZE
    ):
        num__lbl = NUM__MAX__IMG__TO__VISUALIZE
    if num__lbl != num__img_vis:
        print(
            f"{TAG__WARNING} Number of images and labels do not match: {num__img_vis} != {num__lbl}"
        )
        print(f"    [+] {num__lbl} labels")
        print(f"    [+] {num__img_vis} visualized images")

        exit(1)

    print(
        f"{TAG__PASSED} Done: {num__lbl} labels == {num__img_vis} visualized images: {kwargs['path__dir__img']}"
    )


ls_kwargs = []


def lambda__id_frame__from(x):
    return x.split(".")[0]


# Iterate over the subpaths
for subpath__dir in MAP__SUBPATH_DIR__TO__:
    path__dir__img = f"{PATH__DIR__IMAGE}/{subpath__dir}/images{POSTFIX__DIR__IMAGE}"
    path__dir__lbl = f"{PATH__DIR__LABEL}/{subpath__dir}/labels{POSTFIX__DIR__LABEL}"
    path__dir__output = f"{PATH__DIR__OUTPUT}/{subpath__dir}/vis{POSTFIX__DIR__LABEL}"

    if os.path.exists(path__dir__output):
        shutil.rmtree(path__dir__output)
    os.makedirs(path__dir__output)

    kwargs = dict(
        path__dir__img=path__dir__img,
        path__dir__lbl=path__dir__lbl,
        path__dir__output=path__dir__output,
        to_concat__original_img=False,
        concat__axis=1,
        to_draw__id_frame=True,
        id_frame__from="filename",
        lambda__id_frame__from=lambda__id_frame__from,
        to_draw__id_track=True,
        to_draw__box_x1y1whn=True,
        to_draw__box_polygon=False,
        to_draw__box_conf=False,
        to_draw__id_class=False,
        to_draw__name_class=False,
        to_draw__pose=True,
        to_draw__connected_keypoints=True,
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
        path__file__map__id_class__to__name_class=PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS,
        path__file__map__id_action__to__name_action=PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION,
        num__max__img=NUM__MAX__IMG__TO__VISUALIZE,
        seed=42,
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
        list__keypoints_to_include=[
            "left_shoulder",
            "right_shoulder",
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist",
        ],
        # list__keypoints_to_include=[
        #     "nose",
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
    )

    ls_kwargs.append(kwargs)


# ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ multi-process run ============
with Pool(10) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
