PATH__DIR__ANNOT__DOWNLOADED_ZIP="/home/laptq/laptq-prj-44/outputs/20250217--downloaded-annotations"

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-44/outputs/20250217--downloaded-annotations--extracted
POSTFIX__DIR__LABEL__OUTPUT="--raw"

SUBPATH_TEMP=temp
PATH__DIR__OUTPUT__TEMP="${PATH__DIR__OUTPUT}-${SUBPATH_TEMP}"
SUBPATH_STRIP=obj_train_data/P44-20250211

# [[ -d $PATH__DIR__OUTPUT ]] && rm -r $PATH__DIR__OUTPUT
mkdir -p $PATH__DIR__OUTPUT
# [[ -d $PATH__DIR__OUTPUT__TEMP ]] && rm -r $PATH__DIR__OUTPUT__TEMP
mkdir -p $PATH__DIR__OUTPUT__TEMP


declare -A MAP__SUBPATH_DIR__TO__=(
    ["P44-20250211-batch-24"]=""
    ["P44-20250211-batch-25"]=""
    ["P44-20250211-batch-26"]=""
    ["P44-20250211-batch-27"]=""
    ["P44-20250211-batch-28"]=""
    ["P44-20250211-batch-29"]=""
    ["P44-20250211-batch-30"]=""
    ["P44-20250211-batch-31"]=""
    ["P44-20250211-batch-32"]=""
    ["P44-20250211-batch-33"]=""
    ["P44-20250211-batch-34"]=""
    ["P44-20250211-batch-35"]=""
    ["P44-20250211-batch-36"]=""
    ["P44-20250211-batch-37"]=""
    ["P44-20250211-batch-38"]=""
    ["P44-20250211-batch-39"]=""
    ["P44-20250211-batch-40"]=""
    ["P44-20250211-batch-41"]=""
    ["P44-20250211-batch-42"]=""
    ["P44-20250211-batch-43"]=""
    ["P44-20250211-batch-44"]=""
    ["P44-20250211-batch-45"]=""
    ["P44-20250211-batch-46"]=""
    ["P44-20250211-batch-47"]=""
    ["P44-20250211-batch-48"]=""
)


IFS=$'\n'
TAG__FAILED="\033[31m[FAILED]\033[0m"
TAG__PASSED="\033[92m[PASSED]\033[0m"
TAG__INFO="\033[94m[INFO]\033[0m"
TAG__WARNING="\033[33m[WARNING]\033[0m"



IFS=$'\n'
for name__file__zip in $( ls $PATH__DIR__ANNOT__DOWNLOADED_ZIP | grep .zip ); do
    file__file__zip="${PATH__DIR__ANNOT__DOWNLOADED_ZIP}/${name__file__zip}"
    name__dir__extracted=$( echo $name__file__zip | sed 's/.zip$//' )
    path__dir__extracted="${PATH__DIR__OUTPUT__TEMP}/${name__dir__extracted}"
    
    unzip -q $file__file__zip -d $path__dir__extracted
    status=$?

    if [ $status -ne 0 ]; then
        echo -e "${TAG__FAILED} Failed: ${name__file__zip}"
        exit 1
    fi

    # the $path__dir__extracted/$SUBPATH_STRIP/ contains only 1 subfolder, so assert that and store the subfolder name to $name__dir__output
    num__subdir=$( ls -l $path__dir__extracted/$SUBPATH_STRIP | grep ^d | wc -l )
    if [ $num__subdir -ne 1 ]; then
        echo -e "${TAG__FAILED} Failed: There are $num__subdir subfolders in $path__dir__extracted/$SUBPATH_STRIP. Expecting 1."
        exit 1
    fi
    name__dir__output=$( ls $path__dir__extracted/$SUBPATH_STRIP )

    path__dir__input="$path__dir__extracted/$SUBPATH_STRIP/$name__dir__output"
    
    # skip if name__dir__output is not a "key" in MAP__SUBPATH_DIR__TO__ (a key might be mapped to an empty string)
    if [[ -z "${MAP__SUBPATH_DIR__TO__[$name__dir__output]}" && ! ${MAP__SUBPATH_DIR__TO__[$name__dir__output]+_} ]]; then
        echo -e "${TAG__WARNING} Skipping the extracted ${path__dir__input}: not contains a key in MAP__SUBPATH_DIR__TO__"
        continue
    fi

    path__dir__output="$PATH__DIR__OUTPUT/$name__dir__output/labels${POSTFIX__DIR__LABEL__OUTPUT}"
    
    [[ -d $path__dir__output ]] && rm -r $path__dir__output
    mkdir -p $path__dir__output
    
    mv $path__dir__input/* $path__dir__output

    echo -e "${TAG__PASSED} Done: ${name__file__zip} -> ${name__dir__output}"
done

rm -r $PATH__DIR__OUTPUT__TEMP

