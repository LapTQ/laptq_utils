# PATH__DIR__INPUT__1=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN
# PATH__DIR__INPUT__2=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/major_vote_action
PATH__DIR__INPUT__1=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials
PATH__DIR__INPUT__2=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN

PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/concat--videos

[[ -d "$PATH__DIR__OUTPUT" ]] && rm -r "$PATH__DIR__OUTPUT"
mkdir -p "$PATH__DIR__OUTPUT"

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

for name__file in "${!MAP__NAME_VIDEO__TO__[@]}"; do
    path__file__input__1="$PATH__DIR__INPUT__1/$name__file"
    path__file__input__2="$PATH__DIR__INPUT__2/$name__file"
    path__file__output="$PATH__DIR__OUTPUT/$name__file"

    if [[ ! -f "$path__file__input__1" ]]; then
        continue
    fi 
    echo $path__file__input__1
    
    # create output directory
    path__dir__output=$(dirname "$path__file__output")
    [[ -d "$path__dir__output" ]] || mkdir -p "$path__dir__output"

    ffmpeg \
        -i "$path__file__input__1" \
        -i "$path__file__input__2" \
        -filter_complex "[0:v][1:v]hstack=inputs=2" \
        -c:v libx264 -preset ultrafast -crf 18 \
        -y \
        "$path__file__output"
    
    echo "Done: ${name__file}"
done

# -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,scale=iw:ih" \

# to make it fast:
# -c:v libx264 -preset ultrafast -crf 18 \
# compression vs speed options: ultrafast medium low
# lossless level: from 18 (lossless) to 28