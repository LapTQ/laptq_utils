#!/bin/bash

# Configuration
PATH__DIR__INPUT="/home/laptq/laptq-fs26-shoplifting-detection/data/customer-video/20250901-1105"
PATH__DIR__OUTPUT="/home/laptq/laptq-fs26-shoplifting-detection/outputs/helper--convert--video--to--mp4/fs26/customer-video/20250901-1105"

# Create output root directory
mkdir -p "$PATH__DIR__OUTPUT"

# Function to convert a single file
convert_to_mp4() {
    local file_input="$1"
    local rel_path="${file_input#$PATH__DIR__INPUT/}"
    local rel_dir=$(dirname "$rel_path")
    local filename=$(basename "$rel_path")
    local basename_no_ext="${filename%.*}"
    
    local dir_output="$PATH__DIR__OUTPUT/$rel_dir"
    local file_output="$dir_output/$basename_no_ext.mp4"
    
    # Create subdirectories if they don't exist
    mkdir -p "$dir_output"
    
    # Check if input is already mp4 and skip if you want, 
    # but here we force conversion to ensure standard h264/aac
    echo -e "\033[94m[INFO]\033[0m Converting: $rel_path"
    
    ffmpeg -i "$file_input" \
        -c copy \
        -y "$file_output" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "\033[92m[PASSED]\033[0m Done: $file_output"
    else
        echo -e "\033[31m[FAILED]\033[0m Error converting: $file_input"
    fi
}

export -f convert_to_mp4
export PATH__DIR__INPUT
export PATH__DIR__OUTPUT

# Find all video files and process them
# We use xargs to run conversions in parallel (4 processes at a time)
find "$PATH__DIR__INPUT" -type f \( -name "*.mkv" -o -name "*.avi" -o -name "*.mov" -o -name "*.flv" -o -name "*.wmv" -o -name "*.webm" -o -name "*.mp4" \) | \
xargs -I {} -P 8 bash -c 'convert_to_mp4 "{}"'

echo -e "\033[94m[INFO]\033[0m All conversions completed."
