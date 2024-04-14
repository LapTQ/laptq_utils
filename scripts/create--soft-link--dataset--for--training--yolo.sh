PATH__DIR__DATASETS__SOURCE=/mnt/hdd10tb/Datasets/road-issues-detection

declare -A MAP__SUBPATH_DIR__TO__POSTFIX_DIR_VERSION=(
    ["APTO_v2/day1_330"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["APTO_v2/night1_190"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["APTO_v2/night3_44"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["APTO_v2/night4_239"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["dataset-ninja/ds1_simplex-test"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["dataset-ninja/ds1_simplex-train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["dataset-ninja/ds2_complex-test"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["dataset-ninja/ds2_complex-train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["pot_det_1240"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    # ["pothole_dataset_v8/only_rainy_frames/train"]=""
    ["pothole_dataset_v8/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["pothole_dataset_v8/train_to_valid"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["pothole_dataset_v8/valid"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["Pothole_detection_yolo/train_original"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["Pothole_Maeda/first_shot"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["Pothole_Maeda/second_shot"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["RDD2022_JAPAN/only_pothole/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["Pothole_235/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"
    ["Pothole_Maeda/first_shot_eval"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0"


    # ["APTO_v2/day1_330"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["APTO_v2/night1_190"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["APTO_v2/night3_44"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["APTO_v2/night4_239"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["dataset-ninja/ds1_simplex-test"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["dataset-ninja/ds1_simplex-train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["dataset-ninja/ds2_complex-test"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["dataset-ninja/ds2_complex-train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["pot_det_1240"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # # ["pothole_dataset_v8/only_rainy_frames/train"]=""
    # ["pothole_dataset_v8/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["pothole_dataset_v8/train_to_valid"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["pothole_dataset_v8/valid"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["Pothole_detection_yolo/train_original"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["Pothole_Maeda/first_shot"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["Pothole_Maeda/second_shot"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["RDD2022_JAPAN/only_pothole/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["Pothole_235/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"
    # ["Pothole_Maeda/first_shot_eval"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked"


    # ["APTO_v2/day1_330"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["APTO_v2/night1_190"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["APTO_v2/night3_44"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["APTO_v2/night4_239"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["dataset-ninja/ds1_simplex-test"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["dataset-ninja/ds1_simplex-train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["dataset-ninja/ds2_complex-test"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["dataset-ninja/ds2_complex-train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["pot_det_1240"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # # ["pothole_dataset_v8/only_rainy_frames/train"]=""
    # ["pothole_dataset_v8/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["pothole_dataset_v8/train_to_valid"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["pothole_dataset_v8/valid"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["Pothole_detection_yolo/train_original"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["Pothole_Maeda/first_shot"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["Pothole_Maeda/second_shot"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["RDD2022_JAPAN/only_pothole/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["Pothole_235/train"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"
    # ["Pothole_Maeda/first_shot_eval"]="--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop"


    # ["Pothole_235/train"]="--20241129--phase-2--annotated-ver2--only-pot"
    # ["Pothole_Maeda/first_shot_eval"]="--20241129--phase-2--annotated-ver2--only-pot"


    # ["Pothole_235/train"]="--20240614--phase-1--pothole"
    # ["Pothole_Maeda/first_shot_eval"]="--20240614--phase-1--pothole"


    # ["APTO_v2/day1_330"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["APTO_v2/night1_190"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["APTO_v2/night3_44"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["APTO_v2/night4_239"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["Pothole_235/train"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["dataset-ninja/ds1_simplex-test"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["dataset-ninja/ds1_simplex-train"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["dataset-ninja/ds2_complex-test"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["dataset-ninja/ds2_complex-train"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["pot_det_1240"]="--20241129--phase-2--annotated-ver2--pot-man"
    # # ["pothole_dataset_v8/only_rainy_frames/train"]=""
    # ["pothole_dataset_v8/train"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["pothole_dataset_v8/train_to_valid"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["pothole_dataset_v8/valid"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["Pothole_detection_yolo/train_original"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["Pothole_Maeda/first_shot"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["Pothole_Maeda/first_shot_eval"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["Pothole_Maeda/second_shot"]="--20241129--phase-2--annotated-ver2--pot-man"
    # ["RDD2022_JAPAN/only_pothole/train"]="--20241129--phase-2--annotated-ver2--pot-man"
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
done