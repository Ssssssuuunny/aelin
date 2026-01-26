"""
pagexml-to-text.py

Convert PageXML files to plain text, merging consecutive lines within each TextRegion with spaces,
unless customizable options are specified.

Usage:
    python pagexml-to-text.py --input_dir <input_directory> --output_dir <output_directory> [options]
    python pagexml-to-text.py --help  # for all parameters

Output: plain text files in the output directory, one per PageXML file.

Dependencies: xml.etree.ElementTree, os, argparse, tqdm
"""

import xml.etree.ElementTree as ET
import os
import argparse
import tqdm


# this tool only supports PageXML 2013 and 2019 formats for now, we will add more later


def read_pagexml_file(file_path, separate_single_words, merge_dashes, split_periods, merge_quotes, separate_colons):
    """
    Parse PageXML file and extract text from PlainText elements.
    Each TextRegion is processed separately.
    Consecutive lines are merged with spaces unless merging options are specified.
    """
    try:
        # Register the namespace
        namespaces = {
            'page19': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15',
            'page13': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'
        }

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Determine which namespace is actually used in this file
        root_tag = root.tag
        if 'pagecontent/2019-07-15' in root_tag:
            ns_key = 'page19'
        else:
            ns_key = 'page13'

        ns = {
            'page': namespaces[ns_key]  # Map to a single 'page' prefix for simplicity in queries
        }

        merged_lines = []

        # Process each TextRegion separately
        for region in root.findall('.//page:TextRegion', ns):
            # Extract text from each line in this region
            region_lines = []
            region_lines_start = []
            for text_line in region.findall('./page:TextLine', ns):
                for text_equiv in text_line.findall('./page:TextEquiv', ns):
                    plain_text = text_equiv.find('./page:PlainText', ns)
                    if plain_text is not None and plain_text.text:
                        region_lines.append(plain_text.text.strip())
            #             add left most x coordinate of the line
                        coords = text_line.find('./page:Coords', ns)
                        if coords is not None and 'points' in coords.attrib:
                            points = coords.attrib['points']
                            x_coords = [int(pt.split(',')[0]) for pt in points.split()]
                            if x_coords:
                                region_lines_start.append(min(x_coords))
                            else:
                                region_lines_start.append(float('inf'))
                        else:
                            region_lines_start.append(float('inf'))



            # Skip empty regions
            if not region_lines:
                continue

            i = 0
            while i < len(region_lines):
                # Get current line
                current = region_lines[i]
                i += 1

                # Skip empty lines
                if not current:
                    continue

                # Option 1: separate single-word lines
                if separate_single_words and len(current.split()) == 1:
                    # if both lines have similar x coordinate, merge them
                    # TODO


                    merged_lines.append(current)
                    continue

                # Collect lines to merge
                while i < len(region_lines):
                    next_line = region_lines[i]

                    # Skip empty lines
                    if not next_line:
                        i += 1
                        continue

                    # Option 2: separate lines ending with period before capital characters
                    if split_periods and current.endswith('.') and next_line and next_line[0].isupper():
                        break

                    # Option 1 continued: if next line is single word, stop merging and keep it separate
                    if separate_single_words and len(next_line.split()) == 1:
                        break

                    # Option 3: merge hyphenated words at line breaks
                    if merge_dashes and current.endswith('-') :
                        current = current[:-1] + next_line
                    # Option 4: keep lines ending with colons separate
                    elif separate_colons and current.endswith(':'):
                        break
                    else:
                        # Default case: merge with space
                        current += " " + next_line

                    i += 1

                # Add the processed line
                merged_lines.append(current)

        return merged_lines
    except Exception as e:
        print(f"Error reading PageXML file {file_path}: {e}")
        return []

def main(input_dir, output_dir, separate_single_words, merge_dashes, split_periods, merge_quotes, separate_colons):
    os.makedirs(output_dir, exist_ok=True)
    pagexml_files = [f for f in os.listdir(input_dir) if f.endswith('.xml')]
    for xml_file in tqdm.tqdm(pagexml_files, desc="Processing PageXML files"):
        input_path = os.path.join(input_dir, xml_file)
        output_path = os.path.join(output_dir, xml_file.replace('.xml', '.txt'))

        lines = read_pagexml_file(input_path, separate_single_words, merge_dashes, split_periods, merge_quotes, separate_colons)

        with open(output_path, 'w', encoding='utf-8') as out_f:
            for line in lines:
                out_f.write(line + '\n')

    print(f"Processed {len(pagexml_files)} files. Output written to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PageXML files to plain text with merging options.")
    parser.add_argument('--input_dir', required=True, help="Directory containing PageXML files")
    parser.add_argument('--output_dir', required=True, help="Directory to save output text files")
    parser.add_argument('--merge_dashes', action='store_true', help="Merge hyphenated words at line breaks")
    parser.add_argument('--split_periods', action='store_true', help="Split lines ending with periods before capital letters. This should result in each text line being a full sentence. If disabled, there should be a full paragraph per outputted text line.")
    parser.add_argument('--merge_quotes', action='store_true', help="Merge lines starting/ending with quotes, typical for early modern handwritten text. This option is not implemented yet.")
    parser.add_argument('--separate_single_words', action='store_true', help="Keep single-word lines separate, typical for headings and question forms")
    parser.add_argument('--separate_colons', action='store_true', help="Keep lines ending with colon separate, typical for lists and definitions")


    args = parser.parse_args()
    main(args.input_dir, args.output_dir, args.separate_single_words, args.merge_dashes, args.split_periods, args.merge_quotes, args.separate_colons)
