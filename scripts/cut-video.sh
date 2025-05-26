ffmpeg \
    -i /home/laptq/laptq-fs26-shoplifting-detection/outputs/crop--videos/shoplifting-25min--compr.mp4 \
    -ss 00:00:00 \
    -to 00:01:00 \
    -c copy \
    -y \
    /home/laptq/laptq-fs26-shoplifting-detection/outputs/shoplifting-1min.mp4