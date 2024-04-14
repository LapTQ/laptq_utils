PATH__DIR__DATASETS__SOURCE__IMG=/mnt/hdd10tb/Datasets/road-issues-detection
POSTFIX__DIR__IMG=--20241121--checked--backup
PATH__DIR__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241121--check-duplicate-images
POSTFIX__DIR__IMG__DEDUP=--20241121--imgdedup--ver2


declare -A MAP__SUBPATH_DIR__TO__NEED_TO_CHECK=(
    # ["APTO_v2/day1_330"]="False"
    # ["APTO_v2/night1_190"]="False"
    # ["APTO_v2/night3_44"]="False"
    # ["APTO_v2/night4_239"]="False"
    # ["Pothole_235/train"]="True"
    # ["dataset-ninja/ds1_simplex-test"]="False"
    # ["dataset-ninja/ds1_simplex-train"]="False"
    # ["dataset-ninja/ds2_complex-test"]="False"
    # ["dataset-ninja/ds2_complex-train"]="False"
    # ["pot_det_1240"]="True"
    # ["pothole_dataset_v8/only_rainy_frames/train"]="False"
    # ["pothole_dataset_v8/train"]="True"
    # ["pothole_dataset_v8/train_to_valid"]="False"
    # ["pothole_dataset_v8/valid"]="False"
    # ["Pothole_detection_yolo/train_original"]="True"
    # ["Pothole_Maeda/first_shot"]="False"
    # ["Pothole_Maeda/first_shot_eval"]="False"
    # ["Pothole_Maeda/second_shot"]="False"
    ["RDD2022_JAPAN/only_pothole/train"]="True"
)


[[ -d "$PATH__DIR__OUTPUT" ]] && rm -r "$PATH__DIR__OUTPUT"


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# check for duplicate images
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[@]}"; do
    is_need_to_check="${MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[$subpath_dir]}"

    if [[ $is_need_to_check != "True" ]]; then
        continue
    fi 

    path__dir__img="${PATH__DIR__DATASETS__SOURCE__IMG}/${subpath_dir}/images${POSTFIX__DIR__IMG}"
    path__dir__output="${PATH__DIR__OUTPUT}/${subpath_dir}"

    python3 submodules/laptq_utils/main.py \
        helper__check__duplicate__images \
        --path__dir__img "$path__dir__img" \
        --path__dir__output "$path__dir__output" \
        --method PHash \
        --max_distance_threshold 5 \
        --to__plot True
done


# create new image version
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[@]}"; do
    is_need_to_check="${MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[$subpath_dir]}"
    
    path__dir__img="${PATH__DIR__DATASETS__SOURCE__IMG}/${subpath_dir}/images${POSTFIX__DIR__IMG}"
    path__dir__img__dedup="${PATH__DIR__DATASETS__SOURCE__IMG}/${subpath_dir}/images${POSTFIX__DIR__IMG__DEDUP}"

    [[ -d "$path__dir__img__dedup" ]] && rm -r "$path__dir__img__dedup"
    mkdir -p "$path__dir__img__dedup"

    if [[ $is_need_to_check = "True" ]]; then
        while IFS= read -r name__file__img; do
            name__file__img="${name__file__img%$'\r'}"  # right strip
            name__file__img="${name__file__img%\"}" # right strip
            name__file__img="${name__file__img#\"}" # left strip
            ln -s $( realpath "${path__dir__img}/${name__file__img}" ) "${path__dir__img__dedup}"
        done < "${PATH__DIR__OUTPUT}/${subpath_dir}/originals_to_keep__no_json.txt"
    else
        IFS=$'\n'
        for name__file__img in $( ls "${path__dir__img}" ); do
            ln -s $( realpath "${path__dir__img}/${name__file__img}" ) "${path__dir__img__dedup}"
        done
    fi 

    echo -e "${TAG__INFO} $( ls ${path__dir__img__dedup} | wc -l )/$( ls ${path__dir__img} | wc -l ) original images in ${subpath_dir}"
done

