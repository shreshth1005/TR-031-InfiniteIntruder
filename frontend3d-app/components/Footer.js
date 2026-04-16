"use client";

export default function Footer() {
  return (
    <footer
      id="contact"
      className="mt-20 border-t border-white/10 bg-[#0b1120]/90"
    >
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-10 px-6 py-10 md:grid-cols-3">
        <div>
          <h3 className="text-lg font-semibold">LexSight AI</h3>
          <p className="mt-3 text-sm text-slate-400">
            AI-assisted legal review platform for identifying obligations,
            compliance gaps, and contractual risks.
          </p>
        </div>

        <div>
          <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300">
            Contact
          </h4>
          <p className="mt-3 text-sm text-slate-400">Email: support@lexsight.ai</p>
          <p className="mt-2 text-sm text-slate-400">Phone: +91 98765 43210</p>
          <p className="mt-2 text-sm text-slate-400">Hours: Mon–Fri, 9 AM to 6 PM</p>
        </div>

        <div>
          <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300">
            Feedback & Reporting
          </h4>
          <p className="mt-3 text-sm text-slate-400">
            Report interface issues, analysis mismatches, or upload failures.
          </p>
          <div className="mt-4 flex flex-col gap-2">
            <button className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-left text-slate-200 hover:bg-white/10 transition">
              Submit Feedback
            </button>
            <button className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-left text-slate-200 hover:bg-white/10 transition">
              Report an Issue
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
}