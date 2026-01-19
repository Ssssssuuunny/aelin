#!/bin/bash
# convert-jp2-to-jpeg.sh
# Description: convert jp2 images in the given directory to jpeg format using multiple threads (default 16)
# Usage: ./convert-jp2-to-jpeg.sh /PATH/TO/IMAGES [NUM_THREADS]
# Expected output: files converted to jpeg format in the same directory, skipping already converted files
# Dependencies: ImageMagick
# Note: on systems with ImageMagick 6.x or earlier, replace 'magick' with 'convert' on line 29
# Warning: this script assumes that image file names contain no special characters like spaces

input_dir="$1"
numthreads="${2:-16}"
if [ -z "$input_dir" ]; then
    echo "Usage: $0 /PATH/TO/IMAGES [NUM_THREADS]"
    exit 1
fi

# find jp2 files to be converted and skip converted ones
>/tmp/toconvert2jp2.txt
for file in `find "$input_dir" -name '*.jp2'` ; do
  base=${file%.*}
  if [ ! -f "$base.jpg" ]; then
    echo "To be converted: $file"
    echo "$file" >> /tmp/toconvert2jp2.txt
  fi
done

# convert jp2 files using multiple threads
cat /tmp/toconvert2jp2.txt | xargs -P"$numthreads" -I{} convert {} {}.jpg

# rename converted files
for file in `find "$input_dir" -name '*.jp2.jpg'`; do
  mv "$file" "${file%jp2\.jpg}jpg"; 
done

