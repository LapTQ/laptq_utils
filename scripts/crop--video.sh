

ffmpeg \
    -i /mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos/00000064_2401230859_NR.MP4 \
    -vf "crop=1420:630:450:250" \
    -c:v libx264 -preset ultrafast -crf 0 -c:a copy \
    -y \
    /mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos--cropped/00000064_2401230859_NR.MP4

# -vf "crop=out_width:out_height:x:y" \