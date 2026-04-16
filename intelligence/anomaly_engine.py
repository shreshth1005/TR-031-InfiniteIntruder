import re


class AnomalyEngine:
    def __init__(self, clause_library):
        self.clause_library = clause_library

    def _contains_vague_language(self, text: str):
        vague_terms = [
            "as soon as possible",
            "reasonable time",
            "if needed",
            "when necessary",
            "from time to time",
            "as applicable"
        ]

        lowered = text.lower()
        for term in vague_terms:
            if term in lowered:
                return term
        return None

    def _extract_party(self, text: str):
        lowered = text.lower()

        if "vendor" in lowered:
            return "Vendor"
        if "client" in lowered:
            return "Client"
        if "buyer" in lowered:
            return "Buyer"
        if "seller" in lowered:
            return "Seller"
        return "Unspecified"

    def _extract_deadline(self, text: str):
        match = re.search(r"(\d+)\s+(day|days|month|months|week|weeks)", text.lower())
        if match:
            return match.group(0)

        if "quarterly" in text.lower():
            return "Quarterly"

        if "monthly" in text.lower():
            return "Monthly"

        return "Not clearly specified"

    def _risk_from_score(self, score: float):
        if score >= 0.75:
            return "Low"
        if score >= 0.55:
            return "Medium"
        return "High"

    def build_obligation(self, clause_id: str, text: str, best_match: str, best_score: float):
        return {
            "clause_id": clause_id,
            "party": self._extract_party(text),
            "obligation": text,
            "deadline": self._extract_deadline(text),
            "risk_level": self._risk_from_score(best_score),
            "matched_clause_type": best_match,
            "match_score": round(best_score, 4)
        }

    def detect_anomalies(self, input_clauses, similarity_results):
        anomalies = []
        matched_types = set()

        for clause, similarity in zip(input_clauses, similarity_results):
            clause_id = clause["clause_id"]
            text = clause["text"]
            best_match = similarity["best_match"]
            best_score = similarity["best_score"]

            matched_types.add(best_match)

            if best_score < 0.55:
                anomalies.append({
                    "clause_id": clause_id,
                    "issue": "Weak clause match",
                    "severity": "High",
                    "description": f"This clause does not align strongly with expected legal clause standards. Best match was '{best_match}' with low confidence."
                })

            elif best_score < 0.75:
                anomalies.append({
                    "clause_id": clause_id,
                    "issue": "Moderate clause ambiguity",
                    "severity": "Medium",
                    "description": f"This clause partially matches '{best_match}' but may need clarification or stronger drafting."
                })

            vague_term = self._contains_vague_language(text)
            if vague_term:
                anomalies.append({
                    "clause_id": clause_id,
                    "issue": "Vague wording detected",
                    "severity": "Medium",
                    "description": f"The phrase '{vague_term}' is ambiguous and may weaken legal precision."
                })

            if self._extract_deadline(text) == "Not clearly specified" and best_match in ["payment_clause", "delivery_clause", "termination_clause"]:
                anomalies.append({
                    "clause_id": clause_id,
                    "issue": "Missing deadline",
                    "severity": "High",
                    "description": "This clause appears important but does not clearly define a deadline or timeline."
                })

        for clause_type, clause_data in self.clause_library.items():
            if clause_data["required"] and clause_type not in matched_types:
                anomalies.append({
                    "clause_id": f"Missing:{clause_type}",
                    "issue": "Required clause missing",
                    "severity": "High",
                    "description": clause_data["risk_hint"]
                })

        return anomalies