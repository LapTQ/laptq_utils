import os

from laptq_pyutils.draw import draw__image
from laptq_pyutils.objects import (
    ListAligner,
    UltralyticsPredictor,
    YOLOv5CompatDetectPredictor,
    RTMPosePredictor,
)
from laptq_pyutils.log import load_logger
from laptq_pyutils.common import LIST__MODE__BOX
from laptq_pyutils.ops import (
    box__miniou,
    xcycwh__to__x1y1wh,
    xcycwh__to__x1y1x2y2,
    xcycwh__to__polygon,
    box_normalized__to__box_pixels,
    box_pixels__to__box_normalized,
    cluster__detection__boxes,
)
from laptq_pyutils.algo import KMeans


LOGGER = load_logger()


def parse__ultralytics_model(**kwargs):

    task = kwargs["task"]
    to_use__yolov5_compat = kwargs["to_use__yolov5_compat"]

    assert task in ["detect", "pose", "track"]

    if to_use__yolov5_compat:
        if task == "detect":
            model = YOLOv5CompatDetectPredictor(**kwargs)
        else:
            raise NotImplementedError("Task {} is not supported yet.".format(task))
    else:
        model = UltralyticsPredictor(**kwargs)

    return model


def helper__extract__ultralytics__imgdir(**kwargs):

    import os
    from tqdm import tqdm
    import cv2
    import json
    import time

    path__dir__img = kwargs["path__dir__img"]
    path__dir__output = kwargs["path__dir__output"]

    model = parse__ultralytics_model(**kwargs)

    os.makedirs(path__dir__output, exist_ok=True)

    list__name__file__img = sorted(os.listdir(path__dir__img))
    log__time = {
        "time__inference": None,
    }
    pbar = tqdm(list__name__file__img)
    for name__file__img in pbar:
        path__file__img = os.path.join(path__dir__img, name__file__img)
        img__bgr = cv2.imread(path__file__img)

        mtime_1 = time.time()
        dict__result = model.predict(
            img__bgr=img__bgr,
            **kwargs,
        )
        mtime_2 = time.time()

        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__lbl = os.path.join(path__dir__output, name__file__lbl)

        with open(path__file__lbl, "w") as f:
            json.dump(dict__result, f, indent=4)

        if log__time["time__inference"] is None:
            log__time["time__inference"] = mtime_2 - mtime_1
        else:
            log__time["time__inference"] = 0.9 * log__time["time__inference"] + 0.1 * (
                mtime_2 - mtime_1
            )
        pbar.set_postfix(time__inference=log__time["time__inference"])


def helper__extract__ultralytics__video(**kwargs):

    import cv2
    import json
    import os
    from tqdm import tqdm
    import time

    path__file__input = kwargs["path__file__input"]
    path__dir__output = kwargs["path__dir__output"]
    num__pad__0 = kwargs["num__pad__0"]

    model = parse__ultralytics_model(**kwargs)

    cap = cv2.VideoCapture(path__file__input)
    os.makedirs(path__dir__output, exist_ok=True)

    pbar = tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    log__time = {
        "time__inference": None,
    }
    for id__frame in pbar:
        success, img__bgr = cap.read()
        if not success:
            break

        mtime_1 = time.time()
        dict__result = model.predict(
            img__bgr=img__bgr,
            **kwargs,
        )
        mtime_2 = time.time()

        name__file__lbl = f"{id__frame:0{num__pad__0}d}.json"
        path__file__lbl = os.path.join(path__dir__output, name__file__lbl)

        with open(path__file__lbl, "w") as f:
            json.dump(dict__result, f, indent=4)

        if log__time["time__inference"] is None:
            log__time["time__inference"] = mtime_2 - mtime_1
        else:
            log__time["time__inference"] = 0.9 * log__time["time__inference"] + 0.1 * (
                mtime_2 - mtime_1
            )
        pbar.set_postfix(time__inference=log__time["time__inference"])


def helper__filter__detection__result__by__id_class(**kwargs):

    import json
    from tqdm import tqdm
    import os

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    list__id_class__to_include: list | None = kwargs["list__id_class__to_include"]
    list__id_class__to_exclude: list = kwargs["list__id_class__to_exclude"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__lbl in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list_aligner__result = ListAligner.from_dict(dict__result=dict__result)

        list__index__to_pop = []
        list__obj__id_class = list_aligner__result.get__key("list__obj__id_class")
        for i_obj, id_class in enumerate(list__obj__id_class):
            if (
                list__id_class__to_include is not None
                and id_class not in list__id_class__to_include
            ) or id_class in list__id_class__to_exclude:
                list__index__to_pop.append(i_obj)

        list_aligner__result.pop__indexes(list__index__to_pop)

        dict__result = list_aligner__result.item()

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__change__detection__id_class(**kwargs):

    import json
    from tqdm import tqdm
    import os

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    map__id_old__to__id_new: dict = kwargs["map__id_old__to__id_new"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__lbl in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list_aligner__result = ListAligner.from_dict(dict__result=dict__result)
        list__obj__id_class = list_aligner__result.get__key("list__obj__id_class")
        for i_obj, id_class in enumerate(list__obj__id_class):
            if id_class in map__id_old__to__id_new:
                list__obj__id_class[i_obj] = map__id_old__to__id_new[id_class]

        dict__result = list_aligner__result.item()

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__filter__detection__result__by__conf(**kwargs):

    import json
    from tqdm import tqdm
    import os

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    map__id_class__to__thresh_conf: dict = kwargs["map__id_class__to__thresh_conf"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__lbl in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list_aligner__result = ListAligner.from_dict(dict__result=dict__result)

        list__index__to_pop = []
        list__obj__id_class = list_aligner__result.get__key("list__obj__id_class")
        list__obj__box_conf = list_aligner__result.get__key("list__obj__box_conf")
        for i_obj, (id_class, conf) in enumerate(
            zip(list__obj__id_class, list__obj__box_conf)
        ):
            if conf < map__id_class__to__thresh_conf[id_class]:
                list__index__to_pop.append(i_obj)

        list_aligner__result.pop__indexes(list__index__to_pop)

        dict__result = list_aligner__result.item()

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__filter__detection__result__by__miniou(**kwargs):

    import json
    import numpy as np
    from tqdm import tqdm
    import os

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    thresh__miniou = kwargs["thresh__miniou"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__lbl in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list_aligner__result = ListAligner.from_dict(dict__result=dict__result)

        list__index__to_pop = []
        list__obj__box_xcycwhn = list_aligner__result.get__key("list__obj__box_xcycwhn")
        list__obj__id_class = list_aligner__result.get__key("list__obj__id_class")

        list__obj__box_xcycwhn = np.array(list__obj__box_xcycwhn).reshape(-1, 4)
        list__obj__id_class = np.array(list__obj__id_class)

        list__obj__box_x1y1x2y2 = xcycwh__to__x1y1x2y2(list__obj__box_xcycwhn)
        mat__miniou = box__miniou(list__obj__box_x1y1x2y2, list__obj__box_x1y1x2y2)
        mask__miniou = mat__miniou > thresh__miniou

        list__obj__box_area = (
            list__obj__box_xcycwhn[:, 2] * list__obj__box_xcycwhn[:, 3]
        )
        mask__area_smaller = (
            list__obj__box_area.reshape(-1, 1) < list__obj__box_area
        )  # must not <=

        mask__same_class = list__obj__id_class.reshape(-1, 1) == list__obj__id_class

        list__index__to_pop = np.where(
            mask__miniou & mask__area_smaller & mask__same_class
        )[0]
        list_aligner__result.pop__indexes(list__index__to_pop)

        dict__result = list_aligner__result.item()
        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__filter__detection__result__by__roi(**kwargs):

    import os
    import json
    from tqdm import tqdm
    import numpy as np
    from shapely.geometry import Polygon

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    roi__polygonn = np.array(kwargs["roi__polygonn"]).reshape(-1, 2)
    thresh__miniou = kwargs["thresh__miniou"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    roi__polygon = Polygon(roi__polygonn)
    roi_area = roi__polygon.area

    for name__file__lbl in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list_aligner__result = ListAligner.from_dict(dict__result=dict__result)

        list__obj__box_xcycwhn = list_aligner__result.get__key("list__obj__box_xcycwhn")
        list__obj__box_polygonn = xcycwh__to__polygon(
            np.array(list__obj__box_xcycwhn).reshape(-1, 4)
        )

        list__index__to_pop = []
        for i_obj, box_polygon in enumerate(list__obj__box_polygonn):
            box_polygon = Polygon(box_polygon.reshape(-1, 2))
            box_area = box_polygon.area
            inter_area = roi__polygon.intersection(box_polygon).area
            miniou = inter_area / min(box_area, roi_area)
            if miniou < thresh__miniou:
                list__index__to_pop.append(i_obj)

        list_aligner__result.pop__indexes(list__index__to_pop)

        dict__result = list_aligner__result.item()
        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__draw__imgdir(**kwargs):

    import os
    from tqdm import tqdm
    import cv2
    import json
    import numpy as np
    import yaml

    path__dir__img = kwargs["path__dir__img"]
    path__dir__lbl = kwargs["path__dir__lbl"]
    path__dir__output = kwargs["path__dir__output"]
    num__max__img = kwargs["num__max__img"]
    seed = kwargs["seed"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    to_draw__id_frame = kwargs["to_draw__id_frame"]
    id_frame__from = kwargs["id_frame__from"]
    lambda__id_frame__from = kwargs["lambda__id_frame__from"]
    to_draw__name_class = kwargs["to_draw__name_class"]
    to_draw__name_action = kwargs["to_draw__name_action"]
    path__file__map__id_class__to__name_class = kwargs[
        "path__file__map__id_class__to__name_class"
    ]
    path__file__map__id_action__to__name_action = kwargs[
        "path__file__map__id_action__to__name_action"
    ]
    to_concat__original_img = kwargs["to_concat__original_img"]
    concat__axis = kwargs["concat__axis"]
    displacement_key = kwargs["displacement_key"]
    speed_key = kwargs["speed_key"]

    assert id_frame__from in [
        "filename"
    ], "id_frame__from {} not supported. Supporting: 'filename'.".format(id_frame__from)

    os.makedirs(path__dir__output, exist_ok=True)

    list__name__file__img = []
    list__path__file__lbl = []
    for name__file__img in sorted(os.listdir(path__dir__img)):
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__lbl = os.path.join(path__dir__lbl, name__file__lbl)
        if not os.path.exists(path__file__lbl):
            if is_ok__lbl_not_exist:
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {path__file__lbl}")
        list__name__file__img.append(name__file__img)
        list__path__file__lbl.append(path__file__lbl)

    if num__max__img is not None:
        num__max__img = min(num__max__img, len(list__name__file__img))
        if seed is not None:
            np.random.seed(seed)
        list__index__sample = np.random.choice(
            len(list__name__file__img), num__max__img, replace=False
        )
    else:
        list__index__sample = range(len(list__name__file__img))

    if to_draw__name_class:
        with open(path__file__map__id_class__to__name_class, "r") as f:
            map__id_class__to__name_class = yaml.safe_load(f)
    else:
        map__id_class__to__name_class = {}

    if to_draw__name_action:
        with open(path__file__map__id_action__to__name_action, "r") as f:
            map__id_action__to__name_action = yaml.safe_load(f)
    else:
        map__id_action__to__name_action = {}

    for i_f in tqdm(list__index__sample):
        name__file__img = list__name__file__img[i_f]
        path__file__lbl = list__path__file__lbl[i_f]
        path__file__img = os.path.join(path__dir__img, name__file__img)

        if to_draw__id_frame:
            if id_frame__from == "filename":
                id__frame = lambda__id_frame__from(name__file__img)

        img__bgr = cv2.imread(path__file__img)
        with open(path__file__lbl, "r") as f:
            dict__result = json.load(f)

        img__vis = draw__image(
            data={
                "id__frame": id__frame if to_draw__id_frame else None,
                "img__bgr": img__bgr,
                "list__obj__box_x1y1whn": (
                    xcycwh__to__x1y1wh(
                        np.array(dict__result["list__obj__box_xcycwhn"]).reshape(-1, 4)
                    )
                    if "list__obj__box_xcycwhn" in dict__result
                    else None
                ),
                "list__obj__box_polygonn": dict__result.get(
                    "list__obj__box_polygonn", None
                ),
                "list__obj__id_track": dict__result.get("list__obj__id_track", None),
                "list__obj__id_class": dict__result["list__obj__id_class"],
                "list__obj__box_conf": dict__result.get("list__obj__box_conf", None),
                "list__obj__kpts_xyn": dict__result.get("list__obj__kpts_xyn", None),
                "list__obj__kpts_conf": dict__result.get("list__obj__kpts_conf", None),
                "list__obj__action_conf": dict__result.get(
                    "list__obj__action_conf", None
                ),
                "list__obj__action_status": dict__result.get(
                    "list__obj__action_status", None
                ),
                "list__obj__kpts_displacement": dict__result.get(
                    displacement_key, None
                ),
                "list__obj__kpts_speed": dict__result.get(speed_key, None),
                "list__obj__event_info": dict__result.get(
                    "list__obj__event_info", None
                ),
            },
            map__id_class__to__name_class=map__id_class__to__name_class,
            map__id_action__to__name_action=map__id_action__to__name_action,
            **kwargs,
        )

        path__file__output = os.path.join(path__dir__output, name__file__img)

        if to_concat__original_img:
            img__vis = np.concatenate([img__bgr, img__vis], axis=concat__axis)

        cv2.imwrite(path__file__output, img__vis)


def helper__draw__video(**kwargs):

    import cv2
    import yaml
    from tqdm import tqdm
    import os
    import json
    import numpy as np

    path__file__video__input = kwargs["path__file__video__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__file__output = kwargs["path__file__output"]
    num__pad__0 = kwargs["num__pad__0"]
    to_draw__name_class = kwargs["to_draw__name_class"]
    to_draw__name_action = kwargs["to_draw__name_action"]
    fourcc = kwargs["fourcc"]
    path__file__map__id_class__to__name_class = kwargs[
        "path__file__map__id_class__to__name_class"
    ]
    path__file__map__id_action__to__name_action = kwargs[
        "path__file__map__id_action__to__name_action"
    ]
    to_concat__original_img = kwargs["to_concat__original_img"]
    displacement_key = kwargs["displacement_key"]
    speed_key = kwargs["speed_key"]

    if to_draw__name_class:
        with open(path__file__map__id_class__to__name_class, "r") as f:
            map__id_class__to__name_class = yaml.safe_load(f)
    else:
        map__id_class__to__name_class = {}

    if to_draw__name_action:
        with open(path__file__map__id_action__to__name_action, "r") as f:
            map__id_action__to__name_action = yaml.safe_load(f)
    else:
        map__id_action__to__name_action = {}

    cap = cv2.VideoCapture(path__file__video__input)

    os.makedirs(os.path.dirname(path__file__output), exist_ok=True)

    writer = cv2.VideoWriter(
        path__file__output,
        cv2.VideoWriter_fourcc(*fourcc),
        cap.get(cv2.CAP_PROP_FPS),
        (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            * (2 if to_concat__original_img else 1),
        ),
    )

    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    id__frame = 0
    while True:
        success, img__bgr = cap.read()
        if not success:
            break

        name__file__lbl = f"{id__frame:0{num__pad__0}d}.json"
        path__file__lbl = os.path.join(path__dir__lbl__input, name__file__lbl)
        with open(path__file__lbl, "r") as f:
            dict__result = json.load(f)

        img__vis = draw__image(
            data={
                "id__frame": id__frame,
                "img__bgr": img__bgr,
                "list__obj__box_x1y1whn": (
                    xcycwh__to__x1y1wh(
                        np.array(dict__result["list__obj__box_xcycwhn"]).reshape(-1, 4)
                    )
                    if "list__obj__box_xcycwhn" in dict__result
                    else None
                ),
                "list__obj__box_polygonn": dict__result.get(
                    "list__obj__box_polygonn", None
                ),
                "list__obj__id_track": dict__result.get("list__obj__id_track", None),
                "list__obj__id_class": dict__result["list__obj__id_class"],
                "list__obj__box_conf": dict__result["list__obj__box_conf"],
                "list__obj__kpts_xyn": dict__result.get("list__obj__kpts_xyn", None),
                "list__obj__kpts_conf": dict__result.get("list__obj__kpts_conf", None),
                "list__obj__action_conf": dict__result.get(
                    "list__obj__action_conf", None
                ),
                "list__obj__action_status": dict__result.get(
                    "list__obj__action_status", None
                ),
                "list__obj__kpts_displacement": dict__result.get(
                    displacement_key, None
                ),
                "list__obj__kpts_speed": dict__result.get(speed_key, None),
                "list__obj__event_info": dict__result.get(
                    "list__obj__event_info", None
                ),
            },
            map__id_class__to__name_class=map__id_class__to__name_class,
            map__id_action__to__name_action=map__id_action__to__name_action,
            **kwargs,
        )

        if to_concat__original_img:
            img__vis = np.concatenate([img__bgr, img__vis], axis=0)

        writer.write(img__vis)
        id__frame += 1
        pbar.update(1)

    writer.release()
    cap.release()


def helper__convert__detection__json__to__txt(**kwargs):

    import json
    from tqdm import tqdm
    import os

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__lbl__input in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        name__file__lbl__output = os.path.splitext(name__file__lbl__input)[0] + ".txt"

        path__file__lbl__input = os.path.join(
            path__dir__lbl__input, name__file__lbl__input
        )
        path__file__lbl__output = os.path.join(
            path__dir__lbl__output, name__file__lbl__output
        )

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list__obj__id_class = dict__result["list__obj__id_class"]
        list__obj__box_xcycwhn = dict__result["list__obj__box_xcycwhn"]

        with open(path__file__lbl__output, "w") as f:
            for id_class, box_xcycwhn in zip(
                list__obj__id_class, list__obj__box_xcycwhn
            ):
                xcn, ycn, wn, hn = box_xcycwhn
                f.write(f"{id_class} {xcn} {ycn} {wn} {hn}\n")


def helper__convert__detection__txt__to__json(**kwargs):

    import json
    from tqdm import tqdm
    import os

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    mode__box = kwargs["mode__box"]

    assert mode__box in LIST__MODE__BOX, "mode__box must be one of {}".format(
        LIST__MODE__BOX
    )

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__lbl__input in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        name__file__lbl__output = os.path.splitext(name__file__lbl__input)[0] + ".json"

        path__file__lbl__input = os.path.join(
            path__dir__lbl__input, name__file__lbl__input
        )
        path__file__lbl__output = os.path.join(
            path__dir__lbl__output, name__file__lbl__output
        )

        list__obj__id_class = []
        list__obj__box_ANY = []
        with open(path__file__lbl__input, "r") as f:
            for line in f:
                id_class, *list__xy = map(eval, line.strip().split())
                list__obj__id_class.append(id_class)
                list__obj__box_ANY.append([*list__xy])

        dict__result = {
            "list__obj__id_class": list__obj__id_class,
            "list__obj__box_{}".format(mode__box): list__obj__box_ANY,
        }

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__convert__detection__xcycwhn__to__polygonn(**kwargs):

    import json
    from tqdm import tqdm
    import os
    import numpy as np

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__lbl__input in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        path__file__lbl__input = os.path.join(
            path__dir__lbl__input, name__file__lbl__input
        )
        path__file__lbl__output = os.path.join(
            path__dir__lbl__output, name__file__lbl__input
        )

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list__obj__box_xcycwhn = dict__result["list__obj__box_xcycwhn"]

        list__obj__box_polygonn = xcycwh__to__polygon(
            np.array(list__obj__box_xcycwhn).reshape(-1, 4)
        )

        dict__result["list__obj__box_polygonn"] = list__obj__box_polygonn.tolist()

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__convert__labelstudio_json__to__json(**kwargs):

    import json
    from tqdm import tqdm
    import os
    import yaml
    import traceback

    path__file__lbl__input = kwargs["path__file__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    path__file__map__id_class__to__name_class = kwargs[
        "path__file__map__id_class__to__name_class"
    ]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    with open(path__file__lbl__input, "r") as f:
        result__labelstudio = json.load(f)

    with open(path__file__map__id_class__to__name_class, "r") as f:
        map__id_class__to__name_class = yaml.safe_load(f)
    map__name_class__to__id_class = {
        v: k for k, v in map__id_class__to__name_class.items()
    }

    for data__per_img in tqdm(result__labelstudio):
        link_to__img = data__per_img["data"]["image"]
        annotations = data__per_img["annotations"]

        try:
            assert len(annotations) == 1
        except Exception as e:
            LOGGER.exception("Error in the file: {}".format(link_to__img))

        name__file__img = os.path.basename(link_to__img)
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"

        boxes = annotations[0]["result"]
        list__obj__id_class = []
        list__obj__box_xcycwhn = []
        for box in boxes:
            try:
                W = box["original_width"]
                H = box["original_height"]
                x1 = box["value"]["x"]
                y1 = box["value"]["y"]
                w = box["value"]["width"]
                h = box["value"]["height"]
                assert (
                    len(box["value"]["rectanglelabels"]) == 1
                ), "box['value']['rectanglelabels'] is {}".format(
                    box["value"]["rectanglelabels"]
                )
                name_class = box["value"]["rectanglelabels"][0]
            except Exception as e:
                LOGGER.exception("Error in the file: {}\n{}".format(link_to__img, box))
                continue

            xc = x1 + w / 2
            yc = y1 + h / 2

            xcn = xc / 100
            ycn = yc / 100
            wn = w / 100
            hn = h / 100
            id_class = map__name_class__to__id_class[name_class]

            list__obj__id_class.append(id_class)
            list__obj__box_xcycwhn.append([xcn, ycn, wn, hn])

        dict__result = {
            "list__obj__id_class": list__obj__id_class,
            "list__obj__box_xcycwhn": list__obj__box_xcycwhn,
        }

        path__file__lbl = os.path.join(path__dir__lbl__output, name__file__lbl)
        with open(path__file__lbl, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__convert__result__coco__to__json(**kwargs):

    import json
    from tqdm import tqdm
    import os
    import yaml
    import numpy as np

    path__file__lbl__input = kwargs["path__file__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    offset__id_class = kwargs["offset__id_class"]
    path__file__map__id_class__to__name_class = kwargs[
        "path__file__map__id_class__to__name_class"
    ]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    with open(path__file__lbl__input, "r") as f:
        dict__annot__coco = json.load(f)

    list__class = dict__annot__coco["categories"]
    list__class = sorted(list__class, key=lambda x: x["id"])
    map__id_class__to__name_class = {
        (obj["id"] + offset__id_class): obj["name"] for obj in list__class
    }

    with open(path__file__map__id_class__to__name_class, "w") as f:
        yaml.dump(map__id_class__to__name_class, f)

    map__id_img__to__info_img = {_["id"]: _ for _ in dict__annot__coco["images"]}

    map__id_img__to__labels = {}
    for annot in tqdm(dict__annot__coco["annotations"]):
        id_img = annot["image_id"]
        id_class = annot["category_id"] + offset__id_class
        x1, y1, w, h = annot["bbox"]
        list__seg_part__list_xy = annot["segmentation"]
        iscrowd = annot["iscrowd"]
        if iscrowd:
            continue

        H = map__id_img__to__info_img[id_img]["height"]
        W = map__id_img__to__info_img[id_img]["width"]

        x1n = x1 / W
        y1n = y1 / H
        wn = w / W
        hn = h / H
        xc = x1n + wn / 2
        yc = y1n + hn / 2

        list__seg_part__list_xy = [
            np.array(_).reshape(-1, 2) for _ in list__seg_part__list_xy
        ]
        list__seg_part__list_xyn = [_ / [W, H] for _ in list__seg_part__list_xy]
        list__seg_part__list_xyn = [
            _.reshape(-1).tolist() for _ in list__seg_part__list_xyn
        ]

        if id_img not in map__id_img__to__labels:
            map__id_img__to__labels[id_img] = {
                "list__obj__id_class": [],
                "list__obj__box_xcycwhn": [],
                "list__obj__seg__polygonn": [],
            }

        map__id_img__to__labels[id_img]["list__obj__id_class"].append(id_class)
        map__id_img__to__labels[id_img]["list__obj__box_xcycwhn"].append(
            [xc, yc, wn, hn]
        )
        map__id_img__to__labels[id_img]["list__obj__seg__polygonn"].append(
            list__seg_part__list_xyn
        )

    for id_img, dict__result in tqdm(map__id_img__to__labels.items()):
        name__file__img = map__id_img__to__info_img[id_img]["file_name"]

        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__lbl = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__filter__detection__result__by__size(**kwargs):

    from PIL import Image
    import json
    from tqdm import tqdm
    import os
    import numpy as np

    path__dir__img = kwargs["path__dir__img"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    filter_by = kwargs["filter_by"]
    to_keep__only_max = kwargs["to_keep__only_max"]
    thresh = kwargs["thresh"]

    assert filter_by in ["area", "width", "height"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    for name__file__img in tqdm(sorted(os.listdir(path__dir__img))):
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__img = os.path.join(path__dir__img, name__file__img)
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        if not os.path.exists(path__file__lbl__input):
            continue

        W, H = Image.open(path__file__img).size

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list_aligner__result = ListAligner.from_dict(dict__result=dict__result)

        list__index__to_pop = []
        list__obj__box_xcycwhn = list_aligner__result.get__key("list__obj__box_xcycwhn")

        num__box__popped = 0
        list__size = []
        for i_obj, box_xcycwhn in enumerate(list__obj__box_xcycwhn):
            xcn, ycn, wn, hn = box_xcycwhn
            w = wn * W
            h = hn * H
            tobe__popped = False
            if (
                (filter_by == "area" and w * h < thresh)
                or (filter_by == "width" and w < thresh)
                or (filter_by == "height" and h < thresh)
            ):
                tobe__popped = True

            if tobe__popped:
                list__index__to_pop.append(i_obj)
                num__box__popped += 1

            if to_keep__only_max:
                if filter_by == "area":
                    size = w * h
                elif filter_by == "width":
                    size = w
                else:
                    size = h

                list__size.append(size)

        if to_keep__only_max and len(list__size) > 0:
            list__size = np.array(list__size)
            argmax = np.argmax(list__size)
            for i_obj in range(len(list__size)):
                if i_obj != argmax and i_obj not in list__index__to_pop:
                    list__index__to_pop.append(i_obj)
                    num__box__popped += 1

        list_aligner__result.pop__indexes(list__index__to_pop)

        if num__box__popped > 0:
            print(
                f"num__box__popped: {num__box__popped}/{len(list__obj__box_xcycwhn)} ({path__file__lbl__input}: {i_obj})"
            )

        dict__result = list_aligner__result.item()

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__filter__image__by__id_class(**kwargs):

    import os
    import json
    from tqdm import tqdm

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    list__id_class__to_include = kwargs["list__id_class__to_include"]
    list__id_class__to_exclude = kwargs["list__id_class__to_exclude"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    num__img__filtered_out = 0
    num__img__total = 0
    for name__file__lbl in tqdm(sorted(os.listdir(path__dir__lbl__input))):
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        num__img__total += 1

        list__obj__id_class = dict__result["list__obj__id_class"]

        to__filter_out = False
        if list__id_class__to_include is not None and len(list__obj__id_class) == 0:
            to__filter_out = True
        for id_class in list__obj__id_class:
            if (
                list__id_class__to_include is not None
                and id_class not in list__id_class__to_include
            ) or id_class in list__id_class__to_exclude:
                to__filter_out = True
                break

        if to__filter_out:
            num__img__filtered_out += 1
            continue

        os.system(
            'cp "{}" "{}"'.format(path__file__lbl__input, path__file__lbl__output)
        )

    if num__img__filtered_out > 0:
        print(
            f"num__img__filtered_out: {num__img__filtered_out}/{num__img__total} ({path__dir__lbl__input})"
        )


def helper__rescale__detection__box(**kwargs):

    import os
    import json
    from tqdm import tqdm
    import PIL.Image

    path__dir__img = kwargs["path__dir__img"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    ratio__w = kwargs["ratio__w"]
    ratio__h = kwargs["ratio__h"]
    pad__w__max = kwargs["pad__w__max"]
    pad__h__max = kwargs["pad__h__max"]
    cut__w__max = kwargs["cut__w__max"]
    cut__h__max = kwargs["cut__h__max"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    to__get__img__size = (
        pad__w__max is not None
        or pad__h__max is not None
        or cut__w__max is not None
        or cut__h__max is not None
    )
    if to__get__img__size:
        list__name__file__img = []
        list__name__file__lbl = []
        for name__file__img in sorted(os.listdir(path__dir__img)):
            name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
            path__file__lbl = os.path.join(path__dir__lbl__input, name__file__lbl)

            if not os.path.exists(path__file__lbl):
                continue

            list__name__file__img.append(name__file__img)
            list__name__file__lbl.append(name__file__lbl)
    else:
        list__name__file__lbl = sorted(os.listdir(path__dir__lbl__input))
        list__name__file__img = [None] * len(list__name__file__lbl)

    for name__file__img, name__file__lbl in tqdm(
        zip(list__name__file__img, list__name__file__lbl)
    ):
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        if to__get__img__size:
            path__file__img = os.path.join(path__dir__img, name__file__img)
            W, H = PIL.Image.open(path__file__img).size

        list__obj__box_xcycwhn = dict__result["list__obj__box_xcycwhn"]
        for i_b, box in enumerate(list__obj__box_xcycwhn):
            xcn, ycn, wn, hn = box
            assert 0 <= xcn <= 1 and 0 <= ycn <= 1 and 0 <= wn <= 1 and 0 <= hn <= 1
            assert wn > 0 and hn > 0

            if pad__w__max is not None:
                ratio__w = min(ratio__w, pad__w__max / wn / W + 1)
            if pad__h__max is not None:
                ratio__h = min(ratio__h, pad__h__max / hn / H + 1)
            if cut__w__max is not None:
                ratio__w = max(ratio__w, 1 - cut__w__max / wn / W)
            if cut__h__max is not None:
                ratio__h = max(ratio__h, 1 - cut__h__max / hn / H)

            wn *= ratio__w
            hn *= ratio__h
            x1n = max(0, xcn - wn / 2)
            y1n = max(0, ycn - hn / 2)
            x2n = min(1, x1n + wn)
            y2n = min(1, y1n + hn)

            xcn = (x1n + x2n) / 2
            ycn = (y1n + y2n) / 2
            wn = x2n - x1n
            hn = y2n - y1n

            list__obj__box_xcycwhn[i_b] = [xcn, ycn, wn, hn]

        dict__result["list__obj__box_xcycwhn"] = list__obj__box_xcycwhn

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__erase__classes__on__images(**kwargs):

    import json
    from tqdm import tqdm
    import cv2
    import os

    path__dir__img__input = kwargs["path__dir__img__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__img__output = kwargs["path__dir__img__output"]
    list__id_class = kwargs["list__id_class"]
    color = kwargs["color"]

    os.makedirs(path__dir__img__output, exist_ok=True)

    for name__file__img in tqdm(sorted(os.listdir(path__dir__img__input))):
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__img__input = os.path.join(path__dir__img__input, name__file__img)
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__img__output = os.path.join(path__dir__img__output, name__file__img)

        if not os.path.exists(path__file__lbl__input):
            continue

        img = cv2.imread(path__file__img__input)
        H, W = img.shape[:2]

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        list__obj__id_class = dict__result["list__obj__id_class"]
        list__obj__box_xcycwhn = dict__result["list__obj__box_xcycwhn"]

        for id__class, xcycwhn in zip(list__obj__id_class, list__obj__box_xcycwhn):
            if id__class not in list__id_class:
                continue

            xcn, ycn, wn, hn = xcycwhn
            x1n = xcn - wn / 2
            y1n = ycn - hn / 2
            x2n = x1n + wn
            y2n = y1n + hn

            x1 = int(x1n * W)
            y1 = int(y1n * H)
            x2 = int(x2n * W)
            y2 = int(y2n * H)

            img[y1:y2, x1:x2] = color

        cv2.imwrite(path__file__img__output, img)


def helper__cluster__detection__bboxes(**kwargs):

    import os
    import json
    import yaml
    from tqdm import tqdm
    import numpy as np
    from PIL import Image
    import random
    import cv2

    path__dir__img__input = kwargs["path__dir__img__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    imgsz = kwargs["imgsz"]
    n_clusters = kwargs["n_clusters"]
    num__max__box = kwargs["num__max__box"]
    seed = kwargs["seed"]
    path__dir__output = kwargs["path__dir__output"]

    list__wh = []
    for name__file__img in tqdm(sorted(os.listdir(path__dir__img__input))):
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__img = os.path.join(path__dir__img__input, name__file__img)
        path__file__lbl = os.path.join(path__dir__lbl__input, name__file__lbl)

        if not os.path.exists(path__file__lbl):
            if is_ok__lbl_not_exist:
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {path__file__lbl}")

        W, H = Image.open(path__file__img).size

        with open(path__file__lbl, "r") as f:
            dict__result = json.load(f)

        list__obj__box_xcycwhn = dict__result["list__obj__box_xcycwhn"]
        list__obj__box_xcycwhn = np.array(list__obj__box_xcycwhn).reshape(-1, 4)

        rx = imgsz / W
        ry = imgsz / H
        r = min(rx, ry)

        list__obj__box_xcycwh = box_normalized__to__box_pixels(
            list__obj__box_xcycwhn, WH=(W, H)
        )

        # rescale to imgsz
        list__obj__box_xcycwh = list__obj__box_xcycwh * r

        list__wh.extend(list__obj__box_xcycwh[:, [2, 3]].tolist())

    if num__max__box is not None:
        num__max__box = min(num__max__box, len(list__wh))
        if seed is not None:
            random.seed(seed)
        list__wh = random.sample(list__wh, num__max__box)

    list__wh = np.array(list__wh).reshape(-1, 2)

    list__anchor_box__wh = cluster__detection__boxes(
        list__wh=list__wh, n_clusters=n_clusters
    )
    list__anchor_box__wh = sorted(list__anchor_box__wh, key=lambda x: x[0] * x[1])

    # plot
    img__plot = np.zeros((imgsz, imgsz, 3), dtype=np.uint8)
    list__box_xcycwh = np.concatenate(
        [
            np.full_like(list__anchor_box__wh, imgsz // 2),
            list__anchor_box__wh,
        ],
        axis=1,
    )
    img__plot = draw__image(
        data={
            "img__bgr": img__plot,
            "list__obj__box_x1y1whn": xcycwh__to__x1y1wh(
                box_pixels__to__box_normalized(list__box_xcycwh, WH=(imgsz, imgsz))
            ),
        },
    )

    path__file__output__anchor_boxes = os.path.join(
        path__dir__output, "anchor-boxes.yaml"
    )
    path__file__output__plot = os.path.join(path__dir__output, "anchor-boxes.png")

    with open(path__file__output__anchor_boxes, "w") as f:
        yaml.dump(list__anchor_box__wh, f)

    cv2.imwrite(path__file__output__plot, img__plot)


def helper__merge__detection__result(**kwargs):

    import os
    import json
    from tqdm import tqdm

    list__path__dir__lbl__input = kwargs["list__path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    is_ok__key_not_exist = kwargs["is_ok__key_not_exist"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    set__name__file__lbl = set()
    for path__dir__lbl__input in list__path__dir__lbl__input:
        for name__file__lbl in os.listdir(path__dir__lbl__input):
            set__name__file__lbl.add(name__file__lbl)
    list__name__file__lbl = sorted(list(set__name__file__lbl))

    for name__file__lbl in tqdm(list__name__file__lbl):
        dict__result = None

        for path__dir__lbl__input in list__path__dir__lbl__input:
            path__file__lbl__input = os.path.join(
                path__dir__lbl__input, name__file__lbl
            )
            if not os.path.exists(path__file__lbl__input):
                if is_ok__lbl_not_exist:
                    continue
                else:
                    raise FileNotFoundError(
                        f"Label file not found: {path__file__lbl__input}"
                    )

            with open(path__file__lbl__input, "r") as f:
                dict__result__input = json.load(f)

            if dict__result is None:
                dict__result = dict__result__input
            else:
                # check if keys are the same
                list__key__src = set(dict__result__input.keys())
                list__key__dst = set(dict__result.keys())
                list__key__diff = list__key__src - list__key__dst
                if len(list__key__diff) > 0:
                    if is_ok__key_not_exist:
                        continue
                    else:
                        raise KeyError(f"Key not found: {list__key__diff}")

                for key in list__key__dst:
                    if isinstance(dict__result[key], list):
                        dict__result[key].extend(dict__result__input[key])
                    else:
                        dict__result[key] = dict__result__input[key]

        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)
        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


class ExtractCropsFromDetectionCore:
    def __init__(self, **kwargs):
        pass

    def predict(self, **kwargs):
        img__bgr = kwargs["img__bgr"]
        dict__result = kwargs["dict__result"]
        name__file__lbl = kwargs["name__file__lbl"]
        to_save__img = kwargs["to_save__img"]
        to_resize_box__wrt__pose = kwargs["to_resize_box__wrt__pose"]
        to_shift__coords__wrt__box = kwargs["to_shift__coords__wrt__box"]
        split_by = kwargs["split_by"]
        path__dir__crop__img__output = kwargs["path__dir__crop__img__output"]
        path__dir__crop__lbl__output = kwargs["path__dir__crop__lbl__output"]
        num__pad__0__crop = kwargs["num__pad__0__crop"]
        ratio_pad_w = kwargs["ratio_pad_w"]
        ratio_pad_h = kwargs["ratio_pad_h"]
        pad_for_image_only = kwargs["pad_for_image_only"]

        if pad_for_image_only is False:
            raise NotImplementedError("Please implement for this option")

        if to_save__img:
            H, W = img__bgr.shape[:2]

        list__obj__box_xcycwhn = dict__result["list__obj__box_xcycwhn"]
        list__obj__id_track = dict__result.get(
            "list__obj__id_track", [None] * len(list__obj__box_xcycwhn)
        )
        list__obj__id_class = dict__result.get(
            "list__obj__id_class", [None] * len(list__obj__box_xcycwhn)
        )
        list__obj__kpts_xyn = dict__result.get(
            "list__obj__kpts_xyn", [None] * len(list__obj__box_xcycwhn)
        )

        ret = []
        for i_obj, (id__track, id__class, box_xcycwhn, kpts_xyn) in enumerate(
            zip(
                list__obj__id_track,
                list__obj__id_class,
                list__obj__box_xcycwhn,
                list__obj__kpts_xyn,
            )
        ):
            if id__track is None:
                continue

            b_xcn, b_ycn, b_wn, b_hn = box_xcycwhn
            b_x1n = b_xcn - b_wn / 2
            b_y1n = b_ycn - b_hn / 2
            b_x2n = b_x1n + b_wn
            b_y2n = b_y1n + b_hn

            # resize box wrt pose
            if kpts_xyn is not None and to_resize_box__wrt__pose:
                k_xnmin = 1e9
                k_ynmin = 1e9
                k_xnmax = -1e9
                k_ynmax = -1e9
                for k_xn, k_yn in kpts_xyn.values():
                    if k_xn < k_xnmin:
                        k_xnmin = k_xn
                    if k_yn < k_ynmin:
                        k_ynmin = k_yn
                    if k_xn > k_xnmax:
                        k_xnmax = k_xn
                    if k_yn > k_ynmax:
                        k_ynmax = k_yn
                b_x1n = min(b_x1n, k_xnmin)
                b_y1n = min(b_y1n, k_ynmin)
                b_x2n = max(b_x2n, k_xnmax)
                b_y2n = max(b_y2n, k_ynmax)

                b_x1n = max(0, b_x1n)
                b_y1n = max(0, b_y1n)
                b_x2n = min(1, b_x2n)
                b_y2n = min(1, b_y2n)

                b_xcn = (b_x1n + b_x2n) / 2
                b_ycn = (b_y1n + b_y2n) / 2
                b_wn = b_x2n - b_x1n
                b_hn = b_y2n - b_y1n

                if b_wn == 0 or b_hn == 0:
                    continue

                # update new box
                box_xcycwhn[0] = b_xcn
                box_xcycwhn[1] = b_ycn
                box_xcycwhn[2] = b_wn
                box_xcycwhn[3] = b_hn

            # get croped patch
            if to_save__img:
                b_x1 = int(b_x1n * W)
                b_y1 = int(b_y1n * H)
                b_x2 = int(b_x2n * W)
                b_y2 = int(b_y2n * H)

                # pad_for_image_only
                b_xc = (b_x1 + b_x2) // 2
                b_yc = (b_y1 + b_y2) // 2
                b_w = b_x2 - b_x1
                b_h = b_y2 - b_y1
                b_w = int(b_w * (1 + ratio_pad_w))
                b_h = int(b_h * (1 + ratio_pad_h))
                b_x1 = b_xc - b_w // 2
                b_y1 = b_yc - b_h // 2
                b_x2 = b_x1 + b_w
                b_y2 = b_y1 + b_h
                b_x1 = max(0, b_x1)
                b_y1 = max(0, b_y1)
                b_x2 = min(W, b_x2)
                b_y2 = min(H, b_y2)

                crop_img = img__bgr[b_y1:b_y2, b_x1:b_x2]

            if to_shift__coords__wrt__box:
                # shift keypoints
                if kpts_xyn is not None:
                    for kname, (k_xn, k_yn) in kpts_xyn.items():
                        if k_xn == 0 and k_yn == 0:
                            continue
                        k_xn = (k_xn - b_x1n) / b_wn
                        k_yn = (k_yn - b_y1n) / b_hn
                        kpts_xyn[kname] = [k_xn, k_yn]

                # shift box
                box_xcycwhn[0] = 0.5
                box_xcycwhn[1] = 0.5
                box_xcycwhn[2] = 1
                box_xcycwhn[3] = 1

            dict__result__crop = {
                k: (
                    v[i_obj : i_obj + 1]
                    if not isinstance(v, dict)
                    else ({vk: [vv[i_obj]] for vk, vv in v.items()})
                )
                for k, v in dict__result.items()
            }

            if split_by is not None:
                if split_by == "id__track":
                    subpathd = str(id__track)
                elif split_by == "id__class":
                    subpathd = str(id__class)

                # assuming path__dir__crop__img__output has a {} placeholder
                __path__dir__crop__img__output = path__dir__crop__img__output.format(
                    subpathd
                )
                __path__dir__crop__lbl__output = path__dir__crop__lbl__output.format(
                    subpathd
                )
            else:
                __path__dir__crop__img__output = path__dir__crop__img__output
                __path__dir__crop__lbl__output = path__dir__crop__lbl__output

            path__file__crop__img__output = (
                os.path.join(
                    __path__dir__crop__img__output,
                    "{}--crop-{:0{}}.jpg".format(
                        os.path.splitext(name__file__lbl)[0], i_obj, num__pad__0__crop
                    ),
                )
                if to_save__img
                else None
            )

            path__file__crop__lbl__output = os.path.join(
                __path__dir__crop__lbl__output,
                "{}--crop-{:0{}}.json".format(
                    os.path.splitext(name__file__lbl)[0], i_obj, num__pad__0__crop
                ),
            )

            ret.append(
                {
                    "crop_img": crop_img if to_save__img else None,
                    "dict__result__crop": dict__result__crop,
                    "path__file__crop__img__output": path__file__crop__img__output,
                    "path__file__crop__lbl__output": path__file__crop__lbl__output,
                }
            )

        return ret


def helper__extract__crops__from__detection__imgdir(**kwargs):

    LOGGER.warning(
        "Please consider generalize this function with helper__extract__crops__with__mask__from__segmentation. These functions have something in common."
    )

    import os
    import json
    from tqdm import tqdm
    import cv2
    import numpy as np

    path__dir__img__input = kwargs["path__dir__img__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    split_by = kwargs["split_by"]
    to_save__img = kwargs["to_save__img"]

    assert split_by in [None, "id__track", "id__class"]

    if to_save__img:
        list__name__file = sorted(os.listdir(path__dir__img__input))
    else:
        list__name__file = sorted(os.listdir(path__dir__lbl__input))

    predictor = ExtractCropsFromDetectionCore(**kwargs)

    for name__file in tqdm(list__name__file):
        if to_save__img:
            name__file__img = name__file
            name__file__lbl = os.path.splitext(name__file)[0] + ".json"
            path__file__img = os.path.join(path__dir__img__input, name__file__img)
        else:
            name__file__lbl = name__file
        path__file__lbl = os.path.join(path__dir__lbl__input, name__file__lbl)

        if not os.path.exists(path__file__lbl):
            if is_ok__lbl_not_exist:
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {path__file__lbl}")

        with open(path__file__lbl, "r") as f:
            dict__result = json.load(f)

        if to_save__img:
            img__bgr = cv2.imread(path__file__img)

        ret = predictor.predict(
            img__bgr=img__bgr,
            dict__result=dict__result,
            name__file__lbl=name__file__lbl,
            **kwargs,
        )

        for i_obj, crop_data in enumerate(ret):
            crop_img = crop_data["crop_img"]
            dict__result__crop = crop_data["dict__result__crop"]
            path__file__crop__img__output = crop_data["path__file__crop__img__output"]
            path__file__crop__lbl__output = crop_data["path__file__crop__lbl__output"]

            if to_save__img:
                os.makedirs(
                    os.path.dirname(path__file__crop__img__output), exist_ok=True
                )
                cv2.imwrite(path__file__crop__img__output, crop_img)

            os.makedirs(os.path.dirname(path__file__crop__lbl__output), exist_ok=True)
            with open(path__file__crop__lbl__output, "w") as f:
                json.dump(dict__result__crop, f, indent=4)


def helper__extract__crops__from__detection__video(**kwargs):

    LOGGER.warning(
        "Please consider generalize this function with helper__extract__crops__with__mask__from__segmentation. These functions have something in common."
    )

    import os
    import json
    from tqdm import tqdm
    import cv2
    import numpy as np

    path__file__video__input = kwargs["path__file__video__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    split_by = kwargs["split_by"]
    to_save__img = kwargs["to_save__img"]
    num__pad__0__frame = kwargs["num__pad__0__frame"]

    assert split_by in [None, "id__track", "id__class"]

    cap = cv2.VideoCapture(path__file__video__input)

    predictor = ExtractCropsFromDetectionCore(**kwargs)

    for id__frame in tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
        if to_save__img:
            success, img__bgr = cap.read()
        else:
            img__bgr = None

        name__file__lbl = f"{id__frame:0{num__pad__0__frame}d}.json"
        path__file__lbl = os.path.join(path__dir__lbl__input, name__file__lbl)

        if not os.path.exists(path__file__lbl):
            if is_ok__lbl_not_exist:
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {path__file__lbl}")

        with open(path__file__lbl, "r") as f:
            dict__result = json.load(f)

        ret = predictor.predict(
            img__bgr=img__bgr,
            dict__result=dict__result,
            name__file__lbl=name__file__lbl,
            **kwargs,
        )

        for i_obj, crop_data in enumerate(ret):
            crop_img = crop_data["crop_img"]
            dict__result__crop = crop_data["dict__result__crop"]
            path__file__crop__img__output = crop_data["path__file__crop__img__output"]
            path__file__crop__lbl__output = crop_data["path__file__crop__lbl__output"]

            if to_save__img:
                os.makedirs(
                    os.path.dirname(path__file__crop__img__output), exist_ok=True
                )
                cv2.imwrite(path__file__crop__img__output, crop_img)

            os.makedirs(os.path.dirname(path__file__crop__lbl__output), exist_ok=True)
            with open(path__file__crop__lbl__output, "w") as f:
                json.dump(dict__result__crop, f, indent=4)

    cap.release()


def helper__extract__topdown__pose__imgdir(**kwargs):

    import json
    from tqdm import tqdm
    import os
    import cv2

    path__dir__img = kwargs["path__dir__img"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    batch_size = kwargs["batch_size"]

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    pose_estimator = RTMPosePredictor(**kwargs)

    list_name__file__img = sorted(os.listdir(path__dir__img))

    batch_images = []
    batch_labels = []
    batch_paths = []
    batch_names = []

    for idx, name__file__img in enumerate(tqdm(list_name__file__img)):
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__img__input = os.path.join(path__dir__img, name__file__img)
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        if not os.path.exists(path__file__lbl__input):
            if is_ok__lbl_not_exist:
                continue
            else:
                raise FileNotFoundError(
                    f"Label file not found: {path__file__lbl__input}"
                )

        img__bgr = cv2.imread(path__file__img__input)

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        batch_images.append(img__bgr)
        batch_labels.append(dict__result)
        batch_paths.append(path__file__lbl__output)
        batch_names.append(name__file__img)

        # Process batch when full or at last image
        if len(batch_images) == batch_size or idx == len(list_name__file__img) - 1:
            # write each dict__result in-place
            pose_estimator.predict_batch(
                list_img__bgr=batch_images,
                list_dict__result=batch_labels,
                **kwargs,
            )

            # Write results
            for dict__result, path__file__lbl__output in zip(batch_labels, batch_paths):
                with open(path__file__lbl__output, "w") as f:
                    json.dump(dict__result, f, indent=4)

            # Clear batch
            batch_images = []
            batch_labels = []
            batch_paths = []
            batch_names = []


def helper__extract__topdown__pose__video(**kwargs):

    import json
    from tqdm import tqdm
    import os
    import cv2

    path__file__video = kwargs["path__file__video"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    num__pad__0 = kwargs["num__pad__0"]
    batch_size = kwargs["batch_size"]  # Default batch size

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    cap = cv2.VideoCapture(path__file__video)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    pose_estimator = RTMPosePredictor(**kwargs)

    # Batch processing
    batch_frames = []
    batch_labels = []
    batch_paths = []
    batch_ids = []

    for id__frame in tqdm(range(total_frames)):
        success, img__bgr = cap.read()
        name__file__lbl = f"{id__frame:0{num__pad__0}d}.json"
        path__file__lbl__input = os.path.join(path__dir__lbl__input, name__file__lbl)
        path__file__lbl__output = os.path.join(path__dir__lbl__output, name__file__lbl)

        if not os.path.exists(path__file__lbl__input):
            if is_ok__lbl_not_exist:
                continue
            else:
                raise FileNotFoundError(
                    f"Label file not found: {path__file__lbl__input}"
                )

        with open(path__file__lbl__input, "r") as f:
            dict__result = json.load(f)

        batch_frames.append(img__bgr)
        batch_labels.append(dict__result)
        batch_paths.append(path__file__lbl__output)
        batch_ids.append(id__frame)

        # Process batch when full or at last frame
        if len(batch_frames) == batch_size or id__frame == total_frames - 1:
            pose_estimator.predict_batch(
                list_img__bgr=batch_frames,
                list_dict__result=batch_labels,
                **kwargs,
            )

            # Write results
            for dict__result, path__file__lbl__output in zip(batch_labels, batch_paths):
                with open(path__file__lbl__output, "w") as f:
                    json.dump(dict__result, f, indent=4)

            # Clear batch
            batch_frames = []
            batch_labels = []
            batch_paths = []
            batch_ids = []

    cap.release()
