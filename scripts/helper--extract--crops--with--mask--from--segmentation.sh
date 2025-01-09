PATH__DIR__IMAGE=/home/laptq/laptq-prj-21/data/COCO--reformated--splitted
POSTFIX__DIR__IMAGE=""

PATH__DIR__LABEL=/home/laptq/laptq-prj-21/data/COCO--reformated--splitted
POSTFIX__DIR__LABEL=""

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/outputs/test-sample--crops
POSTFIX__DIR__OUTPUT=""

declare -A MAP__SUBPATH_DIR__TO__=(
    # ["val2017"]=""
    ["test-sample"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl__input="${PATH__DIR__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__crop__output="${PATH__DIR__OUTPUT}/${subpath__dir}/crops${POSTFIX__DIR__OUTPUT}"
    path__dir__mask__output="${PATH__DIR__OUTPUT}/${subpath__dir}/masks${POSTFIX__DIR__OUTPUT}"
    path__dir__lbl__output="${PATH__DIR__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__OUTPUT}"

    [[ -d "${path__dir__crop__output}" ]] && rm -r "${path__dir__crop__output}"
    [[ -d "${path__dir__mask__output}" ]] && rm -r "${path__dir__mask__output}"
    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__crop__output}"
    mkdir -p "${path__dir__mask__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__extract__crops__with__mask__from__segmentation \
        --path__dir__img__input "${path__dir__img__input}" \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__dir__crop__output "${path__dir__crop__output}" \
        --path__dir__mask__output "${path__dir__mask__output}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --is_ok__lbl_not_exist False \
        --num__pad__0 6
    
    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done