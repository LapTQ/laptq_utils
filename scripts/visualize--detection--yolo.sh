PATH__DIR__DATASETS__SOURCE__IMG=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__IMG=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0
PATH__DIR__DATASETS__SOURCE__LABEL=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__LABEL=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0
PATH__FILE__CLASS_ID__TO__LABEL=src/configs/class_id_to_label.yaml
PATH__DIR__VISUALIZATION__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241122--visualize
NUM__MAX__IMG__TO__VISUALIZE=None


declare -A MAP__SUBPATH_DIR__TO__NAME_ZIP=(
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
)


[[ -d "$PATH__DIR__VISUALIZATION__OUTPUT" ]] && rm -r "$PATH__DIR__VISUALIZATION__OUTPUT"


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
    path__dir__img="${PATH__DIR__DATASETS__SOURCE__IMG}/${subpath_dir}/images${POSTFIX__DIR__IMG}"
    path__dir__label="${PATH__DIR__DATASETS__SOURCE__LABEL}/${subpath_dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__img_vis="${PATH__DIR__VISUALIZATION__OUTPUT}/${subpath_dir}"

    python3 submodules/laptq_utils/main.py \
        helper__visualize__detection \
        --path__dir__img "${path__dir__img}" \
        --path__dir__label "${path__dir__label}" \
        --path__dir__output "${path__dir__img_vis}" \
        --draw_track_id False \
        --draw_conf False \
        --draw_class_id True \
        --fontScale 1 \
        --thickness 2 \
        --draw_class_name True \
        --box_color_by class_id \
        --path__file__class_id_to_label $PATH__FILE__CLASS_ID__TO__LABEL \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE
    
    num__lbl=$(find "${path__dir__label}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img_vis=$(find "${path__dir__img_vis}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $NUM__MAX__IMG__TO__VISUALIZE != "None" ] && [ $num__lbl > $NUM__MAX__IMG__TO__VISUALIZE ]; then
        num__lbl=$NUM__MAX__IMG__TO__VISUALIZE
    fi
    if [ $num__lbl != $num__img_vis ]; then
        echo -e "${TAG__FAILED} Number of visualized images and annotations mismatch: ${subpath_dir}"
        echo "    [+] $num__lbl labels"
        echo "    [+] $num__img_vis visualized images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl} labels == ${num__img_vis} visualized images: ${subpath_dir}"
done