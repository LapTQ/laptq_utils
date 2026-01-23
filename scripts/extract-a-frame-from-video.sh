PATHD_VIDEO=/mnt/ssd2/shared_workspace/cuongdh/FSPRJ26/data/250516/rotate
PATHD_OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/extract-a-frame-from-video

declare -A MAP_SUBPATHF_TO_=(
    ["R7_2025_05_15_23_40_32_rotate.mp4"]=""
    ["R8_2025_05_15_23_40_32_rotate.mp4"]=""
    ["R3_2025_05_15_23_40_32_rotate.mp4"]=""
    ["R4_2025_05_15_23_40_32_rotate.mp4"]=""
    ["R9_2025_05_15_23_40_32_rotate.mp4"]=""
    ["R10_2025_05_15_23_40_32_rotate.mp4"]=""
)

mkdir -p "$PATHD_OUTPUT"

for subpathf in "${!MAP_SUBPATHF_TO_[@]}"; do
    pathf_video="${PATHD_VIDEO}/${subpathf}"
    pathf_output="${PATHD_OUTPUT}/${subpathf}.jpg"

    ffmpeg \
        -ss 00:00:05.000 \
        -i "$pathf_video" \
        -vframes 1 \
        "$pathf_output"
done