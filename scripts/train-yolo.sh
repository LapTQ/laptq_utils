sleep 0

# data=data--public--satudora
# data=data--synthetic--satudora-center-box
# data=data--RAP-change-clothes
# data=data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person
data=data--phase2-4cam-factory--phase1-4cam-factory

path__dir__run=/home/laptq/laptq-prj-21/runs

YOLO=yolov5s
IMGSZ=640
SCALE=0.5
MULTI_SCALE=True
# LR0=0.005

yolo detect train \
    data=src/configs/$data.yaml \
    epochs=100 \
    imgsz=$IMGSZ \
    device=1 \
    batch=16 \
    project=$path__dir__run/$data/$YOLO--$IMGSZ--scale-$SCALE--multiscale-$MULTI_SCALE \
    plots=True \
    patience=40 \
    scale=$SCALE \
    multi_scale=$MULTI_SCALE \
    model=/home/laptq/laptq-prj-21/runs/data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person/yolov5s--832--scale-0.5--multiscale-True/train/weights/best.pt \
    # model=${YOLO}.pt \
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

