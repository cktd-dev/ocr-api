import os
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'

import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

from fastapi import FastAPI, File, UploadFile, Form  
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI(title="FREE OCR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "OCR Live!", "docs": "/docs", "health": "/health"}

@app.get("/health")
async def health():
    try:
        version = pytesseract.get_tesseract_version()
        return {"status": "ready", "tesseract_version": str(version)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ocr")
async def ocr(file:
