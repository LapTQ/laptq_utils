path__dir__run=/home/lap_awlv/fed-object-detection/runs

# data_val=data--subset-d2.1
# data_val=data--subset-d2.2
# data_val=data--subset-d2
# data_val=data--subset-d1
data_val=data--subset-d1-d2
# data_val=data--subset-d3

# data=data--subset-d2.1
# data=data--subset-d2.2
data=data--subset-d2

ver__model=yolov8s--640


imgsz=640

ver__train=train2
# conf=0.1

yolo val \
    data=src/configs/$data_val.yaml \
    imgsz=$imgsz \
    iou=0.6 \
    device=1 \
    batch=16 \
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