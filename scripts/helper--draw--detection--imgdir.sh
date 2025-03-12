PATH__DIR__IMAGE=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__IMAGE=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0

PATH__DIR__LABEL=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241208--true-labels--json
POSTFIX__DIR__LABEL=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0--rescaled

NUM__MAX__IMG__TO__VISUALIZE=10
IS_OK__LBL_NOT_FOUND=True
PATH__DIR__OUTPUT=//mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241208--visualize
PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/home/laptq/laptq-prj-44/src/configs/class_name.yaml

declare -A MAP__SUBPATH_DIR__TO__=(
    ["APTO_v2/day1_330"]=""
    ["APTO_v2/night1_190"]=""
    ["APTO_v2/night3_44"]=""
    ["APTO_v2/night4_239"]=""
    ["Pothole_235/train"]=""
    ["dataset-ninja/ds1_simplex-test"]=""
    ["dataset-ninja/ds1_simplex-train"]=""
    ["dataset-ninja/ds2_complex-test"]=""
    ["dataset-ninja/ds2_complex-train"]=""
    ["pot_det_1240"]=""

    # ["pothole_dataset_v8/only_rainy_frames/train"]=""

    ["pothole_dataset_v8/train"]=""
    ["pothole_dataset_v8/train_to_valid"]=""
    ["pothole_dataset_v8/valid"]=""
    ["Pothole_detection_yolo/train_original"]=""
    ["Pothole_Maeda/first_shot"]=""
    ["Pothole_Maeda/first_shot_eval"]=""
    ["Pothole_Maeda/second_shot"]=""
    ["RDD2022_JAPAN/only_pothole/train"]=""

    ["20241121--syn--selected/Pothole_Maeda/first_shot"]=""
    ["20241121--syn--selected/Pothole_Maeda/second_shot"]=""
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
        helper__draw__detection__imgdir \
        --path__dir__img "${path__dir__img}" \
        --path__dir__lbl "${path__dir__lbl}" \
        --path__dir__output "${path__dir__output}" \
        --to_concat__original_img False \
        --concat__axis 1 \
        --to_draw__box_x1y1whn True \
        --to_draw__box_polygonn False \
        --to_draw__box_conf True \
        --to_draw__id_class False \
        --to_draw__name_class True \
        --fontScale 2 \
        --thickness 2 \
        --box_color_by id__class \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE \
        --seed 42 \
        --is_ok__lbl_not_exist $IS_OK__LBL_NOT_FOUND


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