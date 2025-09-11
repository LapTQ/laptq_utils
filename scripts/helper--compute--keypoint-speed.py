import os
import json
import numpy as np
from tqdm import tqdm


def run(**kwargs):
    input_dir = kwargs["input_dir"]
    output_dir = kwargs["output_dir"]
    displacement_key = kwargs["displacement_key"]
    fps = kwargs["fps"]
    frame_width = kwargs["frame_width"]
    frame_height = kwargs["frame_height"]
    anchors = kwargs["anchors"]

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

    # compute speed
    for frame_idx, json_file in enumerate(tqdm(json_files, desc="Computing speed")):
        pred_data = predictions[json_file]

        list__obj__id_track = pred_data.get(
            "list__obj__id_track", [None] * len(pred_data["list__obj__box_xcycwhn"])
        )
        list__obj__kpts_displacement = pred_data[displacement_key]

        list__obj__kpts_speed = []
        for i_obj, id_track in enumerate(list__obj__id_track):
            kpts_displacement = list__obj__kpts_displacement[i_obj]

            if kpts_displacement is None:
                kpts_speed = None
            else:
                kpts_speed = {}
                for kpt, displacement in kpts_displacement.items():
                    if displacement is None:
                        dxn, dyn = None, None
                    else:
                        dxn, dyn = displacement

                    if dxn is None or dyn is None:
                        kpts_speed[kpt] = None
                    else:
                        dx = dxn * frame_width
                        dy = dyn * frame_height
                        speed = np.sqrt(dx**2 + dy**2) * fps  # pixels per second
                        kpts_speed[kpt] = speed
            list__obj__kpts_speed.append(kpts_speed)

        pred_data["list__obj__kpts_speed"] = list__obj__kpts_speed

    # compute speed relative to body
    for frame_idx, json_file in enumerate(tqdm(json_files, desc="Predicting actions")):
        pred_data = predictions[json_file]

        # Get object tracks and keypoints
        list__obj__id_track = pred_data.get(
            "list__obj__id_track", [None] * len(pred_data["list__obj__box_xcycwhn"])
        )
        list__obj__kpts_speed = pred_data["list__obj__kpts_speed"]

        list__obj__kpts_speed_relative = []
        for i_obj, id_track in enumerate(list__obj__id_track):
            kpts_speed = list__obj__kpts_speed[i_obj]

            anchor_speeds = [
                kpts_speed[anchor]
                for anchor in anchors
                if kpts_speed[anchor] is not None
            ]
            if not anchor_speeds:
                kpts_speed_relative = None
            else:
                avg_anchor_speed = np.mean(anchor_speeds)
                kpts_speed_relative = {}
                for kpt, speed in kpts_speed.items():
                    if speed is None:
                        kpts_speed_relative[kpt] = None
                    else:
                        kpts_speed_relative[kpt] = speed / avg_anchor_speed
            list__obj__kpts_speed_relative.append(kpts_speed_relative)

        pred_data["list__obj__kpts_speed_relative"] = list__obj__kpts_speed_relative

    for json_file, pred_data in predictions.items():
        with open(os.path.join(output_dir, json_file), "w") as f:
            json.dump(pred_data, f, indent=4)


if __name__ == "__main__":

    for subpathf in [
        "fall_violence/test/fall/Falling_and_Slow_Falling.mp4",
        "fall_violence/test/violence/Fighting_1.mp4",
        "fall_violence/test/violence/Fighting_2.mp4",
        "fall_violence/test/violence/Fighting_3.mp4",
        "fall_violence/test/violence/Fighting_4.mp4",
    ]:
        kwargs = {
            "input_dir": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-displacement/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-0.25-extend-wrist-hip/{}/labels".format(
                subpathf
            ),
            "output_dir": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-speed/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-0.25-extend-wrist-hip/{}/labels".format(
                subpathf
            ),
            "displacement_key": "list__obj__kpts_displacement_average",  # list__obj__kpts_displacement, list__obj__kpts_displacement_ema, list__obj__kpts_displacement_average
            "anchors": ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
            "fps": 15,
            "frame_width": 1920,
            "frame_height": 1080,
        }
        run(**kwargs)
