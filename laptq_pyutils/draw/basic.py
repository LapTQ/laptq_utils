COLORS = [
    (68, 255, 0),
    (255, 36, 125),
    (186, 0, 221),
    (79, 68, 255),
    (221, 111, 255),
    (255, 42, 4),
    (108, 27, 255),
    (0, 237, 204),
    (235, 219, 11),
    (255, 0, 189),
    (255, 100, 0),
    (243, 243, 243),
    (47, 109, 252),
    (183, 223, 0),
    (104, 31, 17),
    (255, 255, 0),
    (104, 0, 123),
    (179, 255, 1),
    (11, 255, 162),
    (0, 192, 38),
]


def cv2_imshow(img, **kwargs):
    import cv2

    window_name = kwargs.get("window_name", "show")
    flag = kwargs.get("flag", cv2.WINDOW_AUTOSIZE)
    wait = kwargs.get("wait", 0)

    cv2.namedWindow(window_name, flag)
    cv2.imshow(window_name, img)
    key = cv2.waitKey(wait)
    return key


def cv2_putText(img, text, org, **kwargs):
    import cv2

    fontFace = kwargs.get("fontFace", cv2.FONT_HERSHEY_SIMPLEX)
    fontScale = kwargs.get("fontScale", 1)
    color = kwargs.get("color", (255, 255, 255))
    thickness = kwargs.get("thickness", 1)
    lineType = kwargs.get("lineType", cv2.LINE_AA)

    x1, y1 = org
    b, g, r = color
    cv2.putText(
        img, text, (x1 + 2, y1 + 2), fontFace, fontScale, (0, 0, 0), thickness, lineType
    )
    cv2.putText(
        img,
        text,
        (x1 + 1, y1 + 1),
        fontFace,
        fontScale,
        (b // 2, g // 2, r // 2),
        thickness,
        lineType,
    )
    cv2.putText(
        img,
        text,
        (x1 + 1, y1),
        fontFace,
        fontScale,
        (b // 2, g // 2, r // 2),
        thickness,
        lineType,
    )
    cv2.putText(
        img,
        text,
        (x1, y1 + 1),
        fontFace,
        fontScale,
        (b // 2, g // 2, r // 2),
        thickness,
        lineType,
    )
    cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType)


def cv2_rectangle(img, pt1, pt2, **kwargs):
    import cv2

    color = kwargs.get("color", (255, 255, 255))
    thickness = kwargs.get("thickness", 1)
    lineType = kwargs.get("lineType", cv2.LINE_AA)

    x1, y1 = pt1
    x2, y2 = pt2
    b, g, r = color
    cv2.rectangle(
        img, (x1 + 2, y1 + 2), (x2 + 2, y2 + 2), (0, 0, 0), thickness, lineType
    )
    cv2.rectangle(
        img,
        (x1 + 1, y1 + 1),
        (x2 + 1, y2 + 1),
        (b // 2, g // 2, r // 2),
        thickness,
        lineType,
    )
    cv2.rectangle(img, pt1, pt2, color, thickness, lineType)


def cv2_circle(img, center, radius, **kwargs):
    import cv2

    color = kwargs.get("color", (255, 255, 255))
    thickness = kwargs.get("thickness", 1)
    lineType = kwargs.get("lineType", cv2.LINE_AA)

    x1, y1 = center
    b, g, r = color
    cv2.circle(img, (x1 + 2, y1 + 2), radius, (0, 0, 0), thickness, lineType)
    cv2.circle(
        img, (x1 + 1, y1 + 1), radius, (b // 2, g // 2, r // 2), thickness, lineType
    )
    cv2.circle(img, center, radius, color, thickness, lineType)


def cv2_polylines(img, pts, isClosed, **kwargs):
    import cv2

    color = kwargs.get("color", (255, 255, 255))
    thickness = kwargs.get("thickness", 1)
    lineType = kwargs.get("lineType", cv2.LINE_AA)

    b, g, r = color
    cv2.polylines(
        img,
        pts,
        isClosed,
        (0, 0, 0),
        thickness,
        lineType,
    )
    cv2.polylines(
        img,
        pts,
        isClosed,
        (b // 2, g // 2, r // 2),
        thickness // 2,
        lineType,
    )
    cv2.polylines(img, pts, isClosed, color, thickness, lineType)
