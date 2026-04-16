"use client";

import { useState } from "react";

export default function UploadPanel({ setAnalysisData, setUploadedFile }) {
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadedFile(file);
    setFileName(file.name);
    setLoading(true);

    const extractedClauses = [
      {
        clause_id: "Clause 1.1",
        text: "The client must make payment within 30 days of invoice receipt."
      },
      {
        clause_id: "Clause 2.1",
        text: "The vendor shall deliver the services as soon as possible."
      },
      {
        clause_id: "Clause 3.1",
        text: "Either party may terminate the agreement."
      }
    ];

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          clauses: extractedClauses
        })
      });

      const data = await response.json();
      setAnalysisData(data);
    } catch (error) {
      console.error("Backend connection error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="legal-card rounded-3xl p-8">
      <div className="mb-6">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          Document Intake
        </p>
        <h2 className="mt-2 text-2xl font-semibold">Upload Contract</h2>
        <p className="mt-3 text-sm leading-6 text-slate-400">
          Upload a legal agreement in PDF format to extract obligations,
          identify anomalies, and generate a review summary for consulting and compliance workflows.
        </p>
      </div>

      <label className="block cursor-pointer rounded-2xl border border-dashed border-slate-500/40 bg-slate-900/40 p-8 text-center transition hover:bg-slate-800/50">
        <input
          type="file"
          accept=".pdf"
          onChange={handleUpload}
          className="hidden"
        />
        <span className="text-lg font-medium text-slate-100">Upload Legal Document</span>
        <p className="mt-2 text-sm text-slate-400">PDF only • Contract review ready</p>
      </label>

      {fileName && (
        <div className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs uppercase tracking-wider text-slate-400">Selected File</p>
          <p className="mt-2 text-base font-medium text-slate-100">{fileName}</p>
        </div>
      )}

      {loading && (
        <div className="mt-6 rounded-2xl border border-[#d4af37]/20 bg-[#d4af37]/10 p-4 text-sm text-[#f5d97b]">
          Reviewing document and preparing structured analysis...
        </div>
      )}
    </div>
  );
}