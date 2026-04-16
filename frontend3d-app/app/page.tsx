"use client";

import Hero3D from "../components/Hero3D";
import UploadPanel from "../components/UploadPanel";
import ResultsPanel from "../components/ResultsPanel";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import { useState } from "react";

export default function Home() {
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  return (
    <main className="page-shell min-h-screen text-white">
      <Header />

      <section id="overview" className="relative flex min-h-[70vh] items-center justify-center overflow-hidden px-6 pt-28">
        <Hero3D />

        <div className="relative z-10 mx-auto max-w-5xl text-center">
          <p className="mb-4 inline-block rounded-full border border-[#d4af37]/20 bg-[#d4af37]/10 px-4 py-2 text-sm text-[#f5d97b]">
            Enterprise Contract Intelligence
          </p>

          <h1 className="text-5xl font-bold leading-tight md:text-7xl">
            Legal Document Review,
            <br />
            Structured for Decisions
          </h1>

          <p className="mx-auto mt-6 max-w-3xl text-base leading-7 text-slate-300 md:text-lg">
            Review contracts through a consulting-grade interface that extracts
            obligations, highlights anomalies, and presents executive insights
            in a format suitable for legal, risk, and compliance workflows.
          </p>
        </div>
      </section>

      <section id="workspace" className="relative z-20 mx-auto max-w-7xl px-6 pb-20">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-[280px_1fr]">
          <Sidebar />

          <div className="grid grid-cols-1 gap-8 xl:grid-cols-2">
            <UploadPanel
              setAnalysisData={setAnalysisData}
              setUploadedFile={setUploadedFile}
            />
            <ResultsPanel
              analysisData={analysisData}
              uploadedFile={uploadedFile}
            />
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}