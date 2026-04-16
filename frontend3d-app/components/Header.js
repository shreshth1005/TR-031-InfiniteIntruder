"use client";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-[200] border-b border-white/10 bg-[#0b1120]/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <div>
          <h1 className="text-xl font-semibold tracking-wide">LexSight AI</h1>
          <p className="text-xs text-slate-400">Contract Review & Risk Intelligence</p>
        </div>

        <nav className="hidden md:flex items-center gap-8 text-sm text-slate-300">
          <a href="#overview" className="hover:text-white transition">Overview</a>
          <a href="#workspace" className="hover:text-white transition">Workspace</a>
          <a href="#reports" className="hover:text-white transition">Reports</a>
          <a href="#contact" className="hover:text-white transition">Contact</a>
        </nav>

        <button
          type="button"
          className="rounded-full border border-[#d4af37]/40 bg-[#d4af37]/10 px-4 py-2 text-sm font-medium text-[#f5d97b] hover:bg-[#d4af37]/20 transition"
        >
          Request Demo
        </button>
      </div>
    </header>
  );
}