from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pypdf import PdfReader
from io import BytesIO
from .agents import analyze

app = FastAPI(title="CareerLens AI", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=100_000)
    job_description: str = Field(min_length=1, max_length=50_000)

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/analyze")
def analyze_endpoint(body: AnalyzeRequest):
    return analyze(body.resume_text, body.job_description)

@app.post("/resume/extract")
async def extract_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf" or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(415, "Upload a PDF file")
    data = await file.read(8 * 1024 * 1024 + 1)
    if len(data) > 8 * 1024 * 1024: raise HTTPException(413, "PDF must be 8 MB or smaller")
    try:
        text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(data)).pages)
    except Exception as exc:
        raise HTTPException(400, "Could not read PDF") from exc
    if not text.strip(): raise HTTPException(422, "No selectable text found. Scanned PDF OCR is not included in this MVP; paste resume text instead.")
    return {"resume_text": text[:100_000]}
