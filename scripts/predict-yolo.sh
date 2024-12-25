path__dir__run=/home/laptq/laptq-prj-21/runs

# data=unknown
data=data

# ver__model=unknown
# imgsz=832
ver__model=yolo11s--832--scale-0.5--multiscale-True
imgsz=832

ver__train=train
conf=0.1


yolo predict \
    source=/home/laptq/laptq-prj-21/data/Videos/241210_受け取り動画/mp4_5min \
    model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    project=$path__dir__run/$data/${ver__model}/predict--$ver__train--imgsz-$imgsz--conf-$conf \
    imgsz=$imgsz \
    conf=$conf \
    device=2


    model=/home/laptq/laptq-prj-21/weights/20221310_PersonHeadHand_yolov5s_832x832_Satudora_datasets.pt \
    project=$path__dir__run/$data/20221310_PersonHeadHand_yolov5s_832x832_Satudora_datasets/predict--imgsz-$imgsz--conf-$conf \

    # model=/home/laptq/laptq-prj-21/weights/yolov11s_640_LOAF_top_view.pt \
    # project=$path__dir__run/$data/yolov11s_640_LOAF_top_view/predict--imgsz-$imgsz--conf-$conf \