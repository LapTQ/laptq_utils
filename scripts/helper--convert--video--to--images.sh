# PATH__DIR__VIDEO=/home/laptq/laptq-fs26-shoplifting-detection/data
# PATH__DIR__VIDEO=/mnt/ssd2/shared_workspace/cuongdh/FSPRJ26/data/250516
# PATH__DIR__VIDEO=/mnt/ssd2/shared_workspace/cuongdh/FSPRJ26/data/250516/rotate
PATH__DIR__VIDEO=/mnt/ssd2/shared_workspace/prj54_fall_violence_detection/dataset

# PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images
PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images/fall_violence


declare -A MAP__SUBPATH_VIDEO__TO__=(
    # ["shoplifting-25min.mp4"]=""
    # ["satudora-1min.mp4"]=""
    # ["1568080723085_67014_fix.mkv"]=""
    # ["shoplifting-1min_anonymized.mp4"]=""
    # ["r10_10min_rotate.mp4"]=""
    # ["r9_25min_rotate.mp4"]=""
    # ["R10_2025_05_15_23_40_32_rotate.mp4"]=""
    
    # ["test/fall/Fall_1.mp4"]=""
    # ["test/fall/Fall_2.mp4"]=""
    # ["test/violence/Violence_1.mp4"]=""
    ["test/fall/Falling_and_Slow_Falling.mp4"]=""
    ["test/violence/Fighting_1.mp4"]=""
    ["test/violence/Fighting_2.mp4"]=""
    ["test/violence/Fighting_3.mp4"]=""
    ["test/violence/Fighting_4.mp4"]=""
)
# source /home/laptq/laptq-fs26-shoplifting-detection/data/shoplifting-gen-video-paths.sh

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


main() {
    local subpath__video=$1

    path__file__input="${PATH__DIR__VIDEO}/${subpath__video}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${subpath__video}/images"

    [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
    mkdir -p "${path__dir__img__output}"

    python3 submodules/laptq_utils/main.py \
        helper__convert__video__to__images \
        --path__file__input "${path__file__input}" \
        --path__dir__img__output "${path__dir__img__output}" \
        --step_size 2 \
        --num__pad__0 9

    echo -e "${TAG__INFO} Done: ${subpath__video}"
}

# ============= if parallel ================
# export -f main

# cleanup() {
#     echo "Cleaning up..."
#     # Kill background processes if they are still running
#     kill $(jobs -p) 2>/dev/null
#     echo "All background processes terminated."
# }

# trap cleanup SIGINT

# for subpath__video in "${!MAP__SUBPATH_VIDEO__TO__[@]}"; do
#     main "$subpath__video" &
# done

# wait

# ==========================================

# ============= if sequentially ============
for subpath__video in "${!MAP__SUBPATH_VIDEO__TO__[@]}"; do
    main "$subpath__video"
done
# ==========================================


echo "Done"
