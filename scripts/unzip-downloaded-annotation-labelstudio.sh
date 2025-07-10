PATHD_INPUT=/home/laptq/laptq-prj-44/outputs/downloaded-labelstudio-annotation-zip  # folder containing Label Studio's downloaded .zip
PATHD_OUTPUT=/home/laptq/laptq-prj-44/outputs/unzip-downloaded-annotation-labelstudio


# REPLACE__SLASH=--SLASH--
REPLACE__SLASH=--


declare -A MAP__NAME_ZIP__TO__=(
    ["P52-customer-SLS-train-batch-1.zip"]=""
    ["P52-customer-SLS-train-batch-3.zip"]=""
    ["P52-customer-SLS-val.zip"]=""
    ["P52-private-SLS-train-batch-1.zip"]=""
    ["P52-private-SLS-train-batch-3.zip"]=""
    ["P52-customer-SLS-train-batch-2.zip"]=""
    ["P52-customer-SLS-train-batch-4.zip"]=""
    ["P52-private-SLS-test.zip"]=""
    ["P52-private-SLS-train-batch-2.zip"]=""
    ["P52-private-SLS-val.zip"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# =========== extract and rename ===========
IFS=$'\n'
num__dir__extracted=0
for namef_input in "${!MAP__NAME_ZIP__TO__[@]}"; do
    # extract basename from namef_input
    subpath_dir=${namef_input%.*}
    echo -e "$TAG__INFO Extracting $namef_input as $subpath_dir"
    
    pathd_output="${PATHD_OUTPUT}/${subpath_dir}"

    # remove old folder if exists
    [[ -d "$pathd_output" ]] && rm -r "$pathd_output"
    
    mkdir -p "${pathd_output}"
    unzip -o -q "${PATHD_INPUT}/${namef_input}" -d "$pathd_output"
    
    find "$pathd_output/labels" -type f -name "classes.txt" -exec rm -f {} \;
    find "$pathd_output/labels" -type f -name ".DS_Store" -exec rm -f {} \;

    if [[ -d "$pathd_output" ]]; then
        num__dir__extracted=$((num__dir__extracted + 1))
    fi
done
num__zip=$(find "${PATHD_INPUT}/" -mindepth 1 -maxdepth 1 -type f -name "*.zip" | wc -l)
if [ $num__zip -ne $num__dir__extracted ]; then
    echo -e "${TAG__WARNING} Number of .zip and folders mismatch"
    echo "    [+] $num__zip .zip files"
    echo "    [+] $num__dir__extracted folders"
    echo "Please check if you forgot to extract any zip file!!!"
    exit 1
fi
echo -e "${TAG__PASSED} $num__zip .zip files == $num__dir__extracted extracted folders"