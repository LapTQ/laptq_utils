# Define paths and postfixes
PATHD_INPUT_IMAGE = "/home/laptq/datasets/COCO--reformated"
POSTFIXD_IMAGE = ""

PATHD_INPUT_EMBEDDING = "/home/laptq/Downloads/helper--extract--image--embedding/prj46"
POSTFIXD_EMBEDDING = ""

PATHD_OUTPUT = "/home/laptq/Downloads/helper--cluster--images--by--embeddings"

MAP__GROUP__TO__LS_SUBDPATHD = {
    "fs": [
        "parrot",
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
        device="cuda:0",
        batch_size=256,
        thresh__similarity=0.97,
    )

    print(f"{TAG__INFO} Done: {group}")
