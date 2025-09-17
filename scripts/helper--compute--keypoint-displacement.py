import os
import json
import numpy as np
from tqdm import tqdm


def compute_displacement(kpts1_dict, kpts2_dict):
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


def run(**kwargs):
    input_dir = kwargs["input_dir"]
    output_dir = kwargs["output_dir"]
    step_size = kwargs["step_size"]
    left_window = kwargs["left_window"]
    right_window = kwargs["right_window"]
    alpha = kwargs["alpha"]

    os.makedirs(output_dir, exist_ok=True)

    # Get all prediction files
    json_files = sorted(os.listdir(input_dir))

    # Load all predictions and store them for processing
    predictions = {}
    pbar = tqdm(json_files, desc="Loading predictions")
    for json_file in pbar:
        pbar.set_postfix(file=json_file)
        with open(os.path.join(input_dir, json_file), "r") as f:
            predictions[json_file] = json.load(f)

    # First pass: Compute current displacements for all frames
    for frame_idx, json_file in enumerate(
        tqdm(json_files, desc="Computing displacements")
    ):
        pred_data = predictions[json_file]

        # Get object tracks and keypoints
        list__obj__id_track = pred_data.get(
            "list__obj__id_track", [None] * len(pred_data["list__obj__box_xcycwhn"])
        )
        list__obj__kpts_xyn = pred_data.get("list__obj__kpts_xyn", [])

        # Process each object
        list__obj__kpts_displacement = []
        for i_obj, (id_track, kpts_dict) in enumerate(
            zip(list__obj__id_track, list__obj__kpts_xyn)
        ):
            # For first frame or if track doesn't exist in previous frame
            if frame_idx < step_size:
                curr_displacement = {kpt: None for kpt in kpts_dict}
            else:
                # Get keypoints from previous frame
                prev_file = json_files[frame_idx - step_size]
                prev_data = predictions[prev_file]
                prev_tracks = prev_data.get(
                    "list__obj__id_track",
                    [None] * len(prev_data["list__obj__box_xcycwhn"]),
                )

                if id_track in prev_tracks:
                    prev_idx = prev_tracks.index(id_track)
                    prev_kpts = prev_data["list__obj__kpts_xyn"][prev_idx]
                    curr_displacement = compute_displacement(prev_kpts, kpts_dict)
                else:
                    curr_displacement = {kpt: None for kpt in kpts_dict}

            list__obj__kpts_displacement.append(curr_displacement)

        pred_data["list__obj__kpts_displacement"] = list__obj__kpts_displacement

    # Compute EMAs
    track_ema = {}
    for frame_idx, json_file in enumerate(
        tqdm(json_files, desc="Computing EMAs displacements")
    ):
        pred_data = predictions[json_file]
        list__obj__id_track = pred_data.get(
            "list__obj__id_track", [None] * len(pred_data["list__obj__box_xcycwhn"])
        )
        list__obj__kpts_displacement = pred_data["list__obj__kpts_displacement"]

        list__obj__kpts_displacement_ema = []
        for id_track, curr_displacement in zip(
            list__obj__id_track, list__obj__kpts_displacement
        ):
            if id_track not in track_ema:
                new_ema = {k: None for k in curr_displacement}
            else:
                new_ema = {}
                for kpt_name in curr_displacement:
                    curr_val = curr_displacement[kpt_name]
                    prev_ema = track_ema[id_track][kpt_name]

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

            track_ema[id_track] = new_ema
            list__obj__kpts_displacement_ema.append(new_ema)

        pred_data["list__obj__kpts_displacement_ema"] = list__obj__kpts_displacement_ema

    # Compute window averages
    for frame_idx, json_file in enumerate(
        tqdm(json_files, desc="Computing window averages displacements")
    ):
        pred_data = predictions[json_file]
        list__obj__id_track = pred_data.get(
            "list__obj__id_track", [None] * len(pred_data["list__obj__box_xcycwhn"])
        )

        list__obj__kpts_displacement_average = []
        for i_obj, id_track in enumerate(list__obj__id_track):
            # Get window bounds
            window_start = max(0, frame_idx - left_window * step_size)
            window_end = min(len(json_files) - 1, frame_idx + right_window * step_size)

            # Collect displacements within the window
            window_displacements = []

            for win_idx in range(window_start, window_end + 1, step_size):
                win_file = json_files[win_idx]
                win_data = predictions[win_file]

                win_tracks = win_data.get(
                    "list__obj__id_track",
                    [None] * len(win_data["list__obj__box_xcycwhn"]),
                )

                if id_track in win_tracks:
                    track_idx = win_tracks.index(id_track)
                    win_displacement = win_data["list__obj__kpts_displacement"][
                        track_idx
                    ]
                    window_displacements.append(win_displacement)

            window_avg = {}
            for kpt_name in pred_data["list__obj__kpts_xyn"][i_obj].keys():
                values = [
                    d[kpt_name] for d in window_displacements if d[kpt_name] is not None
                ]
                window_avg[kpt_name] = (
                    np.mean(values, axis=0).tolist() if len(values) > 0 else None
                )

            list__obj__kpts_displacement_average.append(window_avg)

        pred_data["list__obj__kpts_displacement_average"] = (
            list__obj__kpts_displacement_average
        )

    for json_file, pred_data in predictions.items():
        with open(os.path.join(output_dir, json_file), "w") as f:
            json.dump(pred_data, f, indent=4)


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
            "input_dir": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/filter_action_by_keypoint_distance/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97/{}/labels".format(
                subpathf
            ),
            "output_dir": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-displacement/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97/{}/labels".format(
                subpathf
            ),
            "step_size": params["step_size"],  # currently not apply for EMA
            "left_window": 7,
            "right_window": 0,
            "alpha": 0.5,  # EMA smoothing factor
        }
        run(**kwargs)
