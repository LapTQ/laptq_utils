# convert ultralytics .txt to COCO json

LS__PATHF_INPUT = [
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/train_d1_90k.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/valid_d1_90k.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/train_d2_110k.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/valid_d2_110k.txt",
    # "/home/lap_awlv/laptq-nedo-fed/outputs/trivials/toy_dataset.txt"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/trivials/toy_dataset2.txt"
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/train_d6_cam1.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/valid_d6_cam1.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/train_d6_cam2.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/valid_d6_cam2.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/train_d3.1_32k.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/train_d32.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/valid_d3.1_32k.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch1/data/valid_d32.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/train_d3-satudora.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/test_d3-satudora.txt"
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch2/D5_May_cam1.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/batch2/D5_May_cam2.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/train_d7_cam1.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/valid_d7_cam1.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/train_d7_cam2.txt",
    # "/home/lap_awlv/laptq-nedo-fed/data/detection_people_pseudo/data/valid_d7_cam2.txt",
    # "/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/locount_train.txt",
    "/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/locount_val.txt",
    # "/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/sku_train.txt",
    "/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/sku_val.txt",

]
PATHF_OUTPUT = (
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d1_90k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d1_90k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d2_110k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d2_110k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d1_90k--train_d2_110k.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/toy.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/toy2.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d1_90k--train_d6_cam1.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d1_90k--valid_d6_cam1.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d2_110k--train_d6_cam2.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d2_110k--valid_d6_cam2.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/train_d1_90k--train_d2_110k--train_d6_cam1--train_d6_cam2.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/valid_d1_90k--valid_d2_110k--valid_d6_cam1--valid_d6_cam2.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/d3.1--d3.2.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/d3-satudora.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/d5.1--d5.2.json"
    # "/home/lap_awlv/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/d7.1--d7.2.json"
    # "/home/pocuser2/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/locount_train.json"
    # "/home/pocuser2/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/locount_val.json"
    # "/home/pocuser2/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/sku_train.json"
    # "/home/pocuser2/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/sku_val.json"
    # "/home/pocuser2/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/sku_train--locount_train.json"
    "/home/pocuser2/laptq-nedo-fed/outputs/helper--convert--ultralytics-txt--to--coco/sku_val--locount_val.json"

)

from tqdm import tqdm
from PIL import Image
import json
import os


images = []
annotations = []
categories = [
    {"supercategory": "product", "id": 0, "name": "product"},
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
