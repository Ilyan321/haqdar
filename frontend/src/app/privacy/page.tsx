import React from "react";
import Link from "next/link";
import { ShieldCheck, ArrowLeft, Lock, Database, EyeOff, UserCheck, Scale } from "lucide-react";

export const metadata = {
  title: "Privacy Policy | HaqDar (حقدار)",
  description: "Privacy Policy and Client Data Protection Protocols for the HaqDar Inheritance Recovery Platform.",
};

export default function PrivacyPolicyPage() {
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
          <span className="text-[11px] font-semibold text-slate-400">
            Last Updated: October 2026 • Version 1.2
          </span>
        </div>

        {/* Title */}
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full border border-emerald-200 text-xs font-bold uppercase tracking-wider">
            <ShieldCheck className="w-3.5 h-3.5" /> Client Data Confidentiality
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary-900">
            Privacy Policy & Data Security Protocols
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            HaqDar (&quot;حقدار&quot;) is committed to the absolute privacy, legal privilege, and safety of dispossessed women and claimants seeking inheritance justice under Pakistani and Islamic Law.
          </p>
        </div>

        {/* Policy Sections */}
        <div className="space-y-6 text-xs sm:text-sm text-slate-700 leading-relaxed divide-y divide-slate-100">
          
          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <Lock className="w-4 h-4 text-accent-600" />
              1. Sensitive Legal Information Handled
            </h2>
            <p>
              During autonomous case intake and document auditing, our platform processes case facts provided voluntarily by claimants:
            </p>
            <ul className="list-disc pl-5 space-y-1 text-slate-600">
              <li>Names of deceased family heads and approximate dates of passing.</li>
              <li>Genealogical rosters (sons, daughters, surviving widows, mothers, and paternal ascendants).</li>
              <li>Disputed property identifiers (land measurements, rural revenue mutations, Intiqal numbers, district/tehsil).</li>
              <li>Descriptions of fraud, coerced waivers (*Dastbardari*), and unauthorized revenue alienation.</li>
            </ul>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <EyeOff className="w-4 h-4 text-emerald-600" />
              2. Zero Commercial Data Monetization
            </h2>
            <p className="bg-emerald-50/70 p-4 rounded-2xl border border-emerald-200/80 text-emerald-900">
              <strong>Non-Negotiable Commitment:</strong> HaqDar does not sell, rent, license, or monetize claimant family records, property values, or legal dossiers to any commercial third parties, brokers, or data harvesters.
            </p>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <Database className="w-4 h-4 text-primary-700" />
              3. Processing and Multi-Agent Inference Security
            </h2>
            <p>
              Conversational intake data is processed ephemerally using pooled enterprise language inference endpoints with strict zero-training guarantees. Real-time telemetry is broadcast via isolated server-sent event (SSE) channels unique to each active session UUID.
            </p>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <Scale className="w-4 h-4 text-red-600" />
              4. Compliance with Pakistani Legal Frameworks
            </h2>
            <p>
              Our data management practices operate in strict alignment with:
            </p>
            <ul className="list-disc pl-5 space-y-1 text-slate-600">
              <li><strong>Prevention of Electronic Crimes Act (PECA 2016)</strong> — Securing unauthorized access and preserving digital integrity.</li>
              <li><strong>Enforcement of Women&apos;s Property Rights Act (2020 / 2021)</strong> — Safeguarding whistleblowers and vulnerable female heirs against intimidation or retribution.</li>
              <li><strong>Section 498A Pakistan Penal Code</strong> — Documenting statutory deprivation of inheritance with verifiable evidence trails.</li>
            </ul>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <UserCheck className="w-4 h-4 text-accent-600" />
              5. Client Rights & Data Erasure
            </h2>
            <p>
              Claimants retain the unconditional right to reset active discovery sessions, clear local memory stores, and request immediate purging of generated forensic dossiers at any time.
            </p>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div>© 2026 HaqDar (حقدار) • All Rights Reserved.</div>
          <div className="flex gap-4 font-semibold text-primary-800">
            <Link href="/terms" className="hover:underline">Terms of Service</Link>
            <Link href="/disclaimer" className="hover:underline">Legal & Sharia Disclaimer</Link>
          </div>
        </div>

      </div>
    </div>
  );
}
