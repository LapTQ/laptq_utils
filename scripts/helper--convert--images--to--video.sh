PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-prj-21/outputs/20250220--visualized
POSTFIX__DIR__IMAGE="--PRED--DATA--data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person--MODEL--yolov5s--832--scale-0.5--multiscale-True--TRAIN--train--PREDICT--imgsz-832--conf-0.1--JSON"

PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-prj-21/outputs/20250220--frames-to-video-2

declare -A MAP__NAME_VIDEO__TO__=(
    ["1_2024-11-26_081159_0.mp4"]=""
    ["1_2024-11-26_081159_1.mp4"]=""
    ["1_2024-11-26_081159_2.mp4"]=""
    ["1_2024-11-26_081159_3.mp4"]=""
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
        -i "${path__dir__img__input}/%06d.jpg" \
        -c:v libx264 \
        -pix_fmt yuv420p \
        "$path__file__output"
    
    echo -e "${TAG__INFO} Done: ${name__video}"
done