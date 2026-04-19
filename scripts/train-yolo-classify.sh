

path__dir__run=/home/laptq/laptq-fs26-shoplifting-detection/runs

YOLO=yolov8m-cls
IMGSZ=224
# SCALE=0.5
# MULTI_SCALE=True

yolo classify train \
    data=/home/laptq/laptq-fs26-shoplifting-detection/outputs/yolov8_classification_dataset/cluster-CNN-10 \
    model=${YOLO}.pt \
    epochs=100 \
    imgsz=$IMGSZ \
    device=2 \
    batch=128 \
    project=$path__dir__run/cluster-CNN-10/$YOLO--$IMGSZ \
    plots=True \
    patience=40 \
    erasing=0 \
    translate=0 \
    to_enable_SquarePad=True \
    to_disable_RandomResizedCrop=True \
    # scale=$SCALE \
    # multi_scale=$MULTI_SCALE

