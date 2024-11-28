PATH__DIR__DATASETS__SOURCE__LABEL=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__LABEL=--20241121--phase-2--annotated-ver2--pot-man-drain-difficult--imgdedup--rm-small--rm-difficult

PATH__DIR__OUTPUT=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__VERSION__TARGET=--20241125--phase-2--annotated-ver2--checked--changed-class-id--pot-man


declare -A MAP__SUBPATH_DIR__TO__=(
    # ["APTO_v2/day1_330"]=""
    # ["APTO_v2/night1_190"]=""
    # ["APTO_v2/night3_44"]=""
    # ["APTO_v2/night4_239"]=""
    # ["Pothole_235/train"]=""
    # ["dataset-ninja/ds1_simplex-test"]=""
    # ["dataset-ninja/ds1_simplex-train"]=""
    # ["dataset-ninja/ds2_complex-test"]=""
    # ["dataset-ninja/ds2_complex-train"]=""
    ["pot_det_1240"]=""
    # ["pothole_dataset_v8/only_rainy_frames/train"]=""
    ["pothole_dataset_v8/train"]=""
    # ["pothole_dataset_v8/train_to_valid"]=""
    # ["pothole_dataset_v8/valid"]=""
    ["Pothole_detection_yolo/train_original"]=""
    # ["Pothole_Maeda/first_shot"]=""
    # ["Pothole_Maeda/first_shot_eval"]=""
    # ["Pothole_Maeda/second_shot"]=""
    ["RDD2022_JAPAN/only_pothole/train"]=""
)

declare -A MAP__ID_OLD__TO__ID_NEW=(
    ["2"]="1"
)

ORDER=( "2" )


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__lbl__input="${PATH__DIR__DATASETS__SOURCE__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__lbl__output="${PATH__DIR__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    for name__file__lbl in $( ls $path__dir__lbl__input ); do
        path__file__lbl__output="${path__dir__lbl__output}/${name__file__lbl}"
        cp "${path__dir__lbl__input}/${name__file__lbl}" "${path__dir__lbl__output}/"

        for id__old in "${ORDER[@]}"; do
            id__new=${MAP__ID_OLD__TO__ID_NEW[$id__old]}
            sed -i "s/^$id__old /$id__new /" "$path__file__lbl__output"
        done
    done

    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__output -ne $num__lbl__input ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched: ${subpath__dir}"
        echo "    [+] $num__lbl__input old labels"
        echo "    [+] $num__lbl__output new labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__input} old labels == ${num__lbl__output} target labels: ${subpath__dir}"
done