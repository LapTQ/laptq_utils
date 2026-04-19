#!/bin/bash

path__dir__run=/home/laptq/laptq-fs26-shoplifting-detection/runs

YOLO=yolov8m-cls
IMGSZ=224

yolo classify val \
    model=$path__dir__run/cluster-CNN-10/$YOLO--$IMGSZ/train/weights/best.pt \
    data=/home/laptq/laptq-fs26-shoplifting-detection/outputs/yolov8_classification_dataset/cluster-CNN-10 \
    split=test \
    imgsz=$IMGSZ \
    device=2 \
    batch=512 \
    project=$path__dir__run/cluster-CNN-10/$YOLO--$IMGSZ \
    to_enable_SquarePad=True \
    to_disable_RandomResizedCrop=True \
