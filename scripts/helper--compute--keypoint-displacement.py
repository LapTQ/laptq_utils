import os
import json
import numpy as np
from tqdm import tqdm


def keypoints_distance(kpts1_dict, kpts2_dict):
    """Compute displacement vector between two sets of keypoints stored as dictionaries"""
    if kpts1_dict is None or kpts2_dict is None:
        return None

    if set(kpts1_dict.keys()) != set(kpts2_dict.keys()):
        raise ValueError("Keypoint sets must be identical between frames")

    # Compute displacement vector for each keypoint
    displacement = {}
    for kpt_name in kpts1_dict.keys():
        # Each keypoint value is [x, y]
        xy1 = kpts1_dict[kpt_name]
        xy2 = kpts2_dict[kpt_name]

        if not xy1 or not xy2:
            displacement[kpt_name] = None
            continue

        displacement[kpt_name] = [xy2[0] - xy1[0], xy2[1] - xy1[1]]

    return displacement


class KeypointDisplacementPredictor:
    def __init__(self, **kwargs):
        self.ls__dict__result = []
        self.track_ema = {}

    def append(self, **kwargs):
        dict__result = kwargs["dict__result"]
        self.ls__dict__result.append(dict__result)

    def predict(self, **kwargs):
        idx = kwargs["idx"]
        step_size = kwargs["step_size"]

        dict__result = self.ls__dict__result[idx]

        list__obj__id_track = dict__result["list__obj__id_track"]
        list__obj__kpts_xyn = dict__result.get("list__obj__kpts_xyn", [])

        list__obj__kpts_displacement = []
        for i_obj, (id_track, kpts_dict) in enumerate(
            zip(list__obj__id_track, list__obj__kpts_xyn)
        ):
            # For first frame or if track doesn't exist in previous frame
            if idx < step_size:
                curr_displacement = {kpt: None for kpt in kpts_dict}
            else:
                # Get keypoints from previous frame
                prev__dict__result = self.ls__dict__result[idx - step_size]
                prev__list__obj__id_track = prev__dict__result["list__obj__id_track"]

                if id_track in prev__list__obj__id_track:
                    prev_idx = prev__list__obj__id_track.index(id_track)
                    prev_kpts = prev__dict__result["list__obj__kpts_xyn"][prev_idx]
                    curr_displacement = keypoints_distance(prev_kpts, kpts_dict)
                else:
                    curr_displacement = {kpt: None for kpt in kpts_dict}

            list__obj__kpts_displacement.append(curr_displacement)

        dict__result["list__obj__kpts_displacement"] = list__obj__kpts_displacement

    def predict_ema(self, **kwargs):
        idx = kwargs["idx"]
        alpha = kwargs["alpha"]

        dict__result = self.ls__dict__result[idx]

        list__obj__id_track = dict__result["list__obj__id_track"]
        list__obj__kpts_displacement = dict__result["list__obj__kpts_displacement"]

        list__obj__kpts_displacement_ema = []
        for id_track, curr_displacement in zip(
            list__obj__id_track, list__obj__kpts_displacement
        ):
            if id_track not in self.track_ema:
                new_ema = {k: None for k in curr_displacement}
            else:
                new_ema = {}
                for kpt_name in curr_displacement:
                    curr_val = curr_displacement[kpt_name]
                    prev_ema = self.track_ema[id_track][kpt_name]

                    if curr_val is None:
                        new_ema[kpt_name] = prev_ema
                    elif prev_ema is None:
                        new_ema[kpt_name] = curr_val
                    else:
                        curr_val = np.array(curr_val)
                        prev_ema = np.array(prev_ema)
                        new_ema[kpt_name] = (
                            alpha * curr_val + (1 - alpha) * prev_ema
                        ).tolist()

            self.track_ema[id_track] = new_ema
            list__obj__kpts_displacement_ema.append(new_ema)

        dict__result["list__obj__kpts_displacement_ema"] = (
            list__obj__kpts_displacement_ema
        )

    def predict_avg(self, **kwargs):
        idx = kwargs["idx"]
        step_size = kwargs["step_size"]
        left_window = kwargs["left_window"]
        right_window = kwargs["right_window"]

        dict__result = self.ls__dict__result[idx]

        list__obj__id_track = dict__result["list__obj__id_track"]

        list__obj__kpts_displacement_average = []
        for i_obj, id_track in enumerate(list__obj__id_track):
            # Get window bounds
            window_start = max(0, idx - left_window * step_size)
            window_end = min(
                len(self.ls__dict__result) - 1, idx + right_window * step_size
            )

            # Collect displacements within the window
            window_displacements = []

            for i_w in range(window_start, window_end + 1, step_size):
                w__dict__result = self.ls__dict__result[i_w]
                w__list__obj__id_track = w__dict__result["list__obj__id_track"]

                if id_track in w__list__obj__id_track:
                    track_idx = w__list__obj__id_track.index(id_track)
                    w__displacement = w__dict__result["list__obj__kpts_displacement"][
                        track_idx
                    ]
                    window_displacements.append(w__displacement)

            window_avg = {}
            for kpt_name in dict__result["list__obj__kpts_xyn"][i_obj].keys():
                values = [
                    d[kpt_name] for d in window_displacements if d[kpt_name] is not None
                ]
                window_avg[kpt_name] = (
                    np.mean(values, axis=0).tolist() if len(values) > 0 else None
                )

            list__obj__kpts_displacement_average.append(window_avg)

        dict__result["list__obj__kpts_displacement_average"] = (
            list__obj__kpts_displacement_average
        )


def run(**kwargs):
    pathd_lbl = kwargs["pathd_lbl"]
    pathd_output = kwargs["pathd_output"]
    is_online = kwargs["is_online"]

    kdist_predictor = KeypointDisplacementPredictor(**kwargs)

    ls__namef_lbl = sorted(os.listdir(pathd_lbl))

    if is_online:
        for i_f, namef_lbl in tqdm(
            enumerate(ls__namef_lbl), desc="Predicting displacements"
        ):
            pathf_lbl = os.path.join(pathd_lbl, namef_lbl)

            # load cached pose prediction from YOLO
            with open(pathf_lbl, "r") as f:
                dict__result = json.load(f)

            kdist_predictor.append(dict__result=dict__result)

            # write to dict__result in-place
            kdist_predictor.predict(idx=i_f, **kwargs)
            kdist_predictor.predict_ema(idx=i_f, **kwargs)
            kdist_predictor.predict_avg(idx=i_f, **kwargs)

            os.makedirs(pathd_output, exist_ok=True)
            with open(os.path.join(pathd_output, namef_lbl), "w") as f:
                json.dump(dict__result, f, indent=4)
    else:
        for namef_lbl in tqdm(ls__namef_lbl, desc="Loading offline predictions"):
            with open(os.path.join(pathd_lbl, namef_lbl), "r") as f:
                # load cached pose prediction from YOLO
                dict__result = json.load(f)

            kdist_predictor.append(dict__result=dict__result)

        for i_f, namef_lbl in tqdm(
            enumerate(ls__namef_lbl), desc="Predicting displacements"
        ):
            # write to dict__result in-place
            kdist_predictor.predict(idx=i_f, **kwargs)

        for i_f, namef_lbl in tqdm(enumerate(ls__namef_lbl), desc="Predicting EMA"):
            # write to dict__result in-place
            kdist_predictor.predict_ema(idx=i_f, **kwargs)

        for i_f, namef_lbl in tqdm(enumerate(ls__namef_lbl), desc="Predicting average"):
            # write to dict__result in-place
            kdist_predictor.predict_avg(idx=i_f, **kwargs)

        for i_f, namef_lbl in tqdm(enumerate(ls__namef_lbl)):
            dict__result = kdist_predictor.ls__dict__result[i_f]

            os.makedirs(pathd_output, exist_ok=True)
            with open(os.path.join(pathd_output, namef_lbl), "w") as f:
                json.dump(dict__result, f, indent=4)


if __name__ == "__main__":

    for subpathf, params in {
        "fall_violence/test/fall/Falling_and_Slow_Falling.mp4": {
            "step_size": 2
        },  # 30 fps
        "fall_violence/test/violence/Fighting_1.mp4": {"step_size": 2},
        "fall_violence/test/violence/Fighting_2.mp4": {"step_size": 2},
        "fall_violence/test/violence/Fighting_3.mp4": {"step_size": 2},
        "fall_violence/test/violence/Fighting_4.mp4": {"step_size": 2},
    }.items():
        kwargs = {
            "pathd_lbl": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/filter_action_by_keypoint_distance/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97/{}/labels".format(
                subpathf
            ),
            "pathd_output": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-displacement/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97/{}/labels".format(
                subpathf
            ),
            "is_online": False,
            "step_size": params["step_size"],  # currently not apply for EMA
            "left_window": 7,
            "right_window": 1,
            "alpha": 0.5,  # EMA smoothing factor
        }
        run(**kwargs)
