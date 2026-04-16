import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from similarity_engine import SimilarityEngine
from anomaly_engine import AnomalyEngine
from summary_engine import generate_summary


LIBRARY_PATH = "clause_library.json"

similarity_engine = SimilarityEngine(LIBRARY_PATH)

with open(LIBRARY_PATH, "r", encoding="utf-8") as file:
    clause_library = json.load(file)

anomaly_engine = AnomalyEngine(clause_library)

app = FastAPI(title="Contract Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClauseInput(BaseModel):
    clause_id: str
    text: str


class AnalyzeRequest(BaseModel):
    clauses: List[ClauseInput]


@app.get("/")
def root():
    return {"message": "Contract Intelligence API is running."}


@app.post("/analyze")
def analyze_contract(request: AnalyzeRequest):
    input_clauses = [clause.model_dump() for clause in request.clauses]

    if not input_clauses or len(input_clauses) < 2:
        return {
            "obligations": [],
            "anomalies": [
                {
                    "clause_id": "System",
                    "issue": "Insufficient clause extraction",
                    "severity": "Medium",
                    "description": "The document could not be parsed into enough meaningful clauses for reliable legal analysis."
                }
            ],
            "summary": "The system could not extract enough meaningful clauses for reliable contract analysis."
        }

    similarity_results = similarity_engine.compare_many(input_clauses)

    obligations = []
    for clause, result in zip(input_clauses, similarity_results):
        # Ignore extremely weak text fragments from becoming obligations
        if result["best_score"] < 0.20:
            continue

        obligation = anomaly_engine.build_obligation(
            clause_id=clause["clause_id"],
            text=clause["text"],
            best_match=result["best_match"],
            best_score=result["best_score"]
        )
        obligations.append(obligation)

    if len(obligations) == 0:
        return {
            "obligations": [],
            "anomalies": [
                {
                    "clause_id": "System",
                    "issue": "Low-confidence extraction",
                    "severity": "Medium",
                    "description": "The system processed the document, but the extracted text fragments were too weak for reliable obligation analysis."
                }
            ],
            "summary": "The document was processed, but no reliable obligation clauses could be identified."
        }

    anomalies = anomaly_engine.detect_anomalies(input_clauses, similarity_results)
    summary = generate_summary(obligations, anomalies)

    return {
        "obligations": obligations,
        "anomalies": anomalies,
        "summary": summary
    }