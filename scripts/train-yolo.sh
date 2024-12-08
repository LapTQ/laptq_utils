sleep 0

# ==================== finetune
# data=only_pothole_mix
# data=only_pothole_mix--manhole-241016
data=20241122--phase-2--annotation-ver2

# bash ~/laptq-prj-46/submodules/laptq_utils/scripts/create--soft-link--dataset--for--training--yolo.sh
echo "$( file ~/laptq-prj-46/data/road-issues-detection/APTO_v2/day1_330/images/IMG_488600001.jpg )" >> ~/laptq-prj-46/outputs/progress/log.txt
# YOLO=yolo11s
# IMGSZ=1280
# yolo detect train \
#     data=src/configs/$data.yaml \
#     model=${YOLO}.pt \
#     epochs=200 \
#     imgsz=$IMGSZ \
#     device=0,1 \
#     batch=16 \
#     project=~/laptq-prj-46/runs/$data/${YOLO}--${IMGSZ}--crop-20 \
#     plots=True \
#     patience=30


YOLO=yolo11m-p2
IMGSZ=960
yolo detect train \
    data=src/configs/$data.yaml \
    model=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/coco/yolo11m-p2/train/weights/best.pt \
    epochs=200 \
    imgsz=$IMGSZ \
    device=0,1 \
    batch=8 \
    project=~/laptq-prj-46/runs/${data}/${YOLO}--${IMGSZ}--crop-20 \
    plots=True \
    patience=40


# bash ~/laptq-prj-46/submodules/laptq_utils/scripts/create--soft-link--dataset--for--training--yolo--crop-20--only-pot.sh
# echo "$( file ~/laptq-prj-46/outputs/20241130--resolve--soft-link--dataset/APTO_v2/day1_330/images/IMG_488600001.jpg )" >> ~/laptq-prj-46/outputs/progress/log.txt
# YOLO=yolo11m
# IMGSZ=960
# yolo detect train \
#     data=src/configs/$data.yaml \
#     model=~/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m--960--crop-20/train/weights/best.pt \
#     epochs=4 \
#     imgsz=$IMGSZ \
#     device=0,1 \
#     batch=16 \
#     project=~/laptq-prj-46/runs/$data/${YOLO}--${IMGSZ}--crop-20--finetune-only-pot \
#     plots=True \
#     lr0=0.007129 \
#     warmup_epochs=0 \
#     patience=30


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

