from .basic import cv2_putText, cv2_rectangle, cv2_circle, COLORS


def visualize_frame(
        **kwargs
):
    data = kwargs['data']
    draw_frame_id = kwargs['draw_frame_id']
    draw_box = kwargs['draw_box']
    draw_conf = kwargs.get('draw_conf', False)
    draw_track_id = kwargs['draw_track_id']
    draw_class_id = kwargs['draw_class_id']
    draw_refined_box = kwargs.get('draw_refined_box', False)
    draw_confirmed_status = kwargs.get('draw_confirmed_status', False)
    draw_pose = kwargs['draw_pose']
    fontScale = kwargs['fontScale']
    thickness = kwargs['thickness']

    frame_img = data['frame_img'].copy()
    frame_id = data['frame_id']
    boxes_x1y1whn = data['boxes_x1y1whn']
    track_ids = data['track_ids']
    boxes_conf = data.get('boxes_conf', [-1] * len(boxes_x1y1whn))
    class_ids = data['class_ids']
    kpts_xyn = data.get('kpts_xyn', [None] * len(boxes_x1y1whn))
    kpts_conf = data.get('kpts_conf', [-1] * len(kpts_xyn))
    refined_boxes_x1y1whn = data.get('refined_boxes_x1y1whn', [None] * len(boxes_x1y1whn))
    confirmed_statuses = data.get('confirmed_statuses', [None] * len(boxes_x1y1whn))

    H, W = frame_img.shape[:2]

    if draw_frame_id:
        cv2_putText(frame_img, str(frame_id), (10, 30))

    for box_x1y1whn, track_id, box_conf, class_id, refined_box_x1y1whn, is_confirmed, kpt_xyn, kpt_conf \
            in zip(boxes_x1y1whn, track_ids, boxes_conf, class_ids, refined_boxes_x1y1whn, confirmed_statuses, kpts_xyn, kpts_conf):
        x1n, y1n, wn, hn = box_x1y1whn
        x1 = int(x1n * W)
        y1 = int(y1n * H)
        w = int(wn * W)
        h = int(hn * H)

        if draw_box:
            cv2_rectangle(frame_img, (x1, y1), (x1 + w, y1 + h), color=COLORS[track_id % len(COLORS)], thickness=thickness)

        if draw_refined_box and refined_box_x1y1whn is not None:
            rx1n, ry1n, rwn, rhn = refined_box_x1y1whn
            rx1 = int(rx1n * W)
            ry1 = int(ry1n * H)
            rw = int(rwn * W)
            rh = int(rhn * H)
            cv2_rectangle(frame_img, (rx1, ry1), (rx1 + rw, ry1 + rh), color=COLORS[track_id % len(COLORS)], thickness=thickness)

        label = '{}{}{}{}{}{}{}'.format(
            '*' if (draw_confirmed_status and not is_confirmed) and is_confirmed is not None else '',
            track_id if draw_track_id else '',
            '(' if draw_conf or draw_class_id else '',
            '{:.2f}'.format(box_conf) if draw_conf else '',
            '-' if draw_conf and draw_class_id else '',
            class_id if draw_class_id else '',
            ')' if draw_conf or draw_class_id else '',
        )
        cv2_putText(frame_img, label, (x1, y1 - 10), color=COLORS[track_id % len(COLORS)], fontScale=fontScale, thickness=thickness)

        if draw_pose and kpt_xyn is not None:
            for i, (xn, yn) in enumerate(kpt_xyn):
                x = int(xn * W)
                y = int(yn * H)
                if x == 0 and y == 0:
                    continue
                cv2_circle(frame_img, (x, y), 3, color=COLORS[i], thickness=-1)
                # cv2_putText(frame_img, '{:.2f}'.format(kpt_conf[i]), (x, y), color=COLORS[i % len(COLORS)], fontScale=self.fontScale, thickness=self.thickness)

    return frame_img