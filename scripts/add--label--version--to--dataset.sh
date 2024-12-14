PATH__DIR__IMG__SOURCE=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__IMG__SOURCE=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0

PATH__DIR__LABEL__SOURCE=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241208--true-labels--txt
POSTFIX__DIR__LABEL__SOURCE=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0--rescaled

PATH__DIR__OUTPUT=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__VERSION__TARGET=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0--rescaled


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


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# =========== Copy labels from extracted annotation to source dataset dir ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMG__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"
    path__dir__lbl__output="${PATH__DIR__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$path__dir__lbl__output" ]] && rm -r "$path__dir__lbl__output"
    mkdir -p "$path__dir__lbl__output"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl__input" ]]; then
            continue
        fi
        cp "$path__file__lbl__input" "$path__dir__lbl__output"
    done

    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__input -lt $num__lbl__output ]; then
        echo -e "${TAG__FAILED} Number of labels in the extracted annotation and number of labels copied mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl__input labels in the extracted annotation"
        echo "    [+] $num__lbl__output labels in the copied folder"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__lbl__input} labels to ${num__lbl__output} labels"
done


# =========== Create a soft link to images corresponding to the label version ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__lbl="${PATH__DIR__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__img__input="${PATH__DIR__IMG__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
    mkdir -p "$path__dir__img__output"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl="${path__dir__lbl}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl" ]]; then
            continue
        fi
        ln -s $( realpath "$path__dir__img__input/$name__file__img" ) "$path__dir__img__output"
    done

    num__lbl=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    if [ $num__lbl -ne $num__img ]; then
        echo -e "${TAG__FAILED} Number of labels and images mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl labels"
        echo "    [+] $num__img images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Linked ${num__img} images corresponding to ${num__lbl} labels: ${subpath_dir}"
done