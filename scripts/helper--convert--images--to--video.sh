PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict2/20250428-152326--TSSTG_HO--2-kpt-channels
POSTFIX__DIR__IMAGE="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--STGCN--JSON"

PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video

declare -A MAP__NAME_VIDEO__TO__=(
    # ["shoplifting-25min.mp4"]=""
    ["satudora-1min.mp4"]=""
)

# [[ -d "${PATH__DIR__VIDEO__OUTPUT}" ]] && rm -r "${PATH__DIR__VIDEO__OUTPUT}"
mkdir -p "${PATH__DIR__VIDEO__OUTPUT}"

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${name__video}/vis${POSTFIX__DIR__IMAGE}"
    path__file__output="${PATH__DIR__VIDEO__OUTPUT}/${name__video}"

    ffmpeg \
        -framerate 5 \
        -i "${path__dir__img__input}/%09d.jpg" \
        -c:v libx264 \
        -y \
        -pix_fmt yuv420p \
        "$path__file__output"
    
    echo -e "${TAG__INFO} Done: ${name__video}"
done

# -pattern_type glob -i "${path__dir__img__input}/*.jpg"