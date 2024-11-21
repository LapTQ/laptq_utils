import os
from tqdm import tqdm
import PIL.Image
import numpy as np
import csv


def helper__remove__small__boxes(**kwargs):
    import warnings

    warnings.filterwarnings("ignore")

    path__dir__img = kwargs["path__dir__img"]
    path__dir__label = kwargs["path__dir__label"]
    path__dir__output = kwargs["path__dir__output"]
    thresh__area__min = kwargs["thresh__area__min"]

    os.makedirs(path__dir__output, exist_ok=True)

    num__boxes__total = 0
    num__boxes__removed = 0
    num__images__total = 0
    num__images__with__boxes__removed = 0
    for name__img in tqdm(sorted(os.listdir(path__dir__img))):
        num__images__total += 1
        path__img = os.path.join(path__dir__img, name__img)
        name__label = os.path.splitext(name__img)[0] + ".txt"
        path__label__in = os.path.join(path__dir__label, name__label)
        path__label__out = os.path.join(path__dir__output, name__label)

        if not os.path.exists(path__label__in):
            continue

        label__in = np.loadtxt(
            path__label__in, delimiter=" ", dtype=np.float32, ndmin=2
        )
        W, H = PIL.Image.open(path__img).size
        label__out = []
        has__boxes__removed = False
        for i_box, box in enumerate(label__in):
            num__boxes__total += 1
            id__class, xcn, ycn, wn, hn = box
            id__class = int(id__class)
            w = wn * W
            h = hn * H
            area = w * h

            if area < thresh__area__min:
                if not has__boxes__removed:
                    num__images__with__boxes__removed += 1
                    has__boxes__removed = True
                num__boxes__removed += 1
                continue

            label__out.append([id__class, xcn, ycn, wn, hn])

        with open(path__label__out, "w") as f:
            writer = csv.writer(f, delimiter=" ")
            writer.writerows(label__out)

    if num__images__with__boxes__removed > 0:
        print(
            f"num__boxes__removed: {num__boxes__removed}/{num__boxes__total}, num__images__with__boxes__removed: {num__images__with__boxes__removed}/{num__images__total}"
        )


def helper__remove__images__containing__classes(**kwargs):
    import warnings

    warnings.filterwarnings("ignore")

    path__dir__label = kwargs["path__dir__label"]
    path__dir__output = kwargs["path__dir__output"]
    list__id_class = kwargs["list__id_class"]

    os.makedirs(path__dir__output, exist_ok=True)

    num__labels__total = 0
    num__labels__removed = 0
    for name__label in tqdm(sorted(os.listdir(path__dir__label))):
        num__labels__total += 1
        path__label__in = os.path.join(path__dir__label, name__label)
        path__label__out = os.path.join(path__dir__output, name__label)

        label__in = np.loadtxt(
            path__label__in, delimiter=" ", dtype=np.float32, ndmin=2
        )

        tobe__removed = False
        for box__id_class in label__in[:, 0]:
            if int(box__id_class) in list__id_class:
                tobe__removed = True
                break

        if tobe__removed:
            num__labels__removed += 1
            continue

        os.system(f'cp "{path__label__in}" "{path__label__out}"')

    if num__labels__removed > 0:
        print(f"num__labels__removed: {num__labels__removed}/{num__labels__total}")
