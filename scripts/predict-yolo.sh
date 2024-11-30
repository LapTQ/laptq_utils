path__dir__run=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs

data=20241122--phase-2--annotation-ver2

# ver__model=yolo11m--960--full
# imgsz=960
ver__model=yolo11m--640--crop
imgsz=640
# ver__model=yolo11s--960--crop
# imgsz=960

ver__train=train
conf=0.2

yolo predict \
    model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    source=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos--cropped/00000064_2401230859_NR.MP4 \
    imgsz=$imgsz \
    conf=$conf \
    device=1 \
    project=$path__dir__run/$data/${ver__model}/predict--conf-$conf