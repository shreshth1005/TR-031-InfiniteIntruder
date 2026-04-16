import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    doc.close()
    return text