# PATH__DIR__VIDEO=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper-convert-video-to-images
PATH__DIR__VIDEO=/mnt/ssd2/shared_workspace/cuongdh/FSPRJ26/data/250516/rotate

TO_USE__YOLOv5_COMPAT=False
PATH__FILE__MODEL=yolov8x-pose.pt
ID__DATA=None
ID__MODEL=yolov8x-pose
ID__TRAIN=None

IMGSZ=640
THRESH__CONF__MIN=0.1
THRESH__IOU=0.45
ID__PREDICT=imgsz-$IMGSZ--conf-$THRESH__CONF__MIN--iou-$THRESH__IOU

DEVICE="cuda:1"
NUM__PAD__0=9

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--video
# PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials
POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--${ID__DATA}--MODEL--${ID__MODEL}--TRAIN--${ID__TRAIN}--PREDICT--${ID__PREDICT}--all-keypoints--JSON"


declare -A MAP__SUBPATH_VIDEO__TO__=(
    # ["R7_2025_05_15_23_40_32_rotate.mp4"]=""
    # ["R8_2025_05_15_23_40_32_rotate.mp4"]=""
    # ["R3_2025_05_15_23_40_32_rotate.mp4"]=""
    ["R4_2025_05_15_23_40_32_rotate.mp4"]=""
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
        helper__extract__ultralytics__video \
        --path__file__input "${path__file__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device $DEVICE \
        --imgsz $IMGSZ \
        --thresh__conf__min $THRESH__CONF__MIN \
        --thresh__iou $THRESH__IOU \
        --to_save__img False \
        --num__pad__0 $NUM__PAD__0 \
        --to_use__yolov5_compat $TO_USE__YOLOv5_COMPAT \
        --task track \
        --persist True \
        --list__name_keypoints "['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']" \
        --thresh__conf__keypoints__min 0.0 \

    echo -e "${TAG__INFO} Done: ${subpath__video}"
        
done