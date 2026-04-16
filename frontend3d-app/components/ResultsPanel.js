"use client";

export default function ResultsPanel({ analysisData, uploadedFile }) {
  if (!analysisData) {
    return (
      <div className="legal-card rounded-3xl p-8">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          Review Output
        </p>
        <h2 className="mt-2 text-2xl font-semibold">Consulting Summary</h2>
        <p className="mt-4 text-sm leading-6 text-slate-400">
          Upload a contract to view extracted obligations, flagged risks,
          and an executive-level advisory summary.
        </p>
      </div>
    );
  }

  const highRiskCount = analysisData.anomalies.filter(
    (item) => item.severity === "High"
  ).length;

  return (
    <div id="reports" className="legal-card rounded-3xl p-8">
      <div className="mb-6">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          Review Output
        </p>
        <h2 className="mt-2 text-2xl font-semibold">Consulting Summary</h2>
      </div>

      {uploadedFile && (
        <div className="mb-6 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs uppercase tracking-wider text-slate-400">Uploaded Document</p>
          <p className="mt-2 font-medium text-slate-100">{uploadedFile.name}</p>
        </div>
      )}

      <div className="mb-6 grid grid-cols-3 gap-4">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs uppercase tracking-wider text-slate-400">Obligations</p>
          <p className="mt-2 text-2xl font-bold">{analysisData.obligations.length}</p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs uppercase tracking-wider text-slate-400">Anomalies</p>
          <p className="mt-2 text-2xl font-bold">{analysisData.anomalies.length}</p>
        </div>

        <div className="rounded-2xl border border-[#d4af37]/20 bg-[#d4af37]/10 p-4">
          <p className="text-xs uppercase tracking-wider text-slate-300">High Risk</p>
          <p className="mt-2 text-2xl font-bold text-[#f5d97b]">{highRiskCount}</p>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="mb-3 text-lg font-semibold">Executive Summary</h3>
        <div className="rounded-2xl border border-[#d4af37]/20 bg-[#d4af37]/10 p-4 text-sm leading-6 text-slate-200">
          {analysisData.summary}
        </div>
      </div>

      <div className="mb-6">
        <h3 className="mb-3 text-lg font-semibold">Obligations Review</h3>
        <div className="space-y-3">
          {analysisData.obligations.map((item, i) => (
            <div
              key={i}
              className="rounded-2xl border border-white/10 bg-white/5 p-4"
            >
              <p className="font-semibold text-slate-100">{item.clause_id}</p>
              <p className="mt-1 text-sm text-slate-300">{item.obligation}</p>
              <p className="mt-2 text-xs text-slate-400">
                Party: {item.party} | Deadline: {item.deadline} | Risk: {item.risk_level}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="mb-3 text-lg font-semibold">Risk Flags</h3>
        <div className="space-y-3">
          {analysisData.anomalies.map((item, i) => (
            <div
              key={i}
              className={`rounded-2xl border p-4 ${
                item.severity === "High"
                  ? "border-red-400/20 bg-red-500/10"
                  : item.severity === "Medium"
                  ? "border-yellow-400/20 bg-yellow-500/10"
                  : "border-emerald-400/20 bg-emerald-500/10"
              }`}
            >
              <p className="font-semibold text-slate-100">
                {item.clause_id} • {item.issue}
              </p>
              <p className="mt-1 text-sm text-slate-300">{item.description}</p>
              <p className="mt-2 text-xs text-slate-400">Severity: {item.severity}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}