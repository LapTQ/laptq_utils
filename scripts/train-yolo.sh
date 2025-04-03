sleep 0

# data=data--c1-d19
# data=data--c2-d20
data=data--c1-d19--c2-d20

path__dir__run=/home/laptq/laptq-nedo-fed/runs

YOLO=yolov8s
IMGSZ=640


yolo detect train \
    data=src/configs/$data.yaml \
    epochs=100 \
    imgsz=$IMGSZ \
    device=0 \
    batch=64 \
    project=$path__dir__run/$data/$YOLO--$IMGSZ \
    plots=True \
    patience=40 \
    save_period=1 \
    model=${YOLO}.pt \
    # optimizer=SGD \
    # lr0=$LR0 \

exit

# ===================== finetune keypoint
data=only_pothole_mix--manhole-241016--dataset-ninja-road-pothole-images--crop--keypoint
YOLO=yolo11m-pose
yolo pose train \
    data=src/configs/$data.yaml \
    model=${YOLO}.pt \
    epochs=300 \
    imgsz=960 \
    device=0,1,3 \
    batch=24 \
    project=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/${data}/${YOLO} \
    plots=True \
    patience=50 \
    workers=24

exit

# ===================== pre-train COCO + finetune
data=coco
YOLO=yolo11m-p2
# yolo detect train \
#     data=src/configs/$data.yaml \
#     model=src/configs/${YOLO}.yaml \
#     epochs=300 \
#     imgsz=640 \
#     device=0,1,3 \
#     batch=30 \
#     project=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/${data}/${YOLO} \
#     plots=True \
#     patience=40 \
#     workers=24
yolo train resume model=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/$data/$YOLO/train/weights/last.pt

data=only_pothole_mix--manhole-241016
yolo detect train \
    data=src/configs/$data.yaml \
    model=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/coco/$YOLO/train/weights/best.pt \
    epochs=100 \
    imgsz=960 \
    device=0,1,3 \
    batch=12 \
    project=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/${data}/${YOLO} \
    plots=True \
    patience=40

