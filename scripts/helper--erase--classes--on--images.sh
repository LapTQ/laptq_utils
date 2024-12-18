# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-prj-44/outputs/20241213--prepare--annotate--part1--undo-split
PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-prj-44/outputs/20241213--prepare--annotate--part2--undo-split     # can be ignored if pad__max not set
POSTFIX__DIR__IMAGE__INPUT=""

# PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-44/outputs/20241217--downloaded--annotation--json--undo-split
PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-44/outputs/20241213--prepare--annotate--part2--undo-split--merge-old-new--json
POSTFIX__DIR__LABEL__INPUT=""

# PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-44/outputs/20241213--prepare--annotate--part1--undo-split--erase-ignored
PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-44/outputs/20241213--prepare--annotate--part2--undo-split--erase-ignored
POSTFIX__DIR__IMAGE__OUTPUT=""

declare -A MAP__SUBPATH_DIR__TO__=(
    ["beppu_sue"]=""
    # ["P44-nothing-2個持ち_cut_fit"]=""
    # ["P44-notProducts-2個持ち_cut_fit"]=""
    # ["P44-1products-台置き_cut_fit"]=""
    # ["P44-nothing-台置き_cut_fit"]=""
    # ["P44-notProducts-台置き_cut_fit"]=""
    # ["P44-notProducts-bag20240906_1022"]=""
    # ["P44-2products-2個持ち_cut_fit"]=""
    # ["P44-1products-2個持ち_cut_fit"]=""
    # ["P44-2products-台置き_cut_fit"]=""
    # ["P44-notProducts-bag20240906_0000"]=""
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