"use client";

const menuItems = [
  "Dashboard",
  "Upload Review",
  "Obligations",
  "Anomalies",
  "Executive Summary",
  "Compliance Report"
];

export default function Sidebar() {
  return (
    <aside className="legal-card sticky top-24 h-fit rounded-3xl p-6">
      <p className="mb-4 text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
        Navigation
      </p>

      <div className="space-y-2">
        {menuItems.map((item, index) => (
          <button
            key={index}
            className={`w-full rounded-2xl px-4 py-3 text-left text-sm transition ${
              index === 0
                ? "bg-[#d4af37]/10 text-[#f5d97b] border border-[#d4af37]/20"
                : "text-slate-300 hover:bg-white/5"
            }`}
          >
            {item}
          </button>
        ))}
      </div>

      <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-4">
        <p className="text-xs uppercase tracking-wider text-slate-400">System Status</p>
        <p className="mt-2 text-sm text-emerald-400">Operational</p>
        <p className="mt-1 text-xs text-slate-400">
          Contract parsing and anomaly pipeline ready
        </p>
      </div>
    </aside>
  );
}