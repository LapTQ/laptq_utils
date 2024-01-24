import numpy as np


def set_seed(seed=42):
    import torch
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)