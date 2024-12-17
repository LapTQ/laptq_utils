PATH__DIR__DATASETS__SOURCE__IMG=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__IMG=--20241121--checked--backup

PATH__DIR__DATASETS__SOURCE__LABEL=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__LABEL=--20241121--checked--backup

PATH__FILE__LIST_SUBPATH_TO_IMG=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241121--checklist--phase-2--annotation-ver2/list--subpath--to--img.txt

PATH__DIR__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241121--visual-check--downloaded--phase-2--annotation-ver2
POSTFIX__DIR__VERSION__TARGET=""
CLASSES="pothole\nmanhole\ndrainage\ndifficult"

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

