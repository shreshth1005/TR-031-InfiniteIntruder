import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

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
    summary = generate_summary(obligations, anomalies)

    return {
        "obligations": obligations,
        "anomalies": anomalies,
        "summary": summary
    }