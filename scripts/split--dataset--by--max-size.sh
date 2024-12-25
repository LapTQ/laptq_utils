PATH__DIR__DATASETS__SOURCE=/home/laptq/laptq-prj-44/outputs/20241217--cleaned--dataset
POSTFIX__DIR__IMG__SOURCE="--raw"

PATH__DIR__LABEL__SOURCE=/home/laptq/laptq-prj-44/outputs/20241217--cleaned--dataset
POSTFIX__DIR__LABEL__SOURCE="--raw"

PATH__DIR__DATASETS__OUTPUT=/home/laptq/laptq-prj-44/outputs/20241217--cleaned--dataset--splitted
POSTFIX__DIR__VERSION__TARGET="--raw"

TO__SHUFFLE=True
SEED=42

SIZE__MAX=400
POSTFIX__DIR__SPLITTED='-batch-'


declare -A MAP__SUBPATH_DIR__TO__=(
    ["PoC2--2個持ち_cut_fit-1products"]=""
    ["PoC2--2個持ち_cut_fit-2products"]=""
    ["PoC2--2個持ち_cut_fit-nothing"]=""
    ["PoC2--2個持ち_cut_fit-notProducts"]=""
    ["PoC2--bag20240906_0000-notProducts"]=""
    ["PoC2--bag20240906_1022-notProducts"]=""
    ["PoC1--beppu_sue"]=""
    ["PoC2--beppu_sue"]=""
    ["PoC2--台置き_cut_fit-1products"]=""
    ["PoC2--台置き_cut_fit-2products"]=""
    ["PoC2--台置き_cut_fit-nothing"]=""
    ["PoC2--台置き_cut_fit-notProducts"]=""
)


########################################################################################################################################################


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"


for subpath_dir in "${!MAP__SUBPATH_DIR__TO__[@]}"; do
    path__dir__img__input="${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/images${POSTFIX__DIR__IMG__SOURCE}"
    path__dir__lbl__input="${PATH__DIR__LABEL__SOURCE}/${subpath_dir}/labels${POSTFIX__DIR__LABEL__SOURCE}"


    num__file__img=$( ls "${path__dir__img__input}" | wc -l )
    num__file__lbl=$( ls "${path__dir__lbl__input}" | wc -l )

    if [[ $num__file__img -ne $num__file__lbl ]]; then
        echo -e "${TAG__FAILED} $subpath_dir: number of images and labels are not equal"
        exit 1
    fi

    num__dir__splitted=$(( $num__file__img / $SIZE__MAX ))
    num__remain=$(( $num__file__img % $SIZE__MAX ))
    if [[ $num__remain -ne 0 ]]; then
        num__dir__splitted=$(( $num__dir__splitted + 1 ))
    fi
    list__name__file__img=($( ls "$path__dir__img__input" | sort -V ))

    if [[ $TO__SHUFFLE == True ]]; then
        list__name__file__img=($(printf "%s\n" "${list__name__file__img[@]}" | shuf -n ${#list__name__file__img[@]} --random-source=<(openssl enc -aes-256-ctr -pass pass:"$SEED" -nosalt < /dev/zero 2>/dev/null)))
    fi

    sum__num__file__splitted=0
    for id__batch in $(seq 1 $num__dir__splitted); do
        if [[ $num__dir__splitted -eq 1 ]]; then
            postfix=""
        else
            postfix=${POSTFIX__DIR__SPLITTED}${id__batch}
        fi
        path__dir__img__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}${postfix}/images${POSTFIX__DIR__VERSION__TARGET}"
        path__dir__lbl__output="${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}${postfix}/labels${POSTFIX__DIR__VERSION__TARGET}"

        [[ -d "$path__dir__img__output" ]] && rm -r "$path__dir__img__output"
        [[ -d "$path__dir__lbl__output" ]] && rm -r "$path__dir__lbl__output"
        mkdir -p "$path__dir__img__output"
        mkdir -p "$path__dir__lbl__output"

        idx__img__start=$(( $SIZE__MAX * ( $id__batch - 1 ) ))
        if [[ $id__batch -eq $num__dir__splitted ]]; then
            idx__img__end=$(( $num__file__img - 1 ))
        else
            idx__img__end=$(( $SIZE__MAX * $id__batch - 1 ))
        fi

        for idx__img in $(seq $idx__img__start $idx__img__end); do
            name__file__img=${list__name__file__img[$idx__img]}
            name__file__lbl=${name__file__img%.*}.txt
            path__file__img__input=$( realpath "$path__dir__img__input/$name__file__img" )
            path__file__lbl__input="${path__dir__lbl__input}/${name__file__lbl}"

            cp "$path__file__img__input" "$path__dir__img__output"

            # choose either
            # touch "${path__dir__lbl__output}/${name__file__lbl}"
            cp "$path__file__lbl__input" "$path__dir__lbl__output"
        done
        # cp "${PATH__DIR__DATASETS__SOURCE}/${subpath_dir}/classes.txt" "${PATH__DIR__DATASETS__OUTPUT}/${subpath_dir}${postfix}/"

        sum__num__file__splitted=$(( $sum__num__file__splitted + $(find "${path__dir__img__output}/" -mindepth 1 -maxdepth 1 \( -type f -o -type l \) | wc -l) ))

    done

    if [[ $sum__num__file__splitted -ne $num__file__img ]]; then
        echo -e "${TAG__FAILED} Number of images mismatched: ${subpath_dir}"
        echo "    [+] ${num__file__img} source images"
        echo "    [+] ${sum__num__file__splitted} splitted images"

        exit 1
    else
        echo -e "${TAG__PASSED} ${num__file__img} source images == ${sum__num__file__splitted} target images: ${subpath_dir}"
    fi

done