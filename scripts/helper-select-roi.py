import cv2
import numpy as np
import argparse
import os
import json


def select_frame(**kwargs):
    path_video = kwargs["path_video"]
    index_frame = kwargs["index_frame"]

    cap = cv2.VideoCapture(path_video)
    index_running = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if index_running == index_frame:
            break
        index_running += 1

    return {"frame": frame}


def helper_autoimg(**kwargs):
    path_video = kwargs["path_video"]
    path_img = kwargs["path_img"]

    if path_video is not None and path_img is None:
        _ = select_frame(path_video=path_video, index_frame=0)
        img = _["frame"]
    elif path_video is None and path_img is not None:
        img = cv2.imread(path_img)
    else:
        raise ValueError("Either path_video or path_img must be provided.")

    return {"img": img}


def handler_select_polygon(event, x, y, flag, param):
    vertices = param["vertices"]
    show_img = param["show_img"]
    window_name = param["window_name"]
    thickness_point = param.get("thickness_point", 2)

    if event == cv2.EVENT_LBUTTONDOWN:
        vertices.append([x, y])
        print("Selected", vertices[-1])

        cv2.circle(
            show_img, (x, y), radius=10, color=(0, 0, 255), thickness=thickness_point
        )

        if len(vertices) >= 2:
            cv2.line(
                show_img, vertices[-2], vertices[-1], color=(0, 255, 0), thickness=2
            )

        cv2.imshow(window_name, show_img)


def select_polygon_interactive(**kwargs):
    img = kwargs["img"]
    window_name = kwargs["window_name"]
    max_points = kwargs["max_points"]
    min_points = kwargs["min_points"]
    thickness_point = kwargs.get("thickness_point", 2)

    # select polygon
    window_name = (
        window_name
        + ": <y> to submit. <ESC> to reset. <s> to skip. <q> to abort. <c> to select corners. <r> to select tlbr."
    )
    while True:
        vertices = []
        show_img = img.copy()

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, show_img)
        cv2.setMouseCallback(
            window_name,
            handler_select_polygon,
            param={
                "vertices": vertices,
                "show_img": show_img,
                "window_name": window_name,
                "thickness_point": thickness_point,
            },
        )
        key = cv2.waitKey(0)
        if key == 27:
            print("User reset")
            show_img = img.copy()
            continue
        elif key == ord("s"):
            print("User skip")
            state = "[SKIP]"
            show_img = img.copy()
            break
        elif key == ord("q"):
            print("User abort")
            show_img = img.copy()
            state = "[ABORT]"
            break
        elif key == ord("c"):
            print("User select image corner as polygon")
            vertices = [
                [0, 0],
                [img.shape[1] - 1, 0],
                [img.shape[1] - 1, img.shape[0] - 1],
                [0, img.shape[0] - 1],
            ]
            cv2.rectangle(
                show_img, vertices[0], vertices[2], color=(0, 255, 0), thickness=4
            )
            cv2.imshow(window_name, show_img)
            cv2.waitKey(1000)
            state = "[OK]"
            break
        elif key == ord("r"):
            print("User select 2 points as top-left and bottom-right.")
            if len(vertices) != 2:
                msg = "Need exactly 2 points as top-left and bottom-right."
                cv2.putText(
                    show_img,
                    msg,
                    org=(50, 100),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2,
                    color=(0, 0, 255),
                    thickness=2,
                )
                cv2.imshow(window_name, show_img)
                cv2.waitKey(1000)
                if len(vertices) > 2:
                    continue
            (x1, y1), (x2, y2) = vertices
            vertices = [
                [x1, y1],
                [x1, y2],
                [x2, y2],
                [x2, y1],
            ]
            cv2.rectangle(
                show_img, vertices[0], vertices[2], color=(0, 255, 0), thickness=4
            )
            cv2.imshow(window_name, show_img)
            cv2.waitKey(1000)
            state = "[OK]"
            break
        elif key == ord("y"):
            is_valid = True
            if min_points is not None and len(vertices) < min_points:
                is_valid = False
                msg = "Need at least {} points.".format(min_points)
            if max_points is not None and len(vertices) > max_points:
                is_valid = False
                msg = "Need at most {} points.".format(max_points)

            if not is_valid:
                cv2.putText(
                    show_img,
                    msg,
                    org=(50, 100),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2,
                    color=(0, 0, 255),
                    thickness=2,
                )
                cv2.imshow(window_name, show_img)
                cv2.waitKey(1000)
                continue

            if len(vertices) >= 2:
                cv2.line(
                    show_img, vertices[-1], vertices[0], color=(0, 255, 0), thickness=2
                )
                cv2.imshow(window_name, show_img)
                cv2.waitKey(500)
            state = "[OK]"
            break
    cv2.destroyAllWindows()

    return {"state": state, "vertices": vertices, "show_img": show_img}


def helper_select_roi(**kwargs):

    path_video = kwargs["path_video"]
    path_img = kwargs["path_img"]
    dir_output = kwargs["dir_output"]
    use_img = kwargs.get("use_img", None)

    if use_img is None:
        img = helper_autoimg(path_video=path_video, path_img=path_img)["img"]
    else:
        img = use_img.copy()

    os.makedirs(dir_output, exist_ok=True)

    # select polygon
    _ = select_polygon_interactive(
        img=img, min_points=3, max_points=None, window_name="Select polygon"
    )
    state = _["state"]
    vertices = _["vertices"]
    show_img = _["show_img"]

    assert state in ["[OK]", "[SKIP]", "[ABORT]"]

    if state == "[OK]":
        vertices = np.array(vertices, dtype="int32")

        vertices_norm = vertices.astype("float32")
        vertices_norm[:, 0] /= img.shape[1]
        vertices_norm[:, 1] /= img.shape[0]

        path_vertices = os.path.join(dir_output, "vertices.json")
        with open(path_vertices, "w") as f:
            json.dump(vertices.tolist(), f)

        path_vertices_norm = os.path.join(dir_output, "vertices_norm.json")
        with open(path_vertices_norm, "w") as f:
            json.dump(vertices_norm.tolist(), f)

        path_img_show = os.path.join(dir_output, "img_show.jpg")
        cv2.imwrite(path_img_show, show_img)

    return {
        "state": state,
        "show_img": show_img,
    }


def helper_select_anchor(**kwargs):

    path_video = kwargs["path_video"]
    path_img = kwargs["path_img"]
    dir_output = kwargs["dir_output"]
    use_img = kwargs.get("use_img", None)

    if use_img is None:
        img = helper_autoimg(path_video=path_video, path_img=path_img)["img"]
    else:
        img = use_img.copy()

    os.makedirs(dir_output, exist_ok=True)

    # select anchor point
    _ = select_polygon_interactive(
        img=img,
        min_points=1,
        max_points=1,
        window_name="Select anchor",
        thickness_point=-1,
    )
    state = _["state"]
    anchors = _["vertices"]
    show_img = _["show_img"]

    assert state in ["[OK]", "[SKIP]", "[ABORT]"]

    if state == "[OK]":
        anchors = np.array(anchors, dtype="int32")

        anchors_norm = anchors.astype("float32")
        anchors_norm[:, 0] /= img.shape[1]
        anchors_norm[:, 1] /= img.shape[0]

        path_anchors = os.path.join(dir_output, "anchors.json")
        with open(path_anchors, "w") as f:
            json.dump(anchors.tolist(), f)

        path_anchors_norm = os.path.join(dir_output, "anchors_norm.json")
        with open(path_anchors_norm, "w") as f:
            json.dump(anchors_norm.tolist(), f)

        path_img_show = os.path.join(dir_output, "img_show.jpg")
        cv2.imwrite(path_img_show, show_img)

    return {
        "state": state,
        "show_img": show_img,
    }


def helper_select_roi_and_anchor(**kwargs):

    dir_output = kwargs["dir_output"]

    _ = helper_select_roi(**kwargs)
    state = _["state"]
    show_img = _["show_img"]

    if state == "[ABORT]":
        return

    # select anchor point
    kwargs["use_img"] = show_img
    _ = helper_select_anchor(**kwargs)
    state = _["state"]
    show_img = _["show_img"]

    if state == "[ABORT]":
        return

    print("Data saved at {}".format(dir_output))


if __name__ == "__main__":

    PATHD_INPUT = "/Users/user/Downloads/extract-a-frame-from-video"
    PATHD_OUTPUT = (
        "/Users/user/Downloads/helper-select-roi"
    )

    for subpathf in [
        "R7_2025_05_15_23_40_32_rotate.mp4.jpg",
        "R8_2025_05_15_23_40_32_rotate.mp4.jpg",
        "R3_2025_05_15_23_40_32_rotate.mp4.jpg",
        "R4_2025_05_15_23_40_32_rotate.mp4.jpg",
        "R9_2025_05_15_23_40_32_rotate.mp4.jpg",
        "R10_2025_05_15_23_40_32_rotate.mp4.jpg",
    ]:
        pathf_input = os.path.join(PATHD_INPUT, subpathf)
        pathd_output = os.path.join(PATHD_OUTPUT, subpathf)

        os.makedirs(pathd_output, exist_ok=True)

        kwargs = dict(
            path_video=pathf_input,
            path_img=None,
            dir_output=pathd_output,
            use_img=None,
        )

        helper_select_roi(**kwargs)
