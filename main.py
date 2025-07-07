from laptq_pyutils.convert import convert_onnx_to_tensorrt

from laptq_pyutils.helper import (
    helper__extract__ultralytics__imgdir,
    helper__extract__ultralytics__video,
    helper__convert__detection__json__to__txt,
    helper__convert__detection__txt__to__json,
    helper__convert__result__coco__to__json,
    helper__convert__detection__xcycwhn__to__polygonn,
    helper__convert__video__to__images,
    helper__convert__labelstudio_json__to__json,
    helper__filter__detection__result__by__conf,
    helper__filter__detection__result__by__id_class,
    helper__filter__detection__result__by__miniou,
    helper__filter__detection__result__by__size,
    helper__filter__detection__result__by__roi,
    helper__filter__image__by__id_class,
    helper__change__detection__id_class,
    helper__draw__imgdir,
    helper__draw__video,
    helper__rescale__detection__box,
    helper__erase__classes__on__images,
    helper__check__duplicate__images,
    helper__cluster__detection__bboxes,
    helper__extract__crops__with__mask__from__segmentation,
    helper__paste__seg_crops__over__det_boxes,
    helper__paste__seg_crops__over__background,
    helper__merge__detection__result,
    helper__extract__crops__from__detection,
)
import argparse


def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument("action")
    ap.add_argument("--path__dir__img", type=str)
    ap.add_argument("--path__dir__img__input", type=str)
    ap.add_argument("--path__dir__img__output", type=str)
    ap.add_argument("--path__dir__lbl", type=str)
    ap.add_argument("--path__dir__output", type=str)
    ap.add_argument("--path__dir__lbl__input", type=str)
    ap.add_argument("--path__dir__lbl__output", type=str)
    ap.add_argument("--path__dir__crop__img__input", type=str)
    ap.add_argument("--path__dir__crop__img__output", type=str)
    ap.add_argument("--path__dir__crop__mask__input", type=str)
    ap.add_argument("--path__dir__crop__mask__output", type=str)
    ap.add_argument("--path__dir__crop__lbl__input", type=str)
    ap.add_argument("--path__dir__crop__lbl__output", type=str)
    ap.add_argument("--path__file__img", type=str)
    ap.add_argument("--path__file__input", type=str)
    ap.add_argument("--path__file__video__input", type=str)
    ap.add_argument("--path__file__lbl__input", type=str)
    ap.add_argument("--path__file__lbl__output", type=str)
    ap.add_argument("--path__file__output", type=str)
    ap.add_argument("--path__file__model", type=str)
    ap.add_argument("--list__path__dir__lbl__input", type=str)  # sep by ,
    ap.add_argument("--device", type=str)
    ap.add_argument("--imgsz", type=int)
    ap.add_argument("--map__id_class__to__thresh_conf", type=str)
    ap.add_argument("--list__id_class__to_include", type=str)
    ap.add_argument("--list__id_class__to_exclude", type=str)
    ap.add_argument("--list__id_class", type=str)
    ap.add_argument("--map__id_old__to__id_new", type=str)
    ap.add_argument("--thresh", type=float)
    ap.add_argument("--thresh__iou", type=float)
    ap.add_argument("--thresh__miniou", type=float)
    ap.add_argument("--thresh__conf__min", type=float)
    ap.add_argument("--thresh__leftiou__min", type=float)
    ap.add_argument("--thresh__leftiou__max", type=float)
    ap.add_argument("--concat__axis", type=int)
    ap.add_argument("--to_concat__original_img", type=str)
    ap.add_argument("--to_draw__id_frame", type=str)
    ap.add_argument("--to_draw__box_x1y1whn", type=str)
    ap.add_argument("--to_draw__box_polygonn", type=str)
    ap.add_argument("--to_draw__id_track", choices=["True", "False"])
    ap.add_argument("--to_draw__box_conf", choices=["True", "False"])
    ap.add_argument("--to_draw__id_class", choices=["True", "False"])
    ap.add_argument("--to_draw__name_class", choices=["True", "False"])
    ap.add_argument("--to_draw__pose", choices=["True", "False"])
    ap.add_argument("--to_draw__id_action", choices=["True", "False"])
    ap.add_argument("--to_draw__name_action", choices=["True", "False"])
    ap.add_argument("--to_draw__action_conf", choices=["True", "False"])
    ap.add_argument("--to_save__img", type=str)
    ap.add_argument("--fontScale", type=float)
    ap.add_argument("--thickness", type=int)
    ap.add_argument("--box_color_by", type=str)
    ap.add_argument("--num", type=int)
    ap.add_argument("--num__max__img", type=str)
    ap.add_argument("--num__max__box", type=str)
    ap.add_argument("--num__pad__0", type=int)
    ap.add_argument("--num__steps", type=int)
    ap.add_argument("--seed", type=str)
    ap.add_argument("--is_ok__lbl_not_exist", type=str)
    ap.add_argument("--is_ok__key_not_exist", type=str)
    ap.add_argument("--fourcc", type=str)
    ap.add_argument("--path__file__map__id_class__to__name_class", type=str)
    ap.add_argument("--path__file__map__id_action__to__name_action", type=str)
    ap.add_argument("--filter_by", type=str)
    ap.add_argument("--ratio__w", type=float)
    ap.add_argument("--ratio__h", type=float)
    ap.add_argument("--margin__xn", type=float)
    ap.add_argument("--margin__yn", type=float)
    ap.add_argument("--pad__w__max", type=str)
    ap.add_argument("--pad__h__max", type=str)
    ap.add_argument("--cut__w__max", type=str)
    ap.add_argument("--cut__h__max", type=str)
    ap.add_argument("--mode__box", type=str)
    ap.add_argument("--offset__id_class", type=int)
    ap.add_argument("--n_clusters", type=int)
    ap.add_argument("--prob", type=float)
    ap.add_argument("--method", type=str)
    ap.add_argument("--flags", type=str)
    ap.add_argument("--roi__polygonn", type=str)
    ap.add_argument("--to_use__yolov5_compat", type=str)
    ap.add_argument("--precision", type=str)
    ap.add_argument("--dynamic_shape", type=str)
    ap.add_argument("--max_workspace_size", type=int)
    ap.add_argument("--list__name_keypoints", type=str)
    ap.add_argument("--task", type=str)
    ap.add_argument("--to_keep__only_max", type=str)
    ap.add_argument("--to_draw__connected_keypoints", type=str)
    ap.add_argument("--list__keypoints_same_color", type=str)
    ap.add_argument("--list__keypoints_edge", type=str)
    ap.add_argument("--list__edges_same_color", type=str)
    ap.add_argument("--persist", type=str)
    ap.add_argument("--split_by", type=str)
    ap.add_argument("--thresh__conf__keypoints__min", type=float)
    ap.add_argument("--to_resize_box__wrt__pose", type=str, choices=["True", "False"])
    ap.add_argument("--to_shift__coords__wrt__box", type=str, choices=["True", "False"])
    ap.add_argument("--id_frame__from", type=str)
    ap.add_argument("--lambda__id_frame__from", type=str)
    ap.add_argument("--step_size", type=int)
    ap.add_argument("--color", type=str)

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
    args.pad__w__max = eval(args.pad__w__max) if args.pad__w__max is not None else None
    args.pad__h__max = eval(args.pad__h__max) if args.pad__h__max is not None else None
    args.cut__w__max = eval(args.cut__w__max) if args.cut__w__max is not None else None
    args.cut__h__max = eval(args.cut__h__max) if args.cut__h__max is not None else None
    args.to_concat__original_img = (
        eval(args.to_concat__original_img)
        if args.to_concat__original_img is not None
        else None
    )

    args.to_draw__box_x1y1whn = (
        eval(args.to_draw__box_x1y1whn)
        if args.to_draw__box_x1y1whn is not None
        else None
    )
    args.to_draw__box_polygonn = (
        eval(args.to_draw__box_polygonn)
        if args.to_draw__box_polygonn is not None
        else None
    )
    args.num__max__box = (
        eval(args.num__max__box) if args.num__max__box is not None else None
    )
    args.to_draw__id_frame = (
        eval(args.to_draw__id_frame) if args.to_draw__id_frame is not None else None
    )
    args.to_save__img = (
        eval(args.to_save__img) if args.to_save__img is not None else None
    )
    args.roi__polygonn = (
        eval(args.roi__polygonn) if args.roi__polygonn is not None else None
    )
    args.to_use__yolov5_compat = (
        eval(args.to_use__yolov5_compat)
        if args.to_use__yolov5_compat is not None
        else None
    )
    args.is_ok__key_not_exist = (
        eval(args.is_ok__key_not_exist)
        if args.is_ok__key_not_exist is not None
        else None
    )
    args.list__path__dir__lbl__input = (
        args.list__path__dir__lbl__input.split(",")
        if args.list__path__dir__lbl__input is not None
        else None
    )
    args.dynamic_shape = (
        eval(args.dynamic_shape) if args.dynamic_shape is not None else None
    )
    args.list__name_keypoints = (
        eval(args.list__name_keypoints)
        if args.list__name_keypoints is not None
        else None
    )
    args.to_draw__pose = (
        eval(args.to_draw__pose) if args.to_draw__pose is not None else None
    )
    args.to_keep__only_max = (
        eval(args.to_keep__only_max) if args.to_keep__only_max is not None else None
    )
    args.to_draw__connected_keypoints = (
        eval(args.to_draw__connected_keypoints)
        if args.to_draw__connected_keypoints is not None
        else None
    )
    args.list__keypoints_same_color = (
        eval(args.list__keypoints_same_color)
        if args.list__keypoints_same_color is not None
        else None
    )
    args.list__keypoints_edge = (
        eval(args.list__keypoints_edge)
        if args.list__keypoints_edge is not None
        else None
    )
    args.list__edges_same_color = (
        eval(args.list__edges_same_color)
        if args.list__edges_same_color is not None
        else None
    )
    args.persist = eval(args.persist) if args.persist is not None else None
    args.to_draw__id_action = (
        eval(args.to_draw__id_action) if args.to_draw__id_action is not None else None
    )
    args.to_draw__name_action = (
        eval(args.to_draw__name_action)
        if args.to_draw__name_action is not None
        else None
    )
    args.to_draw__action_conf = (
        eval(args.to_draw__action_conf)
        if args.to_draw__action_conf is not None
        else None
    )
    args.split_by = eval(args.split_by) if args.split_by is not None else None
    args.to_resize_box__wrt__pose = (
        eval(args.to_resize_box__wrt__pose)
        if args.to_resize_box__wrt__pose is not None
        else None
    )
    args.to_shift__coords__wrt__box = (
        eval(args.to_shift__coords__wrt__box)
        if args.to_shift__coords__wrt__box is not None
        else None
    )
    args.lambda__id_frame__from = (
        eval(args.lambda__id_frame__from)
        if args.lambda__id_frame__from is not None
        else None
    )
    args.color = (
        eval(args.color)
        if args.color is not None
        else None
    )

    return args


if __name__ == "__main__":
    args = parse_args()
    kwargs = vars(args)

    # pprint_color(kwargs)

    exec("{}(**kwargs)".format(kwargs["action"]))
