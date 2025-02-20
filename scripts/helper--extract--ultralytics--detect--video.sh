PATH__DIR__VIDEO=/home/laptq/Downloads/videos

PATH__FILE__MODEL=/home/laptq/Downloads/yolo11n.pt

PATH__DIR__IMAGE__OUTPUT=/home/laptq/Downloads/outputs--video--1
POSTFIX__DIR__IMAGE__OUTPUT=""
PATH__DIR__LABEL__OUTPUT=/home/laptq/Downloads/outputs--video--1
POSTFIX__DIR__LABEL__OUTPUT=""

declare -A MAP__SUBPATH_VIDEO__TO__=(
    # ["1_2024-11-26_081159_0_5min.mp4"]=""
    # ["1_2024-11-26_081159_1_5min.mp4"]=""
    # ["1_2024-11-26_081159_2_5min.mp4"]=""
    # ["1_2024-11-26_081159_3_5min.mp4"]=""

    ["1_2024-11-26_081159_0.mp4"]=""
    ["1_2024-11-26_081159_1.mp4"]=""
    ["1_2024-11-26_081159_2.mp4"]=""
    ["1_2024-11-26_081159_3.mp4"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__video in "${!MAP__SUBPATH_VIDEO__TO__[@]}"; do
    path__file__input="${PATH__DIR__VIDEO}/${subpath__video}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${subpath__video}/images${POSTFIX__DIR__IMAGE__OUTPUT}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__video}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__img__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 main.py \
        helper__extract__ultralytics__detect__video \
        --path__file__input "${path__file__input}" \
        --path__dir__img__output "${path__dir__img__output}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device "cuda:0" \
        --imgsz 640 \
        --thresh__conf__min 0.01 \
        --to_save__img False \
        --num__pad__0 6

    echo -e "${TAG__INFO} Done: ${subpath__video}"
        
done