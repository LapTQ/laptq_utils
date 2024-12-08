from laptq_pyutils.draw import cv2_putText, cv2_rectangle, cv2_circle, COLORS


def draw__image(**kwargs):
    data = kwargs["data"]
    to_draw__id_frame = kwargs.get("to_draw__id_frame", False)
    to_draw__box = kwargs.get("to_draw__box", True)
    to_draw__box_conf = kwargs.get("to_draw__box_conf", False)
    to_draw__id_track = kwargs.get("to_draw__id_track", False)
    to_draw__name_track = kwargs.get("to_draw__name_track", False)
    to_draw__id_class = kwargs.get("to_draw__id_class", False)
    to_draw__name_class = kwargs.get("to_draw__name_class", False)
    to_draw__id_action = kwargs.get("to_draw__id_action", False)
    to_draw__name_action = kwargs.get("to_draw__name_action", False)
    to_draw__box_refined = kwargs.get("to_draw__box_refined", False)
    to_draw__confirmed_status = kwargs.get("to_draw__confirmed_status", False)
    to_draw__pose = kwargs.get("to_draw__pose", False)
    to_draw__index_pose = kwargs.get("to_draw__index_pose", False)
    box_color_by = kwargs.get("box_color_by", None)
    fontScale = kwargs["fontScale"]
    thickness = kwargs["thickness"]
    map__id_class__to__name_class = kwargs.get("map__id_class__to__name_class", {})
    map__id_action__to__name_action = kwargs.get("map__id_action__to__name_action", {})

    assert box_color_by in [None, "id__track", "id__class"]

    img__bgr = data["img__bgr"].copy()
    id__frame = data.get("id__frame", None)
    list__obj__box_x1y1whn = data["list__obj__box_x1y1whn"]
    list__obj__id_track = data.get("list__obj__id_track", None)
    list__obj__name_track = data.get("list__obj__name_track", None)
    list__obj__box_conf = data.get("list__obj__box_conf", None)
    list__obj__id_class = data.get("list__obj__id_class", None)
    list__obj__action_conf = data.get("list__obj__action_conf", {})
    list__obj__action_status = data.get(
        "list__obj__action_status",
        {
            id__action: [False] * len(list__obj__box_x1y1whn)
            for id__action in list__obj__action_conf
        },
    )
    list__obj__kpts_xyn = data.get(
        "list__obj__kpts_xyn", [None] * len(list__obj__box_x1y1whn)
    )
    list__obj__kpts_conf = data.get(
        "list__obj__kpts_conf", [-1] * len(list__obj__kpts_xyn)
    )
    list__obj__box_x1y1whn_refined = data.get(
        "list__obj__box_x1y1whn_refined", [None] * len(list__obj__box_x1y1whn)
    )
    list__obj__confirmed_status = data.get(
        "list__obj__confirmed_status", [None] * len(list__obj__box_x1y1whn)
    )

    # preprocesss arguments
    if list__obj__id_track is None:
        list__obj__id_track = [-1] * len(list__obj__box_x1y1whn)  # -1 to get color
    if list__obj__name_track is None:
        list__obj__name_track = [None] * len(list__obj__box_x1y1whn)
    if list__obj__box_conf is None:
        list__obj__box_conf = [None] * len(list__obj__box_x1y1whn)
    if list__obj__id_class is None:
        list__obj__id_class = [-1] * len(list__obj__box_x1y1whn)    # -1 to get color

    H, W = img__bgr.shape[:2]

    if to_draw__id_frame and id__frame is not None:
        cv2_putText(img__bgr, str(id__frame), (10, 30))

    for i_obj, (
        box__x1y1whn,
        id__track,
        name__track,
        box__conf,
        id__class,
        box__x1y1whn__refined,
        is__confirmed,
        kpts__xyn,
        kpts__conf,
    ) in enumerate(
        zip(
            list__obj__box_x1y1whn,
            list__obj__id_track,
            list__obj__name_track,
            list__obj__box_conf,
            list__obj__id_class,
            list__obj__box_x1y1whn_refined,
            list__obj__confirmed_status,
            list__obj__kpts_xyn,
            list__obj__kpts_conf,
        )
    ):
        x1n, y1n, wn, hn = box__x1y1whn
        x1 = int(x1n * W)
        y1 = int(y1n * H)
        w = int(wn * W)
        h = int(hn * H)

        if box_color_by is None:
            color_box = COLORS[i_obj % len(COLORS)]
        elif box_color_by == "id__track":
            color_box = COLORS[id__track % len(COLORS)]
        elif box_color_by == "id__class":
            color_box = COLORS[id__class % len(COLORS)]
        else:
            raise ValueError("Invalid box_color_by: {}".format(box_color_by))

        if to_draw__box:
            cv2_rectangle(
                img__bgr,
                (x1, y1),
                (x1 + w, y1 + h),
                color=color_box,
                thickness=thickness,
            )

        if to_draw__box_refined and box__x1y1whn__refined is not None:
            rx1n, ry1n, rwn, rhn = box__x1y1whn__refined
            rx1 = int(rx1n * W)
            ry1 = int(ry1n * H)
            rw = int(rwn * W)
            rh = int(rhn * H)
            cv2_rectangle(
                img__bgr,
                (rx1, ry1),
                (rx1 + rw, ry1 + rh),
                color=color_box,
                thickness=thickness,
            )

        _has_brackets = to_draw__name_track and name__track is not None
        _has_parenthesis = (
            to_draw__confirmed_status or to_draw__id_track or _has_brackets
        ) and (to_draw__box_conf or to_draw__id_class)
        _has_dash = (to_draw__box_conf and box__conf is not None) and to_draw__id_class
        label = "{}{}{}{}{}{}{}{}{}{}".format(
            (
                "*"
                if (to_draw__confirmed_status and not is__confirmed)
                and is__confirmed is not None
                else ""
            ),
            id__track if to_draw__id_track else "",
            "[" if _has_brackets else "",
            (name__track if name__track else "") if to_draw__name_track else "",
            "]" if _has_brackets else "",
            "(" if _has_parenthesis else "",
            (
                (
                    id__class
                    if not to_draw__name_class
                    or id__class not in map__id_class__to__name_class
                    else map__id_class__to__name_class[id__class]
                )
                if to_draw__id_class
                else ""
            ),
            "-" if _has_dash else "",
            (
                "{:.2f}".format(box__conf)
                if to_draw__box_conf and box__conf is not None
                else ""
            ),
            ")" if _has_parenthesis else "",
        )
        cv2_putText(
            img__bgr,
            label,
            (x1, y1 - thickness - 10),
            color=color_box,
            fontScale=fontScale,
            thickness=thickness,
        )

        if to_draw__id_action:
            action_counter = 0
            for id__action, statuses in list__obj__action_status.items():
                status = statuses[i_obj]
                if status is True:
                    action_counter += 1
                    org = (x1 + 3, y1 + 20 * action_counter)
                    msg = (
                        str(id__action)
                        if not to_draw__name_action
                        or id__action not in map__id_action__to__name_action
                        else '"{}"'.format(map__id_action__to__name_action[id__action])
                    )
                    cv2_putText(
                        img__bgr,
                        msg,
                        org,
                        color=color_box,
                        fontScale=fontScale,
                        thickness=thickness,
                    )

        if to_draw__pose and kpts__xyn is not None:
            for i, (xn, yn) in enumerate(kpts__xyn):
                x = int(xn * W)
                y = int(yn * H)
                if x == 0 and y == 0:
                    continue
                cv2_circle(img__bgr, (x, y), 3, color=COLORS[i], thickness=-1)
                if to_draw__index_pose:
                    cv2_putText(
                        img__bgr,
                        str(i),
                        (x, y - thickness - 3),
                        color=COLORS[i % len(COLORS)],
                        fontScale=fontScale,
                        thickness=thickness,
                    )

    return img__bgr
