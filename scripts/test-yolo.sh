# path__dir__run=/home/laptq/laptq-nedo-fed/runs
path__dir__run=/home/lap_awlv/laptq-nedo-fed/runs


LS__DATA_VAL=(
    data--c1
    data--c2
)

data=data--c1
# data=data--c2


imgsz=640

ver__model=yolov8s--640
ver__train=train-B-E150-LR0.01
# conf=0.1

for data_val in ${LS__DATA_VAL[@]}; do
    echo
    echo "========= Evaluating data $data_val ========="

    yolo val \
        data=src/configs/$data_val.yaml \
        imgsz=$imgsz \
        device=0 \
        batch=128 \
        project=/home/lap_awlv/laptq-nedo-fed/outputs/trivials \
        model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
        # model=yolov8s.pt \
        
        # project=/home/laptq/laptq-nedo-fed/outputs/trivials \
        # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz \
        # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
        # project=$path__dir__run/coco/yolov8s/val--imgsz-$imgsz \


        # conf=$conf \
        # iou=0.6 \

done