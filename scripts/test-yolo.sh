path__dir__run=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs

# bash ~/laptq-prj-46/submodules/laptq_utils/scripts/create--soft-link--dataset--for--training--yolo.sh

LS__DATA_VAL=(
    data--c1
    data--c2
)

data=20241122--phase-2--annotation-ver2

# ver__model=yolo11m--960--full
# imgsz=960
# ver__model=yolo11m--640--crop
# imgsz=640
# ver__model=yolo11s--960--crop
# imgsz=960
# ver__model=yolo11s--1280--crop-20
# imgsz=1280
# ver__model=yolo11m--960--crop-20--finetune-only-pot
# imgsz=960
ver__model=yolo11m--960--crop-20
imgsz=960
# ver__model=yolo11s--1280--crop-20
# imgsz=1280
# ver__model=yolo11m-p2--960--crop-20
# imgsz=960

ver__train=train8
conf=0.1

for data_val in ${LS__DATA_VAL[@]}; do
    echo
    echo "========= Evaluating data $data_val ========="

    yolo val \
        data=src/configs/$data_val.yaml \
        imgsz=$imgsz \
        device=0 \
        batch=4 \
        project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
        model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
        conf=$conf \

        # iou=0.6 \

done