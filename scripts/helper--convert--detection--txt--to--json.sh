PATH__DIR__LABEL__INPUT=/home/laptq/laptq-prj-21/data/20250102--testset--4cam-factory
POSTFIX__DIR__LABEL__INPUT="--raw"

PATH__DIR__LABEL__OUTPUT=/home/laptq/laptq-prj-21/outputs/20241231--get--subset--dataset--yolo--test-set--annotated--to-json
POSTFIX__DIR__LABEL__OUTPUT="--raw"

MODE__BOX="xcycwhn"
# MODE__BOX="polygonn"

declare -A MAP__SUBPATH_DIR__TO__=(
    ["1_2024-11-26_081159_0.mp4"]=""
    ["1_2024-11-26_081159_1.mp4"]=""
    ["1_2024-11-26_081159_2.mp4"]=""
    ["1_2024-11-26_081159_3.mp4"]=""
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


    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__output -ne $num__lbl__input ]; then
        echo -e "${TAG__FAILED} Number of labels mismatched: ${subpath__dir}"
        echo "    [+] $num__lbl__input old labels"
        echo "    [+] $num__lbl__output new labels"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl__input} old labels == ${num__lbl__output} target labels: ${subpath__dir}"

done