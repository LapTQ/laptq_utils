PATH__DIR__IMG__INPUT=/home/laptq/laptq-prj-44/outputs/20250116--downloaded--beer-meat--dedup
POSTFIX__DIR__IMG=""

PATH__DIR__OUTPUT__META=/home/laptq/laptq-prj-44/outputs/20250116--check-duplicate-images--ver2

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-44/outputs/20250116--downloaded--beer-meat--dedup--ver2
POSTFIX__DIR__IMG__TARGET=""

TO_USE__SOFTLINK="True"

declare -A MAP__SUBPATH_DIR__TO__NEED_TO_CHECK=(
    ["beer"]="True"
    ["meat"]="True"
)


[[ -d "$PATH__DIR__OUTPUT__META" ]] && rm -r "$PATH__DIR__OUTPUT__META"


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# check for duplicate images
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[@]}"; do
    is_need_to_check="${MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[$subpath_dir]}"

    if [[ $is_need_to_check != "True" ]]; then
        continue
    fi 

    path__dir__img="${PATH__DIR__IMG__INPUT}/${subpath_dir}/images${POSTFIX__DIR__IMG}"
    path__dir__output="${PATH__DIR__OUTPUT__META}/${subpath_dir}"

    python3 submodules/laptq_utils/main.py \
        helper__check__duplicate__images \
        --path__dir__img "$path__dir__img" \
        --path__dir__output "$path__dir__output" \
        --method PHash \
        --max_distance_threshold 5 \
        --to__plot True
done


# create new image version
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[@]}"; do
    is_need_to_check="${MAP__SUBPATH_DIR__TO__NEED_TO_CHECK[$subpath_dir]}"
    
    path__dir__img__input="${PATH__DIR__IMG__INPUT}/${subpath_dir}/images${POSTFIX__DIR__IMG}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__IMG__TARGET}"

    [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
    mkdir -p "$path__dir__img__output"

    if [[ $is_need_to_check = "True" ]]; then
        while IFS= read -r name__file__img; do
            name__file__img="${name__file__img%$'\r'}"  # right strip
            name__file__img="${name__file__img%\"}" # right strip
            name__file__img="${name__file__img#\"}" # left strip
            if [[ $TO_USE__SOFTLINK = "True" ]]; then
                ln -s $( realpath "${path__dir__img__input}/${name__file__img}" ) "${path__dir__img__output}"
            else
                cp $( realpath "${path__dir__img__input}/${name__file__img}" ) "${path__dir__img__output}"
            fi
        done < "${PATH__DIR__OUTPUT__META}/${subpath_dir}/originals_to_keep__no_json.txt"
    else
        IFS=$'\n'
        for name__file__img in $( ls "${path__dir__img__input}" ); do
            if [[ $TO_USE__SOFTLINK = "True" ]]; then
                ln -s $( realpath "${path__dir__img__input}/${name__file__img}" ) "${path__dir__img__output}"
            else
                cp $( realpath "${path__dir__img__input}/${name__file__img}" ) "${path__dir__img__output}"
            fi
        done
    fi 

    echo -e "${TAG__INFO} $( ls ${path__dir__img__output} | wc -l )/$( ls ${path__dir__img__input} | wc -l ) original images in ${subpath_dir}"
done

