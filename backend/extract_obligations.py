import re


def extract_obligations(text: str):
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