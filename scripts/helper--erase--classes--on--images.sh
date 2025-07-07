PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-prj-44/outputs/images-with-central-human-and-product-to-annotate/20250211--finetune--ver3--merged--subset-10k--splitted
POSTFIX__DIR__IMAGE__INPUT="--raw"

PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-44/outputs/20250217--downloaded-annotations--extracted
POSTFIX__DIR__LABEL__INPUT="--raw--json"

PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-44/outputs/images-with-central-human-and-product-to-annotate/20250211--finetune--ver3--merged--subset-10k--splitted
POSTFIX__DIR__IMAGE__OUTPUT="--erase-IGNORE"

declare -A MAP__SUBPATH_DIR__TO__=(
    ["P44-20250211-batch-24"]=""
    ["P44-20250211-batch-25"]=""
    ["P44-20250211-batch-26"]=""
    ["P44-20250211-batch-27"]=""
    ["P44-20250211-batch-28"]=""
    ["P44-20250211-batch-29"]=""
    ["P44-20250211-batch-30"]=""
    ["P44-20250211-batch-31"]=""
    ["P44-20250211-batch-32"]=""
    ["P44-20250211-batch-33"]=""
    ["P44-20250211-batch-34"]=""
    ["P44-20250211-batch-35"]=""
    ["P44-20250211-batch-36"]=""
    ["P44-20250211-batch-37"]=""
    ["P44-20250211-batch-38"]=""
    ["P44-20250211-batch-39"]=""
    ["P44-20250211-batch-40"]=""
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
    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${subpath__dir}/images${POSTFIX__DIR__IMAGE__INPUT}"
    path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__INPUT}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${subpath__dir}/images${POSTFIX__DIR__IMAGE__OUTPUT}"

    [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
    mkdir -p "${path__dir__img__output}"

    python3 submodules/laptq_utils/main.py \
        helper__erase__classes__on__images \
        --path__dir__img__input "${path__dir__img__input}" \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__dir__img__output "${path__dir__img__output}" \
        --list__id_class 1, \
        --color "(0, 0, 0)" \


    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img__output=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__img__output -ne $num__lbl__input ]; then
        echo -e "${TAG__FAILED} Number of labels and images mismatched: ${subpath__dir}"
        echo "    [+] $num__lbl__input input labels"
        echo "    [+] $num__img__output output images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__input} input labels == ${num__img__output} output images: ${subpath__dir}"

done