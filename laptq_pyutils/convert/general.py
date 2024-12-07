def np_to_b64(**kwargs):

    from PIL import Image
    import base64
    from io import BytesIO

    img = kwargs["img"]
    pil_img = Image.fromarray(img)
    buffer = BytesIO()
    pil_img.save(buffer, format="JPEG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()
    return img_b64


def img_to_b64(**kwargs):

    import base64

    path_img = kwargs["path_img"]

    with open(path_img, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def b64_to_np(**kwargs):

    import numpy as np
    from PIL import Image
    import base64
    from io import BytesIO

    img_b64 = kwargs["img_b64"]
    img = np.array(Image.open(BytesIO(base64.b64decode(img_b64))))
    return img


def obj_to_pklstr(**kwargs):

    import pickle

    obj = kwargs["obj"]
    pkl_str = pickle.dumps(obj).decode("latin1")
    return pkl_str


def pklstr_to_obj(**kwargs):

    import pickle

    pkl_str = kwargs["pkl_str"]
    obj = pickle.loads(pkl_str.encode("latin1"))
    return obj


def xcycwh__to__x1y1x2y2(xcycwh):

    x1y1x2y2 = xcycwh.copy()
    x1y1x2y2[:, 0] = xcycwh[:, 0] - xcycwh[:, 2] / 2
    x1y1x2y2[:, 1] = xcycwh[:, 1] - xcycwh[:, 3] / 2
    x1y1x2y2[:, 2] = xcycwh[:, 0] + xcycwh[:, 2] / 2
    x1y1x2y2[:, 3] = xcycwh[:, 1] + xcycwh[:, 3] / 2

    return x1y1x2y2


def xcycwh__to__x1y1wh(xcycwh):

    x1y1wh = xcycwh.copy()
    x1y1wh[:, 0] = xcycwh[:, 0] - xcycwh[:, 2] / 2
    x1y1wh[:, 1] = xcycwh[:, 1] - xcycwh[:, 3] / 2
    x1y1wh[:, 2] = xcycwh[:, 2]
    x1y1wh[:, 3] = xcycwh[:, 3]

    return x1y1wh
