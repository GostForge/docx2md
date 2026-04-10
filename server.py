import sys
import tempfile
import shutil
import os
import zipfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, Response
from core.converter import DocxToMdConverter

app = FastAPI()

@app.post("/convert")
async def convert_docx(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.docx")
        output_md = os.path.join(tmpdir, "output.md")
        media_dir = os.path.join(tmpdir, "media")
        
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        converter = DocxToMdConverter(extract_media_path=media_dir)
        converter.convert(input_path, output_md)
        
        # Package everything into a ZIP
        zip_path = os.path.join(tmpdir, "result.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(output_md, arcname="output.md")
            if os.path.exists(media_dir):
                for root, dirs, files in os.walk(media_dir):
                    for file in files:
                        abs_file = os.path.join(root, file)
                        rel_file = os.path.relpath(abs_file, tmpdir)
                        zipf.write(abs_file, arcname=rel_file)
        
        with open(zip_path, "rb") as f:
            zip_bytes = f.read()

        return Response(content=zip_bytes, media_type="application/zip")
