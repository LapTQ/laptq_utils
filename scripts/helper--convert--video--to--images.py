PATH__DIR__VIDEO = "/home/laptq/laptq-fs26-shoplifting-detection/data"

PATH__DIR__IMAGE__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fs26"

# Define the map of subpaths
# MAP__SUBPATH_VIDEO__TO__={
#     "shoplifting-25min.mp4": None,
#     "r9_25min_rotate.mp4": None,
# }
# -----
import os
import glob

MAP__SUBPATH_VIDEO__TO__ = {
    p[len(PATH__DIR__VIDEO) + 1 :]: None
    for p in glob.glob(f"{PATH__DIR__VIDEO}/customer-video/20250901-1105/*.mkv")
    if os.path.isfile(p)
}

# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__convert__video__to__images
from multiprocessing import Pool
import multiprocessing as mp


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__file__input']}")

    helper__convert__video__to__images(**kwargs)

    print(f"{TAG__PASSED} Done: {kwargs['path__file__input']}")


ls_kwargs = []

for subpath__video in MAP__SUBPATH_VIDEO__TO__:
    path__file__input = f"{PATH__DIR__VIDEO}/{subpath__video}"
    path__dir__img__output = f"{PATH__DIR__IMAGE__OUTPUT}/{subpath__video}/images"

    if os.path.exists(path__dir__img__output):
        shutil.rmtree(path__dir__img__output)
    os.makedirs(path__dir__img__output)

    kwargs = dict(
        path__file__input=path__file__input,
        path__dir__img__output=path__dir__img__output,
        step_size=1,
        num__pad__0=9,
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(10) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
