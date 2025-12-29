import os
from pathlib import Path

IMAGE_FOLDERS = [
    # '/home/pocuser2/laptq-nedo-fed/data/SKU110K_fixed/train/images',
    # '/home/pocuser2/laptq-nedo-fed/data/SKU110K_fixed/val/images',
    # '/home/pocuser2/laptq-nedo-fed/data/SKU110K_fixed/test/images',
    # "/home/pocuser2/laptq-nedo-fed/data/locount/train/images",
    # "/home/pocuser2/laptq-nedo-fed/data/locount/val/images",
    # "/home/pocuser2/datasets/coco/only_person/train2017/images",
    # "/home/pocuser2/datasets/coco/only_person/val2017/images",
    # "/home/pocuser2/datasets/lagenda/restructured/train/images",
    "/home/pocuser2/datasets/lagenda/restructured/val/images",
]

# OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/sku_train.txt'
# OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/sku_val.txt'
# OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/locount_train.txt'
# OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/locount_val.txt'
# OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/coco2017_train.txt'
# OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/coco2017_val.txt'
# OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/lagenda_train.txt'
OUTPUT_FILENAME = '/home/pocuser2/laptq-nedo-fed/outputs/ultralytics_folder_to_txt/lagenda_val.txt'


IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

def generate_image_path_list(image_folders, output_file, extensions):
    """
    Scans a list of folders for image files and writes their absolute paths
    to a single output text file.
    """
    all_image_paths = []
    
    # 1. Collect all paths
    for folder_name in image_folders:
        folder_path = Path(folder_name)
        
        if not folder_path.is_dir():
            print(f"Warning: Folder not found or is not a directory: '{folder_name}'. Skipping.")
            continue
            
        # Use rglob('*') for recursive search (searching subfolders too)
        # Use glob('*') for non-recursive search (only the top level)
        print(f"Scanning folder: {folder_path}...")
        
        # Iterate over all files in the folder and its subdirectories
        for file_path in folder_path.rglob('*'):
            if file_path.is_file():
                # Check if the file extension is in our accepted list (case-insensitive)
                if file_path.suffix.lower() in extensions:
                    # Get the absolute path and convert it to a string
                    absolute_path = file_path.resolve()
                    all_image_paths.append(str(absolute_path))

    # 2. Write paths to the output file
    if not all_image_paths:
        print(f"\n⚠️ No images found in the specified folders. The file '{output_file}' was not created.")
        return

    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as outfile:
            outfile.write('\n'.join(all_image_paths))
        
        print("\n✅ Success!")
        print(f"Total images found: {len(all_image_paths)}")
        print(f"List of paths saved to: {Path(output_file).resolve()}")
        
    except IOError as e:
        print(f"\nError: Could not write to the output file '{output_file}'. Error: {e}")


if __name__ == "__main__":
    generate_image_path_list(IMAGE_FOLDERS, OUTPUT_FILENAME, IMAGE_EXTENSIONS)