import os
import json
import numpy as np
from tqdm import tqdm
from copy import deepcopy


class MajorVoteActionPredictor:
    def __init__(self, **kwargs):
        self.ls__dict__result__not_voted = []
        self.ls__dict__result__voted = []

    def append(self, **kwargs):
        dict__result = kwargs["dict__result"]
        self.ls__dict__result__not_voted.append(deepcopy(dict__result))
        self.ls__dict__result__voted.append(dict__result)  # to write in-place

    def predict(self, **kwargs):
        idx = kwargs["idx"]
        step_size = kwargs["step_size"]
        left_window = kwargs["left_window"]
        right_window = kwargs["right_window"]
        ls__id_action__prioritized = kwargs["ls__id_action__prioritized"]
        min_votes_threshold = kwargs["min_votes_threshold"]
        unconfirmed__id_action = kwargs["unconfirmed__id_action"]

        dict__result__not_voted = self.ls__dict__result__not_voted[idx]
        dict__result__voted = self.ls__dict__result__voted[idx]

        list__obj__id_track = dict__result__not_voted["list__obj__id_track"]

        list__obj__action_status__voted = dict__result__voted[
            "list__obj__action_status"
        ]
        list__obj__action_conf__voted = dict__result__voted["list__obj__action_conf"]

        # # debug
        # print("Before voting:", list__obj__action_status__in, list__obj__action_conf__in)

        # For each object in the current frame
        for i_obj, id_track in enumerate(list__obj__id_track):

            # Get window bounds
            window_start = max(0, idx - left_window * step_size)
            window_end = min(
                len(self.ls__dict__result__not_voted) - 1,
                idx + right_window * step_size,
            )

            # Collect votes and confidence values for this track within the window
            votes = {id_action: 0 for id_action in ls__id_action__prioritized}
            conf_values = {id_action: [] for id_action in ls__id_action__prioritized}

            for i_w in range(window_start, window_end + 1, step_size):
                w__dict__result__input = self.ls__dict__result__not_voted[i_w]

                w__list__obj__id_track = w__dict__result__input["list__obj__id_track"]

                if id_track in w__list__obj__id_track:
                    track_idx = w__list__obj__id_track.index(id_track)

                    # Get action status for this track in this window frame
                    for id_action in ls__id_action__prioritized:
                        if (
                            w__dict__result__input["list__obj__action_status"][
                                id_action
                            ][track_idx]
                            is True
                        ):
                            votes[id_action] += 1
                            conf = w__dict__result__input["list__obj__action_conf"][
                                id_action
                            ][track_idx]
                            if conf is not None:
                                conf_values[id_action].append(conf)

            # # debug
            # print(votes)

            # Determine majority action
            max_votes = max(votes.values())
            if max_votes > 0:  # If we have any votes
                # In case of a tie, prioritize
                for id_action in ls__id_action__prioritized:
                    if votes[id_action] == max_votes:
                        if max_votes >= min_votes_threshold:
                            majority_action = id_action
                        else:
                            majority_action = unconfirmed__id_action
                        break

                # Update action status
                for id_action in ls__id_action__prioritized:
                    list__obj__action_status__voted[id_action][i_obj] = (
                        majority_action == id_action
                    )

                # Update confidence values based on majority class
                for id_action in ls__id_action__prioritized:
                    if len(conf_values[id_action]):
                        list__obj__action_conf__voted[id_action][i_obj] = float(
                            np.mean(conf_values[id_action])
                        )
                    else:
                        list__obj__action_conf__voted[id_action][i_obj] = None


def run(**kwargs):
    pathd_lbl = kwargs["pathd_lbl"]
    pathd_output = kwargs["pathd_output"]
    is_online = kwargs["is_online"]

    vote_predictor = MajorVoteActionPredictor(**kwargs)

    ls__namef_lbl = sorted(os.listdir(pathd_lbl))

    if is_online:
        for i_f, namef_lbl in tqdm(enumerate(ls__namef_lbl), desc="Predicting action"):
            pathf_lbl = os.path.join(pathd_lbl, namef_lbl)

            # load cached pose prediction from YOLO
            with open(pathf_lbl, "r") as f:
                dict__result = json.load(f)

            vote_predictor.append(dict__result=dict__result)

            # write to dict__result in-place
            vote_predictor.predict(idx=i_f, **kwargs)

            os.makedirs(pathd_output, exist_ok=True)
            with open(os.path.join(pathd_output, namef_lbl), "w") as f:
                json.dump(dict__result, f, indent=4)
    else:
        for namef_lbl in tqdm(ls__namef_lbl, desc="Loading offline predictions"):
            with open(os.path.join(pathd_lbl, namef_lbl), "r") as f:
                # load cached pose prediction from YOLO
                dict__result = json.load(f)

                vote_predictor.append(dict__result=dict__result)

        for i_f, namef_lbl in tqdm(enumerate(ls__namef_lbl), desc="Predicting action"):
            # write to dict__result in-place
            vote_predictor.predict(idx=i_f, **kwargs)

        for i_f, namef_lbl in tqdm(enumerate(ls__namef_lbl)):
            dict__result = vote_predictor.ls__dict__result__voted[i_f]

            os.makedirs(pathd_output, exist_ok=True)
            with open(os.path.join(pathd_output, namef_lbl), "w") as f:
                json.dump(dict__result, f, indent=4)


if __name__ == "__main__":
    # Use the same list of videos as in predict.py
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
        kwargs = {
            # ======= fs26 ========
            "pathd_lbl": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/ProtoGCN/fs26/v103--mnit_poselift_roboflow_satudora_awlrecord--r1.0-0xauto-1x1--no-normal-awlrecord--equal-normal-public-vs-satudora--1s-15frames--fixR10/{}/labels".format(
                subpathf
            ),
            "pathd_output": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/ProtoGCN/fs26/v103--mnit_poselift_roboflow_satudora_awlrecord--r1.0-0xauto-1x1--no-normal-awlrecord--equal-normal-public-vs-satudora--1s-15frames--fixR10--left-window-5--right-window-5/{}/labels".format(
                subpathf
            ),
            "left_window": 5,  # counted after stepping
            "right_window": 5,  # counted after stepping
            "ls__id_action__prioritized": [
                "1",
                "0",
                "unk",
            ],  # prioritize when a tie occurs
            "min_votes_threshold": 1,  # if max votes is less than this, then consider it as unsure
            #
            # ======= prj54 ========
            # "pathd_lbl": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/filter_action_by_num_people/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97--filter-speed-1.2-2.0--filter-loc-5--filter-num-people-2/{}/labels".format(
            #     subpathf
            # ),
            # "pathd_output": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97--filter-speed-1.2-2.0--filter-loc-5--filter-num-people-2--15fps--vote-19-9/{}/labels".format(
            #     subpathf
            # ),
            # "left_window": 19,  # counted after stepping
            # "right_window": 0,  # counted after stepping
            # "ls__id_action__prioritized": [
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
            # "min_votes_threshold": 9,  # if max votes is less than this, then consider it as unsure
            #
            # =======================
            "is_online": params["is_online"],
            "step_size": params["step_size"],
            "unconfirmed__id_action": "unk",
        }
        run(**kwargs)
