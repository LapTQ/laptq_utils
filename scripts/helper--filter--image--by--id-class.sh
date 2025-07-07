# actually, I just remove the label files. So you should create symblink to image corresponding to the accepted labels
PATH__DIR__LABEL__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
POSTFIX__DIR__LABEL__INPUT="--PRED--DATA--None--MODEL--yolov8x--TRAIN--exp--PREDICT--imgsz-960--conf-0.25--iou-0.45--backpack-handbag--JSON"

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--None--MODEL--yolov8x--TRAIN--exp--PREDICT--imgsz-960--conf-0.25--iou-0.45--backpack-handbag--img-w-bag--JSON"

LIST__ID_CLASS__TO_INCLUDE=24,26
LIST__ID_CLASS__TO_EXCLUDE="[]"



declare -A MAP__SUBPATH_DIR__TO__=(
    ["R10_2025_05_15_23_40_32_rotate.mp4"]=""
)


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"



for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__INPUT}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"
    
    python3 submodules/laptq_utils/main.py \
        helper__filter__image__by__id_class \
        --path__dir__lbl__input "$path__dir__lbl__input" \
        --path__dir__lbl__output "$path__dir__lbl__output" \
        --list__id_class__to_include $LIST__ID_CLASS__TO_INCLUDE \
        --list__id_class__to_exclude $LIST__ID_CLASS__TO_EXCLUDE
    
    if [[ ! -d "$path__dir__lbl__output" ]]; then
        echo -e "$TAG__FAILED The output $path__dir__lbl__output not existed"
        exit 1
    fi
done
