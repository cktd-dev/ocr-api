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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "OCR API LIVE ✅", "test": "/health", "docs": "/docs"}

@app.get("/health")
async def health():
    try:
        version = pytesseract.get_tesseract_version()
        return {"status": "LIVE", "tesseract": str(version)}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...), lang: str = Form(default="eng")):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image, lang=lang)
        return {"success": True, "text": text.strip(), "lang": lang}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
