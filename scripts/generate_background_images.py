PATHD_IMAGE = "/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--images"
POSTFIXD_IMAGE = ""

PATHD_OUTPUT = (
    "/home/laptq/laptq-fs26-shoplifting-detection/outputs/generate_background_images"
)
POSTFIX_OUTPUT = ""

TO_USE__SOFTLINK = True

MAP_SUBPATHD_TO = {
    "shoplifting-1min_anonymized.mp4": None,
}


import os
from PIL import Image
import numpy as np
import cv2
from tqdm import tqdm


def generate_background_images(**kwargs):
    path__dir__img = kwargs["path__dir__img"]
    path__dir__output = kwargs["path__dir__output"]
    to_use__softlink = kwargs["to_use__softlink"]

    is__1st_image__created = False
    pathf__1st_img__output = None
    for namef_img_input in tqdm(sorted(os.listdir(path__dir__img))):
        pathf_img_input = os.path.join(path__dir__img, namef_img_input)
        W, H = Image.open(pathf_img_input).size

        img_bg = np.full(
            (H, W, 3),
            # (255, 229, 204),
            (25, 25, 25),
            dtype=np.uint8,
        )

        pathf_img_output = os.path.join(path__dir__output, namef_img_input)
        if not is__1st_image__created:
            cv2.imwrite(pathf_img_output, img_bg)
            is__1st_image__created = True
            pathf__1st_img__output = pathf_img_output
            continue

        if to_use__softlink:
            os.system("ln -sf {} {}".format(pathf__1st_img__output, pathf_img_output))
        else:
            cv2.imwrite(pathf_img_output, img_bg)


for subpathd in MAP_SUBPATHD_TO:
    pathd_img = os.path.join(PATHD_IMAGE, subpathd, "images{}".format(POSTFIXD_IMAGE))
    pathd_output = os.path.join(
        PATHD_OUTPUT, subpathd, "images{}".format(POSTFIX_OUTPUT)
    )

    if os.path.exists(pathd_output):
        os.system("rm -rf {}".format(pathd_output))
    os.makedirs(pathd_output, exist_ok=True)

    generate_background_images(
        path__dir__img=pathd_img,
        path__dir__output=pathd_output,
        to_use__softlink=TO_USE__SOFTLINK,
    )

    print("Done: {}".format(subpathd))
