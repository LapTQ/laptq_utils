# RTMPose runs OK with:
# nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
# torch                    2.0.0+cu118
# torchaudio               2.0.1+cu118
# torchvision              0.15.1+cu118
# mmcv                     2.0.1
# mmdet                    3.3.0
# mmengine                 0.10.7
# mmpose                   1.3.2
# pip uninstall mmcv-full && mim uninstall mmpose mmdet mmcv mmengine && mim install mmengine && mim install mmcv==2.0.1 && mim install mmdet==3.3.0 && mim install mmpose==1.3.2

PATHD_IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images
POSTFIX_IMAGE=""

PATHD_LABEL_INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
POSTFIX_LABEL_INPUT="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"

PATH__FILE__MODEL=/home/laptq/laptq-fs26-shoplifting-detection/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.pth
PATH__FILE__CONFIG=/home/laptq/laptq-fs26-shoplifting-detection/submodules/laptq_utils/backlog/rtmpose-m_8xb256-420e_body8-256x192.py

PATHD_LABEL_OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
POSTFIX_LABEL_OUTPUT="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--RTMPose--JSON"

DEVICE="cuda:0"

declare -A MAP__SUBPATH_DIR__TO__=(
    # ["shoplifting-25min.mp4"]=""
    # ["r9_25min_rotate.mp4"]=""
    # ["satudora-1min.mp4"]=""
    # ["1568080723085_67014_fix.mkv"]=""
    # ["r10_10min_rotate.mp4"]=""
    # ["R10_2025_05_15_23_40_32_rotate.mp4"]=""

    # ["fall_violence/test/fall/Fall_1.mp4"]=""
    # ["fall_violence/test/fall/Fall_2.mp4"]=""
    # ["fall_violence/test/violence/Violence_1.mp4"]=""

    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (1).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (2).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (3).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (4).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (5).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (6).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (7).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (8).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (9).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (10).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (11).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (12).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (13).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (14).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (15).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (16).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (17).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (18).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (19).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (20).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (21).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (22).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (23).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (24).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (25).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (26).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (27).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (28).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (29).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (30).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (31).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (32).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (33).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (34).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (35).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (36).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (37).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (38).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (39).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (40).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (41).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (42).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (43).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (44).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (45).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (46).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (47).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_01/Videos/video (48).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (49).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (50).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (51).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (52).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (53).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (54).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (55).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (56).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (57).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (58).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (59).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (60).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (61).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (62).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (63).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (64).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (65).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (66).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (67).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (68).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (69).avi"]=""
    ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (70).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (1).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (2).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (3).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (4).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (5).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (6).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (7).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (8).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (9).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (10).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (11).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (12).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (13).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (14).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (15).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (16).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (17).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (18).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (19).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (20).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (21).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (22).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (23).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (24).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (25).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (26).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (27).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (28).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (29).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_01/Videos/video (30).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (31).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (32).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (33).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (34).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (35).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (36).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (37).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (38).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (39).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (40).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (41).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (42).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (43).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (44).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (45).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (46).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (47).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (48).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (49).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (50).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (51).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (52).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (53).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (54).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (55).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (56).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (57).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (58).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (59).avi"]=""
    ["fall_violence/train/fall/Le2i/Home_02/Videos/video (60).avi"]=""
)
# source /home/laptq/laptq-fs26-shoplifting-detection/data/mnit-video-paths.sh
# source /home/laptq/laptq-fs26-shoplifting-detection/data/shoplifting-gen-video-paths.sh

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
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