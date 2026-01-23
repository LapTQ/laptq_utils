PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict/20250505-000000--TSSTG_HO--2-kpt-channels--match-MrCuong-train-test-split
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/20250505-000000--TSSTG_HO--2-kpt-channels--match-MrCuong-train-test-split
POSTFIX__DIR__IMAGE=""

PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/major_vote_action

declare -A MAP__NAME_VIDEO__TO__=(
    ["shoplifting-25min.mp4"]=30
    ["r9_25min_rotate.mp4"]=15
    # ["satudora-1min.mp4"]=""
)

# [[ -d "${PATH__DIR__VIDEO__OUTPUT}" ]] && rm -r "${PATH__DIR__VIDEO__OUTPUT}"
mkdir -p "${PATH__DIR__VIDEO__OUTPUT}"

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


main() {
    local name__video=$1
    local fps=$2

    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${name__video}/vis${POSTFIX__DIR__IMAGE}"
    path__file__output="${PATH__DIR__VIDEO__OUTPUT}/${name__video}"

    # make parent output dir
    mkdir -p "$(dirname "$path__file__output")"

    ffmpeg \
        -framerate $fps \
        -pattern_type glob -i "${path__dir__img__input}/*.jpg" \
        -c:v libx264 \
        -y \
        -pix_fmt yuv420p \
        "$path__file__output" \
        # -i "${path__dir__img__input}/%09d.jpg" \
    
    echo -e "${TAG__INFO} Done: ${name__video}"
}


# ============= if parallel ================
export -f main

cleanup() {
    echo "Cleaning up..."
    # Kill background processes if they are still running
    kill $(jobs -p) 2>/dev/null
    echo "All background processes terminated."
}

trap cleanup SIGINT

for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    fps="${MAP__NAME_VIDEO__TO__[$name__video]}"
    main "$name__video" $fps &
done

wait

# ==========================================

# ============= if sequentially ============
# for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
#     main "$name__video"
# done
# ==========================================


# # Glob options
# -pattern_type glob -i "${path__dir__img__input}/*.jpg"
# -i "${path__dir__img__input}/%09d.jpg"