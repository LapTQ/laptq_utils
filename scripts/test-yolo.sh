# path__dir__run=/home/laptq/laptq-nedo-fed/runs
path__dir__run=/home/lap_awlv/laptq-nedo-fed/runs


LS__DATA_VAL=(
    # data--c1
    # data--c2
    # data--c1--c2
    # data--c1-day
    # data--c2-night
    # data--c1-day--c2-night
    data--d3.1--d3.2
    # data--d3-satudora
    data--d5.1
    data--d5.2
    data--d5.1-recon
    data--d5.2-recon
)

# data=data--c1
# data=data--c2
# data=data--c1--c2
# data=data--c1-day
# data=data--c2-night
# data=data--c1-day--c2-night
# data=data--c1-recon
# data=data--c2-recon
data=data--c1-recon--c2-recon


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
        model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1-recon--c2-recon--150x1--LR0.01/epoch149.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--150x1--LR0.01/epoch149.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--30x5--LR0.01/epoch145.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--15x10--LR0.01/epoch140.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--10x15--LR0.01/epoch135.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1--c2--5x30--LR0.01/epoch120.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1-day--c2-night--150x1--LR0.01/epoch149.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1-day--c2-night--30x5--LR0.01/epoch149.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1-day--c2-night--15x10--LR0.01/epoch149.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1-day--c2-night--10x15--LR0.01/epoch149.pt \
        # model=/home/lap_awlv/laptq-nedo-fed/outputs/create-global-model-backward-update-on-epoch/fedavg--c1-day--c2-night--5x30--LR0.01/epoch149.pt \
        # model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
        # model=yolov8s.pt \
        
        # project=/home/laptq/laptq-nedo-fed/outputs/trivials \
        # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz \
        # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
        # project=$path__dir__run/coco/yolov8s/val--imgsz-$imgsz \


        # conf=$conf \
        # iou=0.6 \

done