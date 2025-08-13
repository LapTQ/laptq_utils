PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images
POSTFIX__DIR__IMAGE=""

TO_USE__YOLOv5_COMPAT=False
PATH__FILE__MODEL=yolov8x-pose.pt
# PATH__FILE__MODEL=/home/laptq/laptq-fs26-shoplifting-detection/runs/bag-detection/yolov8s--640/train/weights/best.pt
ID__DATA=None
# ID__DATA=bag-detection
ID__MODEL=yolov8x-pose
# ID__MODEL=yolov8s
# ID__TRAIN=train
ID__TRAIN=exp

IMGSZ=640
# IMGSZ=960
THRESH__CONF__MIN=0.1
# THRESH__CONF__MIN=0.01
THRESH__IOU=0.45
ID__PREDICT=imgsz-$IMGSZ--conf-$THRESH__CONF__MIN--iou-$THRESH__IOU

DEVICE="cuda:1"

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--extract--ultralytics--imgdir
POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--${ID__DATA}--MODEL--${ID__MODEL}--TRAIN--${ID__TRAIN}--PREDICT--${ID__PREDICT}--all-keypoints--JSON"
# POSTFIX__DIR__LABEL__OUTPUT="--PRED--DATA--${ID__DATA}--MODEL--${ID__MODEL}--TRAIN--${ID__TRAIN}--PREDICT--${ID__PREDICT}--JSON"

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
    path__dir__img__input="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__extract__ultralytics__imgdir \
        --path__dir__img "${path__dir__img__input}" \
        --path__dir__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device $DEVICE \
        --imgsz $IMGSZ \
        --thresh__conf__min $THRESH__CONF__MIN \
        --thresh__iou $THRESH__IOU \
        --to_use__yolov5_compat $TO_USE__YOLOv5_COMPAT \
        --task track \
        --persist True \
        --list__name_keypoints "['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']" \
        --thresh__conf__keypoints__min 0.0 \
    
    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done