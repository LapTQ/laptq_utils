PATH__DIR__INPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/data/videos--cropped
PATH__DIR__OUTPUT=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/20241202--yolo--prediction

IFS=$'\n'

for name__file in $( ls $PATH__DIR__INPUT ); do
    path__file__input=$( realpath "$PATH__DIR__INPUT/$name__file" )
    path__file__output="$PATH__DIR__OUTPUT/$name__file"

    python3 submodules/laptq_utils/main.py \
        helper__predict__yolo__detect \
        --path__file__input "$path__file__input" \
        --path__file__output "$path__file__output" \
        --path__file__checkpoint /mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m--960--crop-20/train/weights/best.pt \
        --device cuda:0 \
        --imgsz 960 \
        --thresh__conf_min 0.01 \
        --list__conf 0.2,0.5,0.5 \
        --to__filterby__miniou True \
        --thresh__miniou 0.5 \
        --draw_conf True \
        --draw_track_id False \
        --draw_class_id True \
        --fontScale 1 \
        --thickness 1 \
        --draw_class_name True \
        --box_color_by class_id \
        --path__file__class_id_to_label src/configs/class_id_to_label.yaml
    
done