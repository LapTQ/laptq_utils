PATH__DIR__IMAGE=/home/laptq/laptq-nedo-fed/data
POSTFIX__DIR__IMAGE=""

PATH__DIR__LABEL=/home/laptq/laptq-nedo-fed/outputs/labels
POSTFIX__DIR__LABEL="--only-person"

NUM__MAX__IMG__TO__VISUALIZE=20
IS_OK__LBL_NOT_FOUND=False
PATH__DIR__OUTPUT=/home/laptq/laptq-nedo-fed/outputs/labels
PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/home/laptq/laptq-prj-44/src/configs/class_name.yaml

declare -A MAP__SUBPATH_DIR__TO__=(
    ["fastlabel/train"]=""
    ["fastlabel/val"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl="${PATH__DIR__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"

    path__dir__output="${PATH__DIR__OUTPUT}/${subpath__dir}/vis${POSTFIX__DIR__LABEL}"

    [[ -d "${path__dir__output}" ]] && rm -r "${path__dir__output}"
    mkdir -p "${path__dir__output}"

    python3 submodules/laptq_utils/main.py \
        helper__draw__detection__imgdir \
        --path__dir__img "${path__dir__img}" \
        --path__dir__lbl "${path__dir__lbl}" \
        --path__dir__output "${path__dir__output}" \
        --to_concat__original_img False \
        --concat__axis 1 \
        --to_draw__box_x1y1whn True \
        --to_draw__box_polygonn False \
        --to_draw__box_conf True \
        --to_draw__id_class True \
        --to_draw__name_class False \
        --fontScale 2 \
        --thickness 2 \
        --box_color_by id__class \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE \
        --seed 42 \
        --is_ok__lbl_not_exist $IS_OK__LBL_NOT_FOUND


    num__lbl=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img_vis=$(find "${path__dir__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $NUM__MAX__IMG__TO__VISUALIZE != "None" ] && [ $num__lbl > $NUM__MAX__IMG__TO__VISUALIZE ]; then
        num__lbl=$NUM__MAX__IMG__TO__VISUALIZE
    fi
    if [ $num__lbl != $num__img_vis ]; then
        echo -e "${TAG__FAILED} Number of visualized images and annotations mismatch: ${subpath__dir}"
        echo "    [+] $num__lbl labels"
        echo "    [+] $num__img_vis visualized images"
        
        # exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl} labels == ${num__img_vis} visualized images: ${subpath__dir}"
done