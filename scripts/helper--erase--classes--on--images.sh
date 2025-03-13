PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-prj-21/data/fs_prj21/datasets/20250303--phase2--4cam-factory     # can be ignored if pad__max not set
POSTFIX__DIR__IMAGE__INPUT="--raw"

PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-21/outputs/20250310--labels
POSTFIX__DIR__LABEL__INPUT="--raw--JSON"

PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-21/outputs/20250310--labels
POSTFIX__DIR__IMAGE__OUTPUT="--erase-ignored"

declare -A MAP__SUBPATH_DIR__TO__=(
    ["Camera_47/Camera_47_1_2025-01-30_000000.3gp"]=""
    ["Camera_48/Camera_48_1_2025-01-30_000000.3gp"]=""
    ["Camera_49/Camera_49_1_2025-01-30_000000.3gp"]=""
    ["Camera_50/Camera_50_1_2025-01-30_000000.3gp"]=""
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
        --list__id_class 1,


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