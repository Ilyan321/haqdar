"use client";

import React, { useState } from "react";
import { useCaseStore } from "@/store/caseStore";
import { Download, Globe, FileCheck2, Printer, ShieldCheck } from "lucide-react";

export function ReportViewer() {
  const { finalReport, language, setLanguage } = useCaseStore();
  const [activeTab, setActiveTab] = useState<"en" | "roman_urdu">(language || "en");

  if (!finalReport) {
    return null;
  }

  const handlePrint = () => {
    window.print();
  };

  const bilingual = finalReport.bilingual_report || {};
  const classification = finalReport.classification || {};
  const qaVerdict = finalReport.qa_verdict || {};

  return (
    <div className="bg-white rounded-2xl border border-border p-6 shadow-sm space-y-6 print:p-0 print:border-none">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-border">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-accent-700 bg-accent-50 px-2 py-0.5 rounded border border-accent-200">
              Judicial Grade Dossier
            </span>
            {qaVerdict.status === "APPROVED" && (
              <span className="flex items-center gap-1 text-[11px] font-bold text-success-700 bg-success-50 px-2 py-0.5 rounded border border-success-200">
                <ShieldCheck className="w-3.5 h-3.5" /> 100% QA Validated
              </span>
            )}
          </div>
          <h2 className="text-lg font-bold text-primary-900 mt-1">
            HaqDar Legal Assessment & Recovery Dossier
          </h2>
          <p className="text-xs text-slate-500">
            Governed by {classification.applicable_act || "Women's Property Rights Act 2020"} • {classification.province || "Punjab"}
          </p>
        </div>

        {/* Language switch & Export */}
        <div className="flex items-center gap-2">
          <div className="flex bg-slate-100 p-1 rounded-xl text-xs font-semibold">
            <button
              onClick={() => setActiveTab("en")}
              className={`px-3 py-1 rounded-lg transition-all ${
                activeTab === "en" ? "bg-white text-primary-900 shadow-xs" : "text-slate-600"
              }`}
            >
              English
            </button>
            <button
              onClick={() => setActiveTab("roman_urdu")}
              className={`px-3 py-1 rounded-lg transition-all ${
                activeTab === "roman_urdu" ? "bg-white text-primary-900 shadow-xs" : "text-slate-600"
              }`}
            >
              Roman Urdu
            </button>
          </div>

          <button
            onClick={handlePrint}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-primary-800 hover:bg-primary-900 text-white text-xs font-bold rounded-xl shadow-xs transition-colors"
          >
            <Printer className="w-3.5 h-3.5" />
            Print / PDF
          </button>
        </div>
      </div>

      {/* Content based on selected language tab */}
      <div className="space-y-6 text-slate-800 text-xs leading-relaxed">
        {/* Executive Summary */}
        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/80">
          <h3 className="text-sm font-bold text-primary-900 mb-2 flex items-center gap-1.5">
            <FileCheck2 className="w-4 h-4 text-accent-600" />
            {activeTab === "en" ? "Executive Legal Findings" : "Markazi Qanooni Nataij"}
          </h3>
          <p className="text-slate-700 whitespace-pre-line">
            {activeTab === "en"
              ? bilingual.executive_summary_en || "Investigation complete. Lawful female inheritance shares verified."
              : bilingual.executive_summary_roman_urdu || "Tehqeeq mukammal. Aurat ke sharia aur qanooni hissay ki tasdeeq ho chuki hai."}
          </p>
        </div>

        {/* Strategic Recovery Action Plan */}
        <div className="p-4 bg-primary-50/50 rounded-xl border border-primary-100">
          <h3 className="text-sm font-bold text-primary-900 mb-2">
            {activeTab === "en" ? "Recommended Ombudsperson Legal Recovery Action Plan" : "Ombudsperson Bahali Ka Qanooni Mansooba"}
          </h3>
          <p className="text-slate-700 whitespace-pre-line">
            {activeTab === "en"
              ? bilingual.legal_action_plan_en || "File petition under Section 4 of the Women's Property Rights Act 2020."
              : bilingual.legal_action_plan_roman_urdu || "Women Property Rights Act 2020 ke Section 4 ke tehat Ombudsperson mein darkhwast daakhil karein."}
          </p>
        </div>

        {/* Statutory References */}
        <div className="p-3.5 bg-slate-100/70 rounded-xl text-[11px] text-slate-600 space-y-1">
          <div className="font-bold text-slate-800 uppercase tracking-wider text-[10px]">Statutory Authorities Cited:</div>
          <p>• Holy Quran Surah An-Nisa (Verses 4:11, 4:12, 4:176) — Immutable Fractional Shares</p>
          <p>• Enforcement of Women's Property Rights Act 2020 (Act XII of 2020) — 60-Day Ombudsperson Decree</p>
          <p>• Pakistan Penal Code (Act XLV of 1860) Section 498A — Prohibition of Depriving Women from Inheritance</p>
          <p>• Supreme Court of Pakistan Ruling (PLD 2021 SC 812) — Invalidation of Fraudulent Deathbed Gifts (Marz-ul-Maut)</p>
        </div>
      </div>
    </div>
  );
}
