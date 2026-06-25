# convert custom detection JSON format to Ultralytics TXT format (list of image paths)

# --- Configuration ---
PATH__DIR__IMAGE = "/home/laptq/laptq_utils/outputs/fs26/add_label_verson_to_dataset"
POSTFIX__DIR__IMAGE = ""

PATH__DIR__LABEL = "/home/laptq/laptq_utils/outputs/fs26/helper--extract--detection"
POSTFIX__DIR__LABEL = "--PRED--DATA--None--MODEL--dfine_x_obj2coco--TRAIN--exp--PREDICT--imgsz-640--conf-0.1--iou-0.45--all-keypoints--only-person--conf-0.4--filter-size--filter-nms--contain-person--JSON"

PATHF_OUTPUT = (
    "/home/laptq/laptq_utils/outputs/fs26/helper--convert--detection--json--to--ultralytics-txt/val--daiso.txt"
)

IS_OK__LBL_NOT_FOUND = True

# -----
import os
import glob
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, *args, **kwargs):
        return iterable

# MAP__SUBPATH_DIR__TO__ = {
#     p[len(PATH__DIR__LABEL) + 1 :]: None
#     for p in glob.glob(
#         f"{PATH__DIR__LABEL}/*/*.mp4"
#     )
#     if os.path.isdir(p)
#     and ("Kita8jyou" in p or "Tsukisamu-Higashi" in p or "cia--107" in p)
# }
MAP__SUBPATH_DIR__TO__ = {
    p[len(PATH__DIR__LABEL) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__LABEL}/*/*/*.mp4"
    )
    if os.path.isdir(p)
    and not ("Kita8jyou" in p or "Tsukisamu-Higashi" in p or "cia--107" in p)
} | {
    # p[len(PATH__DIR__LABEL) + 1 :]: None
    # for p in glob.glob(
    #     f"{PATH__DIR__LABEL}/*.mp4"
    # )
    # if os.path.isdir(p)
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
    
    image_paths = []
    
    for img_path, lbl_path in tqdm(tasks, desc="Collecting image paths"):
        if not os.path.exists(lbl_path):
            if IS_OK__LBL_NOT_FOUND:
                print(f"\n{TAG__WARNING} Label file for {img_path} not found. Skipping...")
                continue
            else:
                raise FileNotFoundError(f"Label file not found: {lbl_path}")
        
        image_paths.append(img_path)
        
    os.makedirs(os.path.dirname(PATHF_OUTPUT), exist_ok=True)
    with open(PATHF_OUTPUT, "w") as f:
        for img_path in image_paths:
            f.write(img_path + "\n")
            
    print(f"\n{TAG__PASSED} Successfully exported {len(image_paths)} image paths to {PATHF_OUTPUT}")


if __name__ == "__main__":
    main()
