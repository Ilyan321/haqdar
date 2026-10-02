import React from "react";
import Link from "next/link";
import { BookOpen, ArrowLeft, Scale, ShieldCheck, Landmark } from "lucide-react";

export const metadata = {
  title: "Legal & Sharia Disclaimer | HaqDar (حقدار)",
  description: "Statutory Precedents and Theological Citations Governing the HaqDar Inheritance Calculation Platform.",
};

export default function DisclaimerPage() {
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
            Faraizi Jurisprudence Audit • Version 1.2
          </span>
        </div>

        {/* Title */}
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-accent-50 text-accent-700 rounded-full border border-accent-200 text-xs font-bold uppercase tracking-wider">
            <BookOpen className="w-3.5 h-3.5" /> Sharia & Statutory Authorities
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary-900">
            Legal & Sharia Jurisprudential Disclaimer
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            HaqDar operates on immutable Islamic fractional distribution laws and contemporary Pakistani statutory precedents.
          </p>
        </div>

        {/* Authorities */}
        <div className="space-y-6 text-xs sm:text-sm text-slate-700 leading-relaxed divide-y divide-slate-100">
          
          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-emerald-600" />
              1. Primary Quranic Citations (Surah An-Nisa)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-200 text-xs space-y-1">
                <div className="font-bold text-emerald-900">Surah An-Nisa (4:11) — Children & Parents</div>
                <p className="text-slate-700">
                  Prescribes the 2:1 male-to-female ratio for residuary children, fixed 1/6 for parents in presence of children, and fixed 1/3 or 1/6 for mothers.
                </p>
              </div>
              <div className="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-200 text-xs space-y-1">
                <div className="font-bold text-emerald-900">Surah An-Nisa (4:12) — Spousal Entitlements</div>
                <p className="text-slate-700">
                  Prescribes 1/8 for surviving wives/widows with children (1/4 without children), and 1/4 for surviving husbands with children (1/2 without children).
                </p>
              </div>
            </div>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <Landmark className="w-4 h-4 text-primary-700" />
              2. Key Supreme Court Precedents Cited
            </h2>
            <ul className="space-y-3 text-xs text-slate-700">
              <li className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="font-bold text-primary-900">PLD 2021 Supreme Court 812 (Invalidation of Fraudulent Gifts):</span>
                <p className="text-slate-600 mt-1">
                  The Supreme Court of Pakistan ruled that transfers executed during deathbed illness (*Marz-ul-Maut*) or oral gift deeds depriving female heirs of lawful inheritance are void ab initio.
                </p>
              </li>
              <li className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="font-bold text-primary-900">2019 SCMR 1713 (No Limitation Against Female Co-Heirs):</span>
                <p className="text-slate-600 mt-1">
                  Brothers or male colluders cannot claim title via adverse possession; the right of a female heir to claim her inheritance share is imprescriptible and never extinguished by the passage of time.
                </p>
              </li>
            </ul>
          </div>

          <div className="pt-6 space-y-3">
            <h2 className="text-base font-bold text-primary-900 flex items-center gap-2">
              <Scale className="w-4 h-4 text-red-600" />
              3. Criminal Sanctions under PPC Section 498A
            </h2>
            <p className="bg-red-50 p-4 rounded-2xl border border-red-200 text-red-900 text-xs">
              <strong>Section 498A Pakistan Penal Code:</strong> &quot;Whoever by deceitful or illegal means deprives any woman from inheriting any movable or immovable property at the time of opening of succession shall be punished with imprisonment for a term which may extend to ten years but shall not be less than five years and with fine of one million rupees or both.&quot;
            </p>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div>© 2026 HaqDar (حقدار) • All Rights Reserved.</div>
          <div className="flex gap-4 font-semibold text-primary-800">
            <Link href="/privacy" className="hover:underline">Privacy Policy</Link>
            <Link href="/terms" className="hover:underline">Terms of Service</Link>
          </div>
        </div>

      </div>
    </div>
  );
}
