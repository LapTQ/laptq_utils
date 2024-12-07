PATH__DIR__LABEL__INPUT=/home/laptq/Downloads/outputs--1
POSTFIX__DIR__LABEL__INPUT=""

PATH__DIR__LABEL__OUTPUT=/home/laptq/Downloads/outputs--2
POSTFIX__DIR__LABEL__OUTPUT=""

declare -A MAP__SUBPATH_DIR__TO__=(
    ["set1"]=""
    ["set2"]=""
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

    for name__file__lbl in $(ls "${path__dir__lbl__input}"); do
        path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl}"
        path__file__lbl__output="${path__dir__lbl__output}/${name__file__lbl}"

        python3 main.py \
            helper__filter__detection__result__by__id_class \
            --path__file__lbl__input "${path__file__lbl__input}" \
            --path__file__lbl__output "${path__file__lbl__output}" \
            --list__id_class__to_include 0,56 \
            --list__id_class__to_exclude "[]"

    done

done