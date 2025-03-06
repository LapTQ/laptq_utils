# the last substring split by REPLACE__SLASH is the filename
PATH__DIR__IMAGE__SOURCE=/home/laptq/laptq-prj-21/outputs/20250228--phase-2--merged
POSTFIX__DIR__IMG__SOURCE="--erase-ignored"

PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-21/outputs/20250228--phase-2--merged
POSTFIX__DIR__LABEL__SOURCE="--erase-ignored"

PATH__DIR__DATASETS__OUTPUT=/home/laptq/laptq-prj-21/outputs/20250228--phase-2--merged--unslashed
POSTFIX__DIR__VERSION__TARGET="--erase-ignored"

REPLACE__SLASH=--

# [[ -d "$PATH__DIR__DATASETS__OUTPUT" ]] && rm -r "$PATH__DIR__DATASETS__OUTPUT"


declare -A MAP__SUBPATH_DIR__TO__=(
    ["P21"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"


    for name__file__img__input in $( ls "${path__dir__img__input}" ); do
        name__file__lbl__input=${name__file__img__input%.*}.txt

        path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl__input}"
        if [[ ! -f "$path__file__lbl__input" ]]; then
            continue
        fi

        # prefix__fname is the part of the file name before the last slash, postfix is the part after the last slash
        postfix__fname=${name__file__img__input##*$REPLACE__SLASH}
        prefix__fname=${name__file__img__input%$REPLACE__SLASH*}
        prefix__fname__unslashed=${prefix__fname//$REPLACE__SLASH/\/}
        
        subpath_dir_out="${subpath_dir}/${prefix__fname__unslashed}"
        path__dir__img__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir_out}/images${POSTFIX__DIR__VERSION__TARGET}"
        path__dir__lbl__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir_out}/labels${POSTFIX__DIR__VERSION__TARGET}"

        mkdir -p "$path__dir__img__output"
        mkdir -p "$path__dir__lbl__output"

        path__file__img__output="${path__dir__img__output}/${postfix__fname}"
        path__file__lbl__output="${path__dir__lbl__output}/${postfix__fname%.*}.txt"

        cp "$path__file__lbl__input" "$path__file__lbl__output"
        cp "$path__dir__img__input/$name__file__img__input" "$path__file__img__output"
    done

    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -type f | wc -l)
    num__lbl__output=$(find "${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/" -mindepth 1 -type f | grep "/labels${POSTFIX__DIR__VERSION__TARGET}/" | wc -l)
    if [ $num__lbl__input -lt $num__lbl__output ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl__input input labels"
        echo "    [+] $num__lbl__output output labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__lbl__input} labels to ${num__lbl__output} labels"

    num__img__input=$(find "${path__dir__img__input}/" -mindepth 1 \( -type f -o -type l \) | wc -l)
    num__img__output=$(find "${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/" -mindepth 1 -type f | grep "/images${POSTFIX__DIR__VERSION__TARGET}/" | wc -l)
    if [ $num__img__input -lt $num__img__output ]; then
        echo -e "${TAG__FAILED} Number of images mismatched: ${subpath_dir}"
        echo "    [+] $num__img__input input images"
        echo "    [+] $num__img__output output images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__img__input} images to ${num__img__output} images"
done