COLORS = [
    # RED, YELLO, BLUE, GREEN, PUPLE
    (83, 50, 250),
    (55, 250, 250),
    (255, 221, 21),
    (102, 255, 102),
    (240, 120, 240),
    (83, 179, 36),
    (240, 120, 240),
    (51, 153, 204),
    (187, 125, 250),
    (51, 204, 255),
    (80, 83, 239),
    (59, 235, 255),
    (247, 195, 79),
    (132, 199, 129),
    (200, 104, 186),
    (53, 57, 229),
    (45, 192, 251),
    (229, 155, 3),
    (71, 160, 67),
    (176, 39, 156),
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
