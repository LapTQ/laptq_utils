PATH__DIR__VIDEO=/mnt/ssd8tb/shared_workspace/manhpc/FS_prj21

PATH__FILE__MODEL=/home/laptq/laptq-prj-21/runs/data--synthetic/yolo11s--832--scale-0.5--multiscale-True/train/weights/best.pt

PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-21/runs/data--synthetic/yolo11s--832--scale-0.5--multiscale-True/predict--train--imgsz-832--conf-0.1/predict
PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-21/runs/data--synthetic/yolo11s--832--scale-0.5--multiscale-True/predict--train--imgsz-832--conf-0.1/predict

declare -A MAP__NAME_VIDEO__TO__=(
    ["1_2024-11-26_081159_0_30s.mp4"]=""
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

    python3 submodules/laptq_utils/main.py \
        helper__extract__ultralytics__detect__video \
        --path__file__input "${path__file__input}" \
        --path__dir__img__output "${path__dir__img__output}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device "cuda:0" \
        --imgsz 832 \
        --thresh__conf__min 0.1 \
        --pad__id_frame 6
        
done