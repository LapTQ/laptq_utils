PATH__DIR__IMAGE=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/road-issues-detection
POSTFIX__DIR__IMAGE=""
# POSTFIX__DIR__IMAGE="--erase-ignored"

PATH__DIR__LABEL=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/helper--convert--detection--txt--to--json
POSTFIX__DIR__LABEL=""

NUM__MAX__IMG__TO__VISUALIZE=100
IS_OK__LBL_NOT_FOUND=False
PATH__DIR__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/helper--convert--detection--txt--to--json

PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/mnt/hdd10tb/Users/laptq/laptq-prj-46/src/configs/class_id_to_label.yaml
PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION=/home/laptq/laptq-fs26-shoplifting-detection/src/configs/action_names.yaml

declare -A MAP__SUBPATH_DIR__TO__=(
    ["APTO_v2/day1_330"]=""
    ["APTO_v2/night1_190"]=""
    ["APTO_v2/night3_44"]=""
    ["APTO_v2/night4_239"]=""
    ["dataset-ninja/ds1_simplex-test"]=""
    ["dataset-ninja/ds1_simplex-train"]=""
    ["dataset-ninja/ds2_complex-test"]=""
    ["dataset-ninja/ds2_complex-train"]=""
    ["pot_det_1240"]=""

    # # ["pothole_dataset_v8/only_rainy_frames/train"]=""

    ["pothole_dataset_v8/train"]=""
    ["pothole_dataset_v8/train_to_valid"]=""
    ["pothole_dataset_v8/valid"]=""
    ["Pothole_detection_yolo/train_original"]=""
    ["Pothole_Maeda/first_shot"]=""
    ["Pothole_Maeda/second_shot"]=""
    ["RDD2022_JAPAN/only_pothole/train"]=""

    ["Pothole_235/train"]=""
    ["Pothole_Maeda/first_shot_eval"]=""
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
        --to_draw__name_class True \
        --to_draw__pose False \
        --to_draw__connected_keypoints False \
        --to_draw__id_action False \
        --to_draw__name_action False \
        --to_draw__action_conf False \
        --to_draw__keypoints_displacement False \
        --to_draw__keypoints_speed False \
        --to_draw__event_info False \
        --fontScale 1 \
        --thickness 1 \
        --box_color_by id__class \
        --displacement_key "list__obj__kpts_displacement" \
        --speed_key "list__obj__kpts_speed_relative" \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --path__file__map__id_action__to__name_action $PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE \
        --seed 42 \
        --is_ok__lbl_not_exist $IS_OK__LBL_NOT_FOUND \
        --list__keypoints_same_color "[['left_eye', 'right_eye', 'left_ear', 'right_ear'],['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip'],['left_elbow', 'right_elbow', 'left_wrist', 'right_wrist'],['left_knee', 'right_knee', 'left_ankle', 'right_ankle']]" \
        --list__keypoints_edge "[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear'],['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip'],['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist'],['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]" \
        --list__edges_same_color "[[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear']], [['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip']], [['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist']], [['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]]" \
        --list__keypoints_to_include "['left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist']" \
        --list__keypoints_to_exclude "[]" \
        # --list__keypoints_to_include "['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']" \


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