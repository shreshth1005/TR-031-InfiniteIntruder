import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class SimilarityEngine:
    def __init__(self, library_path: str):
        with open(library_path, "r", encoding="utf-8") as file:
            self.library = json.load(file)

        self.vectorizer = TfidfVectorizer()

        self.library_texts = [
            clause_data["text"] for clause_data in self.library.values()
        ]

        self.clause_names = list(self.library.keys())

        self.library_vectors = self.vectorizer.fit_transform(self.library_texts)

    def compare_clause(self, clause_text: str):
        clause_vector = self.vectorizer.transform([clause_text])

        similarities = cosine_similarity(clause_vector, self.library_vectors)[0]

        best_index = similarities.argmax()
        best_score = similarities[best_index]
        best_match = self.clause_names[best_index]

        all_scores = []
        for idx, score in enumerate(similarities):
            all_scores.append({
                "clause_type": self.clause_names[idx],
                "score": float(score)
            })

        all_scores.sort(key=lambda x: x["score"], reverse=True)

        return {
            "input_text": clause_text,
            "best_match": best_match,
            "best_score": float(best_score),
            "all_scores": all_scores
        }

    def compare_many(self, clauses):
        return [self.compare_clause(c["text"]) for c in clauses]