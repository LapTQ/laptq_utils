PATH__DIR__INPUT=/home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4_5min
PATH__DIR__OUTPUT=/home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4_5min--cropped-10-pct

pct__crop__top=0.1
pct__crop__bottom=0.1
pct__crop__left=0.1
pct__crop__right=0.1

[[ -d "$PATH__DIR__OUTPUT" ]] && rm -r "$PATH__DIR__OUTPUT"
mkdir -p "$PATH__DIR__OUTPUT"


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
        -c:v libx264 -preset ultrafast -crf 18 -c:a copy \
        -y \
        "$path__file__output"
done

# -vf "crop=out_width:out_height:x:y" \