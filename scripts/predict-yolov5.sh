path__dir__run=/home/laptq/laptq-prj-21/runs

# data=unknown
data=data--synthetic--syn-text2image-satudora-center--satudora-center-box

# ver__model=unknown
ver__model=yolov5s--832--scale-0.5--multiscale-True
imgsz=832

# ver__train=train
ver__train=exp2
conf=0.1


python3 /home/laptq/laptq-prj-21/submodules/yolov5/detect.py \
    --source /home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4 \
    --weights $path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    --project $path__dir__run/$data/${ver__model}/predict--$ver__train--imgsz-$imgsz--conf-$conf \
    --device 2 \
    --imgsz $imgsz \
    --conf-thres $conf \
    # --hide-labels
    
    # --weights /home/laptq/laptq-prj-21/weights/20221310_PersonHeadHand_yolov5s_832x832_Satudora_datasets.pt \
    # --project $path__dir__run/$data/20221310_PersonHeadHand_yolov5s_832x832_Satudora_datasets/predict--imgsz-$imgsz--conf-$conf \

    # model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    # project=$path__dir__run/$data/${ver__model}/predict--imgsz-$imgsz--conf-$conf \
