PATH__DIR__DATASETS__SOURCE=/mnt/hdd10tb/Datasets/road-issues-detection
PATH__DIR__DATASETS__PREPARED_FOR_ANNOT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241115--prepare-annotation--remove-too-small--no-synthetic--widen-10-percent    # folder containing prepared images used to upload to Label Studio
PATH__DIR__DOWNLOADED_ANNOT_ZIP=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/20241118--annotation--downloaded--pothole-manhole-drainage    # folder containing Label Studio's downloaded .zip


# ----- For visualization
# 1. select label source for visualization
# (using image--raw from source dataset, not from the annotation preparation. Therefore, the path structure of labels must be the same as images)

PATH__DIR__DATASETS__OF_LABEL__FOR__VISUALIZATION=$PATH__DIR__DOWNLOADED_ANNOT_ZIP       # if checking downloaded annotation
POSTFIX__DIR__LABEL__FOR__VISUALIZATION=""
# PATH__DIR__DATASETS__OF_LABEL__FOR__VISUALIZATION=$PATH__DIR__DATASETS__SOURCE         # if checking a label version in source dataset
# POSTFIX__DIR__LABEL__FOR__VISUALIZATION=--20241119--phase-2--annotated-ver2--pothole-manhole-drainage

PATH__FILE__CLASS_ID__TO__LABEL=src/configs/class_id_to_label.yaml
PATH__DIR__VISUALIZATION__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241118--visualization--phase-2--annotated-ver2--pothole-manhole-drainage         # folder to store visualization. Should not be placed in the same parent with image and labels to avoid unwanted modification.
# ----- 


# ----- For merging after checking
# 1. ...
REPLACE__SLASH=--SLASH--
POSTFIX__DIR__IMG__RAW=--raw
PREFIX__DIR__STRIP=PRJ46--SLASH--
POSTFIX__DIR__LABEL__TARGET=--20241119--phase-2--annotated-ver2--pothole-manhole-drainage
# ----- 


# Mapping from subdataset dir name to Label Studio's downloaded .zip
# but the keys in this mapping will be used again and again.
declare -A MAP__SUBPATH_DIR__TO__NAME_ZIP=(
    ["RDD2022_JAPAN/only_pothole/train"]="project-202-at-2024-11-18-09-46-5a8cd644.zip"
    ["Pothole_detection_yolo/train_original"]="project-198-at-2024-11-18-09-48-b7a67123.zip"
    # ["Pothole_Maeda/first_shot"]=""
    # ["Pothole_Maeda/second_shot"]=""
    # ["pot_det_1240"]=""
    # ["APTO_v2/day1_330"]=""
    # ["APTO_v2/night1_190"]=""
    # ["APTO_v2/night3_44"]=""
    # ["APTO_v2/night4_239"]=""
    # ["pothole_dataset_v8/only_rainy_frames/train"]=""
    # ["pothole_dataset_v8/train"]=""
    # ["pothole_dataset_v8/train_to_valid"]=""
    # ["pothole_dataset_v8/valid"]=""
    # ["Pothole_235/train"]=""
    # ["Pothole_Maeda/first_shot_eval"]=""
)


########################################################################################################################################################

# Mapping from subpath dir to the name after replacing slash
declare -A map__subpath_dir__to__name_dir_unslashed
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
    map__subpath_dir__to__name_dir_unslashed[$subpath_dir]=${subpath_dir//\//$REPLACE__SLASH}
done


# remove the folder for visualization
[[ -d "$PATH__DIR__VISUALIZATION__OUTPUT" ]] && rm -r "$PATH__DIR__VISUALIZATION__OUTPUT"


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# # =========== extract and rename ===========
# IFS=$'\n'
# for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
#     name__zip=${MAP__SUBPATH_DIR__TO__NAME_ZIP[$subpath_dir]}
#     echo -e "$TAG__INFO Extracting $name__zip as $subpath_dir"
#     path__dir_extracted="${PATH__DIR__DOWNLOADED_ANNOT_ZIP}/${subpath_dir}"
#     mkdir -p "${PATH__DIR__DOWNLOADED_ANNOT_ZIP}/${subpath_dir}"
#     unzip -o -q "${PATH__DIR__DOWNLOADED_ANNOT_ZIP}/${name__zip}" -d "$path__dir_extracted"
# done


# # =========== Test: Number of folders in the annotation preparation and number of folders in the extraction should be equal ===========
# num__dir__prepared=$(find "${PATH__DIR__DATASETS__PREPARED_FOR_ANNOT}/" -mindepth 1 -maxdepth 1 -type d | wc -l)
# num__dir__extracted=$(find "${PATH__DIR__DOWNLOADED_ANNOT_ZIP}/" -mindepth 1 -maxdepth 1 -type d | wc -l)
# if [ $num__dir__prepared != $num__dir__extracted ]; then
#     echo -e "${TAG__WARNING} Number of folders mismatch"
#     echo "    [+] $num__dir__prepared folders in annotation preparation $PATH__DIR__DATASETS__PREPARED_FOR_ANNOT"
#     echo "    [+] $num__dir__extracted folders in extraction $PATH__DIR__DOWNLOADED_ANNOT_ZIP"
#     echo "Please check if you forgot to download any project!!!"
#     exit 1
# fi
# echo -e "${TAG__PASSED}"


# # =========== Test: Number of images in the annotation preparation and number of labels in the extraction must be equal ===========
# is__mismatched=0
# for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
#     path__dir__img__prepared="${PATH__DIR__DATASETS__PREPARED_FOR_ANNOT}/${PREFIX__DIR__STRIP}${map__subpath_dir__to__name_dir_unslashed[$subpath_dir]}/images"
#     path__dir__lbl__extracted="${PATH__DIR__DOWNLOADED_ANNOT_ZIP}/${subpath_dir}/labels"
    
#     num__img=$(find "${path__dir__img__prepared}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
#     num__lbl=$(find "${path__dir__lbl__extracted}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
#     if [ $num__img != $num__lbl ]; then
#         echo -e "${TAG__FAILED} Number of images and annotations mismatch: ${subpath_dir}"
#         echo "    [+] $num__img images"
#         echo "    [+] $num__lbl labels"
#         echo "Please check if you forgot to annotate any image!!!"
        
#         if [ $is__mismatched -eq 0 ]; then
#             is__mismatched=1
#         fi
#     fi
# done
# if [ $is__mismatched -eq 1 ]; then
#     exit 1
# fi
# echo -e "${TAG__PASSED}"


# =========== Test: (Visual check) visualize images ===========
# for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
#     path__dir__img="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__RAW}"
#     path__dir__annot="${PATH__DIR__DATASETS__OF_LABEL__FOR__VISUALIZATION}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__FOR__VISUALIZATION}"
#     path__dir__img_vis="${PATH__DIR__VISUALIZATION__OUTPUT}/${subpath_dir}"

#     python3 submodules/laptq_utils/main.py \
#         helper__visualize__detection \
#         --path__dir__img "${path__dir__img}" \
#         --path__dir__annot "${path__dir__annot}" \
#         --path__dir__output "${path__dir__img_vis}" \
#         --draw_track_id False \
#         --draw_conf False \
#         --draw_class_id True \
#         --fontScale 0.7 \
#         --thickness 1 \
#         --draw_class_name True \
#         --box_color_by class_id \
#         --path__file__class_id_to_label $PATH__FILE__CLASS_ID__TO__LABEL
    
#     num__lbl=$(find "${path__dir__annot}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
#     num__img_vis=$(find "${path__dir__img_vis}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
#     if [ $num__lbl != $num__img_vis ]; then
#         echo -e "${TAG__FAILED} Number of visualized images and annotations mismatch: ${subpath_dir}"
#         echo "    [+] $num__lbl labels"
#         echo "    [+] $num__img visualized images"
        
#         exit 1
#     fi
#     echo -e "${TAG__PASSED} ${num__lbl} labels vs ${num__img_vis} visualized images"
# done


# # =========== Copy labels from extracted annotation to source dataset dir ===========
# for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
#     path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__RAW}"
#     path__dir__img__output="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__LABEL__TARGET}"
#     path__dir__lbl__input="${PATH__DIR__DOWNLOADED_ANNOT_ZIP}/${subpath_dir}/labels"
#     path__dir__lbl__output="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__TARGET}"

#     [[ -d "$path__dir__lbl__output" ]] && rm -r "$path__dir__lbl__output"
#     mkdir -p "$path__dir__lbl__output"

#     for name__file__img in $( ls "${path__dir__img__input}" ); do
#         name__file__lbl=${name__file__img%.*}.txt
#         path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl}"
#         if [[ ! -f "$path__file__lbl__input" ]]; then
#             continue
#         fi
#         cp "$path__file__lbl__input" "$path__dir__lbl__output"
#     done

#     num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
#     num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
#     if [ $num__lbl__input != $num__lbl__output ]; then
#         echo -e "${TAG__FAILED} Number of labels in the extracted annotation and number of labels copied mismatched: ${subpath_dir}"
#         echo "    [+] $num__lbl__input labels in the extracted annotation"
#         echo "    [+] $num__lbl__output labels in the copied folder"
        
#         exit 1
#     fi
#     echo -e "${TAG__PASSED} Copied ${num__lbl__input} labels to ${num__lbl__output} labels"
# done


# # =========== Create a soft link to images corresponding to the label version ===========
# for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NAME_ZIP[@]}"; do
#     path__dir__lbl="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__TARGET}"
#     path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__RAW}"
#     path__dir__img__output="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__LABEL__TARGET}"

#     [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
#     mkdir -p "$path__dir__img__output"

#     for name__file__img in $( ls "${path__dir__img__input}" ); do
#         name__file__lbl=${name__file__img%.*}.txt
#         path__file__lbl="${path__dir__lbl}/${name__file__lbl}"
#         if [[ ! -f "$path__file__lbl" ]]; then
#             continue
#         fi
#         ln -s "$path__dir__img__input/$name__file__img" "$path__dir__img__output"
#     done

#     num__lbl=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
#     num__img=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
#     if [ $num__lbl != $num__img ]; then
#         echo -e "${TAG__FAILED} Number of labels and images mismatched: ${subpath_dir}"
#         echo "    [+] $num__lbl labels"
#         echo "    [+] $num__img images"
        
#         exit 1
#     fi
#     echo -e "${TAG__PASSED} Linked ${num__img} images corresponding to ${num__lbl} labels"
# done