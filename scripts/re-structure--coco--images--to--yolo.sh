PATH__DIR__IMAGE__INPUT=/home/pocuser2/datasets/coco

PATH__DIR__IMAGE__OUTPUT=/home/pocuser2/datasets/coco/restructured
POSTFIX__DIR__IMAGE__OUTPUT=""


declare -A MAP__SUBPATH_DIR__TO__=(
    ["train2017"]=""
    ["val2017"]=""
    # ["test"]=""
)

IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath__dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__IMAGE__INPUT}/${subpath__dir}"
    path__dir__img__output="${PATH__DIR__IMAGE__OUTPUT}/${subpath__dir}/images${POSTFIX__DIR__IMAGE__OUTPUT}"

    [[ -d "${path__dir__img__output}" ]] && rm -r "${path__dir__img__output}"
    mkdir -p "${path__dir__img__output}"

    for name__file__img in $( ls "${path__dir__img__input}" ); do
        path__file__img__input="${path__dir__img__input}/${name__file__img}"
        ln -s $( realpath ${path__file__img__input} ) "${path__dir__img__output}/"
    done


    num__img__input=$(find "${path__dir__img__input}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    num__img__output=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    if [ $num__img__output -ne $num__img__input ]; then
        echo -e "${TAG__FAILED} Number of images mismatched: ${subpath__dir}"
        echo "    [+] $num__img__input source images"
        echo "    [+] $num__img__output target images"
        
        exit 1
    fi
    echo -e "${TAG__PASSED} ${num__img__input} source images == ${num__img__output} target images: ${subpath__dir}"

done