# actually, I just remove the label files. So you should create symblink to image corresponding to the accepted labels
PATH__DIR__DATASETS__SOURCE__LABEL=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/20241121--downloaded--phase-2--annotation-ver2--pot-man-drain-difficult--remove-small
POSTFIX__DIR__LABEL=""
PATH__DIR__DATASETS__LABEL__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/20241121--downloaded--phase-2--annotation-ver2--pot-man-drain-difficult--remove-small--remove-difficult


[[ -d "$PATH__DIR__DATASETS__LABEL__OUTPUT" ]] && rm -r "$PATH__DIR__DATASETS__LABEL__OUTPUT"


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


declare -A MAP__SUBPATH__DIR=(
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


for subpath__dir in "${!MAP__SUBPATH__DIR[@]}"; do
    path__dir__label="${PATH__DIR__DATASETS__SOURCE__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__output="${PATH__DIR__DATASETS__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    python3 submodules/laptq_utils/main.py \
        helper__remove__images__containing__classes \
        --path__dir__label "$path__dir__label" \
        --path__dir__output "$path__dir__output" \
        --list__id_class 3,
    
    if [[ ! -d "$path__dir__output" ]]; then
        echo -e "$TAG__FAILED The output $path__dir__output not existed"
        exit 1
    fi
done