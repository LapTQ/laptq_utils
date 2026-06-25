# convert custom detection JSON format to RF-DETR format (YOLO structure with symlinks)

# --- Configuration ---
PATH__DIR__IMAGE = "/home/laptq/laptq_utils/outputs/fs26/helper--resize--images"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq_utils/outputs/fs26/helper--extract--detection"
POSTFIX__DIR__LABEL = "--PRED--DATA--None--MODEL--dfine_x_obj2coco--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--only-person--conf-0.4--filter-size--filter-nms--contain-person--JSON"

PATH__DIR__OUTPUT = "/home/laptq/laptq_utils/outputs/fs26/helper--convert--detection--json--to--rf-detr"

IS_OK__LBL_NOT_FOUND = True

MAP__ID_CLASS__TO__NAME_CLASS = {
    0: "person",
}

# -----
import os
import glob
import json
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, *args, **kwargs):
        return iterable


MAP__SUBPATH_DIR__TO__TRAIN = {
    p[len(PATH__DIR__LABEL) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL}/*/*.mp4"
    )
    if os.path.isdir(p)
    and ("Kita8jyou" in p or "Tsukisamu-Higashi" in p or "cia--107" in p)
}

MAP__SUBPATH_DIR__TO__VALID = {
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
    
    for split, subpath_dict in [("train", MAP__SUBPATH_DIR__TO__TRAIN), ("valid", MAP__SUBPATH_DIR__TO__VALID)]:
        for subpath in subpath_dict:
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
                        
                        # Store task with relative path identifier for renaming
                        rel_img_path = f"{subpath}/images{POSTFIX__DIR__IMAGE}/{f}"
                        flat_name = rel_img_path.replace("/", "--")
                        tasks.append((img_path, lbl_path, split, flat_name))

    tasks_train = sum(1 for t in tasks if t[2] == "train")
    tasks_valid = sum(1 for t in tasks if t[2] == "valid")
    print(f"{TAG__INFO} Found {len(tasks)} image-label pairs to process (Train: {tasks_train}, Valid: {tasks_valid}).")
    
    stats = {
        "train": {"processed": 0, "skipped": 0},
        "valid": {"processed": 0, "skipped": 0},
    }
    
    # Process tasks
    for img_path, lbl_path, split, flat_name in tqdm(tasks, desc="Creating RF-DETR dataset"):
        if not os.path.exists(lbl_path):
            if IS_OK__LBL_NOT_FOUND:
                stats[split]["skipped"] += 1
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {lbl_path}")
                
        # Read JSON label
        with open(lbl_path, 'r') as f:
            try:
                dict__result = json.load(f)
            except Exception as e:
                print(f"\n{TAG__FAILED} Failed to load JSON from {lbl_path}: {e}")
                raise e
                
        list__obj__id_class = dict__result.get("list__obj__id_class", [])
        list__obj__box_xcycwhn = dict__result.get("list__obj__box_xcycwhn", [])
        
        lines = []
        for id_class, box_xcycwhn in zip(list__obj__id_class, list__obj__box_xcycwhn):
            xcn, ycn, wn, hn = box_xcycwhn
            lines.append(f"{int(id_class)} {xcn:.6f} {ycn:.6f} {wn:.6f} {hn:.6f}")
            
        # Define output destinations
        dst_img_path = os.path.join(PATH__DIR__OUTPUT, split, "images", flat_name)
        dst_lbl_path = os.path.join(PATH__DIR__OUTPUT, split, "labels", os.path.splitext(flat_name)[0] + ".txt")
        
        # Write label TXT
        os.makedirs(os.path.dirname(dst_lbl_path), exist_ok=True)
        with open(dst_lbl_path, "w") as f:
            f.write("\n".join(lines) + "\n")
            
        # Create symlink for image
        os.makedirs(os.path.dirname(dst_img_path), exist_ok=True)
        if os.path.exists(dst_img_path) or os.path.islink(dst_img_path):
            os.remove(dst_img_path)
        os.symlink(os.path.abspath(img_path), dst_img_path)
        
        stats[split]["processed"] += 1

    # Generate data.yaml
    max_id = max(MAP__ID_CLASS__TO__NAME_CLASS.keys()) if MAP__ID_CLASS__TO__NAME_CLASS else 0
    names_list = []
    for i in range(max_id + 1):
        names_list.append(MAP__ID_CLASS__TO__NAME_CLASS.get(i, f"class_{i}"))
        
    yaml_lines = [
        "names:",
    ]
    for name in names_list:
        yaml_lines.append(f"  - {name}")
    yaml_lines.extend([
        "",
        f"nc: {len(names_list)}",
        "",
        "train: train/images",
        "val: valid/images"
    ])
    
    yaml_path = os.path.join(PATH__DIR__OUTPUT, "data.yaml")
    os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
    with open(yaml_path, "w") as f:
        f.write("\n".join(yaml_lines) + "\n")
        
    print(f"\n{TAG__PASSED} Successfully formatted dataset:")
    print(f"  - Output folder: {PATH__DIR__OUTPUT}")
    for split in ["train", "valid"]:
        print(f"  - [{split.upper()}] Processed: {stats[split]['processed']} | Skipped (no label): {stats[split]['skipped']}")
    print(f"  - Generated configuration: {yaml_path}")


if __name__ == "__main__":
    main()
