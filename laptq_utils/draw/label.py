from .basic import cv2_putText, cv2_rectangle, cv2_circle, COLORS


def visualize_frame(**kwargs):
    data = kwargs["data"]
    draw_frame_id = kwargs.get("draw_frame_id", True)
    draw_box = kwargs.get("draw_box", True)
    draw_conf = kwargs.get("draw_conf", False)
    draw_track_id = kwargs.get("draw_track_id", True)
    draw_track_name = kwargs.get("draw_track_name", False)
    draw_class_id = kwargs.get("draw_class_id", False)
    draw_action_id = kwargs.get("draw_action_id", False)
    draw_refined_box = kwargs.get("draw_refined_box", False)
    draw_confirmed_status = kwargs.get("draw_confirmed_status", False)
    draw_pose = kwargs.get("draw_pose", False)
    draw_pose_index = kwargs.get("draw_pose_index", False)
    fontScale = kwargs["fontScale"]
    thickness = kwargs["thickness"]
    class_id_to_label = kwargs.get("class_id_to_label", {})
    draw_class_name = kwargs.get("draw_class_name", False)
    action_id_to_label = kwargs.get("action_id_to_label", {})
    draw_action_name = kwargs.get("draw_action_name", False)
    box_color_by = kwargs.get("box_color_by", None)

    assert box_color_by in [None, "track_id", "class_id"]

    frame_img = data["frame_img"].copy()
    frame_id = data.get("frame_id", None)
    boxes_x1y1whn = data["boxes_x1y1whn"]
    track_ids = data["track_ids"]
    track_names = data.get("track_names", [None] * len(track_ids))
    boxes_conf = data.get("boxes_conf", [-1] * len(boxes_x1y1whn))
    class_ids = data["class_ids"]
    action_scores = data.get("action_scores", {})
    action_statuses = data.get(
        "action_statuses",
        {action_id: [False] * len(boxes_x1y1whn) for action_id in action_scores},
    )
    kpts_xyn = data.get("kpts_xyn", [None] * len(boxes_x1y1whn))
    kpts_conf = data.get("kpts_conf", [-1] * len(kpts_xyn))
    refined_boxes_x1y1whn = data.get(
        "refined_boxes_x1y1whn", [None] * len(boxes_x1y1whn)
    )
    confirmed_statuses = data.get("confirmed_statuses", [None] * len(boxes_x1y1whn))

    H, W = frame_img.shape[:2]

    if draw_frame_id and frame_id is not None:
        cv2_putText(frame_img, str(frame_id), (10, 30))

    for det_index, (
        box_x1y1whn,
        track_id,
        track_name,
        box_conf,
        class_id,
        refined_box_x1y1whn,
        is_confirmed,
        kpt_xyn,
        kpt_conf,
    ) in enumerate(
        zip(
            boxes_x1y1whn,
            track_ids,
            track_names,
            boxes_conf,
            class_ids,
            refined_boxes_x1y1whn,
            confirmed_statuses,
            kpts_xyn,
            kpts_conf,
        )
    ):
        x1n, y1n, wn, hn = box_x1y1whn
        x1 = int(x1n * W)
        y1 = int(y1n * H)
        w = int(wn * W)
        h = int(hn * H)

        if box_color_by is None:
            color_box = COLORS[det_index % len(COLORS)]
        elif box_color_by == "track_id":
            color_box = COLORS[track_id % len(COLORS)]
        elif box_color_by == "class_id":
            color_box = COLORS[class_id % len(COLORS)]
        else:
            raise ValueError("Invalid box_color_by: {}".format(box_color_by))

        if draw_box:
            cv2_rectangle(
                frame_img,
                (x1, y1),
                (x1 + w, y1 + h),
                color=color_box,
                thickness=thickness,
            )

        if draw_refined_box and refined_box_x1y1whn is not None:
            rx1n, ry1n, rwn, rhn = refined_box_x1y1whn
            rx1 = int(rx1n * W)
            ry1 = int(ry1n * H)
            rw = int(rwn * W)
            rh = int(rhn * H)
            cv2_rectangle(
                frame_img,
                (rx1, ry1),
                (rx1 + rw, ry1 + rh),
                color=color_box,
                thickness=thickness,
            )

        _has_parenthesis = draw_conf or draw_class_id
        _has_brackets = draw_track_name and track_name is not None
        _has_dash = draw_conf and draw_class_id
        label = "{}{}{}{}{}{}{}{}{}{}".format(
            (
                "*"
                if (draw_confirmed_status and not is_confirmed)
                and is_confirmed is not None
                else ""
            ),
            track_id if draw_track_id else "",
            "[" if _has_brackets else "",
            (track_name if track_name else "") if draw_track_name else "",
            "]" if _has_brackets else "",
            "(" if _has_parenthesis else "",
            "{:.2f}".format(box_conf) if draw_conf else "",
            "-" if _has_dash else "",
            (
                (
                    class_id
                    if not draw_class_name or class_id not in class_id_to_label
                    else class_id_to_label[class_id]
                )
                if draw_class_id
                else ""
            ),
            ")" if _has_parenthesis else "",
        )
        cv2_putText(
            frame_img,
            label,
            (x1, y1 - 10),
            color=color_box,
            fontScale=fontScale,
            thickness=thickness,
        )

        if draw_action_id:
            action_counter = 0
            for action_id, statuses in action_statuses.items():
                status = statuses[det_index]
                if status is True:
                    action_counter += 1
                    org = (x1 + 3, y1 + 20 * action_counter)
                    msg = (
                        str(action_id)
                        if not draw_action_name or action_id not in action_id_to_label
                        else '"{}"'.format(action_id_to_label[action_id])
                    )
                    cv2_putText(
                        frame_img,
                        msg,
                        org,
                        color=color_box,
                        fontScale=fontScale,
                        thickness=thickness,
                    )

        if draw_pose and kpt_xyn is not None:
            for i, (xn, yn) in enumerate(kpt_xyn):
                x = int(xn * W)
                y = int(yn * H)
                if x == 0 and y == 0:
                    continue
                cv2_circle(frame_img, (x, y), 3, color=COLORS[i], thickness=-1)
                if draw_pose_index:
                    cv2_putText(
                        frame_img,
                        str(i),
                        (x, y - 3),
                        color=COLORS[i % len(COLORS)],
                        fontScale=fontScale,
                        thickness=thickness,
                    )

    return frame_img
