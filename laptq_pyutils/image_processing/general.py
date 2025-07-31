import numpy as np


def crop_with_pad(img, x1, y1, x2, y2, pad=0):
    """Crop a region from an image with padding if the region is out of bounds."""
    imH, imW = img.shape[:2]

    # Define output dimensions
    W_out = x2 - x1
    H_out = y2 - y1

    # Create an output image filled with black (or zero)
    img_out = np.full((H_out, W_out, 3), pad, dtype=np.uint8)

    # Determine the area to crop from the original image
    left = max(min(x1, imW), 0)
    upper = max(min(y1, imH), 0)
    right = max(min(x2, imW), 0)
    lower = max(min(y2, imH), 0)

    # Calculate the position to paste the cropped area in the output image
    paste_x = max(0, -x1)
    paste_y = max(0, -y1)

    # Crop the area from the original image
    cropped_area = img[upper:lower, left:right]

    # Paste the cropped area into the output image
    img_out[
        paste_y : paste_y + cropped_area.shape[0],
        paste_x : paste_x + cropped_area.shape[1],
    ] = cropped_area

    return img_out


import torchvision.transforms.functional as F


class SquarePad:

    def __init__(self, fill=0, padding_mode="constant"):

        self.fill = fill
        self.padding_mode = padding_mode

    def __call__(self, image):
        w, h = image.size  # PIL
        max_wh = np.max([w, h])
        hp = max_wh - w
        vp = max_wh - h

        lp = hp // 2
        rp = hp - lp
        tp = vp // 2
        bp = vp - tp
        padding = (lp, tp, rp, bp)
        return F.pad(image, padding, self.fill, self.padding_mode)
