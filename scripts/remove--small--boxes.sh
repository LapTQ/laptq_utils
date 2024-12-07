PATH__DIR__DATASETS__SOURCE__IMG=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__IMG=--20241121--phase-2--annotated-ver2--pot-man-drain-difficult--imgdedup--rm-small--rm-difficult-checked
PATH__DIR__DATASETS__SOURCE__LABEL=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__LABEL=--20241121--phase-2--annotated-ver2--pot-man-drain-difficult--imgdedup--rm-small--rm-difficult-checked

PATH__DIR__DATASETS__LABEL__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/20241121--downloaded--phase-2--annotation-ver2--pot-man-drain-difficult--remove-small
POSTFIX__DIR__LABEL__OUTPUT=""


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
    path__dir__img="${PATH__DIR__DATASETS__SOURCE__IMG}/${subpath__dir}/images${POSTFIX__DIR__IMG}"
    path__dir__lbl="${PATH__DIR__DATASETS__SOURCE__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__output="${PATH__DIR__DATASETS__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    if [[ -d "$path__dir__output" ]]; then
        echo -e "${TAG__FAILED} Output folder already existed: ${path__dir__output}"
        exit 1
    fi

    python3 submodules/laptq_utils/main.py \
        helper__remove__small__boxes \
        --path__dir__img "${path__dir__img}" \
        --path__dir__lbl "${path__dir__lbl}" \
        --path__dir__output "${path__dir__output}" \
        --thresh__area__min 64
    
    num__lbl__in=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__out=$(find "${path__dir__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__in != $num__lbl__out ]; then
        echo -e "${TAG__FAILED} Number of labels mismatch: ${subpath__dir}"
        echo "    [+] $num__lbl__in input labels"
        echo "    [+] $num__lbl__out output labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__in} input labels == ${num__lbl__out} output: ${subpath__dir}"
done
