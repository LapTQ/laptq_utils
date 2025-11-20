PATH__DIR__MEDIA = "/media/home4/free_space/bachws/actiondata/awlvn_shopping_ds/videos"  # can be ignored if pad__max not set
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL__INPUT = (
    "/home/laptq/laptq-fs26-shoplifting-detection/data/ground-truth/fs26"
)
POSTFIX__DIR__LABEL__INPUT = ""

PATH__DIR__LABEL__OUTPUT = (
    "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--rescale--detection--box/fs26/ground-truth"
)
POSTFIX__DIR__LABEL__OUTPUT = ""

# Define the map of subpaths
MAP__SUBPATH_MEDIA__TO__ = {
    "shoplifting-25min.mp4": None,
    # "r9_25min_rotate.mp4": None,
}
# -----
# import os
# import glob

# MAP__SUBPATH_MEDIA__TO__ = {
#     p[len(PATH__DIR__MEDIA) + 1 :]: None
#     for p in glob.glob(f"{PATH__DIR__MEDIA}/*.mp4")
#     # if os.path.isdir(p)
#     if os.path.isfile(p)
# }

# =============================================================
import os
import subprocess
from laptq_pyutils.helper import helper__rescale__detection__box
import shutil
from multiprocessing import Pool
import multiprocessing as mp


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__lbl__input']}")
    helper__rescale__detection__box(**kwargs)
    print(f"{TAG__PASSED} Done: {kwargs['path__dir__lbl__input']}")

    num__lbl__input = len(os.listdir(kwargs["path__dir__lbl__input"]))
    num__lbl__output = len(os.listdir(kwargs["path__dir__lbl__output"]))

    if num__lbl__output != num__lbl__input:
        print(
            f"{TAG__FAILED} Number of labels mismatched: {kwargs['path__dir__lbl__input']}"
        )
        print(f"    [+] {num__lbl__input} old labels")
        print(f"    [+] {num__lbl__output} new labels")
        exit(1)
    else:
        print(
            f"{TAG__PASSED} {num__lbl__input} old labels == {num__lbl__output} target labels: {kwargs['path__dir__lbl__input']}"
        )


ls_kwargs = []

# Iterate over the subpaths
for subpath in MAP__SUBPATH_MEDIA__TO__:
    path__dir__img = f"{PATH__DIR__MEDIA}/{subpath}/images{POSTFIX__DIR__IMAGE}"
    path__file__video = f"{PATH__DIR__MEDIA}/{subpath}"
    path__dir__lbl__input = (
        f"{PATH__DIR__LABEL__INPUT}/{subpath}/labels{POSTFIX__DIR__LABEL__INPUT}"
    )
    path__dir__lbl__output = (
        f"{PATH__DIR__LABEL__OUTPUT}/{subpath}/labels{POSTFIX__DIR__LABEL__OUTPUT}"
    )

    # Remove existing
    if os.path.exists(path__dir__lbl__output):
        shutil.rmtree(path__dir__lbl__output)
    os.makedirs(path__dir__lbl__output)

    kwargs = dict(
        path__dir__img=path__dir__img,
        path__file__video=path__file__video,
        type_media="imgdir",  # imgdir, video
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__lbl__output=path__dir__lbl__output,
        ratio__w=2,
        ratio__h=1.4,
        pad__w__max=None,
        pad__h__max=None,
        cut__w__max=None,
        cut__h__max=None,
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(15) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
