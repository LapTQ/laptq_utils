# path__dir__run=/home/laptq/laptq-nedo-fed/runs
path__dir__run=/home/lap_awlv/laptq-nedo-fed/runs

# data_val=data--c1-d19-splitv2
# data_val=data--c2-d20-splitv2
# data_val=data--c1-d19-splitv2--c2-d20-splitv2
# data_val=data--c1
# data_val=data--c2
# data_val=data--c1--c2
# data_val=data--d3.1--d3.2
data_val=data--d3-satudora

# data=data--c1-d19-splitv2
# data=data--c2-d20-splitv2
# data=data--c1-d19-splitv2--c2-d20-splitv2
# data=data--c1
data=data--c2
# data=data--c1--c2

imgsz=640

ver__model=yolov8s--640
ver__train=train-B-E150-LR0.01
# conf=0.1

yolo val \
    data=src/configs/$data_val.yaml \
    imgsz=$imgsz \
    device=2 \
    batch=128 \
    project=/home/lap_awlv/laptq-nedo-fed/outputs/trivials \
    model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--5x30--LR0.01/epoch120.pt \
    # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--10x15--LR0.01/epoch135.pt \
    # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--15x10--LR0.01/epoch140.pt \
    # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--30x5--LR0.01/epoch145.pt \
    # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--150x1--LR0.01/epoch149.pt \
    # project=/home/laptq/laptq-nedo-fed/outputs/trivials \

    # model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz \

    # model=yolov8s.pt \
    # project=$path__dir__run/coco/yolov8s/val--imgsz-$imgsz \

    # conf=$conf \
    # iou=0.6 \