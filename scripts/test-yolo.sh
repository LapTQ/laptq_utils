path__dir__run=/home/laptq/laptq-fs26-shoplifting-detection/runs

data=bag-detection
data_val=bag-detection


ver__model=yolov8s--640
imgsz=640

ver__train=train
conf=0.05

yolo val \
    data=src/configs/$data_val.yaml \
    model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
    imgsz=$imgsz \
    device=0 \
    batch=8

    # model=/mnt/ssd8tb/shared_workspace/manhpc/FS_prj21/runs/train_RAF_val_RAF/weights/best.pt \
    # project=$path__dir__run/RAF/train_RAF_val_RAF/val--train_RAF_val_RAF--imgsz-$imgsz--conf-$conf \
    
    # conf=$conf \
    # iou=0.5 \
    