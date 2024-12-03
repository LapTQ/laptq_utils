PATH__DIR__INPUT__1=/Users/user/Downloads/old-pipeline
PATH__DIR__INPUT__2=/Users/user/Downloads/new-pipeline

PATH__DIR__OUTPUT=/Users/user/Downloads/20241202--yolo--prediction--merged

rm -r "$PATH__DIR__OUTPUT" && mkdir -p "$PATH__DIR__OUTPUT"

for name__file in $( ls "$PATH__DIR__INPUT__1" ); do
    path__file__input__1="$PATH__DIR__INPUT__1/$name__file"
    path__file__input__2="$PATH__DIR__INPUT__2/$name__file"
    path__file__output="$PATH__DIR__OUTPUT/$name__file"

    ffmpeg \
        -i "$path__file__input__1" \
        -i "$path__file__input__2" \
        -filter_complex "[0:v][1:v]hstack=inputs=2" \
        -y \
        "$path__file__output"
done

# -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,scale=iw:ih" \