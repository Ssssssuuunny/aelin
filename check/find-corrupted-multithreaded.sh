#!/bin/bash
# find-corrupted-multithreaded.sh
# Description: checks all jpg images in the given directory and its subdirectories for corruption using multiple threads
# Usage: ./find-corrupted-multithreaded.sh /PATH/TO/IMAGES NUM_THREADS
# Expected output: A summary file 'corrupted_jpgs_summary.txt' in the current directory and 'corrupted_jpgs.txt' files in each subdirectory
# Dependencies: ImageMagick, find-corrupted-jpg.sh

input_dir="$1"
numthreads="$2"
if [ -z "$input_dir" ] || [ -z "$numthreads" ]; then
    echo "Usage: $0 /PATH/TO/IMAGES NUM_THREADS"
    exit 1
fi

dirs=$(find "$input_dir" -type d)
# use xargs
echo "$dirs" | 
    xargs -I {} -P $numthreads bash -c '
    ./find-corrupted-jpg.sh "{}" > {}/corrupted_jpgs.txt
    '

# summarize results into one file
output_file="corrupted_jpgs_summary.txt"
echo "" > "$output_file"  # clear output file
for dir in $dirs; do
    corrupted_file="${dir}/corrupted_jpgs.txt"
    if [ -f "$corrupted_file" ]; then
        echo "Directory: $dir" >> "$output_file"
        cat "$corrupted_file" >> "$output_file"
        echo -e "\n" >> "$output_file"
    fi
done