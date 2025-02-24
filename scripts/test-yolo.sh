path__dir__run=~/laptq-prj-44/runs

data=product-person--public--Satudora-finetune--Deployment-store
data_val=Deployment-store


ver__model=yolo11m--640--weighted-fitness
imgsz=640

ver__train=train
# conf=0.05

yolo val \
    data=src/configs/$data_val.yaml \
    model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
    imgsz=$imgsz \
    device=0 \
    batch=16 \
    # conf=$conf \
    # iou=0.5 \

    
    # model=/mnt/ssd8tb/shared_workspace/manhpc/FS_prj21/runs/train_RAF_val_RAF/weights/best.pt \
    # project=$path__dir__run/RAF/train_RAF_val_RAF/val--train_RAF_val_RAF--imgsz-$imgsz--conf-$conf \