path__dir__run=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs

data=20241122--phase-2--annotation-ver2

# ver__model=yolo11m--960--full
# imgsz=960
# ver__model=yolo11m--640--crop
# imgsz=640
# ver__model=yolo11s--960--crop
# imgsz=960
ver__model=yolo11m--960--crop-20
imgsz=960

ver__train=train
conf=0.2

yolo predict \
    source=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos--cropped/00000064_2401230859_NR.MP4 \
    model=/mnt/hdd10tb/Users/laptq/laptq-prj-46/weights/yolov10m_only_pot_det_960x960.pt \
    project=$path__dir__run/$data/yolov11m-yolov10m_only_pot_det_960x960/predict--conf-$conf \
    imgsz=$imgsz \
    conf=$conf \
    device=0 

    # model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    # project=$path__dir__run/$data/${ver__model}/predict--conf-$conf \

    # model=/mnt/ssd4tb/shared_workspace/prj46/models/pytorch/yolov11m-p2_pot_man_crop_det_960x960_new_data.pt \
    # project=$path__dir__run/$data/yolov11m-p2_pot_man_crop_det_960x960_new_data/predict--conf-$conf \