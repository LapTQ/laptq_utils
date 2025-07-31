# convert ultralytics .txt to COCO json

LS__PATHF_INPUT = [
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/train_d1_90k.txt",
    "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/valid_d1_90k.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/train_d2_110k.txt",
    "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/valid_d2_110k.txt",
]
PATHF_OUTPUT = (
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d1_90k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d1_90k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d2_110k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d2_110k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d1_90k--train_d2_110k.json"
    "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d1_90k--valid_d2_110k.json"
)


from tqdm import tqdm
from PIL import Image
import json
import os


images = []
annotations = []
categories = [
    {"supercategory": "person", "id": 0, "name": "person"},
]

count_img = 0
count_ann = 0
for pathf_input in LS__PATHF_INPUT:
    with open(pathf_input, "r") as f:
        for pathf_img in tqdm(f):
            count_img += 1
            pathf_img = pathf_img.strip()
            pathf_lbl = pathf_img.replace("images/", "labels/").replace(".jpg", ".txt")
            W, H = Image.open(pathf_img).size

            image_id = count_img
            image_info = {
                "id": image_id,
                "file_name": pathf_img,
                "width": W,
                "height": H,
            }

            images.append(image_info)

            with open(pathf_lbl, "r") as f:
                for obj in f:
                    count_ann += 1
                    id_class, xcn, ycn, wn, hn = map(eval, obj.strip().split())
                    x1n = xcn - wn / 2
                    y1n = ycn - hn / 2
                    x1 = int(x1n * W)
                    y1 = int(y1n * H)
                    w = int(wn * W)
                    h = int(hn * H)

                    annotation_id = count_ann
                    annotation_info = {
                        "id": annotation_id,
                        "category_id": id_class,
                        "iscrowd": 0,
                        "image_id": image_id,
                        "bbox": [x1, y1, w, h],
                        "area": w * h,
                        "segmentation": [],
                    }

                    annotations.append(annotation_info)

output_data = {
    "images": images,
    "annotations": annotations,
    "categories": categories,
}

os.makedirs(os.path.dirname(PATHF_OUTPUT), exist_ok=True)
with open(PATHF_OUTPUT, "w") as f:
    json.dump(output_data, f, indent=4)
