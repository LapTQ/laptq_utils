PATH__DIR__INPUT__1=/home/laptq/laptq-prj-21/runs/data--synthetic/yolo11s--832--scale-0.5--multiscale-True/predict--train--imgsz-832--conf-0.1/predict/draw--video
PATH__DIR__INPUT__2=/home/laptq/laptq-prj-21/runs/data--synthetic/yolo11s--832--scale-0.5--multiscale-True/predict--train2--imgsz-832--conf-0.1/predict/draw--video

PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/outputs/trivial

[[ -d "$PATH__DIR__OUTPUT" ]] && rm -r "$PATH__DIR__OUTPUT"
mkdir -p "$PATH__DIR__OUTPUT"


for name__file in $( ls "$PATH__DIR__INPUT__1" ); do
    path__file__input__1="$PATH__DIR__INPUT__1/$name__file"
    path__file__input__2="$PATH__DIR__INPUT__2/$name__file"
    path__file__output="$PATH__DIR__OUTPUT/$name__file"

    # if [[ ! -f "$path__file__input__1" ]]; then
    #     continue
    # fi 

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