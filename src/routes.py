from src.functions.scraping import scraping

from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import json


router = APIRouter()

UPLOADS_DIR = "public/uploads"

# Create a directory if it doesn't exist
os.makedirs(UPLOADS_DIR, exist_ok=True)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/upload-file/")
async def upload_files(file: UploadFile):
    res_json = None
    # Check if the file is an .xml file
    if not file.filename.endswith('.xml'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .xml são permitidos")
    
    invoice_path = os.path.join(UPLOADS_DIR, file.filename)
    if os.path.exists(invoice_path):
        print('Arquivo já existe')
        res = scraping(invoice_path)
        res_json = json.dumps(res)
    else:
        upload_path = os.path.join(UPLOADS_DIR, file.filename)
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        res = scraping(invoice_path)
        res_json = json.dumps(res)
        

    return JSONResponse(content={"":res_json}, status_code=200)