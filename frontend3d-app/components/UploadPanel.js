"use client";

import { useState } from "react";

export default function UploadPanel({ setAnalysisData, setUploadedFile }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);
    setUploadedFile(file);
    setFileName(file.name);
    setStatusMessage("File selected successfully. Click Analyze Contract.");
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    setStatusMessage("Uploading PDF to extraction service...");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const backendRes = await fetch("http://127.0.0.1:5000/extract", {
        method: "POST",
        body: formData,
      });

      const backendText = await backendRes.text();

      if (!backendRes.ok) {
        throw new Error("Backend extraction failed.");
      }

      const backendData = JSON.parse(backendText);

      if (!backendData.clauses || !Array.isArray(backendData.clauses)) {
        throw new Error("Backend did not return valid clauses.");
      }

      setStatusMessage("Clauses extracted. Sending to intelligence service...");

      const intelRes = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          clauses: backendData.clauses,
        }),
      });

      const intelText = await intelRes.text();

      if (!intelRes.ok) {
        throw new Error("Intelligence analysis failed.");
      }

      const finalData = JSON.parse(intelText);

      setAnalysisData(finalData);
      setStatusMessage("Analysis complete.");
    } catch (error) {
      console.error("Pipeline error:", error);
      setStatusMessage(`Error: ${error.message}`);
      alert(`Upload failed: ${error.message}`);
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
          Step 1: Select a PDF. Step 2: Analyze the contract.
        </p>
      </div>

      <div className="rounded-2xl border border-dashed border-slate-500/40 bg-slate-900/40 p-8">
        <p className="mb-4 text-lg font-medium text-slate-100">Step 1: Select PDF</p>

        <input
          id="contract-file-input"
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="block w-full rounded-lg border border-white/10 bg-slate-800 p-3 text-slate-100"
        />

        <p className="mt-3 text-sm text-slate-400">
          PDF only • Contract review ready
        </p>
      </div>

      {fileName && (
        <div className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs uppercase tracking-wider text-slate-400">Selected File</p>
          <p className="mt-2 text-base font-medium text-slate-100">{fileName}</p>
        </div>
      )}

      <div className="mt-6">
        <button
          type="button"
          onClick={handleAnalyze}
          disabled={loading || !selectedFile}
          className="w-full rounded-xl border border-emerald-400/30 bg-emerald-500/10 px-6 py-3 text-lg font-medium text-slate-100 hover:bg-emerald-500/20 transition disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Step 2: Analyze Contract"}
        </button>
      </div>

      {statusMessage && (
        <div className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
          {statusMessage}
        </div>
      )}
    </div>
  );
}