from laptq_pyutils.convert import xcycwh__to__x1y1x2y2, xcycwh__to__x1y1wh
from laptq_pyutils.draw import draw__image
from laptq_pyutils.objects import ListAligner
from laptq_pyutils.ops import box__miniou
from laptq_pyutils.loader import pprint_color


def extract__ultralytics__detect(**kwargs):

    img__bgr = kwargs["img__bgr"]
    model = kwargs["model"]
    imgsz = kwargs["imgsz"]
    thresh__conf__min = kwargs["thresh__conf__min"]

    result_ultralytics = (
        model.predict(
            source=img__bgr,
            imgsz=imgsz,
            conf=thresh__conf__min,
            verbose=False,
        )[0]
        .cpu()
        .numpy()
    )

    boxes = result_ultralytics.boxes

    list_aligner__result = ListAligner(
        list__key=[
            "list__obj__id_class",
            "list__obj__box_xcycwhn",
            "list__obj__box_conf",
        ]
    )

    for i_b, box in enumerate(boxes):
        id_class = int(box.cls)
        xcn, ycn, wn, hn = box.xywhn[0].tolist()
        conf = float(box.conf)

        list_aligner__result.extend(
            {
                "list__obj__id_class": [id_class],
                "list__obj__box_xcycwhn": [[xcn, ycn, wn, hn]],
                "list__obj__box_conf": [conf],
            }
        )

    dict__result = list_aligner__result.item()

    return {
        "dict__result": dict__result,
    }


def helper__extract__ultralytics__detect__imgdir(**kwargs):

    from ultralytics import YOLO
    import os
    from tqdm import tqdm
    import cv2
    import json

    path__dir__img = kwargs["path__dir__img"]
    path__dir__output = kwargs["path__dir__output"]
    path__file__model = kwargs["path__file__model"]
    device = kwargs["device"]

    model = YOLO(path__file__model).to(device)

    os.makedirs(path__dir__output, exist_ok=True)

    list__name__file__img = sorted(os.listdir(path__dir__img))
    for name__file__img in tqdm(list__name__file__img):
        path__file__img = os.path.join(path__dir__img, name__file__img)
        img__bgr = cv2.imread(path__file__img)

        _ = extract__ultralytics__detect(
            img__bgr=img__bgr,
            model=model,
            **kwargs,
        )
        dict__result = _["dict__result"]

        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
        path__file__lbl = os.path.join(path__dir__output, name__file__lbl)

        with open(path__file__lbl, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__extract__ultralytics__detect__video(**kwargs):

    from ultralytics import YOLO
    import cv2
    import json
    import os
    from tqdm import tqdm

    path__file__input = kwargs["path__file__input"]
    path__dir__img__output = kwargs["path__dir__img__output"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    path__file__model = kwargs["path__file__model"]
    device = kwargs["device"]
    pad__id_frame = kwargs["pad__id_frame"]

    model = YOLO(path__file__model).to(device)

    cap = cv2.VideoCapture(path__file__input)
    os.makedirs(path__dir__img__output, exist_ok=True)
    os.makedirs(path__dir__lbl__output, exist_ok=True)

    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    id__frame = 0
    while True:
        success, img__bgr = cap.read()
        if not success:
            break

        _ = extract__ultralytics__detect(
            img__bgr=img__bgr,
            model=model,
            **kwargs,
        )
        dict__result = _["dict__result"]

        name__file__img = f"{id__frame:0{pad__id_frame}d}.jpg"
        path__file__img = os.path.join(path__dir__img__output, name__file__img)
        name__file__lbl = f"{id__frame:0{pad__id_frame}d}.json"
        path__file__lbl = os.path.join(path__dir__lbl__output, name__file__lbl)

        cv2.imwrite(path__file__img, img__bgr)
        with open(path__file__lbl, "w") as f:
            json.dump(dict__result, f, indent=4)

        id__frame += 1
        pbar.update(1)


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


def helper__draw__detection__imgdir(**kwargs):

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
    path__file__map__id_class__to__name_class = kwargs[
        "path__file__map__id_class__to__name_class"
    ]

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

    with open(path__file__map__id_class__to__name_class, "r") as f:
        map__id_class__to__name_class = yaml.safe_load(f)

    for i_f in tqdm(list__index__sample):
        name__file__img = list__name__file__img[i_f]
        path__file__lbl = list__path__file__lbl[i_f]
        path__file__img = os.path.join(path__dir__img, name__file__img)

        img__bgr = cv2.imread(path__file__img)
        with open(path__file__lbl, "r") as f:
            dict__result = json.load(f)

        img__vis = draw__image(
            data={
                "img__bgr": img__bgr,
                "list__obj__box_x1y1whn": xcycwh__to__x1y1wh(
                    np.array(dict__result["list__obj__box_xcycwhn"]).reshape(-1, 4)
                ),
                "list__obj__id_class": dict__result["list__obj__id_class"],
                "list__obj__box_conf": dict__result.get("list__obj__box_conf", None),
            },
            map__id_class__to__name_class=map__id_class__to__name_class,
            **kwargs,
        )

        path__file__output = os.path.join(path__dir__output, name__file__img)
        cv2.imwrite(path__file__output, img__vis)


def helper__draw__detection__video(**kwargs):

    import cv2
    import yaml
    from tqdm import tqdm
    import os
    import json
    import numpy as np

    path__file__video__input = kwargs["path__file__video__input"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__file__output = kwargs["path__file__output"]
    pad__id_frame = kwargs["pad__id_frame"]
    fourcc = kwargs["fourcc"]
    path__file__map__id_class__to__name_class = kwargs[
        "path__file__map__id_class__to__name_class"
    ]

    with open(path__file__map__id_class__to__name_class, "r") as f:
        map__id_class__to__name_class = yaml.safe_load(f)

    cap = cv2.VideoCapture(path__file__video__input)

    writer = cv2.VideoWriter(
        path__file__output,
        cv2.VideoWriter_fourcc(*fourcc),
        cap.get(cv2.CAP_PROP_FPS),
        (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        ),
    )

    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    id__frame = 0
    while True:
        success, img__bgr = cap.read()
        if not success:
            break

        name__file__lbl = f"{id__frame:0{pad__id_frame}d}.json"
        path__file__lbl = os.path.join(path__dir__lbl__input, name__file__lbl)
        with open(path__file__lbl, "r") as f:
            dict__result = json.load(f)

        img__vis = draw__image(
            data={
                "img__bgr": img__bgr,
                "list__obj__box_x1y1whn": xcycwh__to__x1y1wh(
                    np.array(dict__result["list__obj__box_xcycwhn"])
                ),
                "list__obj__id_track": [-1]
                * len(dict__result["list__obj__box_xcycwhn"]),
                "list__obj__id_class": dict__result["list__obj__id_class"],
                "list__obj__box_conf": dict__result["list__obj__box_conf"],
            },
            map__id_class__to__name_class=map__id_class__to__name_class,
            **kwargs,
        )

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
        list__obj__box_xcycwhn = []
        with open(path__file__lbl__input, "r") as f:
            for line in f:
                id_class, xcn, ycn, wn, hn = map(eval, line.strip().split())
                list__obj__id_class.append(id_class)
                list__obj__box_xcycwhn.append([xcn, ycn, wn, hn])

        dict__result = {
            "list__obj__id_class": list__obj__id_class,
            "list__obj__box_xcycwhn": list__obj__box_xcycwhn,
        }

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__convert__labelstudio_json__to__json(**kwargs):

    import json
    from tqdm import tqdm
    import os
    import yaml

    path__file__lbl__input = kwargs['path__file__lbl__input']
    path__dir__lbl__output = kwargs['path__dir__lbl__output']
    path__file__map__id_class__to__name_class = kwargs['path__file__map__id_class__to__name_class']

    os.makedirs(path__dir__lbl__output, exist_ok=True)

    with open(path__file__lbl__input, 'r') as f:
        result__labelstudio = json.load(f)

    with open(path__file__map__id_class__to__name_class, 'r') as f:
        map__id_class__to__name_class = yaml.safe_load(f)
    map__name_class__to__id_class = {v: k for k, v in map__id_class__to__name_class.items()}

    for data__per_img in tqdm(result__labelstudio):
        link_to__img = data__per_img['data']['image']
        annotations = data__per_img['annotations']

        assert len(annotations) == 1

        name__file__img = os.path.basename(link_to__img)
        name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"

        boxes = annotations[0]['result']
        list__obj__id_class = []
        list__obj__box_xcycwhn = []
        for box in boxes:
            W = box['original_width']
            H = box['original_height']
            x1 = box['value']['x']
            y1 = box['value']['y']
            w = box['value']['width']
            h = box['value']['height']
            assert len(box['value']['rectanglelabels']) == 1, "len(box['value']['rectanglelabels']) is {}".format(box['value']['rectanglelabels'])
            name_class = box['value']['rectanglelabels'][0]

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
        with open(path__file__lbl, 'w') as f:
            json.dump(dict__result, f, indent=4)

        




def helper__filter__detection__result__by__size(**kwargs):

    from PIL import Image
    import json
    from tqdm import tqdm
    import os

    path__dir__img = kwargs["path__dir__img"]
    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    filter_by = kwargs["filter_by"]
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

        list_aligner__result.pop__indexes(list__index__to_pop)

        if num__box__popped > 0:
            print(
                f"num__box__popped: {num__box__popped}/{len(list__obj__box_xcycwhn)} ({path__file__lbl__input}: {i_obj})"
            )

        dict__result = list_aligner__result.item()

        with open(path__file__lbl__output, "w") as f:
            json.dump(dict__result, f, indent=4)


def helper__filterout__image__by__id_class(**kwargs):

    import os
    import json
    from tqdm import tqdm

    path__dir__lbl__input = kwargs["path__dir__lbl__input"]
    path__dir__lbl__output = kwargs["path__dir__lbl__output"]
    list__id_class = kwargs["list__id_class"]

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
        tobe__filtered_out = False
        for id_class in list__obj__id_class:
            if id_class in list__id_class:
                tobe__filtered_out = True
                break

        if tobe__filtered_out:
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
