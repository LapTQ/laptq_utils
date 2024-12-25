PATH__DIR__IMAGE=/mnt
POSTFIX__DIR__IMAGE=""

PATH__DIR__LABEL=/home/laptq/laptq-prj-21/outputs/20241225--true-labels--json--xcycwhn-to-polygonn
POSTFIX__DIR__LABEL=""

NUM__MAX__IMG__TO__VISUALIZE=3
IS_OK__LBL_NOT_FOUND=True
PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/outputs/20241223--img-360--visualize

declare -A MAP__SUBPATH_DIR__TO__=(
    ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/All_off"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/All_off"
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Edge_cases"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Edge_cases"
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/High_activity"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/High_activity"
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/IRfilter"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/IRfilter"
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/IRill"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/IRill"
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Lunch1"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Lunch1"
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Lunch2"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Lunch2"
    # ["ssd8tb/shared_workspace/fisheye/CEPDOF/images/Lunch3"]="ssd8tb/shared_workspace/fisheye/CEPDOF/labels_poly/Lunch3"
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_1/Camera_1"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_1/Camera_1"
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_1/Camera_2"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_1/Camera_2"
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_1/Camera_3"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_1/Camera_3"
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_3/Camera_2"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_3/Camera_2"
    # ["ssd8tb/shared_workspace/fisheye/FRIDA/images/Segment_3/Camera_3"]="ssd8tb/shared_workspace/fisheye/FRIDA/labels_poly/Segment_3/Camera_3"
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Lab1"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Lab1"
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Lab2"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Lab2"
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Meeting1"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Meeting1"
    # ["ssd8tb/shared_workspace/fisheye/HABBOF/images/Meeting2"]="ssd8tb/shared_workspace/fisheye/HABBOF/labels_poly/Meeting2"
    # ["ssd8tb/shared_workspace/fisheye/LOAF/images/resolution_2k/test"]="ssd8tb/shared_workspace/fisheye/LOAF/labels_poly/resolution_2k/test"
    # ["ssd8tb/shared_workspace/fisheye/LOAF/images/resolution_2k/train"]="ssd8tb/shared_workspace/fisheye/LOAF/labels_poly/resolution_2k/train"
    # ["ssd8tb/shared_workspace/fisheye/LOAF/images/resolution_2k/val"]="ssd8tb/shared_workspace/fisheye/LOAF/labels_poly/resolution_2k/val"
    # ["ssd8tb/shared_workspace/fisheye/MW-R/images"]="ssd8tb/shared_workspace/fisheye/MW-R/labels_poly"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/call_center"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/call_center"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/exhibition"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/exhibition"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/exhibition_setup"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/exhibition_setup"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/it_office"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/it_office"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/jewelry_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/jewelry_store"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/convenience_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/convenience_store"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/empty_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/empty_store"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/jewelry_store_2"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/jewelry_store_2"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/kindergarten"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/kindergarten"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/large_office"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/large_office"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/large_office_2"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/large_office_2"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/printing_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/printing_store"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/repair_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/repair_store"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/street_grocery"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/street_grocery"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/tech_store"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/tech_store"
    # ["ssd8tb/shared_workspace/fisheye/WEPDTOF/images/warehouse"]="ssd8tb/shared_workspace/fisheye/WEPDTOF/labels_poly/warehouse"

    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-0"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-0"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-1"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-1"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-2"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-2"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-3"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-3"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario1/top-4"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario1/top-4"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-0"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-0"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-1"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-1"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-2"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-2"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-3"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-3"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-4"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-4"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-5"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-5"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-6"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-6"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-7"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-7"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-8"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-8"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-9"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-9"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-10"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-10"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-11"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-11"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-12"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-12"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-13"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-13"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-14"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-14"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-15"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-15"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-16"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-16"
    # ["ssd8tb/shared_workspace/fisheye/BOMNI/images/scenario2/top-17"]="ssd8tb/shared_workspace/fisheye/BOMNI/labels/scenario2/top-17"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_1A/omni1A_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_test2"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_1A/omni1A_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_test3"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_1A/omni1A_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_1A/omni1A_training"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_2A/omni2A_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_test2"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_2A/omni2A_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_test3"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_2A/omni2A_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_2A/omni2A_training"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_3A/omni3A_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_test2"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_3A/omni3A_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_test3"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_A/omni_3A/omni3A_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_A/omni_3A/omni3A_training"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_B/omni_1B/omni1B_test2"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_test2"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_B/omni_1B/omni1B_test3"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_test3"
    # ["ssd8tb/shared_workspace/fisheye/PIROPO/images/Room_B/omni_1B/omni1B_training"]="ssd8tb/shared_workspace/fisheye/PIROPO/labels/Room_B/omni_1B/omni1B_training"
    # ["ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/images/test"]="ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/labels/test"
    # ["ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/images/train"]="ssd8tb/shared_workspace/fisheye/top-view-multi-person-tracking-2020/labels/train"
    
    # ["ssd8tb/shared_workspace/manhpc/sat_34k/images/train"]="ssd8tb/shared_workspace/manhpc/sat_34k/labels/train"
    # ["ssd8tb/shared_workspace/manhpc/sat_34k/images/val"]="ssd8tb/shared_workspace/manhpc/sat_34k/labels/val"
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    # path__dir__img="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    # path__dir__lbl="${PATH__DIR__LABEL}/${subpath__dir}/labels${POSTFIX__DIR__LABEL}"
    path__dir__img="${PATH__DIR__IMAGE}/${subpath__dir}"
    path__dir__lbl="${PATH__DIR__LABEL}/${MAP__SUBPATH_DIR__TO__[$subpath__dir]}"

    path__dir__output="${PATH__DIR__OUTPUT}/${subpath__dir}"

    [[ -d "${path__dir__output}" ]] && rm -r "${path__dir__output}"
    mkdir -p "${path__dir__output}"

    python3 submodules/laptq_utils/main.py \
        helper__draw__detection__imgdir \
        --path__dir__img "${path__dir__img}" \
        --path__dir__lbl "${path__dir__lbl}" \
        --path__dir__output "${path__dir__output}" \
        --to_draw__box_x1y1whn False \
        --to_draw__box_polygonn True \
        --to_draw__box_conf True \
        --to_draw__id_class True \
        --to_draw__name_class False \
        --fontScale 1 \
        --thickness 1 \
        --box_color_by id__class \
        --path__file__map__id_class__to__name_class $PATH__FILE__MAP__ID_CLASS__TO__NAME_CLASS \
        --num__max__img $NUM__MAX__IMG__TO__VISUALIZE \
        --seed 42 \
        --is_ok__lbl_not_exist $IS_OK__LBL_NOT_FOUND


    num__lbl=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img_vis=$(find "${path__dir__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $NUM__MAX__IMG__TO__VISUALIZE != "None" ] && [ $num__lbl > $NUM__MAX__IMG__TO__VISUALIZE ]; then
        num__lbl=$NUM__MAX__IMG__TO__VISUALIZE
    fi
    if [ $num__lbl != $num__img_vis ]; then
        echo -e "${TAG__FAILED} Number of visualized images and annotations mismatch: ${subpath__dir}"
        echo "    [+] $num__lbl labels"
        echo "    [+] $num__img_vis visualized images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__lbl} labels == ${num__img_vis} visualized images: ${subpath__dir}"
done