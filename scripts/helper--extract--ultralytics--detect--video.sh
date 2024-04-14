PATH__DIR__VIDEO=/home/laptq/Downloads/videos

PATH__FILE__MODEL=/home/laptq/Downloads/yolo11n.pt

PATH__DIR__IMAGE__OUTPUT=/home/laptq/Downloads/outputs--video--1
PATH__DIR__LABEL__OUTPUT=/home/laptq/Downloads/outputs--video--1

declare -A MAP__NAME_VIDEO__TO__=(
    ["clideo_editor_177d5d7cdb144c1598d5419573b0449c.mp4"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__file__input="${PATH__DIR__VIDEO}/${name__video}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${name__video}/images"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${name__video}/labels"

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
        --pad__id_frame 6
        
done