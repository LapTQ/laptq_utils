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

    ["train/fall/Le2i/Coffee_room_01/Videos/video (1).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (2).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (3).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (4).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (5).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (6).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (7).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (8).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (9).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (10).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (11).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (12).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (13).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (14).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (15).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (16).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (17).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (18).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (19).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (20).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (21).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (22).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (23).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (24).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (25).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (26).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (27).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (28).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (29).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (30).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (31).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (32).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (33).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (34).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (35).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (36).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (37).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (38).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (39).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (40).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (41).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (42).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (43).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (44).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (45).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (46).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (47).avi"]=""
    ["train/fall/Le2i/Coffee_room_01/Videos/video (48).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (49).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (50).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (51).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (52).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (53).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (54).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (55).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (56).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (57).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (58).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (59).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (60).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (61).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (62).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (63).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (64).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (65).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (66).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (67).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (68).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (69).avi"]=""
    ["train/fall/Le2i/Coffee_room_02/Videos/video (70).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (1).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (2).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (3).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (4).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (5).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (6).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (7).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (8).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (9).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (10).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (11).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (12).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (13).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (14).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (15).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (16).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (17).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (18).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (19).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (20).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (21).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (22).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (23).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (24).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (25).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (26).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (27).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (28).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (29).avi"]=""
    ["train/fall/Le2i/Home_01/Videos/video (30).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (31).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (32).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (33).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (34).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (35).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (36).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (37).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (38).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (39).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (40).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (41).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (42).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (43).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (44).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (45).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (46).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (47).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (48).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (49).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (50).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (51).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (52).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (53).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (54).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (55).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (56).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (57).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (58).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (59).avi"]=""
    ["train/fall/Le2i/Home_02/Videos/video (60).avi"]=""
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
        --step_size 1 \
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
