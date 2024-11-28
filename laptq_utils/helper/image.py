import os
import json
import csv


def helper__check__duplicate__images(**kwargs):
    from imagededup.methods import PHash, DHash, WHash, AHash
    from imagededup.utils import plot_duplicates

    path__dir__img = kwargs["path__dir__img"]
    path__dir__output = kwargs["path__dir__output"]
    method = kwargs["method"]
    max_distance_threshold = kwargs[
        "max_distance_threshold"
    ]  # hamming distance, used in methods based on hashing. Should be an int between 0 and 64. Default value is 10
    to__plot = kwargs["to__plot"]

    encoder = eval(method)()

    os.makedirs(path__dir__output, exist_ok=True)

    path__file__duplicates = os.path.join(path__dir__output, "duplicates.json")
    path__file__duplicates_to_remove = os.path.join(
        path__dir__output, "duplicates_to_remove.json"
    )

    encodings = encoder.encode_images(image_dir=path__dir__img)
    duplicates = encoder.find_duplicates(
        encoding_map=encodings,
        scores=True,
        max_distance_threshold=max_distance_threshold,
        outfile=path__file__duplicates,
    )

    duplicates_to_remove = encoder.find_duplicates_to_remove(
        encoding_map=encodings,
        max_distance_threshold=max_distance_threshold,
        outfile=path__file__duplicates_to_remove,
    )

    path__file__duplicates_to_remove__no_json = os.path.join(
        path__dir__output, "duplicates_to_remove__no_json.txt"
    )
    with open(path__file__duplicates_to_remove__no_json, "w") as f:
        writer = csv.writer(f, delimiter=" ")
        for name__file in duplicates_to_remove:
            writer.writerow([name__file])

    originals_to_keep = list(
        set(os.listdir(path__dir__img)).difference(set(duplicates_to_remove))
    )
    path__file__originals_to_keep = os.path.join(
        path__dir__output, "originals_to_keep.json"
    )
    with open(path__file__originals_to_keep, "w") as f:
        json.dump(originals_to_keep, f, indent=2)

    path__file__originals_to_keep__no_json = os.path.join(
        path__dir__output, "originals_to_keep__no_json.txt"
    )
    with open(path__file__originals_to_keep__no_json, "w") as f:
        writer = csv.writer(f, delimiter=" ")
        for name__file in originals_to_keep:
            writer.writerow([name__file])

    if to__plot:
        path__dir__output__plot = os.path.join(path__dir__output, "plot_duplicates")
        os.makedirs(path__dir__output__plot, exist_ok=True)
        for name__img__key, list__img__duplicated in duplicates.items():
            if len(list__img__duplicated) == 0:
                continue

            plot_duplicates(
                image_dir=path__dir__img,
                duplicate_map=duplicates,
                filename=name__img__key,
                outfile=os.path.join(path__dir__output__plot, name__img__key),
            )
