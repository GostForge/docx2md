# docx2md
CLI tool to convert DOCX files to Markdown while replacing the Table of Contents (TOC) with a bare `[TOC]` string and extracting media using `pypandoc`.

## Prerequisites

- Python 3
- Pandoc (must be installed on the system)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py <input.docx> -o <output.md> --extract-media ./media
```

## How it works

1. It parses the document using `python-docx`
2. It locates the Table of Contents (by looking for `w:sdt` blocks handling TOC, or falling back to paragraphs starting with a `TOC` style)
3. It removes the entire TOC and injects a single `[TOC]` paragraph.
4. It calls `pandoc` via `pypandoc` to output Github Flavored Markdown with raw HTML attributes (`gfm-raw_html-attributes`), alongside media extracted to the specified directory.
