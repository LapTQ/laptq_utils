PATH__DIR__VIDEO=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper-convert-video-to-images

PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials

PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials

PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/home/laptq/laptq-prj-44/src/configs/class_name.yaml
PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION=/home/laptq/laptq-fs26-shoplifting-detection/src/configs/action_names.yaml


[[ -d "${PATH__DIR__OUTPUT}" ]] && rm -r "${PATH__DIR__OUTPUT}"
mkdir -p "${PATH__DIR__OUTPUT}"

declare -A MAP__NAME_VIDEO__TO__=(
    # ["1_2024-11-26_081159_0_5min.mp4"]=""
    # ["1_2024-11-26_081159_1_5min.mp4"]=""
    # ["1_2024-11-26_081159_2_5min.mp4"]=""
    # ["1_2024-11-26_081159_3_5min.mp4"]=""

    ["1_2024-11-26_081159_0.mp4"]=""
    ["1_2024-11-26_081159_1.mp4"]=""
    ["1_2024-11-26_081159_2.mp4"]=""
    ["1_2024-11-26_081159_3.mp4"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__file__video__input="${PATH__DIR__VIDEO}/${name__video}"
    path__dir__lbl__input="${PATH__DIR__LABEL}/${name__video}/labels"
    path__file__output="${PATH__DIR__OUTPUT}/${name__video}"

    python3 submodules/laptq_utils/main.py \
        helper__draw__video \
        --path__file__video__input "${path__file__video__input}" \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__file__output "${path__file__output}" \
        --num__pad__0 6 \
        --fourcc "mp4v" \
        --to_draw__id_frame True \
        --to_draw__id_track True \
        --to_draw__box_x1y1whn True \
        --to_draw__box_polygonn False \
        --to_draw__box_conf True \
        --to_draw__id_class False \
        --to_draw__name_class False \
        --to_draw__pose True \
        --to_draw__connected_keypoints True \
        --to_draw__id_action False \
        --to_draw__name_action True \
        --fontScale 1 \
        --thickness 2 \
        --box_color_by id__class \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --path__file__map__id_action__to__name_action $PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION \
        --list__keypoints_same_color "[['left_eye', 'right_eye', 'left_ear', 'right_ear'],['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip'],['left_elbow', 'right_elbow', 'left_wrist', 'right_wrist'],['left_knee', 'right_knee', 'left_ankle', 'right_ankle']]" \
        --list__keypoints_edge "[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear'],['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip'],['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist'],['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]" \
        --list__edges_same_color "[[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear']], [['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip']], [['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist']], [['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]]" \

    echo -e "${TAG__INFO} Done: ${name__video}"
done