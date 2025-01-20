PATH__DIR__VIDEO=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos--cropped

PATH__FILE__MODEL=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m-p2--960--crop-20/train/weights/best.pt

PATH__DIR__IMAGE__OUTPUT=/home/laptq/Downloads/outputs--video--1
POSTFIX__DIR__IMAGE__OUTPUT=""
PATH__DIR__LABEL__OUTPUT=/home/laptq/Downloads/outputs--video--1
POSTFIX__DIR__LABEL__OUTPUT=""

declare -A MAP__NAME_VIDEO__TO__=(
    ["00000049_2403050854_NR.MP4"]=""
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
        --device "cuda:0" \
        --imgsz 960 \
        --thresh__conf__min 0.01 \
        --to_save__img False \
        --num__pad__0 6

    echo -e "${TAG__INFO} Done: ${name__video}"
        
done