# PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/sample_frames_by_skipping/full
PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images
# PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/generate_background_images
POSTFIX__DIR__IMAGE=""
# POSTFIX__DIR__IMAGE="--erase-ignored"


# PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick
# PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick--Le2i
# PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/ProtoGCN/prj54/v1__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick
# PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i
PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-speed/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i
POSTFIX__DIR__LABEL=""
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--None--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--filterby-size--all-keypoints--RTMPose--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--RTMPose--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--filterby-size--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--JSON"
# POSTFIX__DIR__LABEL="--voting"
# POSTFIX__DIR__LABEL="--PRED--DATA--bag-detection--MODEL--yolov8s--TRAIN--train--PREDICT--imgsz-640--conf-0.1--iou-0.45--JSON"
# POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x--TRAIN--exp--PREDICT--imgsz-960--conf-0.25--iou-0.45--backpack-handbag--img-w-bag--JSON"
# POSTFIX__DIR__LABEL="--JSON"
# POSTFIX__DIR__LABEL="--erase-ignored--JSON"


NUM__MAX__IMG__TO__VISUALIZE=None
IS_OK__LBL_NOT_FOUND=False
# PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick
# PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/STGCN/prj54/STGCN--nturgbd--most-variant--left-strip-0.3--no-kickback-kicksth-sidekick--Le2i
# PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/ProtoGCN/prj54/v1__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick
# PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/predict_general/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i
PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--compute--keypoint-speed/ProtoGCN/prj54/v2__nturubg_mostvariant_leftstrip03_no_kickback_kicksth_sidekick__le2i
# PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials

PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/home/laptq/laptq-fs26-shoplifting-detection/src/configs/class_name.yaml
PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION=/home/laptq/laptq-fs26-shoplifting-detection/src/configs/action_names.yaml

declare -A MAP__SUBPATH_DIR__TO__=(
    
    # ["shoplifting-25min.mp4"]=""
    # ["satudora-1min.mp4"]=""
    # ["r10_10min_rotate.mp4"]=""
    # ["r9_25min_rotate.mp4"]=""
    # ["1568080723085_67014_fix.mkv"]=""
    # ["R10_2025_05_15_23_40_32_rotate.mp4"]=""

    # ["shoplifting-1min_anonymized.mp4"]=""
    # ["Shoplifting/Shoplifting__30_.mp4"]=""
    # ["Shoplifting/Shoplifting__68_.mp4"]=""

    # ["train"]=""
    # ["val"]=""
    # ["test"]=""
    # ["split-1"]=""
    # ["split-2"]=""

    # ["fall_violence/test/fall/Fall_1.mp4"]=""
    # ["fall_violence/test/fall/Fall_2.mp4"]=""
    ["fall_violence/test/violence/Violence_1.mp4"]=""

    # ["fall_violence/train/fall/Le2i/Coffee_room_02/Videos/video (68).avi"]=""
)
# source /home/laptq/laptq-fs26-shoplifting-detection/data/shoplifting-gen-video-paths.sh

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl="${PATH__DIR__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"

    path__dir__output="${PATH__DIR__OUTPUT}/${subpath__dir}/vis${POSTFIX__DIR__LABEL}"

    [[ -d "${path__dir__output}" ]] && rm -r "${path__dir__output}"
    mkdir -p "${path__dir__output}"

    python3 submodules/laptq_utils/main.py \
        helper__draw__imgdir \
        --path__dir__img "${path__dir__img}" \
        --path__dir__lbl "${path__dir__lbl}" \
        --path__dir__output "${path__dir__output}" \
        --to_concat__original_img False \
        --concat__axis 1 \
        --to_draw__id_frame False \
        --id_frame__from "filename" \
        --lambda__id_frame__from "lambda x: x.split('.')[0]" \
        --to_draw__id_track False \
        --to_draw__box_x1y1whn True \
        --to_draw__box_polygonn False \
        --to_draw__box_conf False \
        --to_draw__id_class False \
        --to_draw__name_class False \
        --to_draw__pose True \
        --to_draw__connected_keypoints True \
        --to_draw__id_action False \
        --to_draw__name_action True \
        --to_draw__action_conf False \
        --to_draw__keypoints_displacement False \
        --fontScale 2 \
        --thickness 2 \
        --box_color_by id__track \
        --displacement_key "list__obj__kpts_displacement" \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --path__file__map__id_action__to__name_action $PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE \
        --seed 42 \
        --is_ok__lbl_not_exist $IS_OK__LBL_NOT_FOUND \
        --list__keypoints_same_color "[['left_eye', 'right_eye', 'left_ear', 'right_ear'],['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip'],['left_elbow', 'right_elbow', 'left_wrist', 'right_wrist'],['left_knee', 'right_knee', 'left_ankle', 'right_ankle']]" \
        --list__keypoints_edge "[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear'],['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip'],['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist'],['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]" \
        --list__edges_same_color "[[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear']], [['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip']], [['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist']], [['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]]" \
        --list__keypoints_to_exclude "[]" \
        --list__keypoints_to_include "['left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']" \
        # --list__keypoints_to_include "['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']" \
        # --list__keypoints_to_include "['left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist']" \


    num__lbl=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img_vis=$(find "${path__dir__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $NUM__MAX__IMG__TO__VISUALIZE != "None" ] && [ $num__lbl > $NUM__MAX__IMG__TO__VISUALIZE ]; then
        num__lbl=$NUM__MAX__IMG__TO__VISUALIZE
    fi
    if [ $num__lbl != $num__img_vis ]; then
        echo -e "${TAG__FAILED} Number of visualized images and annotations mismatch: ${subpath__dir}"
        echo "    [+] $num__lbl labels"
        echo "    [+] $num__img_vis visualized images"
        
        # exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl} labels == ${num__img_vis} visualized images: ${subpath__dir}"
done