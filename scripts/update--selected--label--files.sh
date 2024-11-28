PATH__DIR__DATASETS__SOURCE=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__VERSION__OLD=--20241121--checked--backup

PATH__DIR__LABEL_SOURCE__NEW=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/20241122--fix-visual-check--phase-2--annotation-ver2
POSTFIX__DIR__VERSION__NEW=""

POSTFIX__DIR__VERSION__TARGET=--20241121--phase-2--annotated-ver2--pot-man-drain-difficult--imgdedup--rm-small--rm-difficult-checked


declare -A MAP__SUBPATH_DIR__TO__=(
    ["APTO_v2/day1_330"]=""
    ["APTO_v2/night1_190"]=""
    ["APTO_v2/night3_44"]=""
    ["APTO_v2/night4_239"]=""
    ["Pothole_235/train"]=""
    # ["dataset-ninja/ds1_simplex-test"]=""
    # ["dataset-ninja/ds1_simplex-train"]=""
    # ["dataset-ninja/ds2_complex-test"]=""
    # ["dataset-ninja/ds2_complex-train"]=""
    ["pot_det_1240"]=""

    # ["pothole_dataset_v8/only_rainy_frames/train"]=""

    # ["pothole_dataset_v8/train"]=""
    # ["pothole_dataset_v8/train_to_valid"]=""
    # ["pothole_dataset_v8/valid"]=""
    # ["Pothole_detection_yolo/train_original"]=""
    ["Pothole_Maeda/first_shot"]=""
    ["Pothole_Maeda/first_shot_eval"]=""
    ["Pothole_Maeda/second_shot"]=""
    ["RDD2022_JAPAN/only_pothole/train"]=""
)


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__source="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/images${POSTFIX__DIR__VERSION__OLD}"
    path__dir__lbl__old="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/labels${POSTFIX__DIR__VERSION__OLD}"
    path__dir__lbl__new="${PATH__DIR__LABEL_SOURCE__NEW}/${subpath__dir}/labels${POSTFIX__DIR__VERSION__NEW}"

    path__dir__img__target="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__target="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    # clone as new copy
    [[ -d "${path__dir__img__target}" ]] && rm -r "${path__dir__img__target}"
    [[ -d "${path__dir__lbl__target}" ]] && rm -r "${path__dir__lbl__target}"
    mkdir -p "${path__dir__img__target}"
    mkdir -p "${path__dir__lbl__target}"

    for name__file__img in $( ls "${path__dir__img__source}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl__old="${path__dir__lbl__old}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl__old" ]]; then
            continue
        fi
        ln -s $( realpath "$path__dir__img__source/$name__file__img" ) "${path__dir__img__target}"
        cp "$path__file__lbl__old" "${path__dir__lbl__target}"
    done

    num__lbl__target=$(find "${path__dir__lbl__target}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img__target=$(find "${path__dir__img__target}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    if [ $num__lbl__target -ne $num__img__target ]; then
        echo -e "${TAG__FAILED} Number of labels and images mismatched (clone step): ${subpath__dir}"
        echo "    [+] $num__lbl__target labels"
        echo "    [+] $num__img__target images"
        
        exit 1
    fi

    # overwrite new label on the cloned folders
    for name__file__lbl in $( ls "${path__dir__lbl__new}" ); do
        path__file__lbl__target="${path__dir__lbl__target}/${name__file__lbl}"
        rm "$path__file__lbl__target"
    done
    num__lbl__old=$(find "${path__dir__lbl__old}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__new=$(find "${path__dir__lbl__new}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__target=$(find "${path__dir__lbl__target}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [[ $num__lbl__old -ne $(( num__lbl__new + num__lbl__target )) ]]; then
        echo -e "${TAG__FAILED} ${num__lbl__old} old labels != ${num__lbl__new} new labels + ${num__lbl__target} remaining labels: ${subpath__dir}"
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__old} old labels == ${num__lbl__new} new labels + ${num__lbl__target} remaining labels: ${subpath__dir}"
    cp "$path__dir__lbl__new"/* "${path__dir__lbl__target}"

    num__lbl__old=$(find "${path__dir__lbl__old}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__target=$(find "${path__dir__lbl__target}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__target -ne $num__lbl__old ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched (overwritting step): ${subpath__dir}"
        echo "    [+] $num__lbl__target target labels"
        echo "    [+] $num__lbl__old old labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__old} old labels == ${num__lbl__target} target labels: ${subpath__dir}"

done