# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/ProtoGCN/prj54/v3__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i__punch0312--15fps--left-window-19--min-votes-threshold-9
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-speed/ProtoGCN/prj54/v3__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i__punch0312--15fps--left-window-19--min-votes-threshold-9
PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/filter_action_by_keypoint_speed/ProtoGCN/prj54/v3__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i__punch0312--15fps--left-window-19--min-votes-threshold-9--filter-speed-1.2-2.0--filter-punch
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/send_telemetry/ProtoGCN/prj54/v3__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i__punch0312--15fps--left-window-19--min-votes-threshold-9
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/generate_background_images
POSTFIX__DIR__IMAGE=""
# POSTFIX__DIR__IMAGE="--voting"
# POSTFIX__DIR__IMAGE="--PRED--DATA--bag-detection--MODEL--yolov8s--TRAIN--train--PREDICT--imgsz-640--conf-0.1--iou-0.45--JSON"

PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/ProtoGCN/prj54/v3__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i__punch0312--15fps--left-window-19--min-votes-threshold-9--filter-speed-1.2-2.0--filter-punch


declare -A MAP__NAME_VIDEO__TO__=(
    # ["shoplifting-25min.mp4"]=""
    # ["r9_25min_rotate.mp4"]=""
    # ["satudora-1min.mp4"]=""
    # ["r10_10min_rotate.mp4"]=""

    ["fall_violence/test/fall/Falling_and_Slow_Falling.mp4"]=""
    # ["fall_violence/test/violence/Fighting_1.mp4"]=""
    # ["fall_violence/test/violence/Fighting_2.mp4"]=""
    # ["fall_violence/test/violence/Fighting_3.mp4"]=""
    # ["fall_violence/test/violence/Fighting_4.mp4"]=""
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