# Define paths and postfixes
PATHD_INPUT = "/home/laptq/laptq-prj-46/outputs/copy-hard--dataset"
POSTFIXD_IMAGE = ""

PATHD_OUTPUT = "/home/laptq/laptq-prj-46/outputs/helper--extract--image--embedding/fs-gray"
POSTFIXD_OUTPUT = ""

MAP__SUBPATHD__TO__ = {
    "parrot": None,
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
    path__dir__input = f"{PATHD_INPUT}/{subpathd}/images{POSTFIXD_IMAGE}"
    path__dir__output = f"{PATHD_OUTPUT}/{subpathd}/embeddings{POSTFIXD_OUTPUT}"

    # Remove existing directories if they exist
    if os.path.exists(path__dir__output):
        shutil.rmtree(path__dir__output)

    # Call the helper function
    helper__extract__image__embedding(
        path__dir__input=path__dir__input,
        path__dir__output=path__dir__output,
        model="ViT-B/32",
        device="cuda:3",
        to_gray=True,
        to_normalize=True,
    )

    print(f"{TAG__INFO} Done: {subpathd}")
