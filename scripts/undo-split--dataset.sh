PATH__DIR__IMAGE__SOURCE=/home/laptq/laptq-prj-44/outputs/undo-unslashed--subpath-dir--dataset
POSTFIX__DIR__IMG__SOURCE=""

PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-44/outputs/undo-unslashed--subpath-dir--dataset
POSTFIX__DIR__LABEL__SOURCE=""

PATH__DIR__DATASETS__OUTPUT=/home/laptq/laptq-prj-44/outputs/undo-split--dataset
POSTFIX__DIR__VERSION__TARGET=""

POSTFIX__DIR__SPLITTED='-batch-'


declare -A MAP__SUBPATH_DIR__TO__=(
    ["customer/train"]=""
    ["customer/val"]=""
    ["private/train"]=""
    ["private/val"]=""
    ["private/test"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/images${POSTFIX__DIR__VERSION__TARGET}"
    path__dir__lbl__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}/labels${POSTFIX__DIR__VERSION__TARGET}"

    [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
    [[ -d "$path__dir__lbl__output" ]] && rm -r "$path__dir__lbl__output"
    mkdir -p "$path__dir__img__output"
    mkdir -p "$path__dir__lbl__output"

    sum__num__file__img=0
    sum__num__file__lbl=0

    subpath_dir_parent=${subpath_dir%/*}
    namef_dir="${subpath_dir##*/}"

    if [[ $( ls "${PATH__DIR__IMAGE__SOURCE}/${subpath_dir_parent}" | grep "${namef_dir}${POSTFIX__DIR__SPLITTED}" | wc -l ) -eq 0 ]]; then
        path__dir__img__input="${PATH__DIR__IMAGE__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
        path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"

        # check if the input directories exist
        if [[ ! -d "${path__dir__img__input}" ]]; then
            echo -e "${TAG__FAILED} missed images: ${subpath_dir}. Skipping or exiting..."
            
            exit 1
            # continue
        fi
        if [[ ! -d "${path__dir__lbl__input}" ]]; then
            echo -e "${TAG__FAILED} missed labels: ${subpath_dir}. Skipping or exiting..."
            
            exit 1
            # continue
        fi

        cp -r "${path__dir__img__input}"/* "${path__dir__img__output}"
        cp -r "${path__dir__lbl__input}"/* "${path__dir__lbl__output}"


        sum__num__file__img=$(find "${path__dir__img__input}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
        sum__num__file__lbl=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    else
        for namef_dir__child in $( ls "${PATH__DIR__IMAGE__SOURCE}/${subpath_dir_parent}" | grep "${namef_dir}${POSTFIX__DIR__SPLITTED}" ); do
            subpath_dir__child=${subpath_dir_parent}/${namef_dir__child}

            path__dir__img__input="${PATH__DIR__IMAGE__SOURCE}/${subpath_dir__child}/images${POSTFIX__DIR__IMG__SOURCE}"
            path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir__child}/labels${POSTFIX__DIR__LABEL__SOURCE}"

            # check if the input directories exist
            if [[ ! -d "${path__dir__img__input}" ]]; then
                echo -e "${TAG__FAILED} missed images: ${subpath_dir__child}. Skipping or exiting..."
                
                exit 1
                # continue
            fi
            if [[ ! -d "${path__dir__lbl__input}" ]]; then
                echo -e "${TAG__FAILED} missed labels: ${subpath_dir__child}. Skipping or exiting..."
                
                exit 1
                # continue
            fi
            cp -r "${path__dir__img__input}"/* "${path__dir__img__output}"
            cp -r "${path__dir__lbl__input}"/* "${path__dir__lbl__output}"


            num__file__img=$(find "${path__dir__img__input}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
            num__file__lbl=$(find "${path__dir__lbl__input}/" -mindepth 1 -maxdepth 1 -type f | wc -l)

            sum__num__file__img=$((sum__num__file__img + num__file__img))
            sum__num__file__lbl=$((sum__num__file__lbl + num__file__lbl))
        done
    fi

    num__file__img=$(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l)
    num__file__lbl=$(find "${path__dir__lbl__output}/" -mindepth 1 -maxdepth 1 -type f | wc -l)
    if [[ $num__file__img -eq $sum__num__file__img ]]; then
        echo -e "${TAG__PASSED} ${sum__num__file__img} summed images == ${num__file__img} target images: ${subpath_dir}"
    else
        echo -e "${TAG__FAILED} ${sum__num__file__img} summed images != ${num__file__img} target images: ${subpath_dir}"
        exit 1
    fi
    if [[ $num__file__lbl -eq $sum__num__file__lbl ]]; then
        echo -e "${TAG__PASSED} ${sum__num__file__lbl} summed labels == ${num__file__lbl} target labels: ${subpath_dir}"
    else
        echo -e "${TAG__FAILED} ${sum__num__file__lbl} summed labels != ${num__file__lbl} target labels: ${subpath_dir}"
        exit 1
    fi

done