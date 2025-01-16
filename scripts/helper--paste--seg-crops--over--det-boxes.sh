PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-prj-21/data/20241225--gen-data--batches
POSTFIX__DIR__IMAGE__INPUT=""
PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-21/data/20241225--gen-data--batches--to-json
POSTFIX__DIR__LABEL__INPUT=""

PATH__DIR__CROP__IMAGE__INPUT=/home/laptq/laptq-prj-21/outputs/test-sample--crops
POSTFIX__DIR__CROP__IMAGE__INPUT=""
PATH__DIR__CROP__MASK__INPUT=/home/laptq/laptq-prj-21/outputs/test-sample--crops
POSTFIX__DIR__CROP__MASK__INPUT=""
PATH__DIR__CROP__LABEL__INPUT=/home/laptq/laptq-prj-21/outputs/test-sample--crops
POSTFIX__DIR__CROP__LABEL__INPUT=""


PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/outputs/20250109--paste--seg-crops--over--det-boxes
POSTFIX__DIR__OUTPUT=""

declare -A MAP__SUBPATH_DIR_IMAGE_TO__=(
    ["gen_only_syn_25Dec-batch-1"]=""
    ["gen_only_syn_25Dec-batch-2"]=""
)

declare -A MAP__SUBPATH_DIR_CROP_TO__=(
    # ["val2017"]=""
    ["test-sample"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir__image in "${!MAP__SUBPATH_DIR_IMAGE_TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${subpath__dir__image}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir__image}/labels${POSTFIX__DIR__LABEL}"

    for subpath__dir__crop in "${!MAP__SUBPATH_DIR_CROP_TO__[@]}"; do
        path__dir__crop__img__input="${PATH__DIR__CROP__IMAGE__INPUT}/${subpath__dir__crop}/crops${POSTFIX__DIR__CROP__IMAGE__INPUT}"
        path__dir__crop__mask__input="${PATH__DIR__CROP__MASK__INPUT}/${subpath__dir__crop}/masks${POSTFIX__DIR__CROP__MASK__INPUT}"
        path__dir__crop__lbl__input="${PATH__DIR__CROP__LABEL__INPUT}/${subpath__dir__crop}/labels${POSTFIX__DIR__CROP__LABEL__INPUT}"

        path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath__dir__image}/${subpath__dir__crop}/images${POSTFIX__DIR__OUTPUT}"
        path__dir__lbl__output="${PATH__DIR__OUTPUT}/${subpath__dir__image}/${subpath__dir__crop}/labels${POSTFIX__DIR__OUTPUT}"

        [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
        [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
        mkdir -p "${path__dir__img__output}"
        mkdir -p "${path__dir__lbl__output}"

        python3 submodules/laptq_utils/main.py \
            helper__paste__seg_crops__over__det_boxes \
            --path__dir__img__input "${path__dir__img__input}" \
            --path__dir__lbl__input "${path__dir__lbl__input}" \
            --path__dir__crop__img__input "${path__dir__crop__img__input}" \
            --path__dir__crop__mask__input "${path__dir__crop__mask__input}" \
            --path__dir__crop__lbl__input "${path__dir__crop__lbl__input}" \
            --path__dir__img__output "${path__dir__img__output}" \
            --path__dir__lbl__output "${path__dir__lbl__output}" \
            --is_ok__lbl_not_exist False \
            --prob 0.5 \
            --seed None \
            --method PASTE__SIMPLE \
            --thresh__leftiou__min 0.2 \
            --thresh__leftiou__max 0.4 \
            --num__steps 7
            # --method PASTE__CV2_SEAMLESS_CLONE \
            # --flags cv2.MONOCHROME_TRANSFER
            # --flags cv2.NORMAL_CLONE \
            # --flags cv2.MIXED_CLONE \
        
        echo -e "${TAG__INFO} Done: ${subpath__dir__image} x ${subpath__dir__crop}"
    done
done