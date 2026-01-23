# =============================================================
import os
import json
import numpy as np
from tqdm import tqdm
from copy import deepcopy
from multiprocessing import Pool
import multiprocessing as mp
from laptq_pyutils.helper import helper__major_vote_action


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['pathd_lbl']}")
    helper__major_vote_action(**kwargs)
    print(f"{TAG__PASSED} Done: {kwargs['pathd_lbl']}")


if __name__ == "__main__":

    ls_kwargs = []

    for subpathf, params in {
        # ======= fs26 ========
        "shoplifting-25min.mp4": {"step_size": 2, "is_online": False},  # 30 fps
        "r9_25min_rotate.mp4": {"step_size": 1, "is_online": False},  # 15 fps
        # ======= prj54 =======
        # "fall_violence/test/fall/Falling_and_Slow_Falling.mp4": {"step_size": 2, "is_online": True}, # 30 fps
        # "fall_violence/test/violence/Fighting_1.mp4": {"step_size": 2, "is_online": True},
        # "fall_violence/test/violence/Fighting_2.mp4": {"step_size": 2, "is_online": True},
        # "fall_violence/test/violence/Fighting_3.mp4": {"step_size": 2, "is_online": True},
        # "fall_violence/test/violence/Fighting_4.mp4": {"step_size": 2, "is_online": True},
    }.items():
        kwargs = dict(
            # ======= fs26 ========
            pathd_lbl="/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials/predict_general/ProtoGCN/fs26/v103--mnit_poselift_roboflow_satudora_awlrecord--r1.0-0xauto-1x1--no-normal-awlrecord--equal-normal-public-vs-satudora--1s-15frames--fixR10/{}/labels".format(
                subpathf
            ),
            pathd_output="/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/ProtoGCN/fs26/v103--mnit_poselift_roboflow_satudora_awlrecord--r1.0-0xauto-1x1--no-normal-awlrecord--equal-normal-public-vs-satudora--1s-15frames--fixR10--left-window-5--right-window-5/{}/labels".format(
                subpathf
            ),
            left_window=5,  # counted after stepping
            right_window=5,  # counted after stepping
            ls__id_action__prioritized=[
                "1",
                "0",
                "unk",
            ],  # prioritize when a tie occurs
            min_votes_threshold=1,  # if max votes is less than this, then consider it as unsure
            #
            # ======= prj54 ========
            # pathd_lbl="/home/laptq/laptq-fs26-shoplifting-detection/outputs/filter_action_by_num_people/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97--filter-speed-1.2-2.0--filter-loc-5--filter-num-people-2/{}/labels".format(
            #     subpathf
            # ),
            # pathd_output="/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97--filter-speed-1.2-2.0--filter-loc-5--filter-num-people-2--15fps--vote-19-9/{}/labels".format(
            #     subpathf
            # ),
            # left_window=19,  # counted after stepping
            # right_window=0,  # counted after stepping
            # ls__id_action__prioritized=[
            #     "0",
            #     "1",
            #     "2",
            #     "3",
            #     "4",
            #     "5",
            #     "6",
            #     "7",
            #     "unk",
            # ],  # prioritize when a tie occurs
            # min_votes_threshold=9,  # if max votes is less than this, then consider it as unsure
            #
            # =======================
            is_online=params["is_online"],
            step_size=params["step_size"],
            unconfirmed__id_action="unk",
        )

        ls_kwargs.append(kwargs)

    # # ============ sequential =============
    # for kwargs in ls_kwargs:
    #     run_wrapper(kwargs)
    # ============ parallel =============
    with Pool(15) as p:
        p.map(run_wrapper, ls_kwargs)
    # ===================================
