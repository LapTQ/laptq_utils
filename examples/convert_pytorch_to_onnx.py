import torch
from torch import nn

from laptq_pyutils.log import load_logger


LOGGER = load_logger()
LOGGER.info("Please ensure `onnx` and `onnxscript` are installed via pip.")


class Net1(nn.Module):

    def forward(self, x):
        return x
    

class Net2(nn.Module):

    def forward(self, x, y):
        return x, y
    

class Net3(nn.Module):

    def forward(self, x):
        x0 = x[0]
        x1 = x[1]

        return x0 + x1
    

def export_net1():

    net = Net1()
    torch.onnx.export(
        net,
        (torch.randn(1, 3, 5, 5),), # tuple of input arguments
        "/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials/net.onnx",
        input_names=["input"],
        output_names=["output"],
        dynamic_axes=None,
        opset_version=12,
    )


def export_net2():

    net = Net2()
    torch.onnx.export(
        net,
        (torch.randn(1, 3, 5, 5), torch.randn(1, 3, 5, 5)),
        "/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials/net.onnx",
        input_names=["input1", "input2"],
        output_names=["output1", "output2"],
        dynamic_axes={
            "input1": {0: "batch_size", 2: "height", 3: "width"},
            "input2": {0: "batch_size", 3: "height", 3: "width"},
        },
        opset_version=12,
    )


def export_net3():

    net = Net3()
    torch.onnx.export(
        net,
        ((torch.randn(1, 3, 5, 5), torch.randn(1, 3, 5, 5)),), # tuple of input arguments
        "/home/laptq/laptq-fs26-shoplifting-detection/outputs/trivials/net.onnx",
        input_names=["input1", "input2"],
        output_names=["output"],
        dynamic_axes=None,
        opset_version=12,
    )


if __name__ == "__main__":
    export_net1()
    export_net2()
    export_net3()