path__dir__run=/home/laptq/laptq-prj-21/runs

data=unknown

ver__model=unknown
imgsz=832

ver__train=train
conf=0.01


python3 /home/laptq/laptq-prj-21/submodules/yolov5/detect.py \
    --source /home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4_5min--cropped \
    --weights /home/laptq/laptq-prj-21/weights/20221310_PersonHeadHand_yolov5s_832x832_Satudora_datasets.pt \
    --device 1 \
    --imgsz $imgsz \
    --conf-thres $conf \
    --project $path__dir__run/$data/20221310_PersonHeadHand_yolov5s_832x832_Satudora_datasets/predict--imgsz-$imgsz--conf-$conf \
    

    # model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    # project=$path__dir__run/$data/${ver__model}/predict--imgsz-$imgsz--conf-$conf \
