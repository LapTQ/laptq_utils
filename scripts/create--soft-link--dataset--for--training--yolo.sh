PATH__DIR__DATASETS__SOURCE=/home/laptq/laptq-prj-44/data/prj44/dataset

declare -A MAP__SUBPATH_DIR__TO__POSTFIX_DIR_VERSION=(
    ["customer/Deployment-Store-20250221-batch-1"]="--erase-IGNORE--productPerson"
    ["customer/Deployment-Store-20250221-batch-2"]="--erase-IGNORE--productPerson"
    ["customer/Deployment-Store-20250221-batch-3"]="--erase-IGNORE--productPerson"
    ["customer/Deployment-Store-20250221-batch-4"]="--erase-IGNORE--productPerson"
    ["customer/Deployment-Store-20250221-batch-5"]="--erase-IGNORE--productPerson"
    ["customer/PoC2--beppu_sue-batch-1"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--beppu_sue-batch-3"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--beppu_sue-batch-4"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--beppu_sue-batch-5"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--2個持ち_cut_fit-1products-batch-1"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--2個持ち_cut_fit-1products-batch-2"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--2個持ち_cut_fit-1products-batch-3"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--2個持ち_cut_fit-2products-batch-1"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--2個持ち_cut_fit-nothing"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--2個持ち_cut_fit-notProducts"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--bag20240906_0000-notProducts"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--bag20240906_1022-notProducts-batch-1"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--台置き_cut_fit-1products"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--台置き_cut_fit-2products-batch-1"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--台置き_cut_fit-notProducts"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--beppu_sue-batch-2"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--2個持ち_cut_fit-2products-batch-2"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--台置き_cut_fit-2products-batch-2"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--bag20240906_1022-notProducts-batch-2"]="--erase-IGNORE-productPerson"
    ["customer/PoC2--台置き_cut_fit-nothing"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/01_regularPurchase"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/02_regularPurchase"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/03_regularPurchase"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/04_regularPurchase"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/05_cancelTea"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/06_pullingCart"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/07_holding2items"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/08_regularPurchase"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/09_holding2items"]="--erase-IGNORE-productPerson"
    ["private/Satudora_det_20250117/10_hideBarcode"]="--erase-IGNORE-productPerson"
)


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__POSTFIX_DIR_VERSION[@]}"; do
    postfix__dir__version=${MAP__SUBPATH_DIR__TO__POSTFIX_DIR_VERSION[$subpath__dir]}
    path__dir__img__source="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/images${postfix__dir__version}"
    path__dir__lbl__source="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/labels${postfix__dir__version}"

    path__dir__img__softlink="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/images"
    path__dir__lbl__softlink="${PATH__DIR__DATASETS__SOURCE}/${subpath__dir}/labels"

    # Symlink loop for Ultralytics >:-(
    # if [ -d "$path__dir__img__softlink" ] && [ ! -L "$path__dir__img__softlink" ]; then
    #     echo -e "${TAG__FAILED} images dir already exist and not a softlink: ${subpath__dir}"
    #     exit 1
    # fi
    # if [ -d "$path__dir__lbl__softlink" ] && [ ! -L "$path__dir__lbl__softlink" ]; then
    #     echo -e "${TAG__FAILED} labels dir already exist and not a softlink: ${subpath__dir}"
    #     exit 1
    # fi

    # rm -r "$path__dir__img__softlink"
    # rm -r "$path__dir__lbl__softlink"

    # if ln -s "$path__dir__img__source" "$path__dir__img__softlink"; then
    #     echo -e "${TAG__PASSED} Created softlink images OK: ${subpath__dir}"
    # else
    #     echo -e "${TAG__FAILED} Created softlink images failed: ${subpath__dir}"
    #     exit 1
    # fi
    # if ln -s "$path__dir__lbl__source" "$path__dir__lbl__softlink"; then
    #     echo -e "${TAG__PASSED} Created softlink labels OK: ${subpath__dir}"
    # else
    #     echo -e "${TAG__FAILED} Created softlink labels failed: ${subpath__dir}"
    #     exit 1
    # fi

    # Workaround for the Symblink loop
    [[ -d "$path__dir__img__softlink" ]] && rm -r "$path__dir__img__softlink"
    [[ -d "$path__dir__lbl__softlink" ]] && rm -r "$path__dir__lbl__softlink"
    mkdir -p "${path__dir__img__softlink}"
    mkdir -p "${path__dir__lbl__softlink}" 
    for name__file in $( ls "$path__dir__img__source" ); do
        ln -s $( realpath "$path__dir__img__source/$name__file" ) $path__dir__img__softlink/
    done
    for name__file in $( ls "$path__dir__lbl__source" ); do
        ln -s $( realpath "$path__dir__lbl__source/$name__file" ) $path__dir__lbl__softlink/
    done

    echo -e "${TAG__INFO} Done: ${subpath__dir}"
done