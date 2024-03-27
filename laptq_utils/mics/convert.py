import base64
from io import BytesIO
from PIL import Image
import numpy as np


def np_to_b64(
        **kwargs
):
    img = kwargs['img']
    pil_img = Image.fromarray(img)
    buffer = BytesIO()
    pil_img.save(buffer, format='JPEG')
    img_b64 = base64.b64encode(buffer.getvalue()).decode()
    return img_b64


def b64_to_np(
        **kwargs
):
    img_b64 = kwargs['img_b64']
    img = np.array(Image.open(BytesIO(base64.b64decode(img_b64))))
    return img
    