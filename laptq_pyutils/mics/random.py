def set_seed(seed=42):
    import numpy as np
    import torch

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)