PATH__DIR__IMAGE=/home/laptq/laptq-prj-21/data/Videos--to--frames/241210_受け取り動画/mp4_5min
POSTFIX__DIR__IMAGE=""

PATH__FILE__MODEL=/home/laptq/laptq-prj-21/runs/data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person/yolov5s--832--scale-0.5--multiscale-True/exp/weights/best.pt
ID__MODEL=yolov5s--832--scale-0.5--multiscale-True--exp

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-21/outputs/trivial/${ID__MODEL}
POSTFIX__DIR__LABEL__OUTPUT="--pred--json"

declare -A MAP__SUBPATH_DIR__TO__=(
    ["1_2024-11-26_081159_0_5min.mp4"]=""
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
        --device "cuda:0" \
        --imgsz 832 \
        --thresh__conf__min 0.01 \
        --to_use__yolov5_compat True
    
    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done