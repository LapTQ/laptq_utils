# PATH__DIR__INPUT__1=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/STGCN
# PATH__DIR__INPUT__2=/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--images--to--video/major_vote_action
PATH__DIR__INPUT__1=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials/1
PATH__DIR__INPUT__2=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials/2

PATH__DIR__OUTPUT=/home/laptq/laptq-fs26-shoplifting-detection/outputs/concat--videos

[[ -d "$PATH__DIR__OUTPUT" ]] && rm -r "$PATH__DIR__OUTPUT"
mkdir -p "$PATH__DIR__OUTPUT"

declare -A MAP__NAME_VIDEO__TO__=(
    
    ["fall_violence/test/fall/Fall_1.mp4"]=""
    ["fall_violence/test/fall/Fall_2.mp4"]=""
    ["fall_violence/test/violence/Violence_1.mp4"]=""
    
    # ["shoplifting-25min.mp4"]=""
    # ["r10_10min_rotate.mp4"]=""
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
        # -i "$path__file__input__3" \
        # -i "$path__file__input__4" \
    
    echo "Done: ${name__file}"
done

# -filter_complex "[0:v][1:v]hstack=inputs=2" \
# -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,scale=iw:ih" \
# -filter_complex "\
#             [0:v][1:v]hstack=inputs=2[top]; \
#             [2:v][3:v]hstack=inputs=2[bottom]; \
#             [top][bottom]vstack=inputs=2" \

# to make it fast:
# -c:v libx264 -preset ultrafast -crf 18 \
# compression vs speed options: ultrafast medium low
# lossless level: from 18 (lossless) to 28