sleep 0

# ==================== finetune
# data=only_pothole_mix
# data=only_pothole_mix--manhole-241016
# data=20241122--phase-2--annotation-ver2
data=general

# bash ~/laptq-prj-46/submodules/laptq_utils/scripts/create--soft-link--dataset--for--training--yolo.sh
# echo "$( file ~/laptq-prj-46/data/road-issues-detection/APTO_v2/day1_330/images/IMG_488600001.jpg )" >> ~/laptq-prj-46/outputs/progress/log.txt
YOLO=yolo11m
IMGSZ=640
yolo detect train \
    data=src/configs/$data.yaml \
    model=/mnt/ssd8tb/shared_workspace/prj44/models/pytorch/yolo11m_640_product_det/weights/best.pt \
    epochs=200 \
    imgsz=$IMGSZ \
    device=2 \
    batch=16 \
    project=~/laptq-prj-44/runs/$data/${YOLO}--${IMGSZ}--weighted-fitness \
    plots=True \
    patience=30 \
    to__use__weighted__fitness=True



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

