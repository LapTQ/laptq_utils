PATH__DIR__VIDEO=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos--cropped

PATH__FILE__MODEL=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m-p2--960--crop-20/train/weights/best.pt

PATH__DIR__IMAGE__OUTPUT=/home/laptq/Downloads/outputs--video--1
POSTFIX__DIR__IMAGE__OUTPUT=""
PATH__DIR__LABEL__OUTPUT=/home/laptq/Downloads/outputs--video--1
POSTFIX__DIR__LABEL__OUTPUT=""
# PATH__DIR__VIDEO=/home/laptq/laptq-prj-21/data/video-20250220

# TO_USE__YOLOv5_COMPAT=True
# PATH__FILE__MODEL=/home/laptq/laptq-prj-21/runs/data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person/yolov5s--832--scale-0.5--multiscale-True/exp/weights/best.pt
# ID__DATA=data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person
# ID__MODEL=yolov5s--832--scale-0.5--multiscale-True
# ID__TRAIN=exp

# IMGSZ=960
# THRESH__CONF__MIN=0.01
# ID__PREDICT=imgsz-$IMGSZ--conf-$THRESH__CONF__MIN

# DEVICE="cuda:0"
# NUM__PAD__0=9

# PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-21/outputs/20250220--labels
# POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--${ID__DATA}--MODEL--${ID__MODEL}--TRAIN--${ID__TRAIN}--PREDICT--${ID__PREDICT}--JSON"


declare -A MAP__NAME_VIDEO__TO__=(
    ["00000049_2403050854_NR.MP4"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__video in "${!MAP__SUBPATH_VIDEO__TO__[@]}"; do
    path__file__input="${PATH__DIR__VIDEO}/${subpath__video}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__video}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__extract__ultralytics__detect__video \
        --path__file__input "${path__file__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device $DEVICE \
        --imgsz $IMGSZ \
        --thresh__conf__min $THRESH__CONF__MIN \
        --to_save__img False \
        --num__pad__0 $NUM__PAD__0 \
        --to_use__yolov5_compat $TO_USE__YOLOv5_COMPAT

    echo -e "${TAG__INFO} Done: ${subpath__video}"
        
done