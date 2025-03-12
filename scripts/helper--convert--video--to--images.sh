PATH__DIR__VIDEO=/home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4_5min

PATH__DIR__IMAGE__OUTPUT=/home/laptq/laptq-prj-21/data/Videos--to--frames/241210_受け取り動画/mp4_5min

declare -A MAP__NAME_VIDEO__TO__=(
    # ["Camera_４８/Camera_48_1_2025-01-28_000000.3gp"]=""
    # ["Camera_４８/Camera_48_1_2025-01-31_000000.3gp"]=""
    # ["Camera_４８/Camera_48_1_2025-01-30_000000.3gp"]=""
    # ["Camera_４８/Camera_48_1_2025-01-27_000000.3gp"]=""
    # ["Camera_４８/Camera_48_1_2025-01-29_000000.3gp"]=""
    # ["Camera_４７/Camera_47_1_2025-01-29_000000.3gp"]=""
    # ["Camera_４７/Camera_47_1_2025-01-31_000000.3gp"]=""
    # ["Camera_４７/Camera_47_1_2025-01-30_000000.3gp"]=""
    # ["Camera_４７/Camera_47_1_2025-01-28_000000.3gp"]=""
    # ["Camera_５０/Camera_50_1_2025-01-30_000000.3gp"]=""
    # ["Camera_５０/Camera_50_1_2025-01-31_000000.3gp"]=""
    # ["Camera_５０/Camera_50_1_2025-01-28_000000.3gp"]=""
    # ["Camera_５０/Camera_50_1_2025-01-29_000000.3gp"]=""
    ["Camera_５０/Camera_50_1_2025-01-27_000000.3gp"]=""
    ["Camera_４９/Camera_49_1_2025-01-28_000001.3gp"]=""
    ["Camera_４９/Camera_49_1_2025-01-29_000000.3gp"]=""
    ["Camera_４９/Camera_49_1_2025-01-30_000000.3gp"]=""
    ["Camera_４９/Camera_49_1_2025-01-31_000000.3gp"]=""
    ["Camera_４９/Camera_49_1_2025-01-27_000000.3gp"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


main() {
    local name__video=$1

    path__file__input="${PATH__DIR__VIDEO}/${name__video}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${name__video}/images"

    [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
    mkdir -p "${path__dir__img__output}"

    python3 submodules/laptq_utils/main.py \
        helper__convert__video__to__images \
        --path__file__input "${path__file__input}" \
        --path__dir__img__output "${path__dir__img__output}" \
        --num__pad__0 9
}

export -f main

cleanup() {
    echo "Cleaning up..."
    # Kill background processes if they are still running
    kill $(jobs -p) 2>/dev/null
    echo "All background processes terminated."
}

trap cleanup SIGINT

for name__video in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    main "$name__video" &
done

wait

echo "Done"
