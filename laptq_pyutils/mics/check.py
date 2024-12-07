import logging


logger = logging.getLogger(__name__)


def get_device(device=None):
    import torch

    if device is None or device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(
            "Device was not specified, while cuda is {}. Using {}.".format(
                "available" if torch.cuda.is_available() else "not available", device
            )
        )
    else:
        device = torch.device(device)
        logger.info("Using {}.".format(device))
    return device
