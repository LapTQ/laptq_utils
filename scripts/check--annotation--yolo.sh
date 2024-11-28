PATH__DIR__DATASETS__PREPARED_FOR_ANNOT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241121--visual-check--downloaded--phase-2--annotation-ver2    # folder containing prepared images used to upload to Label Studio
PATH__DIR__ANNOT__DOWNLOADED_ZIP=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/20241122--fix-visual-check--phase-2--annotation-ver2  # folder containing Label Studio's downloaded .zip
PATH__DIR__ANNOT__EXTRACT_TO=$PATH__DIR__ANNOT__DOWNLOADED_ZIP


# REPLACE__SLASH=--SLASH--
REPLACE__SLASH=--


# Mapping from subdataset dir name to Label Studio's downloaded .zip
# but the keys in this mapping will be used again and again.
declare -A MAP__SUBPATH_DIR__TO__NAME_ZIP=(
    ["APTO_v2/day1_330"]="CK46--APTO_v2--day1_330.zip"
    ["APTO_v2/night1_190"]="CK46--APTO_v2--night1_190.zip"
    ["APTO_v2/night3_44"]="CK46--APTO_v2--night3_44.zip"
    ["APTO_v2/night4_239"]="CK46--APTO_v2--night4_239.zip"
    ["Pothole_235/train"]="CK46--Pothole_235--train.zip"
    # ["dataset-ninja/ds1_simplex-test"]="CK46--dataset-ninja--ds1_simplex-test.zip"
    # ["dataset-ninja/ds1_simplex-train"]="CK46--dataset-ninja--ds1_simplex-train.zip"
    # ["dataset-ninja/ds2_complex-test"]="CK46--dataset-ninja--ds2_complex-test.zip"
    # ["dataset-ninja/ds2_complex-train"]="CK46--dataset-ninja--ds2_complex-train.zip"
    ["pot_det_1240"]="CK46--pot_det_1240.zip"
    # # ["pothole_dataset_v8/only_rainy_frames/train"]=""
    # ["pothole_dataset_v8/train"]="CK46--pothole_dataset_v8--train.zip"
    # ["pothole_dataset_v8/train_to_valid"]="CK46--pothole_dataset_v8--train_to_valid.zip"
    # ["pothole_dataset_v8/valid"]="CK46--pothole_dataset_v8--valid.zip"
    # ["Pothole_detection_yolo/train_original"]="CK46--Pothole_detection_yolo--train_original.zip"
    ["Pothole_Maeda/first_shot"]="CK46--Pothole_Maeda--first_shot.zip"
    ["Pothole_Maeda/first_shot_eval"]="CK46--Pothole_Maeda--first_shot_eval.zip"
    ["Pothole_Maeda/second_shot"]="CK46--Pothole_Maeda--second_shot.zip"
    ["RDD2022_JAPAN/only_pothole/train"]="CK46--RDD2022_JAPAN--only_pothole--train.zip"
)


########################################################################################################################################################

# Mapping from subpath dir to the name after replacing slash
declare -A map__subpath_dir__to__name_dir_unslashed
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
    map__subpath_dir__to__name_dir_unslashed[$subpath_dir]=${subpath_dir//\//$REPLACE__SLASH}
done


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# =========== extract and rename ===========
IFS=$'\n'
num__dir__extracted=0
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
    name__zip=${MAP__SUBPATH_DIR__TO__NAME_ZIP[$subpath_dir]}
    echo -e "$TAG__INFO Extracting $name__zip as $subpath_dir"
    path__dir__extracted="${PATH__DIR__ANNOT__EXTRACT_TO}/${subpath_dir}"
    rm -r "${path__dir__extracted}"
    mkdir -p "${path__dir__extracted}"
    unzip -o -q "${PATH__DIR__ANNOT__DOWNLOADED_ZIP}/${name__zip}" -d "$path__dir__extracted"
    
    find "$path__dir__extracted/labels" -type f -name "classes.txt" -exec rm -f {} \;
    find "$path__dir__extracted/labels" -type f -name ".DS_Store" -exec rm -f {} \;

    if [[ -d "$path__dir__extracted" ]]; then
        num__dir__extracted=$((num__dir__extracted + 1))
    fi
done
num__zip=$(find "${PATH__DIR__ANNOT__DOWNLOADED_ZIP}/" -mindepth 1 -maxdepth 1 -type f -name "*.zip" | wc -l)
if [ $num__zip -ne $num__dir__extracted ]; then
    echo -e "${TAG__WARNING} Number of .zip and folders mismatch"
    echo "    [+] $num__zip .zip files"
    echo "    [+] $num__dir__extracted folders"
    echo "Please check if you forgot to extract any zip file!!!"
    exit 1
fi
echo -e "${TAG__PASSED} $num__zip .zip files == $num__dir__extracted extracted folders"



# =========== Test: Number of folders in the annotation preparation and number of folders in the extraction should be equal ===========
num__dir__prepared=$(find "${PATH__DIR__DATASETS__PREPARED_FOR_ANNOT}/" -mindepth 1 -maxdepth 1 -type d | wc -l)
if [ $num__dir__prepared -ne $num__dir__extracted ]; then
    echo -e "${TAG__WARNING} Number of folders mismatch"
    echo "    [+] $num__dir__prepared folders in annotation preparation $PATH__DIR__DATASETS__PREPARED_FOR_ANNOT"
    echo "    [+] $num__dir__extracted folders in extraction $PATH__DIR__ANNOT__EXTRACT_TO"
    echo "Please check if you forgot to download any project!!!"
    exit 1
fi
echo -e "${TAG__PASSED} ${num__dir__prepared} folders in the annotation preparation == ${num__dir__extracted} folders extracted"


# =========== Test: Number of images in the annotation preparation and number of labels in the extraction must be equal ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
    is__mismatched=0
    path__dir__img__prepared="${PATH__DIR__DATASETS__PREPARED_FOR_ANNOT}/${MAP__SUBPATH_DIR__TO__NAME_ZIP[$subpath_dir]%.*}/images"
    path__dir__lbl__extracted="${PATH__DIR__ANNOT__EXTRACT_TO}/${subpath_dir}/labels"
    
    num__img=$(find "${path__dir__img__prepared}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    num__lbl=$(find "${path__dir__lbl__extracted}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__img -ne $num__lbl ]; then
        echo -e "${TAG__FAILED} Number of images and annotations mismatch: ${subpath_dir}"
        echo "    [+] $num__img images"
        echo "    [+] $num__lbl labels"
        echo "Please check if you forgot to annotate any image!!!"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__img} images in the annotation preparation == ${num__lbl} labels in extraction: $subpath_dir"
done