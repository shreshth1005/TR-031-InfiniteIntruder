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
            "as applicable",
            "as appropriate",
            "where possible"
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
        if "consultant" in lowered:
            return "Consultant"
        return "Unspecified"

    def _extract_deadline(self, text: str):
        match = re.search(r"(\d+)\s+(day|days|month|months|week|weeks|year|years)", text.lower())
        if match:
            return match.group(0)

        if "quarterly" in text.lower():
            return "Quarterly"

        if "monthly" in text.lower():
            return "Monthly"

        if "annually" in text.lower():
            return "Annually"

        return "Not clearly specified"

    def _risk_from_score(self, score: float):
        if score >= 0.72:
            return "Low"
        if score >= 0.50:
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
        anomaly_keys = set()

        for clause, similarity in zip(input_clauses, similarity_results):
            clause_id = clause["clause_id"]
            text = clause["text"]
            best_match = similarity["best_match"]
            best_score = similarity["best_score"]

            matched_types.add(best_match)

            # Only flag weak semantic alignment if score is genuinely poor
            if best_score < 0.35:
                key = (clause_id, "Weak clause match")
                if key not in anomaly_keys:
                    anomalies.append({
                        "clause_id": clause_id,
                        "issue": "Weak clause match",
                        "severity": "High",
                        "description": f"This clause does not align well with standard legal clause patterns. Best match was '{best_match}' with low confidence."
                    })
                    anomaly_keys.add(key)

            elif 0.35 <= best_score < 0.50:
                key = (clause_id, "Moderate clause ambiguity")
                if key not in anomaly_keys:
                    anomalies.append({
                        "clause_id": clause_id,
                        "issue": "Moderate clause ambiguity",
                        "severity": "Medium",
                        "description": f"This clause partially matches '{best_match}' but may require clearer legal drafting."
                    })
                    anomaly_keys.add(key)

            vague_term = self._contains_vague_language(text)
            if vague_term:
                key = (clause_id, "Vague wording detected")
                if key not in anomaly_keys:
                    anomalies.append({
                        "clause_id": clause_id,
                        "issue": "Vague wording detected",
                        "severity": "Low",
                        "description": f"The phrase '{vague_term}' may reduce precision, but it is not automatically a major legal risk."
                    })
                    anomaly_keys.add(key)

            # Only selected clause types truly require explicit time language
            if (
                self._extract_deadline(text) == "Not clearly specified"
                and best_match in ["payment_clause", "termination_clause", "delivery_clause"]
                and best_score >= 0.50
            ):
                key = (clause_id, "Missing deadline")
                if key not in anomaly_keys:
                    anomalies.append({
                        "clause_id": clause_id,
                        "issue": "Missing deadline",
                        "severity": "Medium",
                        "description": "This clause appears operationally important but does not clearly define a deadline or timeline."
                    })
                    anomaly_keys.add(key)

        # Missing required clauses should only be checked if the document had enough usable clauses
        if len(input_clauses) >= 3:
            for clause_type, clause_data in self.clause_library.items():
                if clause_data["required"] and clause_type not in matched_types:
                    key = (f"Missing:{clause_type}", "Required clause missing")
                    if key not in anomaly_keys:
                        anomalies.append({
                            "clause_id": f"Missing:{clause_type}",
                            "issue": "Required clause missing",
                            "severity": "High",
                            "description": clause_data["risk_hint"]
                        })
                        anomaly_keys.add(key)

        return anomalies