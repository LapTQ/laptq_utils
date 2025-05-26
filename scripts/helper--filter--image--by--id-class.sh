# actually, I just remove the label files. So you should create symblink to image corresponding to the accepted labels
PATH__DIR__LABEL__INPUT=/home/laptq/laptq-nedo-fed/outputs/labels
POSTFIX__DIR__LABEL__INPUT=""

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-nedo-fed/outputs/labels
POSTFIX__DIR__LABEL__OUTPUT="--img-w-person"

LIST__ID_CLASS__TO_INCLUDE=0,
LIST__ID_CLASS__TO_EXCLUDE="[]"



declare -A MAP__SUBPATH_DIR__TO__=(
    ["B8-A4-4F-D2-F8-3A/2025_03_19"]=""
    ["B8-A4-4F-D2-F8-3A/2025_03_20"]=""
    ["B8-A4-4F-D2-FF-98/2025_03_19"]=""
    ["B8-A4-4F-D2-FF-98/2025_03_20"]=""
)


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"



for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__INPUT}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"
    
    python3 submodules/laptq_utils/main.py \
        helper__filter__image__by__id_class \
        --path__dir__lbl__input "$path__dir__lbl__input" \
        --path__dir__lbl__output "$path__dir__lbl__output" \
        --list__id_class__to_include $LIST__ID_CLASS__TO_INCLUDE \
        --list__id_class__to_exclude $LIST__ID_CLASS__TO_EXCLUDE
    
    if [[ ! -d "$path__dir__lbl__output" ]]; then
        echo -e "$TAG__FAILED The output $path__dir__lbl__output not existed"
        exit 1
    fi
done
