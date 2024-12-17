PATH__DIR__IMAGE=/home/laptq/laptq-prj-44/outputs/20241213--prepare--annotate--part1
POSTFIX__DIR__IMAGE=""

PATH__DIR__LABEL=/home/laptq/laptq-prj-44/outputs/20241214--true--label--json
POSTFIX__DIR__LABEL=--raw

NUM__MAX__IMG__TO__VISUALIZE=None
IS_OK__LBL_NOT_FOUND=True
PATH__DIR__OUTPUT=/home/laptq/laptq-prj-44/outputs/20241214--visualize
PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS=/home/laptq/laptq-prj-44/src/configs/class_name.yaml

[[ -d "$PATH__DIR__OUTPUT" ]] && rm -r "$PATH__DIR__OUTPUT"

declare -A MAP__SUBPATH_DIR__TO__=(
    # ["beppu_sue_data/batch-1"]=""
    # ["beppu_sue_data/batch-2"]=""
    # ["beppu_sue_data/batch-3"]=""
    # ["beppu_sue_data/batch-4"]=""
    # ["beppu_sue_data/batch-5"]=""
    # ["beppu_sue_data/batch-6"]=""
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
    path__dir__img="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl="${PATH__DIR__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__output="${PATH__DIR__OUTPUT}/${subpath__dir}"

    [[ -d "${path__dir__output}" ]] && rm -r "${path__dir__output}"
    mkdir -p "${path__dir__output}"

    python3 submodules/laptq_utils/main.py \
        helper__draw__detection__imgdir \
        --path__dir__img "${path__dir__img}" \
        --path__dir__lbl "${path__dir__lbl}" \
        --path__dir__output "${path__dir__output}" \
        --to_concat__original_img True \
        --to_draw__box_conf True \
        --to_draw__id_class False \
        --to_draw__name_class True \
        --fontScale 1 \
        --thickness 1 \
        --box_color_by id__class \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE \
        --seed None \
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
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl} labels == ${num__img_vis} visualized images: ${subpath__dir}"
done