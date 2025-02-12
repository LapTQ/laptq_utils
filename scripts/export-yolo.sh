

yolo export \
    model=/mnt/ssd8tb/shared_workspace/laptq/laptq-prj-44/runs/product-person--public--Satudora-finetune/yolo11m--640--weighted-fitness/train/weights/best.pt \
    imgsz=640 \
    format=onnx \
    dynamic=True \
    batch=1 \
    simplify=True \
    opset=12 \
    optimize=True \
