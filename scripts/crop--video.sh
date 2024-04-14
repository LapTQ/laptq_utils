PATH__DIR__INPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos
PATH__DIR__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos--cropped

pct__crop__top=0.5
pct__crop__bottom=0
pct__crop__left=0.2
pct__crop__right=0.2


IFS=$'\n'
for name__file in $( ls $PATH__DIR__INPUT ); do
    path__file__input=$( realpath "$PATH__DIR__INPUT/$name__file" )
    path__file__output="$PATH__DIR__OUTPUT/$name__file"

    IFS=$',' read width height < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$path__file__input")
    IFS=$'\n'

    x1=$(echo "$width * $pct__crop__left / 1" | bc)
    y1=$(echo "$height * $pct__crop__top / 1" | bc)
    x2=$(echo "$width * ( 1 - $pct__crop__right ) / 1" | bc)
    y2=$(echo "$height * ( 1 - $pct__crop__bottom ) / 1" | bc)
    w=$(echo "$x2 - $x1" | bc)
    h=$(echo "$y2 - $y1" | bc)

    ffmpeg \
        -i "$path__file__input" \
        -vf "crop=$w:$h:$x1:$y1" \
        -c:v libx264 -preset ultrafast -crf 0 -c:a copy \
        -y \
        "$path__file__output"
done

# -vf "crop=out_width:out_height:x:y" \