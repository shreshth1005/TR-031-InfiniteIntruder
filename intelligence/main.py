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

    # SAFETY CHECK: if extraction failed or gave too little useful data
    if not input_clauses or len(input_clauses) < 2:
        return {
            "obligations": [],
            "anomalies": [
                {
                    "clause_id": "System",
                    "issue": "Insufficient clause extraction",
                    "severity": "Medium",
                    "description": "The document could not be parsed into enough meaningful clauses for reliable legal analysis. This may be caused by translation quality, OCR issues, or unsupported formatting."
                }
            ],
            "summary": "The system could not extract enough meaningful clauses for reliable contract analysis."
        }

    similarity_results = similarity_engine.compare_many(input_clauses)

    obligations = []
    for clause, result in zip(input_clauses, similarity_results):
        obligation = anomaly_engine.build_obligation(
            clause_id=clause["clause_id"],
            text=clause["text"],
            best_match=result["best_match"],
            best_score=result["best_score"]
        )
        obligations.append(obligation)

    anomalies = anomaly_engine.detect_anomalies(input_clauses, similarity_results)

    # Additional guard: if all obligations are very weak matches, return controlled message
    strong_matches = [o for o in obligations if o["match_score"] >= 0.40]

    if len(strong_matches) == 0:
        return {
            "obligations": obligations,
            "anomalies": [
                {
                    "clause_id": "System",
                    "issue": "Low-confidence legal interpretation",
                    "severity": "Medium",
                    "description": "The system extracted text, but semantic alignment with the legal clause library was too weak for reliable anomaly analysis."
                }
            ],
            "summary": "The document was processed, but the extracted clauses did not align strongly enough with the clause library for reliable legal analysis."
        }

    summary = generate_summary(obligations, anomalies)

    return {
        "obligations": obligations,
        "anomalies": anomalies,
        "summary": summary
    }