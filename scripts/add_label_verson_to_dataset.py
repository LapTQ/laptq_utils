import os
import shutil
from pathlib import Path

# Cấu hình đường dẫn
PATH__DIR__IMG__SOURCE = "/home/laptq/laptq_utils/outputs/fs26/helper--resize--images"
POSTFIX__DIR__IMG__SOURCE = ""

PATH__DIR__LABEL__SOURCE = "/home/laptq/laptq_utils/outputs/fs26/helper--convert--detection--json--to--txt"
POSTFIX__DIR__LABEL__SOURCE = ""

PATH__DIR__OUTPUT = Path("/home/laptq/laptq_utils/outputs/fs26/add_label_verson_to_dataset")
POSTFIX__DIR__VERSION__TARGET = ""

# -----
import os
import glob

MAP__SUBPATH_DIR__TO__ = {
    p[len(PATH__DIR__IMG__SOURCE) + 1 :]: None
    for p in glob.glob(
        f"{PATH__DIR__IMG__SOURCE}/*/*/*.mp4"
    )
    if os.path.isdir(p)
}
# --------

# ANSI Colors
TAG__FAILED = "\033[31m[FAILED]\033[0m"
TAG__PASSED = "\033[92m[PASSED]\033[0m"

for subpath_dir in MAP__SUBPATH_DIR__TO__.keys():
    # Định nghĩa các đường dẫn cụ thể
    p_img_in = Path(PATH__DIR__IMG__SOURCE) / f"{subpath_dir}/images{POSTFIX__DIR__IMG__SOURCE}"
    p_img_out = Path(PATH__DIR__OUTPUT) / f"{subpath_dir}/images{POSTFIX__DIR__VERSION__TARGET}"
    p_lbl_in = Path(PATH__DIR__LABEL__SOURCE) / f"{subpath_dir}/labels{POSTFIX__DIR__LABEL__SOURCE}"
    p_lbl_out = Path(PATH__DIR__OUTPUT) / f"{subpath_dir}/labels{POSTFIX__DIR__VERSION__TARGET}"

    # --- PHẦN 1: COPY LABELS ---
    if p_lbl_out.exists():
        shutil.rmtree(p_lbl_out)
    p_lbl_out.mkdir(parents=True, exist_ok=True)

    num__lbl__output = 0
    # Đếm số file label gốc bằng cách quét generator, không tốn cache
    num__lbl__input = sum(1 for f in p_lbl_in.iterdir() if f.is_file()) if p_lbl_in.exists() else 0

    if p_img_in.exists():
        for img_file in p_img_in.iterdir():
            if not img_file.is_file():
                continue
            
            # Thay đổi đuôi thành .txt
            lbl_name = f"{img_file.stem}.txt"
            lbl_file_in = p_lbl_in / lbl_name

            if lbl_file_in.exists():
                shutil.copy(lbl_file_in, p_lbl_out)
                num__lbl__output += 1

    if num__lbl__input < num__lbl__output:
        print(f"{TAG__FAILED} Mismatched labels in copy step: {subpath_dir}")
        exit(1)
    print(f"{TAG__PASSED} Copied {num__lbl__input} labels to {num__lbl__output} labels: {subpath_dir}")

    # --- PHẦN 2: CREATE SYMLINKS ---
    if p_img_out.exists():
        shutil.rmtree(p_img_out)
    p_img_out.mkdir(parents=True, exist_ok=True)

    num__img = 0
    if p_img_in.exists():
        for img_file in p_img_in.iterdir():
            if not img_file.is_file():
                continue

            lbl_name = f"{img_file.stem}.txt"
            lbl_file_check = p_lbl_out / lbl_name

            if lbl_file_check.exists():
                target_link = p_img_out / img_file.name

                shutil.copy(img_file, target_link) # copy file
                # target_link.symlink_to(img_file.resolve()) # tạo softlink
                
                num__img += 1

    # Đếm số lượng label hiện tại trong thư mục output
    num__lbl = sum(1 for f in p_lbl_out.iterdir() if f.is_file())

    if num__lbl != num__img:
        print(f"{TAG__FAILED} Number of labels and images mismatched: {subpath_dir}")
        exit(1)
    print(f"{TAG__PASSED} Linked {num__img} images corresponding to {num__lbl} labels: {subpath_dir}")