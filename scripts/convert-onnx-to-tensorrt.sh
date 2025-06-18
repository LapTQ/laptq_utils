

python3 submodules/laptq_utils/main.py \
        convert_onnx_to_tensorrt \
        --path__file__input "/home/laptq/laptq-fs26-shoplifting-detection/outputs/convert-torch-to-onnx/protogcn-best-f1.onnx" \
        --path__file__output "/home/laptq/laptq-fs26-shoplifting-detection/outputs/convert-onnx-to-tensorrt/protogcn-best-f1.trt" \
        --precision fp32 \
        --dynamic_shape "{'input1': [(1, 2, 15, 17),(10, 2, 15, 17), (100, 2, 15, 17)]}" \
        --max_workspace_size 1 \