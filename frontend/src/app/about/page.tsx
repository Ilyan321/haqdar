import React from "react";
import Link from "next/link";
import { GitFork, ArrowLeft, Users, ShieldCheck, Scale, FileSearch, Sparkles, Award } from "lucide-react";

export const metadata = {
  title: "About & Methodology | HaqDar (حقدار)",
  description: "Autonomous 8-Agent Architecture for Women's Inheritance Rights Recovery in Pakistan.",
};

const AGENTS = [
  { id: "orchestrator", name: "Jurisdictional Orchestrator", role: "Dispatches recovery pathways based on provincial acts (Punjab, Sindh, KPK, Balochistan, ICT)." },
  { id: "intake_agent", name: "Empathetic Intake Officer", role: "Conducts bilingual discovery in English & Roman Urdu, extracting verified legal facts." },
  { id: "family_tree_agent", name: "Family Tree Genealogist", role: "Reconstructs Shajra Nasab and audits NADRA records for hidden or omitted female heirs." },
  { id: "document_analyzer", name: "Land Revenue Forensic Auditor", role: "Audits PLRA Intiqal mutations, Hiba gift deeds, and deathbed alienation (Marz-ul-Maut)." },
  { id: "sharia_calculator", name: "Chief Faraizi Math Engine", role: "Deterministic rational calculation engine enforcing Quranic shares (4:11, 4:12, 4:176) with Awl and Radd." },
  { id: "fraud_detection_agent", name: "Adversarial PPC 498A Auditor", role: "Cross-checks Sharia entitlements against de facto possession, triggering criminal alerts." },
  { id: "legal_strategy_agent", name: "High Court Strategist", role: "Synthesizes fast-track 60-day Ombudsperson petitions and revenue freeze orders." },
  { id: "qa_reviewer", name: "Judicial Reviewer & Gatekeeper", role: "Executes mathematical closure verification (100.0%) and statutory citations before certification." },
];

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-10 space-y-8">
        
        {/* Header navigation */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-5">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-xs font-bold text-primary-800 hover:text-primary-900 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-xl transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Workspace</span>
          </Link>
          <div className="flex items-center gap-1.5 text-accent-700 bg-accent-50 px-2.5 py-1 rounded-full border border-accent-200 text-xs font-bold">
            <Award className="w-3.5 h-3.5" />
            <span>HEC × PakAngels AI Hackathon</span>
          </div>
        </div>

        {/* Title */}
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-primary-50 text-primary-800 rounded-full border border-primary-200 text-xs font-bold uppercase tracking-wider">
            <GitFork className="w-3.5 h-3.5" /> 8-Agent Autonomous Topology
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary-900">
            About HaqDar & The Autonomous Legal Engine
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            In Pakistan, millions of women are unlawfully dispossessed of their rightful inheritance through forged oral gifts (*Hiba*), coerced relinquishments (*Dastbardari*), and collusive revenue mutations (*Intiqal*). HaqDar transforms civil litigation that typically takes 15–20 years into a rapid, autonomous 60-day recovery process.
          </p>
        </div>

        {/* 8 Agent Grid */}
        <div className="space-y-4 pt-4">
          <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
            <Users className="w-4 h-4 text-accent-600" />
            Autonomous Specialized Agents
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {AGENTS.map((agent, i) => (
              <div key={agent.id} className="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-primary-900 text-xs">
                    {i + 1}. {agent.name}
                  </span>
                  <span className="text-[10px] font-mono bg-primary-100 text-primary-800 px-2 py-0.5 rounded-md font-semibold">
                    Agent {i + 1}
                  </span>
                </div>
                <p className="text-slate-600 leading-relaxed">{agent.role}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Core Pillars */}
        <div className="pt-6 border-t border-slate-100 space-y-4">
          <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            Platform Architectural Guarantees
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div className="p-3.5 bg-emerald-50/60 rounded-xl border border-emerald-200">
              <div className="font-bold text-emerald-900 mb-1">Exact Rational Math</div>
              <p className="text-slate-600">Pure fraction arithmetic guarantees 100.0% closure without rounding errors.</p>
            </div>
            <div className="p-3.5 bg-accent-50/60 rounded-xl border border-accent-200">
              <div className="font-bold text-accent-900 mb-1">60-Day Recovery Limit</div>
              <p className="text-slate-600">Formulates petitions for the Provincial Ombudsperson with mandatory statutory timelines.</p>
            </div>
            <div className="p-3.5 bg-primary-50/60 rounded-xl border border-primary-200">
              <div className="font-bold text-primary-900 mb-1">Zero-Trust Audit Gate</div>
              <p className="text-slate-600">Judicial Reviewer agent audits citations and heir coverage before generating certified dossiers.</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div>© 2026 HaqDar (حقدار) • All Rights Reserved.</div>
          <div className="flex gap-4 font-semibold text-primary-800">
            <Link href="/privacy" className="hover:underline">Privacy Policy</Link>
            <Link href="/terms" className="hover:underline">Terms of Service</Link>
            <Link href="/disclaimer" className="hover:underline">Legal & Sharia Disclaimer</Link>
          </div>
        </div>

      </div>
    </div>
  );
}
