# PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images
PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/sample_frames_by_skipping/full
POSTFIX__DIR__IMAGE=""

# PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
# PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--video
PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/sample_frames_by_skipping/full
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.4--iou-0.45--filterby-size--all-keypoints--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--None--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"
POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"

PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--crops--from--detection
POSTFIX__DIR__OUTPUT=""

declare -A MAP__SUBPATH_DIR__TO__=(
    # ["shoplifting-25min.mp4"]=""
    ["r9_25min_rotate.mp4"]=""
    # ["R7_2025_05_15_23_40_32_rotate.mp4"]=""
    # ["R8_2025_05_15_23_40_32_rotate.mp4"]=""
    # ["R3_2025_05_15_23_40_32_rotate.mp4"]=""
    # ["R4_2025_05_15_23_40_32_rotate.mp4"]=""
    # ["R9_2025_05_15_23_40_32_rotate.mp4"]=""
    # ["R10_2025_05_15_23_40_32_rotate.mp4"]=""

    # ["roboflow-data/filtered--w-label/0"]=""
    # ["roboflow-data/filtered--w-label/1"]=""
    # ["roboflow-data/filtered--w-label/2"]=""
    # ["roboflow-data/filtered--w-label/3"]=""
    # ["roboflow-data/filtered--w-label/4"]=""
    # ["roboflow-data/filtered--w-label/5"]=""
    # ["roboflow-data/filtered--w-label/6"]=""
    # ["roboflow-data/filtered--w-label/7"]=""
    # ["roboflow-data/filtered--w-label/8"]=""
    # ["roboflow-data/filtered--w-label/9"]=""
    # ["roboflow-data/filtered--w-label/10"]=""
    # ["roboflow-data/filtered--w-label/11"]=""
    # ["roboflow-data/filtered--w-label/12"]=""
    # ["roboflow-data/filtered--w-label/13"]=""
    # ["roboflow-data/filtered--w-label/14"]=""
    # ["roboflow-data/filtered--w-label/15"]=""
    # ["roboflow-data/filtered--w-label/16"]=""
    # ["roboflow-data/filtered--w-label/17"]=""
    # ["roboflow-data/filtered--w-label/18"]=""
    # ["roboflow-data/filtered--w-label/19"]=""
    # ["roboflow-data/filtered--w-label/20"]=""
    # ["roboflow-data/filtered--w-label/21"]=""

    # ["roboflow-data/filtered--wo-label/2"]=""
    # ["roboflow-data/filtered--wo-label/3"]=""
    # ["roboflow-data/filtered--wo-label/4"]=""
    # ["roboflow-data/filtered--wo-label/5"]=""
    # ["roboflow-data/filtered--wo-label/6"]=""
    # ["roboflow-data/filtered--wo-label/7"]=""
    # ["roboflow-data/filtered--wo-label/8"]=""
    # ["roboflow-data/filtered--wo-label/10"]=""
)
# source /home/laptq/laptq-fs26-shoplifting-detection/data/mnit-video-paths.sh
source /home/laptq/laptq-fs26-shoplifting-detection/data/shoplifting-gen-video-paths.sh

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_VIDEO__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl__input="${PATH__DIR__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__crop__img__output="${PATH__DIR__OUTPUT}/${subpath__dir}/{}/images${POSTFIX__DIR__OUTPUT}"
    path__dir__crop__lbl__output="${PATH__DIR__OUTPUT}/${subpath__dir}/{}/labels${POSTFIX__DIR__OUTPUT}"

    [[ -d "${path__dir__crop__img__output}" ]] && rm -r "${path__dir__crop__img__output}"
    [[ -d "${path__dir__crop__lbl__output}" ]] && rm -r "${path__dir__crop__lbl__output}"

    # check if "{}" is in path
    if [[ "${path__dir__crop__img__output}" != *"{}"* ]]; then
        mkdir -p "${path__dir__crop__img__output}"
    fi
    if [[ "${path__dir__crop__lbl__output}" != *"{}"* ]]; then
        mkdir -p "${path__dir__crop__lbl__output}"
    fi

    python3 submodules/laptq_utils/main.py \
        helper__extract__crops__from__detection \
        --path__dir__img__input "${path__dir__img__input}" \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__dir__crop__img__output "${path__dir__crop__img__output}" \
        --path__dir__crop__lbl__output "${path__dir__crop__lbl__output}" \
        --is_ok__lbl_not_exist False \
        --num__pad__0 6 \
        --to_resize_box__wrt__pose True \
        --to_shift__coords__wrt__box True \
        --to_save__img False \
        --split_by '"id__track"' # '"id__track"' # if not None, please add a "/{}" before /images and /labels assuming there's an /images and /labels in path__dir__crop__img__output and path__dir__crop__lbl__output
    
    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done