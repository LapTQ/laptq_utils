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
        ],
    )

    ap.add_argument("--path__dir__img", type=str)
    ap.add_argument("--path__dir__annot", type=str)
    ap.add_argument("--path__dir__output", type=str)
    ap.add_argument("--draw_track_id", choices=["True", "False"])
    ap.add_argument("--draw_conf", choices=["True", "False"])
    ap.add_argument("--draw_class_id", choices=["True", "False"])
    ap.add_argument("--draw_class_name", choices=["True", "False"])
    ap.add_argument("--path__file__class_id_to_label", type=str)
    ap.add_argument("--fontScale", type=float)
    ap.add_argument("--thickness", type=int)
    ap.add_argument("--box_color_by", type=str)

    args = ap.parse_args()

    args.draw_track_id = eval(args.draw_track_id)
    args.draw_conf = eval(args.draw_conf)
    args.draw_class_id = eval(args.draw_class_id)
    args.draw_class_name = eval(args.draw_class_name)

    return args


if __name__ == "__main__":
    args = parse_args()
    kwargs = vars(args)

    # pprint_color(kwargs)

    exec("{}(**kwargs)".format(kwargs["action"]))
