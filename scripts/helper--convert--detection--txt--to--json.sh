PATH__DIR__LABEL__INPUT=/mnt
POSTFIX__DIR__LABEL__INPUT=""

PATH__DIR__LABEL__OUTPUT=//home/laptq/laptq-prj-21/outputs/20241225--true-labels--json
POSTFIX__DIR__LABEL__OUTPUT=""

MODE__BOX="xcycwhn"
# MODE__BOX="polygonn"

declare -A MAP__SUBPATH_DIR__TO__=(
    # # poly
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/All_off"]=""
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Edge_cases"]=""
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/High_activity"]=""
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/IRfilter"]=""
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/IRill"]=""
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Lunch1"]=""
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Lunch2"]=""
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Lunch3"]=""
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_1/Camera_1"]=""
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_1/Camera_2"]=""
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_1/Camera_3"]=""
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_3/Camera_2"]=""
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_3/Camera_3"]=""
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Lab1"]=""
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Lab2"]=""
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Meeting1"]=""
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Meeting2"]=""
    # ["ssd8tb/shared_workspace/fisheye/LOAF/labels_poly/resolution_2k/test"]=""
    # ["ssd8tb/shared_workspace/fisheye/LOAF/labels_poly/resolution_2k/train"]=""
    # ["ssd8tb/shared_workspace/fisheye/LOAF/labels_poly/resolution_2k/val"]=""
    # ["ssd8tb/shared_workspace/fisheye/MW-R/labels_poly"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/call_center"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/exhibition"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/exhibition_setup"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/it_office"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/jewelry_store"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/convenience_store"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/empty_store"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/jewelry_store_2"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/kindergarten"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/large_office"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/large_office_2"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/printing_store"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/repair_store"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/street_grocery"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/tech_store"]=""
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/warehouse"]=""
    
    # rect
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-0"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-1"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-2"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-3"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-4"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-0"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-1"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-2"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-3"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-4"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-5"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-6"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-7"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-8"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-9"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-10"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-11"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-12"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-13"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-14"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-15"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-16"]=""
    ["ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-17"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_test2"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_test3"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_training"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_test2"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_test3"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_training"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_test2"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_test3"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_training"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_test2"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_test3"]=""
    ["ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_training"]=""
    ["ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/labels/test"]=""
    ["ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/labels/train"]=""
    ["ssd8tb/shared_workspace/manhpc/sat_34k/labels/train"]=""
    ["ssd8tb/shared_workspace/manhpc/sat_34k/labels/val"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    # path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__INPUT}"
    # path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"
    path__dir__lbl__input="${PATH__DIR__LABEL__INPUT}/${subpath__dir}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}"

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