# path__dir__run=/home/laptq/laptq-nedo-fed/runs
path__dir__run=/home/lap_awlv/laptq-nedo-fed/runs

# data_val=data--c1-d19
# data_val=data--c2-d20
# data_val=data--c1-d19--c2-d20
# data_val=data--c1-d19-splitv2
data_val=data--c2-d20-splitv2
# data_val=data--c1-d19-splitv2--c2-d20-splitv2

# data=data--c1-d19
# data=data--c2-d20
# data=data--c1-d19--c2-d20
data=data--c1-d19-splitv2
# data=data--c2-d20-splitv2
# data=data--c1-d19-splitv2--c2-d20-splitv2

imgsz=640

ver__model=yolov8s--640
ver__train=train
# conf=0.1

yolo val \
    data=src/configs/$data_val.yaml \
    imgsz=$imgsz \
    device=1 \
    batch=64 \
    model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/MODEL-0--DATA_ID-data--c1-d19-splitv2--MODEL_ID-yolov8s--640--TRAIN_ID-train-fedavg-NUM_EPOCH-15x8-LR0-0.01--MODEL-1--DATA_ID-data--c2-d20-splitv2--MODEL_ID-yolov8s--640--TRAIN_ID-train-fedavg-NUM_EPOCH-15x8-LR0-0.01--METHOD-avg/epoch112.pt \
    project=/home/lap_awlv/laptq-nedo-fed/outputs/trivials \

    # model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz \

    # model=yolov8s.pt \
    # project=$path__dir__run/coco/yolov8s/val--imgsz-$imgsz \

    # model=/home/thuongnh_awlv/NEDO/ultralytics/runs/detect/24Mar_person2/weights/best.pt \
    # project=$path__dir__run/data--d1.2/24Mar_person2/val--imgsz-$imgsz \

    # model=/home/thuongnh_awlv/NEDO/ultralytics/runs/detect/24Mar_person13/weights/best.pt \
    # project=$path__dir__run/data--d1.1/24Mar_person13/val--imgsz-$imgsz \

    # conf=$conf \
    # iou=0.6 \