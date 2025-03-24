

yolo export \
    model=/mnt/ssd8tb/shared_workspace/prj44/models/pytorch/yolo11m_640_person_product_general_v5.pt \
    imgsz=640 \
    format=onnx \
    dynamic=True \
    batch=1 \
    simplify=True \
    opset=12 \
    optimize=True \
