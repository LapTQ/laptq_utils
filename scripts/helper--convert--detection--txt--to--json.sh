PATH__DIR__LABEL__INPUT=/mnt/ssd8tb/shared_workspace/prj44/dataset/Satudora_det_20250117
POSTFIX__DIR__LABEL__INPUT="--raw"

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-44/outputs/20250120--convert-detection-txt-to-json
POSTFIX__DIR__LABEL__OUTPUT="--raw"

MODE__BOX="xcycwhn"
# MODE__BOX="polygonn"

declare -A MAP__SUBPATH_DIR__TO__=(
    # ["PoC2--beppu_sue-batch-1"]=""
    # ["PoC2--beppu_sue-batch-3"]=""
    # ["PoC2--beppu_sue-batch-4"]=""
    # ["PoC2--beppu_sue-batch-5"]=""
    # ["PoC2--2個持ち_cut_fit-1products-batch-1"]=""
    # ["PoC2--2個持ち_cut_fit-1products-batch-2"]=""
    # ["PoC2--2個持ち_cut_fit-1products-batch-3"]=""
    # ["PoC2--2個持ち_cut_fit-2products-batch-1"]=""
    # ["PoC2--2個持ち_cut_fit-nothing"]=""
    # ["PoC2--2個持ち_cut_fit-notProducts"]=""
    # ["PoC2--bag20240906_0000-notProducts"]=""
    # ["PoC2--bag20240906_1022-notProducts-batch-1"]=""
    # ["PoC2--台置き_cut_fit-1products"]=""
    # ["PoC2--台置き_cut_fit-2products-batch-1"]=""
    # ["PoC2--台置き_cut_fit-notProducts"]=""
    # ["PoC2--beppu_sue-batch-2"]=""
    # ["PoC2--2個持ち_cut_fit-2products-batch-2"]=""
    # ["PoC2--台置き_cut_fit-2products-batch-2"]=""
    # ["PoC2--bag20240906_1022-notProducts-batch-2"]=""
    # ["PoC2--台置き_cut_fit-nothing"]=""

    ["01_regularPurchase"]=""
    ["02_regularPurchase"]=""
    ["03_regularPurchase"]=""
    ["04_regularPurchase"]=""
    ["05_cancelTea"]=""
    ["06_pullingCart"]=""
    ["07_holding2items"]=""
    ["08_regularPurchase"]=""
    ["09_holding2items"]=""
    ["10_hideBarcode"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__INPUT}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__convert__detection__txt__to__json \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__dir__lbl__output "${path__dir__lbl__output}" \
        --mode__box "${MODE__BOX}"


    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__output -ne $num__lbl__input ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched: ${subpath__dir}"
        echo "    [+] $num__lbl__input old labels"
        echo "    [+] $num__lbl__output new labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__input} old labels == ${num__lbl__output} target labels: ${subpath__dir}"

done