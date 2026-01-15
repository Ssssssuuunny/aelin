#!/bin/bash
# find-corrupted-jpg.sh
# Description: checks all jpg images in the given directory for corruption single-threadedly
# Usage: ./find-corrupted-jpg.sh /PATH/TO/IMAGES [CORRUPTED_ONLY_FILE]
# Expected output: prints all results to stdout: for valid images, 1 for corrupted ones, other numbers for errors
#                  Use [CORRUPTED_ONLY_FILE] to save only corrupted files list.
# Dependencies: ImageMagick

if [ -z "$1" ]; then 
    echo "please provide path to images to be checked"
    exit 1
fi

corrupted_only_file="${2:-}"

# check jpg images for corruption. Only use one process at a time to avoid race conditions in the output
results=$(find -L "$1" -name '*.jpg' -type f |
    xargs -P 1 -I % sh -c '
        identify -regard-warnings -verbose % > /dev/null 2>&1
        echo % $?
    ')

#  save only corrupted images if corrupted_only_file is provided; if not, print all results to stdout
if [ -n "$corrupted_only_file" ]; then
    echo "$results" | grep " 1$" | cut -d " " -f 1 > "$corrupted_only_file"
    echo "Corrupted images saved to: $corrupted_only_file" >&2
else
    echo "$results"
fi

