import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI(title="FREE OCR Text Extractor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "OCR API Live!",
        "docs": "/docs", 
        "upload": "/ocr",
        "languages": ["eng", "hin", "deu"]
    }

@app.post("/ocr")
async def extract_text(
    file: UploadFile = File(...),
    lang: str = Form("eng")
):
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # OCR
        text = pytesseract.image_to_string(image, lang=lang)
        
        return {
            "status": "success",
            "text": text.strip(),
            "lang": lang,
            "words_count": len(text.split()),
            "chars_count": len(text)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
