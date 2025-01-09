

cd submodules/yolov5
python3 export.py \
    --weights /mnt/ssd8tb/shared_workspace/laptq/laptq-prj-21/runs/data--synthetic--satudora-center-box/yolov5m--832--scale-0.5--multiscale-True/exp/weights/best.pt \
    --imgsz 832 \
    --include onnx \
    --dynamic \
    --batch 1 \
    --simplify \
    --opset 12 \
    --optimize \
