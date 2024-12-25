PATH__DIR__LABEL__SOURCE=/mnt
POSTFIX__DIR__LABEL__SOURCE=""

PATH__DIR__DATASETS__SOURCE=/home/laptq/laptq-prj-21/outputs/20241224--img--sampled--uniform
POSTFIX__DIR__IMG__SOURCE=""

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/outputs/20241224--dataset--ready--sampled--uniform
POSTFIX__DIR__VERSION__TARGET=""


declare -A MAP__SUBPATH_DIR__TO__=(
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/All_off"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/All_off"
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Edge_cases"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/Edge_cases"
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/High_activity"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/High_activity"
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/IRfilter"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/IRfilter"
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/IRill"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/IRill"
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Lunch1"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/Lunch1"
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Lunch2"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/Lunch2"
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Lunch3"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_rect/Lunch3"
    ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_1/Camera_1"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_rect/Segment_1/Camera_1"
    ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_1/Camera_2"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_rect/Segment_1/Camera_2"
    ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_1/Camera_3"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_rect/Segment_1/Camera_3"
    ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_3/Camera_2"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_rect/Segment_3/Camera_2"
    ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_3/Camera_3"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_rect/Segment_3/Camera_3"
    ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Lab1"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_rect/Lab1"
    ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Lab2"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_rect/Lab2"
    ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Meeting1"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_rect/Meeting1"
    ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Meeting2"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_rect/Meeting2"
    ["ssd8tb/shared_workspace/fisheye/LOAF/images/resolution_2k/test"]="ssd8tb/shared_workspace/fisheye/LOAF/labels_rect/resolution_2k/test"
    ["ssd8tb/shared_workspace/fisheye/LOAF/images/resolution_2k/train"]="ssd8tb/shared_workspace/fisheye/LOAF/labels_rect/resolution_2k/train"
    ["ssd8tb/shared_workspace/fisheye/LOAF/images/resolution_2k/val"]="ssd8tb/shared_workspace/fisheye/LOAF/labels_rect/resolution_2k/val"
    ["ssd8tb/shared_workspace/fisheye/MW-R/images"]="ssd8tb/shared_workspace/fisheye/MW-R/labels_rect"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/call_center"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/call_center"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/exhibition"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/exhibition"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/exhibition_setup"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/exhibition_setup"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/it_office"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/it_office"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/jewelry_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/jewelry_store"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/convenience_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/convenience_store"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/empty_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/empty_store"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/jewelry_store_2"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/jewelry_store_2"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/kindergarten"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/kindergarten"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/large_office"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/large_office"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/large_office_2"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/large_office_2"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/printing_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/printing_store"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/repair_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/repair_store"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/street_grocery"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/street_grocery"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/tech_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/tech_store"
    ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/warehouse"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_rect/warehouse"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-0"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-0"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-1"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-1"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-2"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-2"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-3"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-3"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-4"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-4"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-0"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-0"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-1"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-1"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-2"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-2"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-3"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-3"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-4"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-4"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-5"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-5"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-6"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-6"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-7"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-7"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-8"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-8"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-9"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-9"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-10"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-10"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-11"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-11"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-12"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-12"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-13"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-13"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-14"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-14"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-15"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-15"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-16"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-16"
    ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-17"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-17"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_1A/omni1A_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_test2"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_1A/omni1A_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_test3"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_1A/omni1A_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_training"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_2A/omni2A_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_test2"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_2A/omni2A_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_test3"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_2A/omni2A_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_training"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_3A/omni3A_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_test2"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_3A/omni3A_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_test3"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_3A/omni3A_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_training"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_B/omni_1B/omni1B_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_test2"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_B/omni_1B/omni1B_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_test3"
    ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_B/omni_1B/omni1B_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_training"
    ["ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/images/test"]="ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/labels/test"
    ["ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/images/train"]="ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/labels/train"
    ["ssd8tb/shared_workspace/manhpc/sat_34k/images/train"]="ssd8tb/shared_workspace/manhpc/sat_34k/labels/train"
    ["ssd8tb/shared_workspace/manhpc/sat_34k/images/val"]="ssd8tb/shared_workspace/manhpc/sat_34k/labels/val"
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# =========== Copy labels from extracted annotation to source dataset dir ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${MAP__SUBPATH_DIR__TO__[$subpath_dir]}"
    path__dir__lbl__output="${PATH__DIR__OUTPUT}/${MAP__SUBPATH_DIR__TO__[$subpath_dir]/labels_rect/labels}"

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
    path__dir__lbl="${PATH__DIR__OUTPUT}/${MAP__SUBPATH_DIR__TO__[$subpath_dir]/labels_rect/labels}"
    path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}"

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