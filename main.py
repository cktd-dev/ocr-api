import os
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import pytesseract

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "OCR API ✅"}

@app.get("/health")
async def health():
    try:
        version = pytesseract.get_tesseract_version()
        return {"status": "LIVE", "version": str(version)}
    except:
        return {"status": "Tesseract Missing"}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...), lang: str = Form("eng")):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        text = pytesseract.image_to_string(image, lang=lang)
        return {"text": text.strip(), "lang": lang}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
