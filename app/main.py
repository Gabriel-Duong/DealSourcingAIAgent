from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import os
import shutil
import csv
import io

from app.pdf_reader import extract_text_from_pdf
from app.classifier import classify_pitch, extract_signals

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory result store
analyzed_results = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": analyzed_results
    })

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(filepath)
    classification = classify_pitch(text)
    signals = extract_signals(text)

    entry = {
        "filename": file.filename,
        "classification": classification,
        "signals": signals
    }
    analyzed_results.append(entry)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": analyzed_results
    })

@app.get("/download")
def download_csv():
    headers = [
        "filename", "classification", 
        "market_potential", "team_experience", 
        "competitive_positioning", "business_model", "exit_strategy"
    ]

    csv_stream = io.StringIO()
    writer = csv.DictWriter(csv_stream, fieldnames=headers)
    writer.writeheader()

    for item in analyzed_results:
        row = {
            "filename": item["filename"],
            "classification": item["classification"],
            **item["signals"]
        }
        writer.writerow(row)

    csv_stream.seek(0)
    return StreamingResponse(csv_stream, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=results.csv"})
