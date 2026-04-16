import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


if __name__ == "__main__":
    pdf_path = "sample_contract.pdf"  # make sure this file exists
    
    extracted_text = extract_text_from_pdf(pdf_path)

    print("\n--- EXTRACTED TEXT (FIRST 1000 CHARS) ---\n")
    print(extracted_text[:1000])