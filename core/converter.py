import os
import tempfile
from pathlib import Path
from typing import Union

import docx
import pypandoc

from core.preprocessor import remove_toc_and_add_placeholder, prepare_tables_for_markdown
from core.postprocessor import apply_postprocessing

class DocxToMdConverter:
    """
    Converts GOST-compliant or dynamically formatted DOCX files into raw Markdown,
    with processing to translate standard Word/manual TOCs, clean headings,
    and convert special inline spacing correctly.
    """
    def __init__(self, extract_media_path: Union[str, Path] = "./media") -> None:
        self.extract_media_path = str(extract_media_path)

    def convert(self, input_file: Union[str, Path], output_file: Union[str, Path]) -> None:
        input_file = Path(input_file).absolute()
        output_file = Path(output_file).absolute()

        if not input_file.exists():
            raise FileNotFoundError(f"Input file '{input_file}' not found.")

        print(f"Opening document: {input_file.name}")
        doc = docx.Document(str(input_file))
        
        print("Replacing TOC with [TOC]...")
        doc = remove_toc_and_add_placeholder(doc)

        print("Preparing tables to prevent [TABLE] fallback...")
        doc = prepare_tables_for_markdown(doc)

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx:
            temp_docx_path = temp_docx.name
        
        try:
            print("Saving modified DOCX...")
            doc.save(temp_docx_path)
            
            print(f"Converting to Markdown '{output_file.name}' and extracting media to '{self.extract_media_path}'...")
            extra_args = ['--extract-media', self.extract_media_path, '--wrap=none']
            
            pypandoc.convert_file(
                temp_docx_path,
                to='gfm-raw_html-attributes',
                format='docx',
                outputfile=str(output_file),
                extra_args=extra_args
            )
            
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            content = apply_postprocessing(content)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        finally:
            if os.path.exists(temp_docx_path):
                os.remove(temp_docx_path)
