# RTMPose runs OK with:
# nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
# torch                    2.0.0+cu118
# torchaudio               2.0.1+cu118
# torchvision              0.15.1+cu118
# mmcv                     2.0.1
# mmdet                    3.3.0
# mmengine                 0.10.7
# mmpose                   1.3.2
# pip uninstall mmcv-full && mim uninstall mmpose mmdet mmcv mmengine && mim install mmengine && mim install --trusted-host download.openmmlab.com mmcv==2.0.1 && mim install --trusted-host download.openmmlab.com mmdet==3.3.0 && mim install --trusted-host download.openmmlab.com mmpose==1.3.2 && pip install numpy==1.26.4

PATHD_IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fs26
# PATHD_IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/prj54
POSTFIX_IMAGE=""

PATHD_LABEL_INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/fs26
# PATHD_LABEL_INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/prj54
POSTFIX_LABEL_INPUT="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"

PATH__FILE__MODEL=/home/laptq/laptq-fs26-shoplifting-detection/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.pth
PATH__FILE__CONFIG=/home/laptq/laptq-fs26-shoplifting-detection/submodules/laptq_utils/backlog/rtmpose-m_8xb256-420e_body8-256x192.py

PATHD_LABEL_OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/fs26
# PATHD_LABEL_OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir/prj54
POSTFIX_LABEL_OUTPUT="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--RTMPose--JSON"

DEVICE="cuda:5"

# declare -A MAP__SUBPATH_DIR__TO__=(
#     # ["shoplifting-25min.mp4"]=""
#     # ["r9_25min_rotate.mp4"]=""
#     # ["satudora-1min.mp4"]=""
#     # ["1568080723085_67014_fix.mkv"]=""
#     # ["r10_10min_rotate.mp4"]=""
#     # ["R10_2025_05_15_23_40_32_rotate.mp4"]=""

#     # ["fall_violence/test/fall/Fall_1.mp4"]=""
#     # ["fall_violence/test/fall/Fall_2.mp4"]=""
#     # ["fall_violence/test/violence/Violence_1.mp4"]=""
#     # ["fall_violence/test/fall/Falling_and_Slow_Falling.mp4"]=""
#     # ["fall_violence/test/violence/Fighting_1.mp4"]=""
#     # ["fall_violence/test/violence/Fighting_2.mp4"]=""
#     # ["fall_violence/test/violence/Fighting_3.mp4"]=""
#     # ["fall_violence/test/violence/Fighting_4.mp4"]=""

#     ["fall_violence/train/violence/punch_03-12-09-21-27-876"]=""
# )
# source /home/laptq/laptq-fs26-shoplifting-detection/data/mnit-video-paths.sh
source /home/laptq/laptq-fs26-shoplifting-detection/data/shoplifting-gen-video-paths.sh

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_VIDEO__TO__[@]}"; do
    path__dir__img__input="${PATHD_IMAGE}/${subpath__dir}/images${POSTFIX_IMAGE}"
    path__dir__lbl__input="${PATHD_LABEL_INPUT}/${subpath__dir}/labels${POSTFIX_LABEL_INPUT}"
    path__dir__lbl__output="${PATHD_LABEL_OUTPUT}/${subpath__dir}/labels${POSTFIX_LABEL_OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__extract__topdown__pose \
        --path__dir__img "${path__dir__img__input}" \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --path__file__config "${PATH__FILE__CONFIG}" \
        --device $DEVICE \
        --list__name_keypoints "['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']" \
    
    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done