import os
import json
from tqdm import tqdm

from laptq_pyutils.objects import MajorVoteActionPredictor


def helper__major_vote_action(**kwargs):
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
