import os
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'  # Fixed path

import pytesseract
# Try multiple common paths
pytesseract.pytesseract.tesseract_cmd = (
    '/usr/bin/tesseract' or 
    '/usr/local/bin/tesseract' or 
    '/snap/bin/tesseract' or 
    'tesseract'
)

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

@app.get("/health")
async def health():
    try:
        pytesseract.get_tesseract_version()
        return {"tesseract": True, "status": "ready"}
    except:
        return {"tesseract": False, "status": "not ready"}

@app.get("/")
async def root():
    return {"message": "OCR Live!", "docs": "/docs", "health": "/health"}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        contents =
