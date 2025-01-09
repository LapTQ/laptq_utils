# PATH__DIR__VIDEO=/home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4_5min
PATH__DIR__VIDEO=/home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4

PATH__FILE__MODEL=/home/laptq/laptq-prj-21/runs/data--syn-text2image-satudora-center--satudora-center-box/yolov5s--832--scale-0.5--multiscale-True/exp/weights/best.pt

PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-21/runs/data--syn-text2image-satudora-center--satudora-center-box/yolov5s--832--scale-0.5--multiscale-True/predict--exp--imgsz-832--conf-0.1/predict
POSTFIX__DIR__IMAGE__OUTPUT=""
PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-21/runs/data--syn-text2image-satudora-center--satudora-center-box/yolov5s--832--scale-0.5--multiscale-True/predict--exp--imgsz-832--conf-0.1/predict
POSTFIX__DIR__LABEL__OUTPUT="--conf-0.001"


declare -A MAP__NAME_VIDEO__TO__=(
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


for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__file__input="${PATH__DIR__VIDEO}/${name__video}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${name__video}/images${POSTFIX__DIR__IMAGE__OUTPUT}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${name__video}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__img__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__extract__ultralytics__detect__video \
        --path__file__input "${path__file__input}" \
        --path__dir__img__output "${path__dir__img__output}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device "cuda:2" \
        --imgsz 832 \
        --thresh__conf__min 0.001 \
        --num__pad__0 6

    echo -e "${TAG__INFO} Done: ${name__video}"
        
done