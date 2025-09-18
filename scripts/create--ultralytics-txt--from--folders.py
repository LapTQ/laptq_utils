# create ultralytics .txt from by iterating through folders

PATHD_INPUT = '/home/laptq/laptq-prj-46/data/prj57-dedup-detection'

LS__SUBPATHD = [
    # # train
    # "APTO_v2/day1_330/images",
    # "APTO_v2/night3_44/images",
    # "APTO_v2/night4_239/images",
    # "Pothole_235/train/images",
    # "dataset-ninja/ds1_simplex-train/images",
    # "dataset-ninja/ds2_complex-train/images",
    # "pothole_dataset_v8/train/images",
    # "pothole_dataset_v8/train_to_valid/images",

    # "pot_det_1240/images",
    # "Pothole_detection_yolo/train_original/images",
    # "Pothole_Maeda/first_shot/images",
    # "Pothole_Maeda/second_shot/images",
    # "RDD2022_JAPAN/only_pothole/train/images"

    # # val
    # "APTO_v2/night1_190/images",
    # "dataset-ninja/ds1_simplex-test/images",
    # "dataset-ninja/ds2_complex-test/images",
    # "pothole_dataset_v8/valid/images",

    # "Pothole_Maeda/first_shot_eval/images"

    # train
    'prj57-v1-batch-1/images',
    'prj57-v1-batch-2/images',
    'prj57-v1-batch-3/images',
    'prj57-v1-batch-4/images',

    # val
    # 'prj57-v1-batch-5/images',
]

PATHF_OUTPUT = (
    '/home/laptq/laptq-prj-46/outputs/create--ultralytics-txt/prj57-v1--train.txt'
    # '/home/laptq/laptq-prj-46/outputs/create--ultralytics-txt/prj57-v1--val.txt'
)


from tqdm import tqdm
from PIL import Image
import json
import os


ls_pathf_img = []
for subpathd in LS__SUBPATHD:
    pathd_input = os.path.join(PATHD_INPUT, subpathd)
    
    for pathf_img in tqdm(sorted(os.listdir(pathd_input))):
        pathf_img = os.path.join(pathd_input, pathf_img)
        if not os.path.isfile(pathf_img):
            print("Skipping non-file:", pathf_img)
            continue
        ls_pathf_img.append(pathf_img)


os.makedirs(os.path.dirname(PATHF_OUTPUT), exist_ok=True)
with open(PATHF_OUTPUT, 'w') as f:
    for pathf_img in ls_pathf_img:
        f.write(pathf_img + '\n')

        
