path__dir__run=/home/laptq/laptq-prj-21/runs

data=data
data_val=data--synthetic


ver__model=yolo11s--832--scale-0.5--multiscale-True
imgsz=832

ver__train=train2
conf=0.01

yolo val \
    data=src/configs/$data_val.yaml \
    model=/mnt/ssd8tb/shared_workspace/manhpc/FS_prj21/runs/train_RAF_val_RAF/weights/best.pt \
    project=$path__dir__run/RAF/train_RAF_val_RAF/val--train_RAF_val_RAF--imgsz-$imgsz--conf-$conf \
    imgsz=$imgsz \
    conf=$conf \
    iou=0.6 \
    device=1 \
    batch=8

    # model=/mnt/hdd10tb/Users/laptq/laptq-prj-46/weights/yolov10m_only_pot_det_960x960.pt \
    # project=$path__dir__run/$data/yolov10m_only_pot_det_960x960/val--conf-$conf \
    
    # model=/mnt/ssd4tb/shared_workspace/prj46/models/pytorch/yolov11m-p2_pot_man_crop_det_960x960_new_data.pt \
    # project=$path__dir__run/$data/yolov11m-p2_pot_man_crop_det_960x960_new_data/val--conf-$conf \

    
    # model=$path__dir__run/$data/${ver__model}/$ver__train/weights/best.pt \
    # project=$path__dir__run/$data/${ver__model}/val--$ver__train--imgsz-$imgsz--conf-$conf \