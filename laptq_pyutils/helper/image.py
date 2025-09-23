from laptq_pyutils.objects import CLIPFeatureExtractor
from laptq_pyutils.ops import compute_batched_pairwise_torch


def helper__convert__video__to__images(**kwargs):

    import cv2
    import os
    from tqdm import tqdm

    path__file__input = kwargs["path__file__input"]
    path__dir__img__output = kwargs["path__dir__img__output"]
    num__pad__0 = kwargs["num__pad__0"]
    step_size = kwargs["step_size"]

    cap = cv2.VideoCapture(path__file__input)
    os.makedirs(path__dir__img__output, exist_ok=True)

    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    id__frame = -1
    while True:
        success, img__bgr = cap.read()
        if not success:
            break
        id__frame += 1

        name__file__img = f"{id__frame:0{num__pad__0}d}.jpg"
        path__file__img = os.path.join(path__dir__img__output, name__file__img)

        if id__frame % step_size != 0:
            pbar.update(1)
            continue

        cv2.imwrite(path__file__img, img__bgr)

        pbar.update(1)


def helper__extract__image__embedding(**kwargs):
    import os
    from tqdm import tqdm
    import cv2
    import numpy as np

    path__dir__input = kwargs["path__dir__input"]
    path__dir__output = kwargs["path__dir__output"]
    to_gray = kwargs["to_gray"]
    to_normalize = kwargs["to_normalize"]

    os.makedirs(path__dir__output, exist_ok=True)

    model = CLIPFeatureExtractor(**kwargs)

    for namef_img in tqdm(
        sorted(os.listdir(path__dir__input)), desc="Extracting features"
    ):
        pathf_img = os.path.join(path__dir__input, namef_img)

        img__bgr = cv2.imread(pathf_img)

        if img__bgr is None:
            continue

        if to_gray:
            img__bgr = cv2.cvtColor(img__bgr, cv2.COLOR_BGR2GRAY)
            img__bgr = cv2.cvtColor(img__bgr, cv2.COLOR_GRAY2BGR)  # Convert back

        _ = model.predict(img__bgr=img__bgr)
        image_feature = _["image_feature"]

        # normalize
        if to_normalize:
            image_feature = image_feature / np.linalg.norm(image_feature)

        namef_output = os.path.splitext(namef_img)[0] + ".npy"
        np.save(os.path.join(path__dir__output, namef_output), image_feature)


def helper__cluster__images__by__embeddings(**kwargs):
    import os
    import torch
    from torch.nn.functional import cosine_similarity
    import numpy as np
    from tqdm import tqdm
    from sklearn.cluster import AgglomerativeClustering
    import json

    list__path__dir__img__input = kwargs["list__path__dir__img__input"]
    list__path__dir__emb__input = kwargs["list__path__dir__emb__input"]
    path__dir__output = kwargs["path__dir__output"]
    device = kwargs["device"]
    batch_size = kwargs["batch_size"]
    linkage = kwargs["linkage"]
    thresh__similarity = kwargs["thresh__similarity"]

    assert len(list__path__dir__img__input) == len(
        list__path__dir__emb__input
    ), "Number of input image folders and embeddings folders must be the same. Got {} and {}.".format(
        len(list__path__dir__img__input), len(list__path__dir__emb__input)
    )

    os.makedirs(path__dir__output, exist_ok=True)

    list__pathf_img = []
    list__pathf_emb = []
    for pathd_img, pathd_emb in tqdm(
        zip(list__path__dir__img__input, list__path__dir__emb__input)
    ):
        for namef_img in sorted(os.listdir(pathd_img)):
            namef_emb = os.path.splitext(namef_img)[0] + ".npy"

            pathf_img = os.path.join(pathd_img, namef_img)
            pathf_emb = os.path.join(pathd_emb, namef_emb)

            if not os.path.isfile(pathf_emb):
                raise FileNotFoundError(f"Embedding file not found: {pathf_emb}")

            list__pathf_img.append(pathf_img)
            list__pathf_emb.append(pathf_emb)

    embeddings = []
    for pathf_emb in tqdm(list__pathf_emb, desc="Loading embeddings"):
        emb = np.load(pathf_emb)
        embeddings.append(emb)

    embeddings = torch.tensor(np.array(embeddings), dtype=torch.float32).to(device)

    distances = 1 - compute_batched_pairwise_torch(
        input_1=embeddings,
        input_2=embeddings,
        op=cosine_similarity,
        op_kwargs=dict(dim=2),
        batch_size=batch_size,
        to_cpu=True,
        to_numpy=True,
    )

    hac = AgglomerativeClustering(
        n_clusters=None,
        metric="precomputed",
        linkage=linkage,
        distance_threshold=1 - thresh__similarity,
    )

    cluster_labels = hac.fit_predict(distances)
    unique_clusters = np.unique(cluster_labels)

    ret = []
    for cluster_id in tqdm(unique_clusters):
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        cluster_pathf_img = [list__pathf_img[i] for i in cluster_indices]
        ret.append(cluster_pathf_img)

    pathf_output = os.path.join(path__dir__output, "cluster_image_paths.json")
    with open(pathf_output, "w") as f:
        json.dump(ret, f, indent=4)
