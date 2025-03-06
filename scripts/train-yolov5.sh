sleep 0

# data=data--public--satudora
# data=data--synthetic--satudora-center-box
# data=data--RAP-change-clothes
# data=data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person
# data=data--phase2-4cam-factory--phase1-4cam-factory
data=data--phase2-4cam-factory-day29

path__dir__run=/home/laptq/laptq-prj-21/runs

YOLO=yolov5s
IMGSZ=640
SCALE=0.5
MULTI_SCALE=True

# yolov5
cd submodules/yolov5
python3 train.py \
    --data /home/laptq/laptq-prj-21/src/configs/$data.yaml \
    --epochs 100 \
    --cfg $YOLO.yaml \
    --batch-size 16 \
    --device 1 \
    --imgsz $IMGSZ \
    --project $path__dir__run/$data/$YOLO--$IMGSZ--scale-$SCALE--multiscale-$MULTI_SCALE \
    --multi-scale \
    --patience 40 \
    --weights /home/laptq/laptq-prj-21/runs/data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person/yolov5s--832--scale-0.5--multiscale-True/exp/weights/best.pt \
    # --weights $YOLO.pt \
    


