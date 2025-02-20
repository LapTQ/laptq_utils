PATH__DIR__VIDEO=/home/laptq/laptq-prj-21/data/video-20250220

PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-21/outputs/20250220--videos-to-frames

declare -A MAP__NAME_VIDEO__TO__=(
    ["Camera_４８/Camera_48_1_2025-01-30_000000.3gp"]=""
    ["Camera_４８/Camera_48_1_2025-01-31_000000.3gp"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__file__input="${PATH__DIR__VIDEO}/${name__video}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${name__video}/images"

    [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
    mkdir -p "${path__dir__img__output}"

    python3 submodules/laptq_utils/main.py \
        helper__convert__video__to__images \
        --path__file__input "${path__file__input}" \
        --path__dir__img__output "${path__dir__img__output}" \
        --num__pad__0 9
        
done