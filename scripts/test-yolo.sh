path__dir__run=/home/laptq/laptq-nedo-fed/runs

# data_val=data--c1-d19
# data_val=data--c2-d20
data_val=data--c1-d19--c2-d20

# data=data--c1-d19
# data=data--c2-d20
data=data--c1-d19--c2-d20

imgsz=640

ver__model=yolov8s--640
ver__train=train
# conf=0.1

yolo val \
    data=src/configs/$data_val.yaml \
    imgsz=$imgsz \
    device=0 \
    batch=64 \
    model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz \

    # model=/home/lap_awlv/fed-object-detection/outputs/soup/yolov8s_model_soup.pt \
    # project=$path__dir__run/soup/yolov8s_model_soup/val--imgsz-$imgsz \

    # model=yolov8s.pt \
    # project=$path__dir__run/coco/yolov8s/val--imgsz-$imgsz \

    # model=/home/thuongnh_awlv/NEDO/ultralytics/runs/detect/24Mar_person2/weights/best.pt \
    # project=$path__dir__run/data--d1.2/24Mar_person2/val--imgsz-$imgsz \

    # model=/home/thuongnh_awlv/NEDO/ultralytics/runs/detect/24Mar_person13/weights/best.pt \
    # project=$path__dir__run/data--d1.1/24Mar_person13/val--imgsz-$imgsz \

    # conf=$conf \
    # iou=0.6 \