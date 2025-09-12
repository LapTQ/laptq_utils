# Define paths and postfixes
PATHD_INPUT_IMAGE = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/road-issues-detection"
POSTFIXD_IMAGE = ""

PATHD_INPUT_EMBEDDING = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/helper--extract--image--embedding/prj46"
POSTFIXD_EMBEDDING = ""

PATHD_OUTPUT = "/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/helper--cluster--images--by--embeddings/fs"

MAP__GROUP__TO__LS_SUBDPATHD = {
    "fs": [
        "APTO_v2/day1_330",
        "APTO_v2/night1_190",
        "APTO_v2/night3_44",
        "APTO_v2/night4_239",
        "dataset-ninja/ds1_simplex-test",
        "dataset-ninja/ds1_simplex-train",
        "dataset-ninja/ds2_complex-test",
        "dataset-ninja/ds2_complex-train",
        "pot_det_1240",
        "pothole_dataset_v8/train",
        "pothole_dataset_v8/train_to_valid",
        "pothole_dataset_v8/valid",
        "Pothole_detection_yolo/train_original",
        "RDD2022_JAPAN/only_pothole/train",
        "roboflow/pot01",
        "roboflow/pot02",
        "roboflow/pot03",
        "roboflow/pot04",
        "roboflow/pot05",
        "roboflow/pot06",
        "roboflow/pot07",
        "roboflow/pot08",
        "roboflow/pot09",
        "roboflow/pot10",
        "roboflow/pot11",
        "roboflow/pot12",
        "roboflow/pot13",
        "roboflow/pot14",
        "roboflow/pot15",
        "roboflow/pot16",
        "roboflow/pot17",
        "roboflow/pot18",
        "roboflow/pot19",
        "roboflow/pot20",
        "roboflow/pot21",
    ]
    
}

# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__cluster__images__by__embeddings


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"

# Iterate over the subpaths
for group, list__subpathd in MAP__GROUP__TO__LS_SUBDPATHD:
    path__dir__input__img = (
        f"{PATHD_INPUT_IMAGE}/{group}/images{POSTFIXD_IMAGE}"
    )
    path__dir__input__emb = (
        f"{PATHD_INPUT_EMBEDDING}/{group}/embeddings{POSTFIXD_EMBEDDING}"
    )
    path__dir__output = (
        f"{PATHD_OUTPUT}/{group}"
    )

    # Remove existing directories if they exist
    if os.path.exists(path__dir__output):
        shutil.rmtree(path__dir__output)

    # Call the helper function
    helper__extract__image__embedding(
        path__dir__input__img=path__dir__input__img,
        path__dir__input__emb=path__dir__input__emb,
        path__dir__output=path__dir__output,
        list__subpathd=list__subpathd,
    )

    print(f"{TAG__INFO} Done: {group}")
