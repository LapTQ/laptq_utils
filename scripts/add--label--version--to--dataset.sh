PATH__DIR__IMG__SOURCE=/home/laptq/laptq-prj-44/data/prj44/dataset
POSTFIX__DIR__IMG__SOURCE="--erase-IGNORE"

PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-44/data/prj44/dataset
POSTFIX__DIR__LABEL__SOURCE="--erase-IGNORE-productPerson"

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-44/data/prj44/dataset
POSTFIX__DIR__VERSION__TARGET="--erase-IGNORE-productPerson"


declare -A MAP__SUBPATH_DIR__TO__=(
    # ["customer/PoC2--beppu_sue-batch-1"]=""
    # ["customer/PoC2--beppu_sue-batch-3"]=""
    # ["customer/PoC2--beppu_sue-batch-4"]=""
    # ["customer/PoC2--beppu_sue-batch-5"]=""
    # ["customer/PoC2--2個持ち_cut_fit-1products-batch-1"]=""
    # ["customer/PoC2--2個持ち_cut_fit-1products-batch-2"]=""
    # ["customer/PoC2--2個持ち_cut_fit-1products-batch-3"]=""
    # ["customer/PoC2--2個持ち_cut_fit-2products-batch-1"]=""
    # ["customer/PoC2--2個持ち_cut_fit-nothing"]=""
    # ["customer/PoC2--2個持ち_cut_fit-notProducts"]=""
    # ["customer/PoC2--bag20240906_0000-notProducts"]=""
    # ["customer/PoC2--bag20240906_1022-notProducts-batch-1"]=""
    # ["customer/PoC2--台置き_cut_fit-1products"]=""
    # ["customer/PoC2--台置き_cut_fit-2products-batch-1"]=""
    # ["customer/PoC2--台置き_cut_fit-notProducts"]=""
    # ["customer/PoC2--beppu_sue-batch-2"]=""
    # ["customer/PoC2--2個持ち_cut_fit-2products-batch-2"]=""
    # ["customer/PoC2--台置き_cut_fit-2products-batch-2"]=""
    # ["customer/PoC2--bag20240906_1022-notProducts-batch-2"]=""
    # ["customer/PoC2--台置き_cut_fit-nothing"]=""
    ["private/Satudora_det_20250117/01_regularPurchase"]=""
    ["private/Satudora_det_20250117/02_regularPurchase"]=""
    ["private/Satudora_det_20250117/03_regularPurchase"]=""
    ["private/Satudora_det_20250117/04_regularPurchase"]=""
    ["private/Satudora_det_20250117/05_cancelTea"]=""
    ["private/Satudora_det_20250117/06_pullingCart"]=""
    ["private/Satudora_det_20250117/07_holding2items"]=""
    ["private/Satudora_det_20250117/08_regularPurchase"]=""
    ["private/Satudora_det_20250117/09_holding2items"]=""
    ["private/Satudora_det_20250117/10_hideBarcode"]=""
    # ["customer/Deployment-Store-20250221-batch-1"]=""
    # ["customer/Deployment-Store-20250221-batch-2"]=""
    # ["customer/Deployment-Store-20250221-batch-3"]=""
    # ["customer/Deployment-Store-20250221-batch-4"]=""
    # ["customer/Deployment-Store-20250221-batch-5"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# =========== Copy labels from extracted annotation to source dataset dir ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMG__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"
    path__dir__lbl__output="${PATH__DIR__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$path__dir__lbl__output" ]] && rm -r "$path__dir__lbl__output"
    mkdir -p "$path__dir__lbl__output"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl__input" ]]; then
            continue
        fi
        cp "$path__file__lbl__input" "$path__dir__lbl__output"
    done

    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__input -lt $num__lbl__output ]; then
        echo -e "${TAG__FAILED} Number of labels in the extracted annotation and number of labels copied mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl__input labels in the extracted annotation"
        echo "    [+] $num__lbl__output labels in the copied folder"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__lbl__input} labels to ${num__lbl__output} labels: ${subpath_dir}"
done


# =========== Create a soft link to images corresponding to the label version ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__lbl="${PATH__DIR__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__img__input="${PATH__DIR__IMG__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
    mkdir -p "$path__dir__img__output"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl="${path__dir__lbl}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl" ]]; then
            continue
        fi
        ln -s $( realpath "$path__dir__img__input/$name__file__img" ) "$path__dir__img__output"
        # cp $( realpath "$path__dir__img__input/$name__file__img" ) "$path__dir__img__output"
    done

    num__lbl=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    if [ $num__lbl -ne $num__img ]; then
        echo -e "${TAG__FAILED} Number of labels and images mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl labels"
        echo "    [+] $num__img images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Linked ${num__img} images corresponding to ${num__lbl} labels: ${subpath_dir}"
done