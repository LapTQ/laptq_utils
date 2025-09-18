# Define paths and postfixes
PATHD_INPUT_IMAGE = "/home/laptq/laptq-prj-46/outputs/copy-hard--dataset"
POSTFIXD_IMAGE = ""

PATHD_INPUT_EMBEDDING = "/home/laptq/laptq-prj-46/outputs/helper--extract--image--embedding/fs-gray"
POSTFIXD_EMBEDDING = ""

PATHD_OUTPUT = "/home/laptq/laptq-prj-46/outputs/helper--cluster--images--by--embeddings"

MAP__GROUP__TO__LS_SUBDPATHD = {
    # "fs-1": [
        # "roboflow/pot01/images/train",
        # "roboflow/pot02/images/train",
        # "roboflow/pot03/images/train",
        # "roboflow/pot04/images/train",
        # "roboflow/pot05/images/train",
        # "roboflow/pot06/images/train",
        # "roboflow/pot07/images/train",
        # "roboflow/pot08/images/train",
        # "roboflow/pot09/images/train",
        # "roboflow/pot10/images/train",
    # ],
    # "fs-2": [
    #     "roboflow/pot11/images/train",
    #     "roboflow/pot12/images/train",
    #     "roboflow/pot13/images/train",
    #     "roboflow/pot14/images/train",
    #     "roboflow/pot15/images/train",
    #     "roboflow/pot16/images/train",
    #     "roboflow/pot17/images/train",
    #     "roboflow/pot18/images/train",
    #     "roboflow/pot19/images/train",
    # ],
    # "fs-3": [
    #     "roboflow/pot20/images/train",
    #     "roboflow/pot21/images/train",
    # ]
    # "fs-4": [
    #     "fs-1/images",
    #     "fs-2/images",
    #     "fs-3/images",
    # ],
    # "fs-v1": [
    #     "roboflow/pot02/images/valid",
    #     "roboflow/pot03/images/valid",
    #     "roboflow/pot04/images/valid",
    #     "roboflow/pot06/images/valid",
    #     "roboflow/pot07/images/valid",
    #     "roboflow/pot08/images/valid",
    #     "roboflow/pot09/images/valid",
    #     "roboflow/pot10/images/valid",
    #     "roboflow/pot11/images/valid",
    #     "roboflow/pot12/images/valid",
    #     "roboflow/pot13/images/valid",
    #     "roboflow/pot14/images/valid",
    #     "roboflow/pot15/images/valid",
    #     "roboflow/pot16/images/valid",
    #     "roboflow/pot17/images/valid",
    #     "roboflow/pot18/images/valid",
    #     "roboflow/pot19/images/valid",
    #     "roboflow/pot20/images/valid",
    #     "roboflow/pot21/images/valid",
    # ],
    # "fs-t1": [
    #     "roboflow/pot02/images/test",
    #     "roboflow/pot03/images/test",
    #     "roboflow/pot04/images/test",
    #     "roboflow/pot07/images/test",
    #     "roboflow/pot08/images/test",
    #     "roboflow/pot09/images/test",
    #     "roboflow/pot10/images/test",
    #     "roboflow/pot11/images/test",
    #     "roboflow/pot12/images/test",
    #     "roboflow/pot13/images/test",
    #     "roboflow/pot14/images/test",
    #     "roboflow/pot15/images/test",
    #     "roboflow/pot16/images/test",
    #     "roboflow/pot17/images/test",
    #     "roboflow/pot18/images/test",
    #     "roboflow/pot19/images/test",
    #     "roboflow/pot20/images/test",
    #     "roboflow/pot21/images/test",
    # ],
    # "fs-6": [
    #     "fs-4/images",
    #     "fs-v1/images",
    #     "fs-t1/images",
    # ],
    # "fs-7": [
    #     "dataset-ninja/ds1_simplex-test/images",
    #     "dataset-ninja/ds1_simplex-train/images",
    #     "dataset-ninja/ds2_complex-test/images",
    #     "dataset-ninja/ds2_complex-train/images",
    #     "pothole_dataset_v8/train/images",
    #     "pothole_dataset_v8/train_to_valid/images",
    #     "pothole_dataset_v8/valid/images",
    #     "pot_det_1240/images",
    # ],
    "fs-9": [
        "APTO_v2/day1_330/images",
        "APTO_v2/night1_190/images",
        "APTO_v2/night3_44/images",
        "APTO_v2/night4_239/images",
        "Pothole_detection_yolo/train_original/images",
        "RDD2022_JAPAN/only_pothole/train/images",
        "fs-6/images",
    ],
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
for group in MAP__GROUP__TO__LS_SUBDPATHD:
    list__subpathd = MAP__GROUP__TO__LS_SUBDPATHD[group]
    list__path__dir__img__input = [
        f"{PATHD_INPUT_IMAGE}/{subpathd}/images{POSTFIXD_IMAGE}"
        for subpathd in list__subpathd
    ]
    list__path__dir__emb__input = [
        f"{PATHD_INPUT_EMBEDDING}/{subpathd}/embeddings{POSTFIXD_EMBEDDING}"
        for subpathd in list__subpathd
    ]
    path__dir__output = f"{PATHD_OUTPUT}/{group}"

    # Remove existing directories if they exist
    if os.path.exists(path__dir__output):
        shutil.rmtree(path__dir__output)

    # Call the helper function
    helper__cluster__images__by__embeddings(
        list__path__dir__img__input=list__path__dir__img__input,
        list__path__dir__emb__input=list__path__dir__emb__input,
        path__dir__output=path__dir__output,
        device="cuda:3",
        batch_size=512,
        linkage="single",
        thresh__similarity=0.97,    # 0.97/0.98 OK
    )

    print(f"{TAG__INFO} Done: {group}")
