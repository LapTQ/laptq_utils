path__dir__run=/home/laptq/laptq-prj-21/runs

data=data--synthetic--syn-text2image-satudora-center--satudora-center-box--paste-not-person
# data=data--phase2-4cam-factory--phase1-4cam-factory
# data=data--phase2-4cam-factory-day29

# data_val=data--testset-4cam-factory
data_val=data--phase2-4cam-factory--testset


ver__model=yolov5s--832--scale-0.5--multiscale-True
imgsz=640
# ver__model=yolov5s--640--scale-0.5--multiscale-True
# imgsz=640


ver__train=exp
conf=0.1

cd submodules/yolov5
python3 val.py \
    --data ../../src/configs/$data_val.yaml \
    --weights $path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    --project $path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \
    --imgsz $imgsz \
    --conf-thres $conf \
    --iou-thres 0.6 \
    --device 1 \
    --batch 8
