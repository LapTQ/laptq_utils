PATH__DIR__IMAGE__INPUT=/media/laptq/data/workspace/laptq_mct/data/datasets/PETS09
POSTFIX__DIR__IMAGE__INPUT=""

PATH__DIR__LABEL__INPUT=/media/laptq/data/workspace/laptq_mct/data/datasets/PETS09/annotations

PATH__DIR__LABEL__OUTPUT=/media/laptq/data/workspace/laptq_mct/data/datasets/PETS09/annotations-json
POSTFIX__DIR__LABEL__OUTPUT=""


declare -A MAP__SUBPATH_DIR__TO__=(
    ["View_001.mp4"]=""
    ["View_005.mp4"]=""
    ["View_006.mp4"]=""
    ["View_007.mp4"]=""
    ["View_008.mp4"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${subpath__dir}/images${POSTFIX__DIR__IMAGE__INPUT}"
    path__file__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}.txt"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 main.py \
        helper__convert__pets2009_label__to__json \
        --path__dir__img__input "${path__dir__img__input}" \
        --path__file__lbl__input "${path__file__lbl__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}"

    echo -e "${TAG__INFO} Done: ${subpath__dir}"

done