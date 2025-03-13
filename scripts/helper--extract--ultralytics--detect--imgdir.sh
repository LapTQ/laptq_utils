PATH__DIR__IMAGE=/home/laptq/laptq-prj-21/data/Videos--to--frames/241210_受け取り動画/mp4
POSTFIX__DIR__IMAGE=""

TO_USE__YOLOv5_COMPAT=True
# PATH__FILE__MODEL=/home/laptq/laptq-prj-21/runs/data--phase2-4cam-factory--phase1-4cam-factory/yolov5s--640--scale-0.5--multiscale-True/exp/weights/best.pt
# ID__DATA=data--phase2-4cam-factory--phase1-4cam-factory
PATH__FILE__MODEL=/home/laptq/laptq-prj-21/runs/data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person/yolov5s--832--scale-0.5--multiscale-True/exp/weights/best.pt
ID__DATA=data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person
ID__MODEL=yolov5s--832--scale-0.5--multiscale-True
ID__TRAIN=exp

IMGSZ=640
THRESH__CONF__MIN=0.01
THRESH__IOU=0.45
ID__PREDICT=imgsz-$IMGSZ--conf-$THRESH__CONF__MIN--iou-$THRESH__IOU

DEVICE="cuda:2"

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-21/outputs/20250310--labels
POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--${ID__DATA}--MODEL--${ID__MODEL}--TRAIN--${ID__TRAIN}--PREDICT--${ID__PREDICT}--JSON"

declare -A MAP__SUBPATH_DIR__TO__=(
    ["Camera_47/Camera_47_1_2025-01-30_000000.3gp"]=""
    ["Camera_48/Camera_48_1_2025-01-30_000000.3gp"]=""
    ["Camera_49/Camera_49_1_2025-01-30_000000.3gp"]=""
    ["Camera_50/Camera_50_1_2025-01-30_000000.3gp"]=""
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
        --device $DEVICE \
        --imgsz $IMGSZ \
        --thresh__conf__min $THRESH__CONF__MIN \
        --thresh__iou $THRESH__IOU \
        --to_use__yolov5_compat $TO_USE__YOLOv5_COMPAT
    
    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done