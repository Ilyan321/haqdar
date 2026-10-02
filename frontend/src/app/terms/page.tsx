import React from "react";
import Link from "next/link";
import { Scale, ArrowLeft, AlertCircle, FileText, CheckCircle2, ShieldAlert } from "lucide-react";

export const metadata = {
  title: "Terms of Service | HaqDar (حقدار)",
  description: "Terms of Service and Legal Platform Usage Framework for HaqDar Autonomous Inheritance Recovery.",
};

export default function TermsOfServicePage() {
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
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-primary-50 text-primary-800 rounded-full border border-primary-200 text-xs font-bold uppercase tracking-wider">
            <FileText className="w-3.5 h-3.5" /> Legal Service Framework
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary-900">
            Terms of Service & Usage Governance
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Please review the operating terms governing access to and utilization of the HaqDar Autonomous Legal Intelligence Platform.
          </p>
        </div>

        {/* Terms Sections */}
        <div className="space-y-6 text-xs sm:text-sm text-slate-700 leading-relaxed divide-y divide-slate-100">
          
          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-accent-600" />
              1. Nature of Platform — AI Legal Assistance vs. Representation
            </h2>
            <div className="p-4 bg-amber-50 rounded-2xl border border-amber-200/80 text-amber-900 space-y-2">
              <p className="font-semibold">
                Critical Notice on Legal Advocacy:
              </p>
              <p className="text-xs leading-relaxed">
                HaqDar provides autonomous computational jurisprudence, forensic record analysis, and petition drafting assistance. HaqDar is not a law firm and does not provide direct courtroom representation. Generated recovery roadmaps and dossiers are designed to be submitted before the Provincial Ombudsperson or reviewed by a licensed High Court advocate.
              </p>
            </div>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              2. Mathematical and Faraizi Accuracy Guarantee
            </h2>
            <p>
              All inheritance fraction calculations are executed using our deterministic rational calculation engine adhering strictly to Sunni Hanafi Islamic jurisprudence (*Ilm al-Fara&apos;id*), handling Quranic Sharers (*Zawil-Furooz*), Residuaries (*Asaba*), Deficit Scaling (*Awl*), and Surplus Return (*Radd*) without floating point drift.
            </p>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-red-600" />
              3. Prohibited Misuse & Fraudulent Claims
            </h2>
            <p>
              Users agree not to utilize HaqDar to manufacture fraudulent genealogy records, forge simulated death certificates, or maliciously harass lawful co-heirs. False submissions may trigger criminal liability under Section 182 and Chapter XVIII of the Pakistan Penal Code.
            </p>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <Scale className="w-4 h-4 text-primary-700" />
              4. Governing Jurisdiction
            </h2>
            <p>
              These terms are construed in accordance with the laws of the Islamic Republic of Pakistan, subject to the primary jurisdiction of the Provincial Ombudspersons and the High Courts of Pakistan.
            </p>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div>© 2026 HaqDar (حقدار) • All Rights Reserved.</div>
          <div className="flex gap-4 font-semibold text-primary-800">
            <Link href="/privacy" className="hover:underline">Privacy Policy</Link>
            <Link href="/disclaimer" className="hover:underline">Legal & Sharia Disclaimer</Link>
          </div>
        </div>

      </div>
    </div>
  );
}
