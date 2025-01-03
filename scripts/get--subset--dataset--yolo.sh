PATH__DIR__DATASETS__SOURCE__IMG=/home/laptq/laptq-prj-21/runs/data--synthetic--satudora-center-box/yolo11s--832--scale-0.5--multiscale-True/predict--train--imgsz-832--conf-0.1/predict
POSTFIX__DIR__IMG=""

PATH__DIR__DATASETS__SOURCE__LABEL=/home/laptq/laptq-prj-21/runs/data--synthetic--satudora-center-box/yolo11s--832--scale-0.5--multiscale-True/predict--train--imgsz-832--conf-0.1/predict
POSTFIX__DIR__LABEL="--txt"

PATH__FILE__LIST_SUBPATH_TO_IMG=/home/laptq/laptq-prj-21/outputs/list--subpath--to--img.txt

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/outputs/20241231--get--subset--dataset--yolo--test-set
POSTFIX__DIR__VERSION__TARGET=""
CLASSES="person"

[[ -d "$PATH__DIR__OUTPUT" ]] && rm -r "$PATH__DIR__OUTPUT"


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


while IFS= read -r subpath__file__img; do
    subpath__file__img="${subpath__file__img%$'\r'}"
    subpath__dir="${subpath__file__img%/*}"

    name__file__img="${subpath__file__img##*/}"
    name__file__lbl=${name__file__img%.*}.txt

    path__file__img="${PATH__DIR__DATASETS__SOURCE__IMG}/${subpath__dir}/images${POSTFIX__DIR__IMG}/${name__file__img}"
    path__file__lbl="${PATH__DIR__DATASETS__SOURCE__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}/${name__file__lbl}"

    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath__dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__output="${PATH__DIR__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    [[ ! -d "${path__dir__img__output}" ]] && mkdir -p "${path__dir__img__output}"
    [[ ! -d "${path__dir__lbl__output}" ]] && mkdir -p "${path__dir__lbl__output}"

    echo -e "${CLASSES}" > "${PATH__DIR__OUTPUT}/${subpath__dir}/classes.txt"

    cp "$( realpath ${path__file__img} )" "${path__dir__img__output}"
    cp "$( realpath ${path__file__lbl} )" "${path__dir__lbl__output}"

done < "${PATH__FILE__LIST_SUBPATH_TO_IMG}"

