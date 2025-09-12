# Define paths and postfixes
PATHD_INPUT = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/road-issues-detection"
# PATHD_INPUT = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs"
POSTFIXD_IMAGE = ""

PATHD_OUTPUT = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/helper--extract--image--embedding/prj46"
POSTFIXD_OUTPUT = ""

MAP__SUBPATHD__TO__ = {
    # "APTO_v2/day1_330": None,
    # "APTO_v2/night1_190": None,
    # "APTO_v2/night3_44": None,
    # "APTO_v2/night4_239": None,
    # "dataset-ninja/ds1_simplex-test": None,
    # "dataset-ninja/ds1_simplex-train": None,
    # "dataset-ninja/ds2_complex-test": None,
    # "dataset-ninja/ds2_complex-train": None,
    # "pot_det_1240": None,
    # "pothole_dataset_v8/train": None,
    # "pothole_dataset_v8/train_to_valid": None,
    # "pothole_dataset_v8/valid": None,
    # "Pothole_detection_yolo/train_original": None,
    # "RDD2022_JAPAN/only_pothole/train": None,
    "roboflow/pot01": None,
    "roboflow/pot02": None,
    "roboflow/pot03": None,
    "roboflow/pot04": None,
    "roboflow/pot05": None,
    "roboflow/pot06": None,
    "roboflow/pot07": None,
    "roboflow/pot08": None,
    "roboflow/pot09": None,
    "roboflow/pot10": None,
    "roboflow/pot11": None,
    "roboflow/pot12": None,
    "roboflow/pot13": None,
    "roboflow/pot14": None,
    "roboflow/pot15": None,
    "roboflow/pot16": None,
    "roboflow/pot17": None,
    "roboflow/pot18": None,
    "roboflow/pot19": None,
    "roboflow/pot20": None,
    "roboflow/pot21": None,
    # "trivials": None
}

# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__extract__image__embedding


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"

# Iterate over the subpaths
for subpathd in MAP__SUBPATHD__TO__:
    path__dir__input = (
        f"{PATHD_INPUT}/{subpathd}/images{POSTFIXD_IMAGE}"
    )
    path__dir__output = (
        f"{PATHD_OUTPUT}/{subpathd}/embeddings{POSTFIXD_OUTPUT}"
    )

    # Remove existing directories if they exist
    if os.path.exists(path__dir__output):
        shutil.rmtree(path__dir__output)

    # Call the helper function
    helper__extract__image__embedding(
        path__dir__input=path__dir__input,
        path__dir__output=path__dir__output,
        model="ViT-B/32",
        device="cuda:0",
        to_normalize=True,
    )

    print(f"{TAG__INFO} Done: {subpathd}")
