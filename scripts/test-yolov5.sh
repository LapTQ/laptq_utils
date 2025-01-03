path__dir__run=/home/laptq/laptq-prj-21/runs

data=data--syn-text2image-satudora-center--satudora-center-box
data_val=data--testset-4cam-factory


ver__model=yolov5s--832--scale-0.5--multiscale-True
imgsz=832

YOLO=yolov5s
ver__train=exp
conf=0.1

cd submodules/yolov5
python3 val.py \
    --data ../../src/configs/$data_val.yaml \
    --weights $path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    --project $path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
    --imgsz $imgsz \
    --conf $conf \
    --iou 0.6 \
    --device 1 \
    --batch 8
