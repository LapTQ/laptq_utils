from laptq_pyutils.convert import convert_onnx_to_tensorrt

convert_onnx_to_tensorrt(
    path__file__input="/home/laptq/laptq-fs26-shoplifting-detection/outputs/convert-torch-to-onnx/fs26/SkateFormer/v210.onnx",
    path__file__output="/home/laptq/laptq-fs26-shoplifting-detection/outputs/convert-onnx-to-tensorrt/fs26/SkateFormer/v210.trt",
    precision="fp32",
    # dynamic_shape={
    #     "input1": [
    #         (1, 2, 15, 12),
    #         (10, 2, 15, 12),
    #         (100, 2, 15, 12),
    #     ]
    # },
    dynamic_shape={
        "input1": [
            (1, 2, 16, 12, 1),
            (10, 2, 16, 12, 1),
            (100, 2, 16, 12, 1),
        ],
    },
    max_workspace_size=1,
)

# {'input1': [(1, 2, 15, 6),(10, 2, 15, 6), (100, 2, 15, 6)], 'input2': [(1, 2, 3, 64, 64),(10, 2, 3, 64, 64),(100, 2, 3, 64, 64)]}
