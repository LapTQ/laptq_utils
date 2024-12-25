PATH__DIR__IMAGE__SOURCE=/home/laptq/laptq-prj-44/outputs/20241130--copy-hard--dataset
POSTFIX__DIR__IMG__SOURCE=""

PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-44/outputs/20241130--copy-hard--dataset
POSTFIX__DIR__LABEL__SOURCE=""

PATH__DIR__DATASETS__OUTPUT=/home/laptq/laptq-prj-44/outputs/20241130--copy-hard--dataset--unslashed
POSTFIX__DIR__VERSION__TARGET=""

REPLACE__SLASH=-SLS-
PREFIX__DIR=P44-

[[ -d "$PATH__DIR__DATASETS__OUTPUT" ]] && rm -r "$PATH__DIR__DATASETS__OUTPUT"


declare -A MAP__SUBPATH_DIR__TO__=(
    ["beppu_sue_data/batch-1"]=""
    ["beppu_sue_data/batch-2"]=""
    ["beppu_sue_data/batch-3"]=""
    ["beppu_sue_data/batch-4"]=""
    ["beppu_sue_data/batch-5"]=""
    ["beppu_sue_data/batch-6"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    subpath_dir__unslashed=${subpath_dir//\//$REPLACE__SLASH}
    path__dir__img__input="${PATH__DIR__IMAGE__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__DATASETS__OUTPUT}/${PREFIX__DIR}${subpath_dir__unslashed}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"
    path__dir__lbl__output="${PATH__DIR__DATASETS__OUTPUT}/${PREFIX__DIR}${subpath_dir__unslashed}/labels${POSTFIX__DIR__VERSION__TARGET}"

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
        cp "$path__dir__img__input/$name__file__img" "$path__dir__img__output"
    done

    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
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