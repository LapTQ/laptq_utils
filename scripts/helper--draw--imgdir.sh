PATH__DIR__IMAGE=/home/laptq/laptq-fs26-shoplifting-detection/outputs/sample_frames_by_skipping/full
POSTFIX__DIR__IMAGE=""
# POSTFIX__DIR__IMAGE="--erase-ignored"


PATH__DIR__LABEL=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict2/20250428-152326--TSSTG_HO--2-kpt-channels
POSTFIX__DIR__LABEL="--PRED--DATA--None--MODEL--yolov8x-pose--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--STGCN--JSON"

NUM__MAX__IMG__TO__VISUALIZE=None
IS_OK__LBL_NOT_FOUND=False
PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict2/20250428-152326--TSSTG_HO--2-kpt-channels

PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/home/laptq/laptq-fs26-shoplifting-detection/src/configs/class_name.yaml
PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION=/home/laptq/laptq-fs26-shoplifting-detection/src/configs/action_names.yaml

declare -A MAP__SUBPATH_DIR__TO__=(
    # ["Normal/Normal__1_.mp4"]=""
    # ["Normal/Normal__2_.mp4"]=""
    # ["Normal/Normal__3_.mp4"]=""
    # ["Normal/Normal__4_.mp4"]=""
    # ["Normal/Normal__6_.mp4"]=""
    # ["Normal/Normal__7_.mp4"]=""
    # ["Normal/Normal__8_.mp4"]=""
    # ["Normal/Normal__9_.mp4"]=""
    # ["Normal/Normal__10_.mp4"]=""
    # ["Normal/Normal__11_.mp4"]=""
    # ["Normal/Normal__12_.mp4"]=""
    # ["Normal/Normal__13_.mp4"]=""
    # ["Normal/Normal__14_.mp4"]=""
    # ["Normal/Normal__15_.mp4"]=""
    # ["Normal/Normal__16_.mp4"]=""
    # ["Normal/Normal__17_.mp4"]=""
    # ["Normal/Normal__18_.mp4"]=""
    # ["Normal/Normal__19_.mp4"]=""
    # ["Normal/Normal__20_.mp4"]=""
    # ["Normal/Normal__22_.mp4"]=""
    # ["Normal/Normal__23_.mp4"]=""
    # ["Normal/Normal__24_.mp4"]=""
    # ["Normal/Normal__25_.mp4"]=""
    # ["Normal/Normal__26_.mp4"]=""
    # ["Normal/Normal__27_.mp4"]=""
    # ["Normal/Normal__28_.mp4"]=""
    # ["Normal/Normal__29_.mp4"]=""
    # ["Normal/Normal__30_.mp4"]=""
    # ["Normal/Normal__31_.mp4"]=""
    # ["Normal/Normal__32_.mp4"]=""
    # ["Normal/Normal__33_.mp4"]=""
    # ["Normal/Normal__34_.mp4"]=""
    # ["Normal/Normal__35_.mp4"]=""
    # ["Normal/Normal__36_.mp4"]=""
    # ["Normal/Normal__37_.mp4"]=""
    # ["Normal/Normal__38_.mp4"]=""
    # ["Normal/Normal__39_.mp4"]=""
    # ["Normal/Normal__40_.mp4"]=""
    # ["Normal/Normal__41_.mp4"]=""
    # ["Normal/Normal__42_.mp4"]=""
    # ["Normal/Normal__43_.mp4"]=""
    # ["Normal/Normal__44_.mp4"]=""
    # ["Normal/Normal__45_.mp4"]=""
    # ["Normal/Normal__46_.mp4"]=""
    # ["Normal/Normal__47_.mp4"]=""
    # ["Normal/Normal__49_.mp4"]=""
    # ["Normal/Normal__50_.mp4"]=""
    # ["Normal/Normal__51_.mp4"]=""
    # ["Normal/Normal__52_.mp4"]=""
    # ["Normal/Normal__53_.mp4"]=""
    # ["Normal/Normal__54_.mp4"]=""
    # ["Normal/Normal__55_.mp4"]=""
    # ["Normal/Normal__56_.mp4"]=""
    # ["Normal/Normal__57_.mp4"]=""
    # ["Normal/Normal__58_.mp4"]=""
    # ["Normal/Normal__59_.mp4"]=""
    # ["Normal/Normal__60_.mp4"]=""
    # ["Normal/Normal__61_.mp4"]=""
    # ["Normal/Normal__62_.mp4"]=""
    # ["Normal/Normal__63_.mp4"]=""
    # ["Normal/Normal__64_.mp4"]=""
    # ["Normal/Normal__65_.mp4"]=""
    # ["Normal/Normal__66_.mp4"]=""
    # ["Normal/Normal__67_.mp4"]=""
    # ["Normal/Normal__69_.mp4"]=""
    # ["Normal/Normal__70_.mp4"]=""
    # ["Normal/Normal__71_.mp4"]=""
    # ["Normal/Normal__72_.mp4"]=""
    # ["Normal/Normal__73_.mp4"]=""
    # ["Normal/Normal__75_.mp4"]=""
    # ["Normal/Normal__76_.mp4"]=""
    # ["Normal/Normal__77_.mp4"]=""
    # ["Normal/Normal__78_.mp4"]=""
    # ["Normal/Normal__79_.mp4"]=""
    # ["Normal/Normal__80_.mp4"]=""
    # ["Normal/Normal__81_.mp4"]=""
    # ["Normal/Normal__82_.mp4"]=""
    # ["Normal/Normal__83_.mp4"]=""
    # ["Normal/Normal__84_.mp4"]=""
    # ["Normal/Normal__85_.mp4"]=""
    # ["Normal/Normal__86_.mp4"]=""
    # ["Normal/Normal__87_.mp4"]=""
    # ["Normal/Normal__88_.mp4"]=""
    # ["Normal/Normal__89_.mp4"]=""
    # ["Normal/Normal__90_.mp4"]=""

    # ["Shoplifting/Shoplifting__1_.mp4"]=""
    # ["Shoplifting/Shoplifting__2_.mp4"]=""
    # ["Shoplifting/Shoplifting__3_.mp4"]=""
    # ["Shoplifting/Shoplifting__4_.mp4"]=""
    # ["Shoplifting/Shoplifting__5_.mp4"]=""
    # ["Shoplifting/Shoplifting__6_.mp4"]=""
    # ["Shoplifting/Shoplifting__7_.mp4"]=""
    # ["Shoplifting/Shoplifting__8_.mp4"]=""
    # ["Shoplifting/Shoplifting__10_.mp4"]=""
    # ["Shoplifting/Shoplifting__11_.mp4"]=""
    # ["Shoplifting/Shoplifting__12_.mp4"]=""
    # ["Shoplifting/Shoplifting__13_.mp4"]=""
    # ["Shoplifting/Shoplifting__14_.mp4"]=""
    # ["Shoplifting/Shoplifting__15_.mp4"]=""
    # ["Shoplifting/Shoplifting__18_.mp4"]=""
    # ["Shoplifting/Shoplifting__19_.mp4"]=""
    # ["Shoplifting/Shoplifting__20_.mp4"]=""
    # ["Shoplifting/Shoplifting__21_.mp4"]=""
    # ["Shoplifting/Shoplifting__22_.mp4"]=""
    # ["Shoplifting/Shoplifting__23_.mp4"]=""
    # ["Shoplifting/Shoplifting__25_.mp4"]=""
    # ["Shoplifting/Shoplifting__26_.mp4"]=""
    # ["Shoplifting/Shoplifting__27_.mp4"]=""
    # ["Shoplifting/Shoplifting__28_.mp4"]=""
    # ["Shoplifting/Shoplifting__29_.mp4"]=""
    # ["Shoplifting/Shoplifting__30_.mp4"]=""
    # ["Shoplifting/Shoplifting__31_.mp4"]=""
    # ["Shoplifting/Shoplifting__32_.mp4"]=""
    # ["Shoplifting/Shoplifting__34_.mp4"]=""
    # ["Shoplifting/Shoplifting__35_.mp4"]=""
    # ["Shoplifting/Shoplifting__36_.mp4"]=""
    # ["Shoplifting/Shoplifting__37_.mp4"]=""
    # ["Shoplifting/Shoplifting__38_.mp4"]=""
    # ["Shoplifting/Shoplifting__39_.mp4"]=""
    # ["Shoplifting/Shoplifting__40_.mp4"]=""
    # ["Shoplifting/Shoplifting__41_.mp4"]=""
    # ["Shoplifting/Shoplifting__42_.mp4"]=""
    # ["Shoplifting/Shoplifting__43_.mp4"]=""
    # ["Shoplifting/Shoplifting__45_.mp4"]=""
    # ["Shoplifting/Shoplifting__47_.mp4"]=""
    # ["Shoplifting/Shoplifting__48_.mp4"]=""
    # ["Shoplifting/Shoplifting__49_.mp4"]=""
    # ["Shoplifting/Shoplifting__51_.mp4"]=""
    # ["Shoplifting/Shoplifting__52_.mp4"]=""
    # ["Shoplifting/Shoplifting__53_.mp4"]=""
    # ["Shoplifting/Shoplifting__54_.mp4"]=""
    # ["Shoplifting/Shoplifting__55_.mp4"]=""
    # ["Shoplifting/Shoplifting__56_.mp4"]=""
    # ["Shoplifting/Shoplifting__57_.mp4"]=""
    # ["Shoplifting/Shoplifting__58_.mp4"]=""
    # ["Shoplifting/Shoplifting__59_.mp4"]=""
    # ["Shoplifting/Shoplifting__61_.mp4"]=""
    # ["Shoplifting/Shoplifting__62_.mp4"]=""
    # ["Shoplifting/Shoplifting__63_.mp4"]=""
    # ["Shoplifting/Shoplifting__64_.mp4"]=""
    # ["Shoplifting/Shoplifting__65_.mp4"]=""
    # ["Shoplifting/Shoplifting__66_.mp4"]=""
    # ["Shoplifting/Shoplifting__67_.mp4"]=""
    # ["Shoplifting/Shoplifting__68_.mp4"]=""
    # ["Shoplifting/Shoplifting__70_.mp4"]=""
    # ["Shoplifting/Shoplifting__71_.mp4"]=""
    # ["Shoplifting/Shoplifting__72_.mp4"]=""
    # ["Shoplifting/Shoplifting__73_.mp4"]=""
    # ["Shoplifting/Shoplifting__74_.mp4"]=""
    # ["Shoplifting/Shoplifting__75_.mp4"]=""
    # ["Shoplifting/Shoplifting__76_.mp4"]=""
    # ["Shoplifting/Shoplifting__77_.mp4"]=""
    # ["Shoplifting/Shoplifting__79_.mp4"]=""
    # ["Shoplifting/Shoplifting__80_.mp4"]=""
    # ["Shoplifting/Shoplifting__82_.mp4"]=""
    # ["Shoplifting/Shoplifting__83_.mp4"]=""
    # ["Shoplifting/Shoplifting__84_.mp4"]=""
    # ["Shoplifting/Shoplifting__85_.mp4"]=""
    # ["Shoplifting/Shoplifting__86_.mp4"]=""
    # ["Shoplifting/Shoplifting__87_.mp4"]=""
    # ["Shoplifting/Shoplifting__88_.mp4"]=""
    # ["Shoplifting/Shoplifting__89_.mp4"]=""
    # ["Shoplifting/Shoplifting__90_.mp4"]=""
    # ["Shoplifting/Shoplifting__92_.mp4"]=""
    # ["Shoplifting/Shoplifting__93_.mp4"]=""
    
    # ["Normal/Normal__5_.mp4"]=""
    # ["Normal/Normal__21_.mp4"]=""
    # ["Normal/Normal__48_.mp4"]=""
    # ["Normal/Normal__68_.mp4"]=""
    # ["Normal/Normal__74_.mp4"]=""
    # ["Shoplifting/Shoplifting__9_.mp4"]=""
    # ["Shoplifting/Shoplifting__16_.mp4"]=""
    # ["Shoplifting/Shoplifting__17_.mp4"]=""
    # ["Shoplifting/Shoplifting__24_.mp4"]=""
    # ["Shoplifting/Shoplifting__33_.mp4"]=""
    # ["Shoplifting/Shoplifting__44_.mp4"]=""
    # ["Shoplifting/Shoplifting__46_.mp4"]=""
    # ["Shoplifting/Shoplifting__50_.mp4"]=""
    # ["Shoplifting/Shoplifting__60_.mp4"]=""
    # ["Shoplifting/Shoplifting__69_.mp4"]=""
    # ["Shoplifting/Shoplifting__78_.mp4"]=""
    # ["Shoplifting/Shoplifting__81_.mp4"]=""
    # ["Shoplifting/Shoplifting__91_.mp4"]=""
    
    ["shoplifting-25min.mp4"]=""
)

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
        --to_draw__id_track True \
        --to_draw__box_x1y1whn True \
        --to_draw__box_polygonn False \
        --to_draw__box_conf True \
        --to_draw__id_class False \
        --to_draw__name_class True \
        --to_draw__pose True \
        --to_draw__connected_keypoints True \
        --to_draw__id_action False \
        --to_draw__name_action True \
        --to_draw__action_conf True \
        --fontScale 1 \
        --thickness 2 \
        --box_color_by id__class \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --path__file__map__id_action__to__name_action $PATH__FILE__MAP__ID_ACTION__TO__NAME_ACTION \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE \
        --seed 42 \
        --is_ok__lbl_not_exist $IS_OK__LBL_NOT_FOUND \
        --list__keypoints_same_color "[['left_eye', 'right_eye', 'left_ear', 'right_ear'],['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip'],['left_elbow', 'right_elbow', 'left_wrist', 'right_wrist'],['left_knee', 'right_knee', 'left_ankle', 'right_ankle']]" \
        --list__keypoints_edge "[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear'],['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip'],['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist'],['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]" \
        --list__edges_same_color "[[['nose', 'left_eye'],['nose', 'right_eye'],['left_eye', 'left_ear'],['right_eye', 'right_ear']], [['left_shoulder', 'right_shoulder'],['left_hip', 'right_hip'],['left_shoulder', 'left_hip'],['right_shoulder', 'right_hip']], [['left_shoulder', 'left_elbow'],['right_shoulder', 'right_elbow'],['left_elbow', 'left_wrist'],['right_elbow', 'right_wrist']], [['left_hip', 'left_knee'],['right_hip', 'right_knee'],['left_knee', 'left_ankle'],['right_knee', 'right_ankle']]]" \


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