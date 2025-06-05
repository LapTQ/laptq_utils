ffmpeg \
    -i /mnt/ssd2/shared_workspace/cuongdh/FSPRJ26/data/250516/rotate/R7_2025_05_15_23_40_32_rotate.mp4 \
    -ss 00:00:00 \
    -to 00:01:00 \
    -c copy \
    -y \
    /home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials/output.mp4