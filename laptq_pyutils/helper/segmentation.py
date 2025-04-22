from laptq_pyutils.log import load_logger

LOGGER = load_logger()


def helper__extract__crops__with__mask__from__segmentation(**kwargs):

    LOGGER.warning(
        "Please consider generalize this function with helper__extract__crops__with__mask__from__segmentation. These functions have something in common."
    )

    import cv2
    import numpy as np
    import json
    from tqdm import tqdm
    import os

    path__dir__img__input = kwargs["path__dir__img__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__crop__img__output = kwargs["path__dir__crop__img__output"]
    path__dir__crop__mask__output = kwargs["path__dir__crop__mask__output"]
    path__dir__crop__lbl__output = kwargs["path__dir__crop__lbl__output"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    num__pad__0 = kwargs["num__pad__0"]

    os.makedirs(path__dir__crop__img__output, exist_ok=True)
    os.makedirs(path__dir__crop__mask__output, exist_ok=True)
    os.makedirs(path__dir__crop__lbl__output, exist_ok=True)

    for name__file__img in tqdm(sorted(os.listdir(path__dir__img__input))):
        path__file__img = os.path.join(path__dir__img__input, name__file__img)
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)

        if not os.path.isfile(path__file__lbl__input):
            if not is_ok__lbl_not_exist:
                raise FileNotFoundError(
                    "File not found: {}".format(path__file__lbl__input)
                )
            else:
                continue

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list__obj__id_class = dict__result["list__obj__id_class"]
        list__obj__box_xcycwhn = dict__result["list__obj__box_xcycwhn"]
        list__obj__seg__polygonn = dict__result["list__obj__seg__polygonn"]

        img__bgr = cv2.imread(path__file__img)
        H, W = img__bgr.shape[:2]

        for i_o, (id__class, box_xcycwhn, seg__polygonn) in enumerate(
            zip(list__obj__id_class, list__obj__box_xcycwhn, list__obj__seg__polygonn)
        ):
            xcn, ycn, wn, hn = box_xcycwhn
            x1n, y1n, x2n, y2n = xcn - wn / 2, ycn - hn / 2, xcn + wn / 2, ycn + hn / 2
            x1, y1, x2, y2 = int(x1n * W), int(y1n * H), int(x2n * W), int(y2n * H)
            seg__polygonn = [np.array(_).reshape(-1, 2) for _ in seg__polygonn]
            seg__polygon = [(_ * [W, H]).astype(int) for _ in seg__polygonn]

            crop = img__bgr[y1:y2, x1:x2]

            # shift coordinate
            xcn, ycn = xcn - x1n, ycn - y1n
            seg__polygonn = [_ - [x1n, y1n] for _ in seg__polygonn]
            x1n, y1n, x2n, y2n = x1n - x1n, y1n - y1n, x2n - x1n, y2n - y1n
            seg__polygon = [_ - [x1, y1] for _ in seg__polygon]
            x1, y1, x2, y2 = 0, 0, x2 - x1, y2 - y1

            mask = np.zeros_like(crop)
            cv2.fillPoly(mask, seg__polygon, (255, 255, 255))
            dict__result__out = {
                "list__obj__id_class": [id__class],
                "list__obj__box_xcycwhn": [[xcn, ycn, wn, hn]],
                "list__obj__seg__polygonn": [
                    [_.reshape(-1).tolist() for _ in seg__polygonn]
                ],
            }

            name__file__img__output = "{}--crop-{}.jpg".format(
                os.path.splitext(name__file__img)[0], f"{i_o:0{num__pad__0}d}"
            )
            path__file__crop__img__output = os.path.join(
                path__dir__crop__img__output, name__file__img__output
            )
            path__file__crop__mask__output = os.path.join(
                path__dir__crop__mask__output, name__file__img__output
            )
            path__file__crop__lbl__output = os.path.join(
                path__dir__crop__lbl__output,
                os.path.splitext(name__file__img__output)[0] + ".json",
            )

            cv2.imwrite(path__file__crop__img__output, crop)
            cv2.imwrite(path__file__crop__mask__output, mask)
            with open(path__file__crop__lbl__output, "w") as f:
                json.dump(dict__result__out, f, indent=4)
