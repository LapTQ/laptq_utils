sleep 0

# data=data--public--satudora
# data=data--synthetic--satudora-center-box
# data=data--RAP-change-clothes

path__dir__run=/home/laptq/laptq-prj-21/runs

data=data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person
YOLO=yolov5s
IMGSZ=832
SCALE=0.5
MULTI_SCALE=True

# yolov5
cd submodules/yolov5
python3 train.py \
    --data /home/laptq/laptq-prj-21/src/configs/$data.yaml \
    --epochs 100 \
    --weights $YOLO.pt \
    --cfg $YOLO.yaml \
    --batch-size 16 \
    --device 1 \
    --imgsz $IMGSZ \
    --project $path__dir__run/$data/$YOLO--$IMGSZ--scale-$SCALE--multiscale-$MULTI_SCALE \
    --multi-scale \
    --patience 40


