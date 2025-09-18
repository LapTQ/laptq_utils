# PATH__DIR__DATASETS__SOURCE=/mnt/hdd10tb/Datasets/road-issues-detection
PATH__DIR__DATASETS__SOURCE=/home/laptq/laptq-prj-46/outputs/drafts/d2
POSTFIX__DIR__IMG__SOURCE=""

# PATH__DIR__LABEL__SOURCE=/mnt/hdd10tb/Datasets/road-issues-detection
PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-46/outputs/drafts/d2
POSTFIX__DIR__LABEL__SOURCE=""

PATH__DIR__DATASETS__OUTPUT=/home/laptq/laptq-prj-46/outputs/copy-hard--dataset
POSTFIX__DIR__VERSION__TARGET=""


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
    # ["pot_det_1240"]=""

    # ["pothole_dataset_v8/only_rainy_frames/train"]=""

    # ["pothole_dataset_v8/train"]=""
    # ["pothole_dataset_v8/train_to_valid"]=""
    # ["pothole_dataset_v8/valid"]=""
    # ["Pothole_detection_yolo/train_original"]=""
    # ["Pothole_Maeda/first_shot"]=""
    # ["Pothole_Maeda/first_shot_eval"]=""
    # ["Pothole_Maeda/second_shot"]=""
    # ["RDD2022_JAPAN/only_pothole/train"]=""

    # ["20241121--syn--selected/Pothole_Maeda/first_shot"]=""
    # ["20241121--syn--selected/Pothole_Maeda/second_shot"]=""

    ["fs-10"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"
    path__dir__lbl__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"
    
    [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
    [[ -d "$path__dir__lbl__output" ]] && rm -r "$path__dir__lbl__output"
    mkdir -p "$path__dir__img__output"
    mkdir -p "$path__dir__lbl__output"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl__input" ]]; then
            continue
        fi
        cp "$path__file__lbl__input" "$path__dir__lbl__output"
        cp $( realpath "$path__dir__img__input/$name__file__img" ) "$path__dir__img__output"
    done

    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__input -lt $num__lbl__output ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl__input input labels"
        echo "    [+] $num__lbl__output output labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__lbl__input} labels to ${num__lbl__output} labels"

    num__img__input=$(find "${path__dir__img__input}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    num__img__output=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__img__input -lt $num__img__output ]; then
        echo -e "${TAG__FAILED} Number of images mismatched: ${subpath_dir}"
        echo "    [+] $num__img__input input images"
        echo "    [+] $num__img__output output images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__img__input} images to ${num__img__output} images"
done