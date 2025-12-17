import os
import numpy as np
import cv2
import json
import random
from tqdm import tqdm
from multiprocessing import Pool

from laptq_pyutils.draw import draw__image
from laptq_pyutils.ops import (
    xcycwh__to__x1y1wh,
)


def _draw_core(kwargs):
    id__frame = kwargs["id__frame"]
    img__bgr = kwargs["img__bgr"]
    path__file__img = kwargs["path__file__img"]
    path__file__lbl = kwargs["path__file__lbl"]
    displacement_key = kwargs["displacement_key"]
    speed_key = kwargs["speed_key"]
    path__dir__output = kwargs["path__dir__output"]
    is_ok__lbl_not_exist = kwargs["is_ok__lbl_not_exist"]
    output_as = kwargs["output_as"]
    name__file__img = kwargs["name__file__img"]

    if not os.path.exists(path__file__lbl):
        if is_ok__lbl_not_exist:
            return None
        else:
            raise FileNotFoundError(f"Label file not found: {path__file__lbl}")

    with open(path__file__lbl, "r") as f:
        dict__result = json.load(f)

    if img__bgr is None:
        img__bgr = cv2.imread(path__file__img)

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
            "list__obj__kpts_displacement": dict__result.get(displacement_key, None),
            "list__obj__kpts_speed": dict__result.get(speed_key, None),
            **dict__result,
        },
        **kwargs,
    )

    if output_as == "imgdir":
        path__file__output = os.path.join(path__dir__output, name__file__img)
        cv2.imwrite(path__file__output, img__vis)
        return None  # Optimization: Don't pickle/return img__vis when using multi-process if already saved

    return {"img__vis": img__vis}


def helper__draw__imgdir(**kwargs):
    path__dir__img = kwargs["path__dir__img"]
    path__dir__lbl = kwargs["path__dir__lbl"]
    output_as = kwargs["output_as"]
    path__dir__output = kwargs["path__dir__output"]
    path__file__output = kwargs["path__file__output"]
    num__max__img = kwargs["num__max__img"]
    seed = kwargs["seed"]
    to_draw__id_frame = kwargs["to_draw__id_frame"]
    id_frame__from = kwargs["id_frame__from"]
    lambda__id_frame__from = kwargs["lambda__id_frame__from"]
    num__workers = kwargs["num__workers"]
    fps = kwargs["fps"]
    fourcc = kwargs["fourcc"]

    assert output_as in ["imgdir", "video"]

    assert id_frame__from in [
        "filename"
    ], "id_frame__from {} not supported. Supporting: 'filename'.".format(id_frame__from)

    if output_as == "imgdir":
        os.makedirs(path__dir__output, exist_ok=True)
    elif output_as == "video":
        os.makedirs(os.path.dirname(path__file__output), exist_ok=True)

    writer = None

    list__name__file__img = sorted(os.listdir(path__dir__img))

    if num__max__img is not None:
        list__index__sample = list(range(len(list__name__file__img)))
        if seed is not None:
            random.seed(seed)
        random.shuffle(list__index__sample)
        list__index__sample = list__index__sample[:num__max__img]
        list__name__file__img = [list__name__file__img[_] for _ in list__index__sample]

    ls_kwargs = []
    with Pool(num__workers) as pool:  # Create Pool once and reuse it
        for i_f, name__file__img in tqdm(
            enumerate(list__name__file__img), total=len(list__name__file__img)
        ):
            name__file__lbl = os.path.splitext(name__file__img)[0] + ".json"
            path__file__lbl = os.path.join(path__dir__lbl, name__file__lbl)

            if to_draw__id_frame:
                if id_frame__from == "filename":
                    id__frame = lambda__id_frame__from(name__file__img)
            else:
                id__frame = None

            path__file__img = os.path.join(path__dir__img, name__file__img)

            ls_kwargs.append(
                dict(
                    id__frame=id__frame,
                    img__bgr=None,
                    path__file__img=path__file__img,
                    path__file__lbl=path__file__lbl,
                    name__file__img=name__file__img,
                    **kwargs,
                )
            )

            # Process batch when full or at last frame
            if output_as == "video" and (
                len(ls_kwargs) == num__workers or i_f == len(list__name__file__img) - 1
            ):
                results = pool.imap(
                    _draw_core, ls_kwargs, chunksize=1
                )  # Don't wrap with list(...) here to avoid "start-stop" pattern that block the main process to wait for the whole batch to finish
                for r in results:
                    if r is None:
                        continue
                    img__vis = r["img__vis"]

                    if writer is None:
                        imH, imW = img__vis.shape[:2]
                        writer = cv2.VideoWriter(
                            path__file__output,
                            cv2.VideoWriter_fourcc(*fourcc),
                            fps,
                            (imW, imH),
                        )

                    writer.write(img__vis)

                # Clear batch
                ls_kwargs = []

        # Process all images at once if output to imgdir
        if output_as == "imgdir":
            list(
                tqdm(
                    pool.imap(_draw_core, ls_kwargs, chunksize=1), total=len(ls_kwargs)
                )
            )

    if writer is not None:
        writer.release()


def helper__draw__video(**kwargs):
    path__file__video = kwargs["path__file__video"]
    path__dir__lbl = kwargs["path__dir__lbl"]
    output_as = kwargs.get("output_as", "video")
    path__dir__output = kwargs["path__dir__output"]
    path__file__output = kwargs["path__file__output"]
    num__pad__0 = kwargs["num__pad__0"]
    fourcc = kwargs["fourcc"]
    num__workers = kwargs["num__workers"]

    assert output_as in ["imgdir", "video"]

    if output_as == "imgdir":
        os.makedirs(path__dir__output, exist_ok=True)
    elif output_as == "video":
        os.makedirs(os.path.dirname(path__file__output), exist_ok=True)

    writer = None

    cap = cv2.VideoCapture(path__file__video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    imW = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    imH = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ls_kwargs = []
    with Pool(num__workers) as pool:
        for id__frame in tqdm(range(num_frames)):
            name__file__lbl = f"{id__frame:0{num__pad__0}d}.json"
            path__file__lbl = os.path.join(path__dir__lbl, name__file__lbl)

            success, img__bgr = cap.read()
            if not success:
                break

            ls_kwargs.append(
                dict(
                    id__frame=id__frame,
                    img__bgr=img__bgr,
                    path__file__img=None,
                    path__file__lbl=path__file__lbl,
                    name__file__img=f"{id__frame:0{num__pad__0}d}.jpg",
                    **kwargs,
                )
            )

            # Process batch when full or at last frame
            if len(ls_kwargs) == num__workers or id__frame == num_frames - 1:
                results = pool.imap(
                    _draw_core, ls_kwargs, chunksize=1
                )  # Don't wrap with list(...) here to avoid "start-stop" pattern that block the main process to wait for the whole batch to finish

                for r in results:
                    if r is None:
                        continue
                    if output_as == "video":
                        img__vis = r["img__vis"]

                        if writer is None:
                            imH, imW = img__vis.shape[:2]
                            writer = cv2.VideoWriter(
                                path__file__output,
                                cv2.VideoWriter_fourcc(*fourcc),
                                fps,
                                (imW, imH),
                            )

                        writer.write(img__vis)

                # Clear batch
                ls_kwargs = []

    cap.release()

    if writer is not None:
        writer.release()
