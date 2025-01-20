from laptq_pyutils.algo import KMeans


def box__iou(boxes1, boxes2):

    import numpy as np

    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])

    boxes1 = boxes1.reshape(-1, 1, 4)
    boxes2 = boxes2.reshape(1, -1, 4)

    x1 = np.maximum(boxes1[..., 0], boxes2[..., 0])
    y1 = np.maximum(boxes1[..., 1], boxes2[..., 1])
    x2 = np.minimum(boxes1[..., 2], boxes2[..., 2])
    y2 = np.minimum(boxes1[..., 3], boxes2[..., 3])

    w = np.maximum(0, x2 - x1)
    h = np.maximum(0, y2 - y1)
    inter = w * h

    area1 = area1.reshape(-1, 1)
    area2 = area2.reshape(1, -1)
    area_sum = area1 + area2
    union = area_sum - inter

    iou = inter / union

    return iou


def box__leftiou(boxes1, boxes2):

    import numpy as np

    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])

    boxes1 = boxes1.reshape(-1, 1, 4)
    boxes2 = boxes2.reshape(1, -1, 4)

    x1 = np.maximum(boxes1[..., 0], boxes2[..., 0])
    y1 = np.maximum(boxes1[..., 1], boxes2[..., 1])
    x2 = np.minimum(boxes1[..., 2], boxes2[..., 2])
    y2 = np.minimum(boxes1[..., 3], boxes2[..., 3])

    w = np.maximum(0, x2 - x1)
    h = np.maximum(0, y2 - y1)
    inter = w * h

    area1 = area1.reshape(-1, 1)

    iou = inter / area1

    return iou


def box__miniou(boxes1, boxes2):

    import numpy as np

    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])

    boxes1 = boxes1.reshape(-1, 1, 4)
    boxes2 = boxes2.reshape(1, -1, 4)

    x1 = np.maximum(boxes1[..., 0], boxes2[..., 0])
    y1 = np.maximum(boxes1[..., 1], boxes2[..., 1])
    x2 = np.minimum(boxes1[..., 2], boxes2[..., 2])
    y2 = np.minimum(boxes1[..., 3], boxes2[..., 3])

    w = np.maximum(0, x2 - x1)
    h = np.maximum(0, y2 - y1)
    inter = w * h

    area1 = area1.reshape(-1, 1)
    area2 = area2.reshape(1, -1)
    area_min = np.minimum(area1, area2)

    miniou = inter / area_min

    return miniou


def xcycwh__to__x1y1x2y2(xcycwh):

    x1y1x2y2 = xcycwh.copy()
    x1y1x2y2[:, 0] = xcycwh[:, 0] - xcycwh[:, 2] / 2
    x1y1x2y2[:, 1] = xcycwh[:, 1] - xcycwh[:, 3] / 2
    x1y1x2y2[:, 2] = xcycwh[:, 0] + xcycwh[:, 2] / 2
    x1y1x2y2[:, 3] = xcycwh[:, 1] + xcycwh[:, 3] / 2

    return x1y1x2y2


def xcycwh__to__x1y1wh(xcycwh):

    x1y1wh = xcycwh.copy()
    x1y1wh[:, 0] = xcycwh[:, 0] - xcycwh[:, 2] / 2
    x1y1wh[:, 1] = xcycwh[:, 1] - xcycwh[:, 3] / 2
    x1y1wh[:, 2] = xcycwh[:, 2]
    x1y1wh[:, 3] = xcycwh[:, 3]

    return x1y1wh


def x1y1wh__to__xcycwh(x1y1wh):

    xcycwh = x1y1wh.copy()
    xcycwh[:, 0] = x1y1wh[:, 0] + x1y1wh[:, 2] / 2
    xcycwh[:, 1] = x1y1wh[:, 1] + x1y1wh[:, 3] / 2
    xcycwh[:, 2] = x1y1wh[:, 2]
    xcycwh[:, 3] = x1y1wh[:, 3]

    return xcycwh


def x1y1wh__to__x1y1x2y2(x1y1wh):

    x1y1x2y2 = x1y1wh.copy()
    x1y1x2y2[:, 2] = x1y1wh[:, 0] + x1y1wh[:, 2]
    x1y1x2y2[:, 3] = x1y1wh[:, 1] + x1y1wh[:, 3]

    return x1y1x2y2


def x1y1x2y2__to__polygon(x1y1x2y2):

    x1y1x2y2 = x1y1x2y2.copy()

    return x1y1x2y2[:, [0, 1, 0, 3, 2, 3, 2, 1]]


def xcycwh__to__polygon(xcycwh):

    xcycwh = xcycwh.copy()
    polygon = x1y1x2y2__to__polygon(xcycwh__to__x1y1x2y2(xcycwh=xcycwh))

    return polygon


def box_normalized__to__box_pixels(box, WH):
    W, H = WH
    return (box * [W, H, W, H]).astype(int)


def box_pixels__to__box_normalized(box, WH):
    W, H = WH
    return box / [W, H, W, H]


def cluster__detection__boxes(**kwargs):

    import numpy as np

    list__wh = kwargs["list__wh"]
    n_clusters = kwargs["n_clusters"]

    xc = list__wh[:, 0].max() / 2
    yc = list__wh[:, 1].max() / 2
    list__xcyc = np.full_like(list__wh, [xc, yc])
    list__xcycwh = np.concatenate([list__xcyc, list__wh], axis=1)

    kmeans = KMeans(
        n_clusters=n_clusters,
        fn__distance=lambda _x, _y: 1
        - box__iou(
            xcycwh__to__x1y1x2y2(_x),
            xcycwh__to__x1y1x2y2(_y),
        ),
        fn__update_centroids=lambda _x: [xc, yc, *np.mean(_x, axis=0)[2:]],
        random_state=42,
    ).fit(list__xcycwh)

    cluster_centers_ = kmeans.cluster_centers_
    list__anchor_box__wh = cluster_centers_[:, 2:].astype(int).tolist()

    return list__anchor_box__wh
