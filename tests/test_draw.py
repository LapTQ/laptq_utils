from laptq_pyutils.draw import cv2_imshow, cv2_putText, cv2_rectangle
import pytest
import numpy as np


def test_cv2_imshow():
    img = 255 + np.zeros((256, 256, 3), dtype=np.uint8)
    key = cv2_imshow(img)
    assert chr(key).strip().lower() == "t"


@pytest.mark.parametrize(
    "imgsz,text,org,fontScale,color,thickness",
    [
        (256, "Yellow text", (10, 128), 1, (0, 255, 255), 1),
        (256, "Bigger text", (10, 128), 2, (0, 255, 255), 1),
        (256, "Thicker text", (10, 128), 1, (0, 255, 255), 2),
    ],
)
def test_cv2_putText(
    imgsz,
    text,
    org,
    fontScale,
    color,
    thickness,
):
    img = 255 + np.zeros((imgsz, imgsz, 3), dtype=np.uint8)
    cv2_putText(img, text, org, fontScale=fontScale, color=color, thickness=thickness)
    key = cv2_imshow(img)
    assert chr(key).strip().lower() == "t"


if __name__ == "__main__":
    pytest.main([__file__])
