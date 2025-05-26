

yolo track \
    source=/home/laptq/laptq-fs26-shoplifting-detection/data/mendeley/Dataset/Shoplifting/Shoplifting__2_.mp4 \
    model=yolov8n-pose.pt \
    project=/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials \
    imgsz=640 \
    conf=0.2 \
    device=1 \
    save_frames=True \
    save_txt=True \
    save_conf=True \
    save_crop=True \
