from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from langdetect import detect, LangDetectException
from deep_translator import MyMemoryTranslator

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


def detect_document_language(text: str) -> str:
    cleaned = (text or "").strip()

    if not cleaned or len(cleaned) < 20:
        return "en"

    try:
        return detect(cleaned)
    except LangDetectException:
        return "en"
    except Exception:
        return "en"


def chunk_text(text: str, max_chars: int = 400):
    """
    Split long text into smaller chunks for safer translation.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 <= max_chars:
            current += (" " if current else "") + line
        else:
            if current:
                chunks.append(current)
            current = line

    if current:
        chunks.append(current)

    if not chunks:
        chunks = [text[:max_chars]]

    return chunks


def translate_text_to_english(text: str) -> str:
    """
    Translate any non-English text into English using MyMemoryTranslator.
    Falls back to original text if translation fails.
    """
    chunks = chunk_text(text, max_chars=400)
    translated_chunks = []

    for chunk in chunks:
        try:
            translated = MyMemoryTranslator(source="auto", target="en").translate(chunk)
            translated_chunks.append(translated)
        except Exception:
            translated_chunks.append(chunk)

    return "\n".join(translated_chunks)


@app.get("/")
def root():
    return {"message": "Backend extraction API is running."}


@app.post("/extract")
async def extract_contract(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # STEP 1: Extract raw text
        extracted_text = extract_text_from_pdf(file_path)

        # STEP 2: Detect language
        detected_language = detect_document_language(extracted_text)

        # STEP 3: Translate if needed
        normalized_text = extracted_text
        translated = False

        if detected_language != "en":
            normalized_text = translate_text_to_english(extracted_text)
            translated = True

        # STEP 4: Extract obligation-like clauses from normalized English text
        extracted_clauses = extract_obligations(normalized_text)

        return {
            "language_detected": detected_language,
            "translated_to_english": translated,
            "clauses": extracted_clauses
        }

    except Exception as e:
        return {
            "error": str(e)
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)