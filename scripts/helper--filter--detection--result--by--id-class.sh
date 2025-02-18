PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-44/outputs/20250217--downloaded-annotations--extracted
POSTFIX__DIR__LABEL__INPUT="--raw--json"

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-44/outputs/20250217--downloaded-annotations--extracted
POSTFIX__DIR__LABEL__OUTPUT="--erase-IGNORE--json"

declare -A MAP__SUBPATH_DIR__TO__=(
    ["P44-20250211-batch-41"]=""
    ["P44-20250211-batch-42"]=""
    ["P44-20250211-batch-43"]=""
    ["P44-20250211-batch-44"]=""
    ["P44-20250211-batch-45"]=""
    ["P44-20250211-batch-46"]=""
    ["P44-20250211-batch-47"]=""
    ["P44-20250211-batch-48"]=""
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
        helper__filter__detection__result__by__id_class \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --list__id_class__to_include None \
        --list__id_class__to_exclude "[1]"


    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__output -ne $num__lbl__input ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched: ${subpath__dir}"
        echo "    [+] $num__lbl__input old labels"
        echo "    [+] $num__lbl__output new labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__input} old labels == ${num__lbl__output} target labels: ${subpath__dir}"

done