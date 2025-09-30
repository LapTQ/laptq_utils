import os
import json
import numpy as np
from tqdm import tqdm


class KeypointSpeedPredictor:

    def __init__(self, **kwargs):
        pass

    def predict(self, **kwargs):
        dict__result = kwargs["dict__result"]
        displacement_key = kwargs["displacement_key"]
        fps = kwargs["fps"]
        frame_width = kwargs["frame_width"]
        frame_height = kwargs["frame_height"]

        list__obj__kpts_displacement = dict__result[displacement_key]

        list__obj__kpts_speed = []
        for i_obj, kpts_displacement in enumerate(list__obj__kpts_displacement):

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

        dict__result["list__obj__kpts_speed"] = list__obj__kpts_speed

    def predict_relative_speed(self, **kwargs):
        dict__result = kwargs["dict__result"]
        anchors = kwargs["anchors"]

        # Get object tracks and keypoints
        list__obj__kpts_speed = dict__result["list__obj__kpts_speed"]

        list__obj__kpts_speed_relative = []
        for i_obj, kpts_speed in enumerate(list__obj__kpts_speed):

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

        dict__result["list__obj__kpts_speed_relative"] = list__obj__kpts_speed_relative


def run(**kwargs):
    pathd_lbl = kwargs["pathd_lbl"]
    pathd_output = kwargs["pathd_output"]

    kspeed_predictor = KeypointSpeedPredictor(**kwargs)

    for namef_lbl in tqdm(sorted(os.listdir(pathd_lbl)), desc="Predicting speed"):
        pathf_lbl = os.path.join(pathd_lbl, namef_lbl)

        # load cached pose prediction from YOLO
        with open(pathf_lbl, "r") as f:
            dict__result = json.load(f)

        # write to dict__result in-place
        kspeed_predictor.predict(
            dict__result=dict__result,
            **kwargs,
        )
        kspeed_predictor.predict_relative_speed(
            dict__result=dict__result,
            **kwargs,
        )

        # debug
        os.makedirs(pathd_output, exist_ok=True)
        with open(os.path.join(pathd_output, namef_lbl), "w") as f:
            json.dump(dict__result, f, indent=4)


if __name__ == "__main__":

    for subpathf in [
        "fall_violence/test/fall/Falling_and_Slow_Falling.mp4",
        "fall_violence/test/violence/Fighting_1.mp4",
        "fall_violence/test/violence/Fighting_2.mp4",
        "fall_violence/test/violence/Fighting_3.mp4",
        "fall_violence/test/violence/Fighting_4.mp4",
    ]:
        kwargs = {
            "pathd_lbl": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-displacement/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97/{}/labels".format(
                subpathf
            ),
            "pathd_output": "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-speed/ProtoGCN/prj54/v9__nturubg_mostvariant_leftstrip03_no_kickback_kicksth__le2i__punch0312__j--filter-punch-push-distance-nose-0.25-hip-0.2-leg-0.97/{}/labels".format(
                subpathf
            ),
            "displacement_key": "list__obj__kpts_displacement_average",  # list__obj__kpts_displacement, list__obj__kpts_displacement_ema, list__obj__kpts_displacement_average
            "anchors": ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
            "fps": 15,
            "frame_width": 1920,
            "frame_height": 1080,
        }
        run(**kwargs)
