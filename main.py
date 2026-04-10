#!/usr/bin/env python3

import argparse
import sys

from core.converter import DocxToMdConverter

def main():
    parser = argparse.ArgumentParser(description="Convert DOCX to Markdown, specifically handling GOST elements.")
    parser.add_argument("input_file", help="Path to the input DOCX file")
    parser.add_argument("-o", "--output", default="output.md", help="Path to the output Markdown file")
    parser.add_argument("--extract-media", default="./media", help="Directory to extract media to")
    
    args = parser.parse_args()

    converter = DocxToMdConverter(extract_media_path=args.extract_media)
    try:
        converter.convert(args.input_file, args.output)
        print("Conversion completed successfully!")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during conversion: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
