# Define paths and postfixes
PATHD_INPUT = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/road-issues-detection"
# PATHD_INPUT = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs"
POSTFIXD_IMAGE = ""

PATHD_OUTPUT = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/helper--extract--image--embedding/prj46"
POSTFIXD_OUTPUT = ""

MAP__SUBPATHD__TO__ = {
    # "APTO_v2/day1_330/images": None,
    # "APTO_v2/night1_190/images": None,
    # "APTO_v2/night3_44/images": None,
    # "APTO_v2/night4_239/images": None,
    # "dataset-ninja/ds1_simplex-test/images": None,
    # "dataset-ninja/ds1_simplex-train/images": None,
    # "dataset-ninja/ds2_complex-test/images": None,
    # "dataset-ninja/ds2_complex-train/images": None,
    # "pot_det_1240/images": None,
    # "pothole_dataset_v8/train/images": None,
    # "pothole_dataset_v8/train_to_valid/images": None,
    # "pothole_dataset_v8/valid/images": None,
    # "Pothole_detection_yolo/train_original/images": None,
    # "RDD2022_JAPAN/only_pothole/train/images": None,
    "roboflow/pot01/images/train": None,
    "roboflow/pot02/images/train": None,
    "roboflow/pot03/images/train": None,
    "roboflow/pot04/images/train": None,
    "roboflow/pot05/images/train": None,
    "roboflow/pot06/images/train": None,
    "roboflow/pot07/images/train": None,
    "roboflow/pot08/images/train": None,
    "roboflow/pot09/images/train": None,
    "roboflow/pot10/images/train": None,
    "roboflow/pot11/images/train": None,
    "roboflow/pot12/images/train": None,
    "roboflow/pot13/images/train": None,
    "roboflow/pot14/images/train": None,
    "roboflow/pot15/images/train": None,
    "roboflow/pot16/images/train": None,
    "roboflow/pot17/images/train": None,
    "roboflow/pot18/images/train": None,
    "roboflow/pot19/images/train": None,
    "roboflow/pot20/images/train": None,
    "roboflow/pot21/images/train": None,
    # "trivials/images": None
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
        f"{PATHD_INPUT}/{subpathd}{POSTFIXD_IMAGE}"
    )
    path__dir__output = (
        f"{PATHD_OUTPUT}/{subpathd.replace('/images/', '/embeddings/')}"
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
