# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict/20250514-000000--STGCN--seed--rm-wrong-normal--LR1e-06--scale-11--plus-roboflow-poselift
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict/20250514-000000--STGCN--seed--rm-wrong-normal--LR1e-06--scale-11--plus-roboflow-poselift--all-keypoints/torch
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict/STGCN--seed--rm-wrong-normal--LR1e-06--scale-11--plus-roboflow-poselift--onlyhand/torch
PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict/STGCN--nturgbd--fps5--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick/torch
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/2DCNN/predict/classification
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/ProtoGCN/predict/ProtoGCN_v24/torch
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/annotated-frames-with-action-labels
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/20250505-000000--TSSTG_HO--2-kpt-channels
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/TSGAD4/predict
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/TSGAD-2class--TRAIN-mnit-roboflow-poselift--lr0.001--no-mse/predict
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/TSGAD-2class--TRAIN-satudoraR-poselift--VAL-poselift/predict/torch
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/generate_background_images
POSTFIX__DIR__IMAGE=""
# POSTFIX__DIR__IMAGE="--voting"
# POSTFIX__DIR__IMAGE="--PRED--DATA--bag-detection--MODEL--yolov8s--TRAIN--train--PREDICT--imgsz-640--conf-0.1--iou-0.45--JSON"

# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN/20250514-000000--STGCN--seed--rm-wrong-normal--LR1e-06--scale-11--plus-roboflow-poselift
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN/20250514-000000--STGCN--seed--rm-wrong-normal--LR1e-06--scale-11--plus-roboflow-poselift--all-keypoints/torch
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN/STGCN--seed--rm-wrong-normal--LR1e-06--scale-11--plus-roboflow-poselift--onlyhand/torch
PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN/STGCN--nturgbd--fps5--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick/torch
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/2DCNN
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/ProtoGCN/ProtoGCN_v24/torch
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/major_vote_action
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/helper--extract--ultralytics--imgdir
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/TSGAD4
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/TSGAD-2class--TRAIN-mnit-roboflow-poselift--lr0.001--no-mse
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/TSGAD-2class--TRAIN-satudoraR-poselift--VAL-poselift/torch
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/annotated-frames-with-action-labels
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/bag-detection
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/NTU-vis


declare -A MAP__NAME_VIDEO__TO__=(
    # ["shoplifting-25min.mp4"]=""
    # ["r9_25min_rotate.mp4"]=""
    # ["satudora-1min.mp4"]=""
    # ["r10_10min_rotate.mp4"]=""

    ["fall_violence/test/fall/Fall_1.mp4"]=""
    ["fall_violence/test/fall/Fall_2.mp4"]=""
    ["fall_violence/test/violence/Violence_1.mp4"]=""
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
        -framerate 15 \
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