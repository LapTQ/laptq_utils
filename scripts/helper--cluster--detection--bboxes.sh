PATH__DIR__IMAGE__INPUT=/home/laptq/datasets/COCO--reformated
POSTFIX__DIR__IMAGE__INPUT=""

PATH__DIR__LABEL__INPUT=/home/laptq/datasets/COCO--reformated
POSTFIX__DIR__LABEL__INPUT=""

IMGSZ=416

PATH__DIR__OUTPUT=/home/laptq/datasets/COCO--reformated


declare -A MAP__SUBPATH_DIR__TO__=(
    ["train2017"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${subpath__dir}/images${POSTFIX__DIR__IMAGE__INPUT}"
    path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__INPUT}"
    path__dir__output="${PATH__DIR__OUTPUT}/${subpath__dir}"

    mkdir -p "${PATH__DIR__OUTPUT}"

    python3 main.py \
        helper__cluster__detection__bboxes \
        --path__dir__img__input "${path__dir__img__input}" \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --is_ok__lbl_not_exist True \
        --imgsz "$IMGSZ" \
        --n_clusters 9 \
        --num__max__box None \
        --seed 42 \
        --path__dir__output "$path__dir__output"

    echo -e "${TAG__INFO} Done: ${subpath__dir}"

    exit
done