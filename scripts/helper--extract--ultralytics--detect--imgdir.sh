PATH__DIR__IMAGE=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/road-issues-detection
POSTFIX__DIR__IMAGE=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0--rescaled-10

PATH__FILE__MODEL=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m--960--crop-20/train8/weights/best.pt

PATH__DIR__LABEL__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241208--model-prediction--json
POSTFIX__DIR__LABEL__OUTPUT=--20241128--phase-2--annotated-ver2--pot-man-drain--checked--crop-top50-side20-botom0--rescaled-10

declare -A MAP__SUBPATH_DIR__TO__=(
    # ["APTO_v2/day1_330"]=""
    # ["APTO_v2/night1_190"]=""
    # ["APTO_v2/night3_44"]=""
    # ["APTO_v2/night4_239"]=""
    # ["dataset-ninja/ds1_simplex-test"]=""
    # ["dataset-ninja/ds1_simplex-train"]=""
    # ["dataset-ninja/ds2_complex-test"]=""
    # ["dataset-ninja/ds2_complex-train"]=""
    # ["pot_det_1240"]=""

    # # ["pothole_dataset_v8/only_rainy_frames/train"]=""

    # ["pothole_dataset_v8/train"]=""
    # ["pothole_dataset_v8/train_to_valid"]=""
    # ["pothole_dataset_v8/valid"]=""
    # ["Pothole_detection_yolo/train_original"]=""
    # ["Pothole_Maeda/first_shot"]=""
    # ["Pothole_Maeda/second_shot"]=""
    # ["RDD2022_JAPAN/only_pothole/train"]=""
    ["Pothole_235/train"]=""
    ["Pothole_Maeda/first_shot_eval"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE}/${subpath__dir}/images${POSTFIX__DIR__IMAGE}"
    path__dir__lbl__output="${PATH__DIR__LABEL__OUTPUT}/${subpath__dir}/labels${POSTFIX__DIR__LABEL__OUTPUT}"

    [[ -d "${path__dir__lbl__output}" ]] && rm -r "${path__dir__lbl__output}"
    mkdir -p "${path__dir__lbl__output}"

    python3 submodules/laptq_utils/main.py \
        helper__extract__ultralytics__detect__imgdir \
        --path__dir__img "${path__dir__img__input}" \
        --path__dir__output "${path__dir__lbl__output}" \
        --path__file__model "${PATH__FILE__MODEL}" \
        --device "cuda:0" \
        --imgsz 960 \
        --thresh__conf__min 0.01
        
done