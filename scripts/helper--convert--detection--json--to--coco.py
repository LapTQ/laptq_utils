# convert custom detection JSON format to COCO JSON format

# --- Configuration ---
PATH__DIR__IMAGE = "/home/laptq/laptq_utils/outputs/fs26/helper--resize--images"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq_utils/outputs/fs26/helper--extract--detection"
POSTFIX__DIR__LABEL = "--PRED--DATA--None--MODEL--dfine_x_obj2coco--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--only-person--conf-0.4--filter-size--contain-person--JSON"

PATHF_OUTPUT = (
    "/home/laptq/laptq_utils/outputs/fs26/helper--convert--detection--json--to--coco/val.json"
)

IS_OK__LBL_NOT_FOUND = True

MAP__ID_CLASS__TO__NAME_CLASS = {
    0: "person",
}

# -----
import os
import glob
import json
from tqdm import tqdm
from PIL import Image

MAP__SUBPATH_DIR__TO__ = {
    p[len(PATH__DIR__LABEL) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL}/*/*.mp4"
    )
    if os.path.isdir(p)
    and not ("Kita8jyou" in p or "Tsukisamu-Higashi" in p or "cia--107" in p)
} | {
    p[len(PATH__DIR__LABEL) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL}/*.mp4"
    )
    if os.path.isdir(p)
}

# --- Log Tags ---
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"
TAG__INFO = "\033[94m[INFO]\033[0m"
TAG__WARNING = "\033[33m[WARNING]\033[0m"


def main():
    tasks = []
    print(f"{TAG__INFO} Collecting files...")
    
    for subpath in MAP__SUBPATH_DIR__TO__:
        path__dir__img = f"{PATH__DIR__IMAGE}/{subpath}/images{POSTFIX__DIR__IMAGE}"
        path__dir__lbl = f"{PATH__DIR__LABEL}/{subpath}/labels{POSTFIX__DIR__LABEL}"
        
        if not os.path.exists(path__dir__img):
            print(f"{TAG__WARNING} Image directory does not exist: {path__dir__img}")
            continue
            
        if not os.path.exists(path__dir__lbl):
            if IS_OK__LBL_NOT_FOUND:
                print(f"{TAG__WARNING} Label directory does not exist: {path__dir__lbl}")
            else:
                raise FileNotFoundError(f"Label directory not found: {path__dir__lbl}")
                
        # Find all images
        valid_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        if os.path.exists(path__dir__img):
            for f in sorted(os.listdir(path__dir__img)):
                if os.path.splitext(f.lower())[1] in valid_exts:
                    img_path = os.path.join(path__dir__img, f)
                    base_name = os.path.splitext(f)[0]
                    lbl_path = os.path.join(path__dir__lbl, f"{base_name}.json")
                    tasks.append((img_path, lbl_path))

    print(f"{TAG__INFO} Found {len(tasks)} image-label pairs to process.")
    
    images = []
    annotations = []
    categories_map = {}
    
    # Initialize categories_map from configuration
    for cid, name in MAP__ID_CLASS__TO__NAME_CLASS.items():
        categories_map[cid] = {
            "supercategory": name,
            "id": cid,
            "name": name,
        }
        
    count_img = 0
    count_ann = 0
    
    for img_path, lbl_path in tqdm(tasks, desc="Converting to COCO"):
        if not os.path.exists(lbl_path):
            if IS_OK__LBL_NOT_FOUND:
                print(f"\n{TAG__WARNING} Label file for {img_path} not found. Skipping...")
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {lbl_path}")
                
        # Read image dimensions
        try:
            with Image.open(img_path) as img:
                W, H = img.size
        except Exception as e:
            print(f"\n{TAG__FAILED} Failed to open image {img_path}: {e}")
            raise e
            
        count_img += 1
        image_id = count_img
        image_info = {
            "id": image_id,
            "file_name": img_path,
            "width": W,
            "height": H,
        }
        images.append(image_info)
        
        # Load label JSON
        with open(lbl_path, 'r') as f:
            try:
                dict__result = json.load(f)
            except Exception as e:
                print(f"\n{TAG__FAILED} Failed to load JSON from {lbl_path}: {e}")
                raise e
                
        list__obj__id_class = dict__result.get("list__obj__id_class", [])
        list__obj__box_xcycwhn = dict__result.get("list__obj__box_xcycwhn", [])
        
        for id_class, box_xcycwhn in zip(list__obj__id_class, list__obj__box_xcycwhn):
            count_ann += 1
            id_class = int(id_class)
            xcn, ycn, wn, hn = box_xcycwhn
            
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
            
            if id_class not in categories_map:
                categories_map[id_class] = {
                    "supercategory": f"class_{id_class}",
                    "id": id_class,
                    "name": f"class_{id_class}",
                }

    categories = [categories_map[cid] for cid in sorted(categories_map.keys())]
    
    output_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }
    
    os.makedirs(os.path.dirname(PATHF_OUTPUT), exist_ok=True)
    with open(PATHF_OUTPUT, "w") as f:
        json.dump(output_data, f, indent=4)
        
    print(f"\n{TAG__PASSED} Successfully exported {count_img} images and {count_ann} annotations to {PATHF_OUTPUT}")


if __name__ == "__main__":
    main()
