sleep 0

# ==================== finetune
# data=only_pothole_mix
# data=only_pothole_mix--manhole-241016
# data=20241122--phase-2--annotation-ver2
# data=product-person
# data=20250120--finetune
# data=product-person--public--Satudora-finetune
# data=Deployment-store
# data=product-person--Satudora-finetune--Deployment-store
data=product-person--public--Satudora-finetune--Deployment-store

path__dir__run=~/laptq-prj-44/runs

YOLO=yolo11m
IMGSZ=640
yolo detect train \
    data=src/configs/$data.yaml \
    epochs=300 \
    imgsz=$IMGSZ \
    device=1 \
    batch=16 \
    project=$path__dir__run/$data/$YOLO--$IMGSZ--weighted-fitness \
    plots=True \
    patience=30 \
    to__use__weighted__fitness=True \
    model=${YOLO}.pt \
    # model=/home/laptq/laptq-prj-44/runs/product-person--public--Satudora-finetune/yolo11m--640--weighted-fitness/train/weights/best.pt \

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

