import re
from extract_text import extract_text_from_pdf


def extract_obligations(text: str):
    """
    Extract likely obligation clauses from raw contract text.
    Returns clauses in the format required by the intelligence API:
    [
        {
            "clause_id": "Clause 1",
            "text": "The client must make payment within 30 days."
        }
    ]
    """

    clauses = []
    sentences = re.split(r'[.\n]+', text)
    clause_number = 1

    obligation_keywords = ["shall", "must", "agree", "will", "required"]

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 25:
            continue

        if any(word in sentence.lower() for word in obligation_keywords):
            clauses.append({
                "clause_id": f"Clause {clause_number}",
                "text": sentence
            })
            clause_number += 1

    return clauses


def process_contract(pdf_path: str):
    """
    Full backend helper:
    1. Extract text from PDF
    2. Extract obligation-like clauses
    Returns:
    {
        "clauses": [...]
    }
    """

    text = extract_text_from_pdf(pdf_path)
    clauses = extract_obligations(text)

    return {
        "clauses": clauses
    }


if __name__ == "__main__":
    result = process_contract("sample_contract.pdf")

    print("\n--- EXTRACTED CLAUSES ---\n")
    for clause in result["clauses"][:10]:
        print(clause)