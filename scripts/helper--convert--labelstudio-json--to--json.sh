PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-44/outputs/20241217--downloaded--annotation

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-44/outputs/20241214--true--label--json
POSTFIX__DIR__LABEL__OUTPUT=--raw

PREFIX__HOSTNAME='http:\/\/tank7:9000\/images\/'

PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/home/laptq/laptq-prj-44/src/configs/class_name.yaml

declare -A MAP__SUBPATH_DIR__TO__=(
    ["P44-1products-2個持ち_cut_fit-batch-1"]="" 
    ["P44-1products-2個持ち_cut_fit-batch-2"]="" 
    ["P44-1products-台置き_cut_fit"]="" 
    ["P44-2products-2個持ち_cut_fit"]="" 
    ["P44-2products-台置き_cut_fit"]="" 
    ["P44-nothing-2個持ち_cut_fit"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__file__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}.json"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__convert__labelstudio_json__to__json \
        --path__file__lbl__input "${path__file__lbl__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS


    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    echo -e "${TAG__INFO} ${num__lbl__output} target labels: ${subpath__dir}"

    # break

done