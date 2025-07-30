PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images
POSTFIX__DIR__IMAGE=""

TO_USE__YOLOv5_COMPAT=False
PATH__FILE__MODEL=yolov8x-pose.pt
# PATH__FILE__MODEL=/home/laptq/laptq-fs26-shoplifting-detection/runs/bag-detection/yolov8s--640/train/weights/best.pt
ID__DATA=None
# ID__DATA=bag-detection
ID__MODEL=yolov8x-pose
# ID__MODEL=yolov8s
# ID__TRAIN=train
ID__TRAIN=exp

IMGSZ=640
# IMGSZ=960
THRESH__CONF__MIN=0.1
# THRESH__CONF__MIN=0.01
THRESH__IOU=0.45
ID__PREDICT=imgsz-$IMGSZ--conf-$THRESH__CONF__MIN--iou-$THRESH__IOU

DEVICE="cuda:4"

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--${ID__DATA}--MODEL--${ID__MODEL}--TRAIN--${ID__TRAIN}--PREDICT--${ID__PREDICT}--all-keypoints--JSON"
# POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--${ID__DATA}--MODEL--${ID__MODEL}--TRAIN--${ID__TRAIN}--PREDICT--${ID__PREDICT}--JSON"

# declare -A MAP__SUBPATH_DIR__TO__=(
#     ["shoplifting-25min.mp4"]=""
#     # ["satudora-1min.mp4"]=""
#     # ["1568080723085_67014_fix.mkv"]=""
#     # ["r10_10min_rotate.mp4"]=""
#     ["r9_25min_rotate.mp4"]=""
#     # ["R10_2025_05_15_23_40_32_rotate.mp4"]=""

#     # ["roboflow-data/filtered--w-label/0"]=""
#     # ["roboflow-data/filtered--w-label/1"]=""
#     # ["roboflow-data/filtered--w-label/2"]=""
#     # ["roboflow-data/filtered--w-label/3"]=""
#     # ["roboflow-data/filtered--w-label/4"]=""
#     # ["roboflow-data/filtered--w-label/5"]=""
#     # ["roboflow-data/filtered--w-label/6"]=""
#     # ["roboflow-data/filtered--w-label/7"]=""
#     # ["roboflow-data/filtered--w-label/8"]=""
#     # ["roboflow-data/filtered--w-label/9"]=""
#     # ["roboflow-data/filtered--w-label/10"]=""
#     # ["roboflow-data/filtered--w-label/11"]=""
#     # ["roboflow-data/filtered--w-label/12"]=""
#     # ["roboflow-data/filtered--w-label/13"]=""
#     # ["roboflow-data/filtered--w-label/14"]=""
#     # ["roboflow-data/filtered--w-label/15"]=""
#     # ["roboflow-data/filtered--w-label/16"]=""
#     # ["roboflow-data/filtered--w-label/17"]=""
#     # ["roboflow-data/filtered--w-label/18"]=""
#     # ["roboflow-data/filtered--w-label/19"]=""
#     # ["roboflow-data/filtered--w-label/20"]=""
#     # ["roboflow-data/filtered--w-label/21"]=""

#     # ["roboflow-data/filtered--wo-label/2"]=""
#     # ["roboflow-data/filtered--wo-label/3"]=""
#     # ["roboflow-data/filtered--wo-label/4"]=""
#     # ["roboflow-data/filtered--wo-label/5"]=""
#     # ["roboflow-data/filtered--wo-label/6"]=""
#     # ["roboflow-data/filtered--wo-label/7"]=""
#     # ["roboflow-data/filtered--wo-label/8"]=""
#     # ["roboflow-data/filtered--wo-label/10"]=""

#     # ["shoplifting-1min_anonymized.mp4"]=""
# )
# source /home/laptq/laptq-fs26-shoplifting-detection/data/mnit-video-paths.sh
source /home/laptq/laptq-fs26-shoplifting-detection/data/shoplifting-gen-video-paths.sh

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
        helper__extract__ultralytics__imgdir \
        --path__dir__img "${path__dir__img__input}" \
        --path__dir__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device $DEVICE \
        --imgsz $IMGSZ \
        --thresh__conf__min $THRESH__CONF__MIN \
        --thresh__iou $THRESH__IOU \
        --to_use__yolov5_compat $TO_USE__YOLOv5_COMPAT \
        --task track \
        --persist True \
        --list__name_keypoints "['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']" \
        --thresh__conf__keypoints__min 0.0 \
    
    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done