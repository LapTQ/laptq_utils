from pathlib import Path
import sys

HERE = Path(__file__).parent
ROOT_DIR = HERE
sys.path.append(str(ROOT_DIR))

from laptq_utils import *

# ==============================================================================

import argparse


def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "action",
        choices=[
            "helper__visualize__detection",
            "helper__remove__small__boxes",
            "helper__remove__images__containing__classes",
            "helper__check__duplicate__images",
            "helper__predict__yolo__detect"
        ],
    )

    ap.add_argument("--path__dir__img", type=str)
    ap.add_argument("--path__dir__label", type=str)
    ap.add_argument("--path__dir__output", type=str)
    ap.add_argument("--path__file__input", type=str)
    ap.add_argument("--path__file__output", type=str)
    ap.add_argument("--draw_track_id", choices=["True", "False"])
    ap.add_argument("--draw_conf", choices=["True", "False"])
    ap.add_argument("--draw_class_id", choices=["True", "False"])
    ap.add_argument("--draw_class_name", choices=["True", "False"])
    ap.add_argument("--path__file__class_id_to_label", type=str)
    ap.add_argument("--fontScale", type=float)
    ap.add_argument("--thickness", type=int)
    ap.add_argument("--box_color_by", type=str)
    ap.add_argument("--num__max__img", type=str)
    ap.add_argument("--thresh__area__min", type=float)
    ap.add_argument("--list__id_class", type=str)
    ap.add_argument("--method", type=str)
    ap.add_argument("--max_distance_threshold", type=int)
    ap.add_argument("--to__plot", choices=["True", "False"])
    ap.add_argument("--cls_loader", choices=["LoaderVideo"])
    ap.add_argument("--path__file__checkpoint", type=str)
    ap.add_argument("--device", type=str)
    ap.add_argument("--imgsz", type=int)
    ap.add_argument("--list__conf", type=str)
    ap.add_argument("--thresh__conf_min", type=float)
    ap.add_argument("--to__filterby__miniou", type=str)
    ap.add_argument("--thresh__miniou", type=float)

    args = ap.parse_args()

    args.draw_track_id = (
        eval(args.draw_track_id) if args.draw_track_id is not None else None
    )
    args.draw_conf = eval(args.draw_conf) if args.draw_conf is not None else None
    args.draw_class_id = (
        eval(args.draw_class_id) if args.draw_class_id is not None else None
    )
    args.draw_class_name = (
        eval(args.draw_class_name) if args.draw_class_name is not None else None
    )
    args.num__max__img = (
        eval(args.num__max__img) if args.num__max__img is not None else None
    )
    args.list__id_class = eval(args.list__id_class) if args.list__id_class is not None else None
    args.to__plot = eval(args.to__plot) if args.to__plot is not None else None
    args.list__conf = eval(args.list__conf) if args.list__conf is not None else None
    args.to__filterby__miniou = (
        eval(args.to__filterby__miniou) if args.to__filterby__miniou is not None else None
    )

    return args


if __name__ == "__main__":
    args = parse_args()
    kwargs = vars(args)

    # pprint_color(kwargs)

    exec("{}(**kwargs)".format(kwargs["action"]))
