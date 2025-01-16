PATH__DIR__VIDEO=/mnt/ssd8tb/shared_workspace/manhpc/FS_prj21

PATH__DIR__LABEL=/home/laptq/laptq-prj-21/runs/data--synthetic/yolo11s--832--scale-0.5--multiscale-True/predict--train--imgsz-832--conf-0.1/predict

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/runs/data--synthetic/yolo11s--832--scale-0.5--multiscale-True/predict--train--imgsz-832--conf-0.1/predict/draw

[[ -d "${PATH__DIR__OUTPUT}" ]] && rm -r "${PATH__DIR__OUTPUT}"
mkdir -p "${PATH__DIR__OUTPUT}"

declare -A MAP__NAME_VIDEO__TO__=(
    # ["1_2024-11-26_081159_0_5min.mp4"]=""
    # ["1_2024-11-26_081159_1_5min.mp4"]=""
    # ["1_2024-11-26_081159_2_5min.mp4"]=""
    # ["1_2024-11-26_081159_3_5min.mp4"]=""

    ["1_2024-11-26_081159_0.mp4"]=""
    ["1_2024-11-26_081159_1.mp4"]=""
    ["1_2024-11-26_081159_2.mp4"]=""
    ["1_2024-11-26_081159_3.mp4"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__file__video__input="${PATH__DIR__VIDEO}/${name__video}"
    path__dir__lbl__input="${PATH__DIR__LABEL}/${name__video}/labels"
    path__file__output="${PATH__DIR__OUTPUT}/${name__video}"

    python3 submodules/laptq_utils/main.py \
        helper__draw__detection__video \
        --path__file__video__input "${path__file__video__input}" \
        --path__dir__lbl__input "${path__dir__lbl__input}" \
        --path__file__output "${path__file__output}" \
        --num__pad__0 6 \
        --fourcc "mp4v" \
        --to_draw__id_frame True \
        --to_draw__box_x1y1whn True \
        --to_draw__box_polygonn False \
        --to_draw__box_conf True \
        --to_draw__id_class False \
        --to_draw__name_class False \
        --fontScale 1 \
        --thickness 2 \
        --box_color_by id__class \
        --path__file__map__id_class__to__name_class /home/laptq/Downloads/class_name.yaml

    echo -e "${TAG__INFO} Done: ${name__video}"
done