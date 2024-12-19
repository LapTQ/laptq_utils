PATH__DIR__IMAGE=/home/laptq/laptq-prj-44/outputs/20241217--merge--annotation--undo-split--erase-ignored--splitted
POSTFIX__DIR__IMAGE=""

PATH__FILE__MODEL=/home/laptq/laptq-prj-46/runs/general/yolo11x--800--weighted-fitness/train/weights/best.pt

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-44/outputs/trash
POSTFIX__DIR__LABEL__OUTPUT=""

declare -A MAP__SUBPATH_DIR__TO__=(
    ["beppu_sue-batch-1"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__extract__ultralytics__detect__imgdir \
        --path__dir__img "${path__dir__img__input}" \
        --path__dir__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device "cuda:1" \
        --imgsz 800 \
        --thresh__conf__min 0.01
        
done