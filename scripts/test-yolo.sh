path__dir__run=~/laptq-prj-44/runs


LS__DATA_VAL=(
    Deployment-store
)

data=product-person--public--Satudora-finetune--Deployment-store


imgsz=640

ver__model=yolo11m--640--weighted-fitness
ver__train=train
# conf=0.1

for data_val in ${LS__DATA_VAL[@]}; do
    echo
    echo "========= Evaluating data $data_val ========="

    yolo val \
        data=src/configs/$data_val.yaml \
        imgsz=$imgsz \
        device=0 \
        batch=128 \
        model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
        project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz \
        # model=yolov8s.pt \
        
        # project=/home/laptq/laptq-nedo-fed/outputs/trivials \
        # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
        # project=$path__dir__run/coco/yolov8s/val--imgsz-$imgsz \


        # conf=$conf \
        # iou=0.6 \

done