PATH__DIR__IMAGE__SOURCE=/home/laptq/laptq-prj-44/outputs/unzip-downloaded-annotation-labelstudio
POSTFIX__DIR__IMG__SOURCE=""

PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-44/outputs/unzip-downloaded-annotation-labelstudio
POSTFIX__DIR__LABEL__SOURCE=""

PATH__DIR__DATASETS__OUTPUT=/home/laptq/laptq-prj-44/outputs/undo-unslashed--subpath-dir--dataset
POSTFIX__DIR__VERSION__TARGET=""

REPLACE__SLASH=-SLS-
PREFIX__DIR=P52-

[[ -d "$PATH__DIR__DATASETS__OUTPUT" ]] && rm -r "$PATH__DIR__DATASETS__OUTPUT"


declare -A MAP__SUBPATH_DIR_UNSLASHED__TO__=(
    ["P52-customer-SLS-train-batch-1"]=""
    ["P52-customer-SLS-train-batch-2"]=""
    ["P52-customer-SLS-train-batch-3"]=""
    ["P52-customer-SLS-train-batch-4"]=""
    ["P52-customer-SLS-val"]=""
    ["P52-private-SLS-test"]=""
    ["P52-private-SLS-train-batch-1"]=""
    ["P52-private-SLS-train-batch-2"]=""
    ["P52-private-SLS-train-batch-3"]=""
    ["P52-private-SLS-val"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath_dir__unslashed in "${!MAP__SUBPATH_DIR_UNSLASHED__TO__[@]}"; do
    subpath_dir=${subpath_dir__unslashed#${PREFIX__DIR}}
    subpath_dir=${subpath_dir//$REPLACE__SLASH/\/}

    pathd_img_input="${PATH__DIR__IMAGE__SOURCE}/${subpath_dir__unslashed}/images${POSTFIX__DIR__IMG__SOURCE}"
    pathd_img_output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    pathd_lbl_input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir__unslashed}/labels${POSTFIX__DIR__LABEL__SOURCE}"
    pathd_lbl_output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$pathd_img_output" ]] && rm -r "$pathd_img_output"
    [[ -d "$pathd_lbl_output" ]] && rm -r "$pathd_lbl_output"
    mkdir -p "$pathd_img_output"
    mkdir -p "$pathd_lbl_output"

    for namef_img in $( ls "${pathd_img_input}" ); do
        cp $( realpath "$pathd_img_input/$namef_img" ) "$pathd_img_output"/$namef_img
    done

    for namef_lbl in $( ls "${pathd_lbl_input}" ); do
        cp $( realpath "$pathd_lbl_input/$namef_lbl" ) "$pathd_lbl_output"/$namef_lbl
    done

    num__lbl__input=$(find "${pathd_lbl_input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__output=$(find "${pathd_lbl_output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__input -lt $num__lbl__output ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl__input input labels"
        echo "    [+] $num__lbl__output output labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__lbl__input} labels to ${num__lbl__output} labels: ${subpath_dir}"

    num__img__input=$(find "${pathd_img_input}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    num__img__output=$(find "${pathd_img_output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__img__input -lt $num__img__output ]; then
        echo -e "${TAG__FAILED} Number of images mismatched: ${subpath_dir}"
        echo "    [+] $num__img__input input images"
        echo "    [+] $num__img__output output images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__img__input} images to ${num__img__output} images: ${subpath_dir}"
done