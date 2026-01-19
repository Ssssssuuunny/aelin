#!/bin/bash
# create-image-cache.sh
# Description: creates thumbnail cache for each jp2 image in the given directory using multiple threads (default 4), preserving directory structure
# Usage: ./create-image-cache.sh /PATH/TO/IMAGES /PATH/TO/OUTPUT_DIR [NUM_THREADS]
# Expected output: thumbnails saved in the provided output directory with the same structure as the input directory
# Dependencies: ImageMagick
# Warning: all input paths are considered to be without special characters like spaces

input_dir="${1}"
output_dir="${2}"
if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
    echo "Usage: $0 /PATH/TO/IMAGES /PATH/TO/OUTPUT_DIR [NUM_THREADS]"
    exit 1
fi

numthreads="${3:-4}"

find "$input_dir" -maxdepth 1 -type d |
    xargs -P8 -I{} mkdir -p $output_dir/{}

find "$input_dir" -name '*.jp2'|
    xargs -P "$numthreads" -I{} bash -c "
    if [ ! -f '$output_dir/{}.thumbnail.jpg' ]; then 
        echo 'Thumbnail to be created for: {}' 
        convert {} -resize 1000x1000 -strip -interlace Plane -gaussian-blur 0.05 -quality 85% '$output_dir/{}.thumbnail.jpg'; 
    fi 
    "