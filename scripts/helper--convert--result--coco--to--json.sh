PATH__DIR__LABEL__INPUT=/home/pocuser2/datasets/coco/annotations
POSTFIX__DIR__LABEL__INPUT=""

PATH__DIR__LABEL__OUTPUT=/home/pocuser2/datasets/coco/restructured
POSTFIX__DIR__LABEL__OUTPUT=""


declare -A MAP__SUBPATH_DIR__TO__=(
    # ["train2017"]=""
    ["val2017"]=""
    # ["test"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__file__lbl__input="${PATH__DIR__LABEL__INPUT}/instances_${subpath__dir}.json"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__convert__result__coco__to__json \
        --path__file__lbl__input "${path__file__lbl__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --offset__id_class -1 \
        --path__file__map__id_class__to__name_class "${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/map__id_class__to__name_class.yaml"

    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done