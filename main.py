from laptq_pyutils.helper import (
    helper__extract__ultralytics__detect__imgdir,
    helper__extract__ultralytics__detect__video,
    helper__convert__detection__json__to__txt,
    helper__convert__detection__txt__to__json,
    helper__filter__detection__result__by__conf,
    helper__filter__detection__result__by__id_class,
    helper__filter__detection__result__by__miniou,
    helper__filter__detection__result__by__size,
    helper__filterout__image__by__id_class,
    helper__change__detection__id_class,
    helper__draw__detection__imgdir,
    helper__draw__detection__video,
)
import argparse


def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument("action")
    ap.add_argument("--path__dir__img", type=str)
    ap.add_argument("--path__dir__img__output", type=str)
    ap.add_argument("--path__dir__lbl", type=str)
    ap.add_argument("--path__dir__output", type=str)
    ap.add_argument("--path__dir__lbl__input", type=str)
    ap.add_argument("--path__dir__lbl__output", type=str)
    ap.add_argument("--path__file__img", type=str)
    ap.add_argument("--path__file__input", type=str)
    ap.add_argument("--path__file__video__input", type=str)
    ap.add_argument("--path__file__lbl__input", type=str)
    ap.add_argument("--path__file__lbl__output", type=str)
    ap.add_argument("--path__file__output", type=str)
    ap.add_argument("--path__file__model", type=str)
    ap.add_argument("--device", type=str)
    ap.add_argument("--imgsz", type=int)
    ap.add_argument("--map__id_class__to__thresh_conf", type=str)
    ap.add_argument("--thresh__conf__min", type=float)
    ap.add_argument("--list__id_class__to_include", type=str)
    ap.add_argument("--list__id_class__to_exclude", type=str)
    ap.add_argument("--map__id_old__to__id_new", type=str)
    ap.add_argument("--thresh__miniou", type=float)
    ap.add_argument("--to_draw__id_track", choices=["True", "False"])
    ap.add_argument("--to_draw__box_conf", choices=["True", "False"])
    ap.add_argument("--to_draw__id_class", choices=["True", "False"])
    ap.add_argument("--to_draw__name_class", choices=["True", "False"])
    ap.add_argument("--fontScale", type=float)
    ap.add_argument("--thickness", type=int)
    ap.add_argument("--box_color_by", type=str)
    ap.add_argument("--num__max__img", type=str)
    ap.add_argument("--seed", type=str)
    ap.add_argument("--is_ok__lbl_not_exist", type=str)
    ap.add_argument("--pad__id_frame", type=int)
    ap.add_argument("--fourcc", type=str)
    ap.add_argument("--path__file__map__id_class__to__name_class", type=str)
    ap.add_argument("--filter_by", type=str)
    ap.add_argument("--thresh", type=float)
    ap.add_argument("--list__id_class", type=str)

    ap.add_argument("--method", type=str)
    ap.add_argument("--max_distance_threshold", type=int)
    ap.add_argument("--to__plot", choices=["True", "False"])

    args = ap.parse_args()

    args.to_draw__id_track = (
        eval(args.to_draw__id_track) if args.to_draw__id_track is not None else None
    )
    args.to_draw__box_conf = (
        eval(args.to_draw__box_conf) if args.to_draw__box_conf is not None else None
    )
    args.to_draw__id_class = (
        eval(args.to_draw__id_class) if args.to_draw__id_class is not None else None
    )
    args.to_draw__name_class = (
        eval(args.to_draw__name_class) if args.to_draw__name_class is not None else None
    )
    args.num__max__img = (
        eval(args.num__max__img) if args.num__max__img is not None else None
    )
    args.list__id_class = (
        eval(args.list__id_class) if args.list__id_class is not None else None
    )
    args.to__plot = eval(args.to__plot) if args.to__plot is not None else None
    args.map__id_class__to__thresh_conf = (
        eval(args.map__id_class__to__thresh_conf)
        if args.map__id_class__to__thresh_conf is not None
        else None
    )
    args.list__id_class__to_include = (
        eval(args.list__id_class__to_include)
        if args.list__id_class__to_include is not None
        else None
    )
    args.list__id_class__to_exclude = (
        eval(args.list__id_class__to_exclude)
        if args.list__id_class__to_exclude is not None
        else None
    )
    args.map__id_old__to__id_new = (
        eval(args.map__id_old__to__id_new)
        if args.map__id_old__to__id_new is not None
        else None
    )
    args.seed = eval(args.seed) if args.seed is not None else None
    args.is_ok__lbl_not_exist = (
        eval(args.is_ok__lbl_not_exist)
        if args.is_ok__lbl_not_exist is not None
        else None
    )

    return args


if __name__ == "__main__":
    args = parse_args()
    kwargs = vars(args)

    # pprint_color(kwargs)

    exec("{}(**kwargs)".format(kwargs["action"]))
