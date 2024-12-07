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
