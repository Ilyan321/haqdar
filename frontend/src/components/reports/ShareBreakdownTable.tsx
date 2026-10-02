"use client";

import React from "react";
import { useCaseStore } from "@/store/caseStore";
import { Scale, BookOpen, CheckCircle2 } from "lucide-react";

export function ShareBreakdownTable() {
  const { shariaShares } = useCaseStore();

  if (!shariaShares || !shariaShares.heir_allocations || shariaShares.heir_allocations.length === 0) {
    return null;
  }

  const allocations = shariaShares.heir_allocations || [];

  return (
    <div className="bg-white rounded-2xl border border-border p-5 shadow-xs">
      <div className="flex items-center justify-between gap-2 mb-4 pb-3 border-b border-border">
        <div className="flex items-center gap-2 text-primary-800 font-bold text-sm">
          <Scale className="w-4 h-4 text-accent-600" />
          <span>Deterministic Islamic Faraizi Shares (Quranic Proof)</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-success-700 bg-success-50 font-semibold px-2.5 py-1 rounded-full border border-success-200">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Sum: 100.0% ({shariaShares.total_estate_share || "1/1"})</span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-200">
              <th className="py-2.5 px-3">Heir Name</th>
              <th className="py-2.5 px-3">Relationship</th>
              <th className="py-2.5 px-3">Exact Fraction</th>
              <th className="py-2.5 px-3">Percentage</th>
              <th className="py-2.5 px-3">Allocated Portion</th>
              <th className="py-2.5 px-3">Quranic Authority</th>
              <th className="py-2.5 px-3">Jurisprudential Rule</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {allocations.map((h: any, idx: number) => (
              <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                <td className="py-2.5 px-3 font-semibold text-slate-800">{h.name}</td>
                <td className="py-2.5 px-3 capitalize text-slate-600 font-medium">{h.relationship}</td>
                <td className="py-2.5 px-3 font-mono font-bold text-primary-800">{h.exact_fraction_str}</td>
                <td className="py-2.5 px-3 font-mono font-bold text-slate-700">{h.share_percentage}%</td>
                <td className="py-2.5 px-3 font-mono font-bold text-emerald-700 bg-emerald-50/50">{h.allocated_area || `${h.share_percentage}%`}</td>
                <td className="py-2.5 px-3">
                  <span className="inline-flex items-center gap-1 font-semibold text-accent-700 bg-accent-50 px-2 py-0.5 rounded border border-accent-200/60">
                    <BookOpen className="w-3 h-3" />
                    {h.quranic_citation}
                  </span>
                </td>
                <td className="py-2.5 px-3 text-slate-500 text-[11px] italic max-w-xs">{h.theological_rationale}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {shariaShares.mathematical_proof && (
        <div className="mt-4 p-3 bg-slate-900 text-emerald-400 font-mono text-[11px] rounded-xl overflow-x-auto whitespace-pre leading-relaxed border border-slate-800">
          {shariaShares.mathematical_proof}
        </div>
      )}
    </div>
  );
}
