import re


LEGAL_KEYWORDS = [
    "shall", "must", "will", "required", "agree", "agrees",
    "payment", "invoice", "liability", "terminate", "termination",
    "confidential", "confidentiality", "deliver", "delivery",
    "notice", "penalty", "renewal", "arbitration", "dispute",
    "service", "services", "obligation", "comply", "compliance"
]


def clean_sentence(sentence: str) -> str:
    sentence = sentence.strip()
    sentence = re.sub(r"\s+", " ", sentence)
    return sentence


def is_meaningful_sentence(sentence: str) -> bool:
    if len(sentence) < 35:
        return False

    words = sentence.split()
    if len(words) < 6:
        return False

    # reject obvious titles/headings
    if sentence.isupper() and len(words) <= 6:
        return False

    return True


def looks_like_legal_clause(sentence: str) -> bool:
    lowered = sentence.lower()

    keyword_hits = sum(1 for keyword in LEGAL_KEYWORDS if keyword in lowered)

    # needs at least one legal keyword
    if keyword_hits >= 1:
        return True

    return False


def deduplicate_clauses(clauses):
    seen = set()
    unique = []

    for clause in clauses:
        normalized = clause["text"].strip().lower()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(clause)

    return unique


def extract_obligations(text: str):
    raw_sentences = re.split(r"[.\n;:]+", text)

    clauses = []
    clause_number = 1

    for raw in raw_sentences:
        sentence = clean_sentence(raw)

        if not is_meaningful_sentence(sentence):
            continue

        if looks_like_legal_clause(sentence):
            clauses.append({
                "clause_id": f"Clause {clause_number}",
                "text": sentence
            })
            clause_number += 1

    clauses = deduplicate_clauses(clauses)

    # fallback only if almost nothing extracted
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

            if clause_number > 12:
                break

        clauses = deduplicate_clauses(clauses)

    return clauses