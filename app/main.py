from fastapi import FastAPI, UploadFile, File
from app.pdf_reader import extract_text_from_pdf
from app.classifier import classify_pitch
from app.classifier import extract_signals
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Deal Classifier AI!"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(filepath)
    result = classify_pitch(text)

    return {"deal_strength": result}

@app.post("/extract-signals")
async def extract(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(filepath)
    result = extract_signals(text)

    return result



