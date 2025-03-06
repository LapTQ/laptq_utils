cd submodules/yolov5
python3 export.py \
    --weights /home/laptq/laptq-prj-21/runs/data--phase2-4cam-factory--phase1-4cam-factory/yolov5s--640--scale-0.5--multiscale-True/exp2/weights/best.pt \
    --imgsz 640 \
    --include onnx \
    --dynamic \
    --batch 1 \
    --simplify \
    --opset 12 \
    --optimize \
