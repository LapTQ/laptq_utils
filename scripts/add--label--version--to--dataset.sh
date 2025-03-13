PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-21/outputs/20250310--labels
POSTFIX__DIR__LABEL__SOURCE="--erase-ignored"

PATH__DIR__DATASETS__SOURCE=/home/laptq/laptq-prj-21/outputs/20250310--labels
POSTFIX__DIR__IMG__SOURCE="--erase-ignored"

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/data/fs_prj21/datasets/20250303--phase2--4cam-factory
POSTFIX__DIR__VERSION__TARGET="--erase-ignored"


declare -A MAP__SUBPATH_DIR__TO__=(
    ["Camera_47/Camera_47_1_2025-01-30_000000.3gp"]=""
    ["Camera_48/Camera_48_1_2025-01-30_000000.3gp"]=""
    ["Camera_49/Camera_49_1_2025-01-30_000000.3gp"]=""
    ["Camera_50/Camera_50_1_2025-01-30_000000.3gp"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


# =========== Copy labels from extracted annotation to source dataset dir ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"
    path__dir__lbl__output="${PATH__DIR__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$path__dir__lbl__output" ]] && rm -r "$path__dir__lbl__output"
    mkdir -p "$path__dir__lbl__output"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl__input" ]]; then
            continue
        fi
        cp "$path__file__lbl__input" "$path__dir__lbl__output"
    done

    num__lbl__input=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__lbl__output=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [ $num__lbl__input -lt $num__lbl__output ]; then
        echo -e "${TAG__FAILED} Number of labels in the extracted annotation and number of labels copied mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl__input labels in the extracted annotation"
        echo "    [+] $num__lbl__output labels in the copied folder"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Copied ${num__lbl__input} labels to ${num__lbl__output} labels: ${subpath_dir}"
done


# =========== Create a soft link to images corresponding to the label version ===========
for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__lbl="${PATH__DIR__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__img__output="${PATH__DIR__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
    mkdir -p "$path__dir__img__output"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        name__file__lbl=${name__file__img%.*}.txt
        path__file__lbl="${path__dir__lbl}/${name__file__lbl}"
        if [[ ! -f "$path__file__lbl" ]]; then
            continue
        fi
        ln -s $( realpath "$path__dir__img__input/$name__file__img" ) "$path__dir__img__output"
        # cp $( realpath "$path__dir__img__input/$name__file__img" ) "$path__dir__img__output"
    done

    num__lbl=$(find "${path__dir__lbl}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    num__img=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    if [ $num__lbl -ne $num__img ]; then
        echo -e "${TAG__FAILED} Number of labels and images mismatched: ${subpath_dir}"
        echo "    [+] $num__lbl labels"
        echo "    [+] $num__img images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} Linked ${num__img} images corresponding to ${num__lbl} labels: ${subpath_dir}"
done