# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick--Le2i
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/ProtoGCN/prj54/v1__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick
PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i--10fps
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-speed/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/send_telemetry/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/generate_background_images
POSTFIX__DIR__IMAGE=""
# POSTFIX__DIR__IMAGE="--voting"
# POSTFIX__DIR__IMAGE="--PRED--DATA--bag-detection--MODEL--yolov8s--TRAIN--train--PREDICT--imgsz-640--conf-0.1--iou-0.45--JSON"

# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick--Le2i
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/ProtoGCN/prj54/v1__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick
PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i--10fps


declare -A MAP__NAME_VIDEO__TO__=(
    # ["shoplifting-25min.mp4"]=""
    # ["r9_25min_rotate.mp4"]=""
    # ["satudora-1min.mp4"]=""
    # ["r10_10min_rotate.mp4"]=""

    # ["fall_violence/test/fall/Fall_1.mp4"]=""
    # ["fall_violence/test/fall/Fall_2.mp4"]=""
    # ["fall_violence/test/violence/Violence_1.mp4"]=""
    # ["fall_violence/test/fall/Falling_and_Slow_Falling.mp4"]=""
    # ["fall_violence/test/violence/Fighting_1.mp4"]=""
    # ["fall_violence/test/violence/Fighting_2.mp4"]=""
    # ["fall_violence/test/violence/Fighting_3.mp4"]=""
    ["fall_violence/test/violence/Fighting_4.mp4"]=""
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

    # make parent output dir
    mkdir -p "$(dirname "$path__file__output")"

    ffmpeg \
        -framerate 30 \
        -pattern_type glob -i "${path__dir__img__input}/*.jpg" \
        -c:v libx264 \
        -y \
        -pix_fmt yuv420p \
        "$path__file__output" \
        # -i "${path__dir__img__input}/%09d.jpg" \
    
    echo -e "${TAG__INFO} Done: ${name__video}"
done

# # Glob options
# -pattern_type glob -i "${path__dir__img__input}/*.jpg"
# -i "${path__dir__img__input}/%09d.jpg"