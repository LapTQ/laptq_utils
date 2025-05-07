PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/STGCN/predict/20250505-000000--TSSTG_HO--2-kpt-channels--match-MrCuong-train-test-split
# PATH__DIR__IMAGE__INPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/major_vote_action/20250505-000000--TSSTG_HO--2-kpt-channels--match-MrCuong-train-test-split
POSTFIX__DIR__IMAGE=""

PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN
# PATH__DIR__VIDEO__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/major_vote_action

declare -A MAP__NAME_VIDEO__TO__=(
    # ["Normal/Normal__66_.mp4"]=""
    # ["Normal/Normal__67_.mp4"]=""
    # ["Normal/Normal__68_.mp4"]=""
    # ["Normal/Normal__69_.mp4"]=""
    # ["Normal/Normal__6_.mp4"]=""
    # ["Normal/Normal__70_.mp4"]=""
    # ["Normal/Normal__71_.mp4"]=""
    # ["Normal/Normal__72_.mp4"]=""
    # ["Normal/Normal__73_.mp4"]=""
    # ["Normal/Normal__74_.mp4"]=""
    # ["Normal/Normal__75_.mp4"]=""
    # ["Normal/Normal__76_.mp4"]=""
    # ["Normal/Normal__77_.mp4"]=""
    # ["Normal/Normal__78_.mp4"]=""
    # ["Normal/Normal__79_.mp4"]=""
    # ["Normal/Normal__7_.mp4"]=""
    # ["Normal/Normal__80_.mp4"]=""
    # ["Normal/Normal__81_.mp4"]=""
    # ["Normal/Normal__82_.mp4"]=""
    # ["Normal/Normal__83_.mp4"]=""
    # ["Normal/Normal__84_.mp4"]=""
    # ["Normal/Normal__85_.mp4"]=""
    # ["Normal/Normal__86_.mp4"]=""
    # ["Normal/Normal__87_.mp4"]=""
    # ["Normal/Normal__88_.mp4"]=""
    # ["Normal/Normal__89_.mp4"]=""
    # ["Normal/Normal__8_.mp4"]=""
    # ["Normal/Normal__90_.mp4"]=""
    # ["Normal/Normal__9_.mp4"]=""
    # ["Shoplifting/Shoplifting__67_.mp4"]=""
    # ["Shoplifting/Shoplifting__68_.mp4"]=""
    # ["Shoplifting/Shoplifting__69_.mp4"]=""
    # ["Shoplifting/Shoplifting__6_.mp4"]=""
    # ["Shoplifting/Shoplifting__70_.mp4"]=""
    # ["Shoplifting/Shoplifting__71_.mp4"]=""
    # ["Shoplifting/Shoplifting__72_.mp4"]=""
    # ["Shoplifting/Shoplifting__73_.mp4"]=""
    # ["Shoplifting/Shoplifting__74_.mp4"]=""
    # ["Shoplifting/Shoplifting__75_.mp4"]=""
    # ["Shoplifting/Shoplifting__76_.mp4"]=""
    # ["Shoplifting/Shoplifting__77_.mp4"]=""
    # ["Shoplifting/Shoplifting__78_.mp4"]=""
    # ["Shoplifting/Shoplifting__79_.mp4"]=""
    # ["Shoplifting/Shoplifting__7_.mp4"]=""
    # ["Shoplifting/Shoplifting__80_.mp4"]=""
    # ["Shoplifting/Shoplifting__81_.mp4"]=""
    # ["Shoplifting/Shoplifting__82_.mp4"]=""
    # ["Shoplifting/Shoplifting__83_.mp4"]=""
    # ["Shoplifting/Shoplifting__84_.mp4"]=""
    # ["Shoplifting/Shoplifting__85_.mp4"]=""
    # ["Shoplifting/Shoplifting__86_.mp4"]=""
    # ["Shoplifting/Shoplifting__87_.mp4"]=""
    # ["Shoplifting/Shoplifting__88_.mp4"]=""
    # ["Shoplifting/Shoplifting__89_.mp4"]=""
    # ["Shoplifting/Shoplifting__8_.mp4"]=""
    # ["Shoplifting/Shoplifting__90_.mp4"]=""
    # ["Shoplifting/Shoplifting__91_.mp4"]=""
    # ["Shoplifting/Shoplifting__92_.mp4"]=""
    # ["Shoplifting/Shoplifting__93_.mp4"]=""
    # ["Shoplifting/Shoplifting__9_.mp4"]=""
    
    ["shoplifting-25min.mp4"]=""
    # ["satudora-1min.mp4"]=""
)

# [[ -d "${PATH__DIR__VIDEO__OUTPUT}" ]] && rm -r "${PATH__DIR__VIDEO__OUTPUT}"
mkdir -p "${PATH__DIR__VIDEO__OUTPUT}"

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${name__video}/vis${POSTFIX__DIR__IMAGE}"
    path__file__output="${PATH__DIR__VIDEO__OUTPUT}/${name__video}"

    # make parent output dir
    mkdir -p "$(dirname "$path__file__output")"

    ffmpeg \
        -framerate 15 \
        -c:v libx264 \
        -y \
        -pix_fmt yuv420p \
        "$path__file__output" \
        -pattern_type glob -i "${path__dir__img__input}/*.jpg"
        # -i "${path__dir__img__input}/%09d.jpg" \
    
    echo -e "${TAG__INFO} Done: ${name__video}"
done

# # Glob options
# -pattern_type glob -i "${path__dir__img__input}/*.jpg"
# -i "${path__dir__img__input}/%09d.jpg"