#!/bin/bash
# find-corrupted-jpg.sh
# Description: checks all jpg images in the given directory for corruption single-threadedly
# Usage: ./find-corrupted-jpg.sh /PATH/TO/IMAGES [OUTPUT_FILE]
# Expected output: prints all results to stdout. If OUTPUT_FILE is provided, saves only corrupted files there.
# Exit codes: 0 for valid images, 1 for corrupted ones, other numbers for errors
# Dependencies: ImageMagick

if [ -z "$1" ]; then 
    echo "please provide path to images to be checked"
    exit 1
fi

output_file="${2:-}"

# check jpg images for corruption. Only use one process at a time to avoid race conditions in the output
results=$(find -L "$1" -name '*.jpg' -type f |
    xargs -P 1 -I % sh -c '
        identify -regard-warnings -verbose % > /dev/null 2>&1
        echo % $?
    ')

#  save only corrupted images if output_file is provided; if not, print all results to stdout
if [ -n "$output_file" ]; then
    echo "$results" | grep " 1$" | cut -d " " -f 1 > "$output_file"
    echo "Corrupted images saved to: $output_file" >&2
else
    echo "$results"
fi

