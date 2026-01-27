# Aelin

Aelin is a collection of various scripts/tools which can be used for various purposes. Use at your own risk. 

## Table of Contents
- [Aelin](#aelin)
  - [Table of Contents](#table-of-contents)
  - [Check](#check)
    - [find-corrupted-jpg.sh](#find-corrupted-jpg.sh)
    - [find-corrupted-multithreaded.sh](#find-corrupted-multithreaded.sh)
  - [Conversion](#conversion)
  - [Convert](#convert)
    - [convert-jp2-to-jpeg.sh](#convert-jp2-to-jpeg.sh)
    - [create-image-cache.sh](#create-image-cache.sh)
  - [Image Analysis](#image-analysis)
  - [Text](#text)

## Check
This contains two checkers for corrupted jpgs, a single-threaded one and a multi-threaded one, both dependent on ImageMagick.

### find-corrupted-jpg.sh
#### Description
A single-threaded checker for corrupted jpgs in a given directory. The optional [CORRUPTED_ONLY_FILE] parameter allows the user to save a list of corrupted files only.

#### Usage
```bash
./find-corrupted-jpg.sh /PATH/TO/IMAGES [CORRUPTED_ONLY_FILE]
```

#### Expected output
Prints all results to stdout (0 for valid images, 1 for corrupted ones, other numbers for errors), unless the [CORRUPTED_ONLY_FILE] parameter is specified for the purpose of saving a list of corrupted files only.

#### Example 1
If you run the following command:
```bash
./find-corrupted-jpg.sh /user/images/
```
The standard ouput will be as below:
```bash
/user/images/valid.jpg 0
/user/images/corrupt.jpg 1
```

#### Example 2
If you run the following command:
```bash
./find-corrupted-jpg.sh /user/images/ /user/images/corrupted.txt
```

The standard ouput will be as below:
```bash
Corrupted images saved to: /user/images/corrupted.txt
```
And a text file `user/images/corrupted.txt` will be created with the following content:
```text
/user/images/corrupt.jpg 
```

### find-corrupted-multithreaded.sh
#### Description
This multi-threaded checker makes use of the single-threaded one to check corrupted jpgs in a given directory, processing multiple files (the number customizable) at once.

#### Usage
```bash
./find-corrupted-multithreaded.sh /PATH/TO/IMAGES NUM_THREADS [OUTPUT_FILE] [CORRUPTED_ONLY_FILE]
```

#### Expected output
To be updated

## Conversion
Documentation coming soon

## Convert
This contains two tools for image conversion purposes, both dependent on ImageMagick.

### convert-jp2-to-jpeg.sh

#### Description
This tool converts all jp2 files in a given directory to jpeg using multiple threads (default 16), skipping the already converted ones

#### Usage
```bash
./convert-jp2-to-jpeg.sh /PATH/TO/IMAGES [NUM_THREADS]
```

#### Expected output
Files converted to jpeg format in the same directory as the original.

#### Example
If you run the following command:
```bash
./convert-jp2-to-jpeg.sh /user/jp2_images/
```
The standard ouput will be as below:
``` bash
To be converted: /user/jp2_images/image1.jp2
To be converted: /user/jp2_images/subfolder/image2.jp2
```
And `user/jp2_images/image1.jp2.jpeg` and `user/jp2_images/subfolder/image2.jp2.jpeg` will be created.

### create-image-cache.sh

#### Description
This tool creates thumbnails for each jp2 file in a given directory using multiple threads (default 4), resizing it to 1000x1000 pixels, stripping metadata, using place interlacing to create progressive jpegs, applying slight blur, and compressing it to a reasonable size with a high quality. Those that have had a corresponding thumbnail will be skipped.

#### Usage 
```bash
./create-image-cache.sh /PATH/TO/IMAGES /PATH/TO/OUTPUT_DIR [NUM_THREADS]
```

#### Output
Thumbnails corresponding with each jp2 saved in the output directory following the structure of the input directory.

#### Example
If you run the following command:
```bash
./create-image-cache.sh /user/jp2_images/ /user/cache/
```
The standard ouput will be as below:
``` bash
Thumbnail to be created for: /user/jp2_images/image1.jp2
Thumbnail to be created for: /user/jp2_images/subfolder/image2.jp2
```
And a new folder `/user/cache/user/jp2_images/` will be created with the following structure and content:
```text
/user/cache/user/jp2_images/
├── image1.jp2.thumbnail.jpg
└── subfolder
    └── image2.jp2.thumbnail.jpg

```

## Image Analysis
Documentation coming soon

## Text
### find-ngrams.py

#### Description
This tool identifies the most common n-grams in text files within a specified directory. Helpful for finding clusters of similar documents. With multiple customizable filters.

#### Usage
```python 
find-ngrams.py --directory <path_to_directory>
```

#### Output
JSON files saved in the `./clusters` directory, each containing file paths for the corresponding n-gram.

#### Example
To be updated

## Automated Tests
Tests are located in the `tests` folder.

Tool | Test Available
---|---
find-corrupted-jpg.sh | ✅
find-corrupted-multithreaded.sh | ✅
convert-jp2-to-jpeg.sh | ✅
create-image-cache.sh | ✅
find-ngrams.py | ✅
