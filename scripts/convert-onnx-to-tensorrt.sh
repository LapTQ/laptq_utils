

python3 submodules/laptq_utils/main.py \
        convert_onnx_to_tensorrt \
        --path__file__input "/home/laptq/laptq-fs26-shoplifting-detection/outputs/convert-torch-to-onnx/tsstg-hand-model-best.onnx" \
        --path__file__output "/home/laptq/laptq-fs26-shoplifting-detection/outputs/convert-onnx-to-tensorrt/tsstg-hand-model-best.trt" \
        --precision fp32 \
        --dynamic_shape "{'input1': [(1, 3, 30, 14), (1, 3, 30, 14), (1, 3, 30, 14)], 'input2': [(1, 2, 29, 14), (1, 2, 29, 14), (1, 2, 29, 14)]}" \
        --max_workspace_size 1 \