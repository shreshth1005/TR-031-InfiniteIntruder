from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from extract_text import extract_text_from_pdf
from extract_obligations import extract_obligations

app = FastAPI(title="Contract Extraction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Backend extraction API is running."}


@app.post("/extract")
async def extract_contract(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_text_from_pdf(file_path)
        extracted_clauses = extract_obligations(extracted_text)

        return {
            "clauses": extracted_clauses
        }

    except Exception as e:
        return {
            "error": str(e)
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)