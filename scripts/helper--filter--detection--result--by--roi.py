PATH__DIR__LABEL__INPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics/fs26/satudora"
POSTFIX__DIR__LABEL__INPUT = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"

PATH__DIR__LABEL__OUTPUT = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--filter--detection--result--by--roi/fs26/satudora"
POSTFIX__DIR__LABEL__OUTPUT = "--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--filter-roi--all-keypoints--JSON"

MAP__SUBPATH_DIR__TO__ = {
    "R3_2025_05_15_23_40_32_rotate.mp4": [
        [0.2212962955236435, 0.09166666865348816],
        [0.0824074074625969, 0.45364582538604736],
        [0.003703703638166189, 0.4619791805744171],
        [0.0027777778450399637, 0.9911458492279053],
        [0.9935185313224792, 0.9880208373069763],
        [0.9944444298744202, 0.25572916865348816],
        [0.6314814686775208, 0.06458333134651184],
    ],
    "R4_2025_05_15_23_40_32_rotate.mp4": [
        [0.4027777910232544, 0.0031250000465661287],
        [0.003703703638166189, 0.34375],
        [0.003703703638166189, 0.9927083253860474],
        [0.9953703880310059, 0.9880208373069763],
        [0.9953703880310059, 0.2692708373069763],
        [0.6796296238899231, 0.008333333767950535],
    ],
    "R7_2025_05_15_23_40_32_rotate.mp4": [
        [0.3740740716457367, 0.03593749925494194],
        [0.003703703638166189, 0.23854166269302368],
        [0.0055555556900799274, 0.9901041388511658],
        [0.9944444298744202, 0.987500011920929],
        [0.9944444298744202, 0.30000001192092896],
        [0.779629647731781, 0.2802083194255829],
        [0.6842592358589172, 0.03958333283662796],
    ],
    "R8_2025_05_15_23_40_32_rotate.mp4": [
        [0.2777777910232544, 0.06145833432674408],
        [0.003703703638166189, 0.4453125],
        [0.004629629664123058, 0.9911458492279053],
        [0.9953703880310059, 0.989062488079071],
        [0.9944444298744202, 0.41354167461395264],
        [0.6407407522201538, 0.0625],
    ],
    "R9_2025_05_15_23_40_32_rotate.mp4": [
        [0.6324074268341064, 0.14374999701976776],
        [0.3490740656852722, 0.12916666269302368],
        [0.14166666567325592, 0.3864583373069763],
        [0.004629629664123058, 0.38593751192092896],
        [0.004629629664123058, 0.9911458492279053],
        [0.9953703880310059, 0.9880208373069763],
        [0.9953703880310059, 0.44843751192092896],
    ],
    "R10_2025_05_15_23_40_32_rotate.mp4": [
        [0.07407407462596893, 0.10260416567325592],
        [0.003703703638166189, 0.13229165971279144],
        [0.003703703638166189, 0.995312511920929],
        [0.9953703880310059, 0.989062488079071],
        [0.9953703880310059, 0.06927083432674408],
        [0.8259259462356567, 0.05364583432674408],
        [0.8305555582046509, 0.07135416567325592],
        [0.5574073791503906, 0.06979166716337204],
        [0.5425925850868225, 0.03697916492819786],
        [0.26851850748062134, 0.06302083283662796],
        [0.2777777910232544, 0.09375],
    ],
}


# =============================================================
import os
import shutil
import subprocess
from laptq_pyutils.helper import helper__filter__detection__result__by__roi
from multiprocessing import Pool
import multiprocessing as mp


# Define tags for logging
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def run_wrapper(kwargs):
    print(f"{TAG__INFO} Processing: {kwargs['path__dir__lbl__input']}")
    helper__filter__detection__result__by__roi(**kwargs)
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

for subpath__dir in MAP__SUBPATH_DIR__TO__:
    path__dir__lbl__input = (
        f"{PATH__DIR__LABEL__INPUT}/{subpath__dir}/labels{POSTFIX__DIR__LABEL__INPUT}"
    )
    path__dir__lbl__output = (
        f"{PATH__DIR__LABEL__OUTPUT}/{subpath__dir}/labels{POSTFIX__DIR__LABEL__OUTPUT}"
    )

    if os.path.exists(path__dir__lbl__output):
        shutil.rmtree(path__dir__lbl__output)
    os.makedirs(path__dir__lbl__output)

    kwargs = dict(
        path__dir__lbl__input=path__dir__lbl__input,
        path__dir__lbl__output=path__dir__lbl__output,
        roi__polygonn=MAP__SUBPATH_DIR__TO__[subpath__dir],
        thresh__miniou=0.3,
    )

    ls_kwargs.append(kwargs)


# # ============ sequential =============
# for kwargs in ls_kwargs:
#     run_wrapper(kwargs)
# ============ parallel =============
with Pool(15) as p:
    p.map(run_wrapper, ls_kwargs)
# ===================================
