

path__dir__run=/home/laptq/laptq-fs26-shoplifting-detection/runs

YOLO=yolov8s-cls
IMGSZ=128
# SCALE=0.5
# MULTI_SCALE=True

yolo classify train \
    data=/home/laptq/laptq-fs26-shoplifting-detection/outputs/create-2DCNN-classification-dataset \
    model=${YOLO}.pt \
    epochs=100 \
    imgsz=$IMGSZ \
    device=2 \
    batch=32 \
    project=$path__dir__run/classification/$YOLO--$IMGSZ \
    plots=True \
    patience=40 \
    erasing=0 \
    to_disable_RandomResizedCrop=True \
    # scale=$SCALE \
    # multi_scale=$MULTI_SCALE

