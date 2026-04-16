import re


def clean_sentence(sentence: str) -> str:
    sentence = sentence.strip()
    sentence = re.sub(r"\s+", " ", sentence)
    return sentence


def is_meaningful_sentence(sentence: str) -> bool:
    if len(sentence) < 20:
        return False

    words = sentence.split()
    if len(words) < 5:
        return False

    return True


def extract_obligations(text: str):
    """
    Extract obligation-like clauses from text.
    This version is broader and has fallback support.
    Returns:
    [
        {"clause_id": "Clause 1", "text": "..."}
    ]
    """

    # Split by punctuation and line breaks
    raw_sentences = re.split(r"[.\n;:]+", text)

    obligation_keywords = [
        "shall", "must", "will", "required", "agree", "agrees",
        "payment", "deliver", "delivery", "terminate", "termination",
        "confidential", "liability", "dispute", "arbitration",
        "notice", "invoice", "penalty", "renewal", "services"
    ]

    clauses = []
    clause_number = 1

    # First pass: keyword-based extraction
    for raw in raw_sentences:
        sentence = clean_sentence(raw)

        if not is_meaningful_sentence(sentence):
            continue

        lowered = sentence.lower()

        if any(keyword in lowered for keyword in obligation_keywords):
            clauses.append({
                "clause_id": f"Clause {clause_number}",
                "text": sentence
            })
            clause_number += 1

    # Fallback: if too few clauses found, take meaningful sentences
    if len(clauses) < 3:
        clauses = []
        clause_number = 1

        for raw in raw_sentences:
            sentence = clean_sentence(raw)

            if not is_meaningful_sentence(sentence):
                continue

            clauses.append({
                "clause_id": f"Clause {clause_number}",
                "text": sentence
            })
            clause_number += 1

            if clause_number > 10:
                break

    return clauses