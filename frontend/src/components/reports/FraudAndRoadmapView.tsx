"use client";

import React from "react";
import { useCaseStore } from "@/store/caseStore";
import { AlertOctagon, ShieldAlert, Navigation, Calendar, Landmark, CheckCircle } from "lucide-react";

export function FraudAndRoadmapView() {
  const { fraudAlerts, legalRoadmap, finalReport } = useCaseStore();

  const roadmapData = legalRoadmap || finalReport?.legal_roadmap;
  const alertsData = (fraudAlerts && fraudAlerts.length > 0) ? fraudAlerts : (finalReport?.fraud_report?.alerts || []);

  if ((!alertsData || alertsData.length === 0) && !roadmapData) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Fraud Forensic Alerts */}
      {alertsData && alertsData.length > 0 && (
        <div className="bg-white rounded-2xl border border-danger-200 p-5 shadow-xs">
          <div className="flex items-center gap-2 mb-3 text-danger-700 font-bold text-sm">
            <AlertOctagon className="w-4 h-4 text-danger-600" />
            <span>Criminal Dispossession & Fraud Alerts (PPC 498A)</span>
          </div>

          <div className="space-y-3">
            {alertsData.map((a: any, i: number) => (
              <div key={i} className="p-3.5 bg-danger-50 rounded-xl border border-danger-200 text-xs">
                <div className="flex items-center justify-between gap-1 mb-1.5">
                  <span className="font-bold text-danger-900 uppercase text-[11px] tracking-wide">
                    {a.fraud_type?.replace(/_/g, " ")}
                  </span>
                  <span className="bg-danger-600 text-white font-bold text-[9px] uppercase px-1.5 py-0.5 rounded">
                    {a.severity || "CRITICAL"}
                  </span>
                </div>
                <p className="text-slate-800 font-medium mb-1.5">{a.deprivation_summary || a.details}</p>
                {a.supreme_court_precedent && (
                  <div className="text-[10px] text-danger-800 bg-white/70 p-2 rounded-lg border border-danger-200/60 mt-1">
                    <span className="font-semibold">Judicial Precedent:</span> {a.supreme_court_precedent}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 60-Day Legal Recovery Roadmap */}
      {roadmapData && (
        <div className="bg-white rounded-2xl border border-primary-200 p-5 shadow-xs">
          <div className="flex items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2 text-primary-800 font-bold text-sm">
              <Navigation className="w-4 h-4 text-primary-700" />
              <span>Fast-Track Recovery Roadmap (60-Day Limit)</span>
            </div>
            <span className="text-[10px] font-bold text-accent-700 bg-accent-50 px-2 py-0.5 rounded-full border border-accent-200">
              Women's Property Rights Act 2020
            </span>
          </div>

          <div className="space-y-3">
            {(roadmapData.action_steps || []).map((step: any, idx: number) => (
              <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="font-bold text-primary-900 flex items-center gap-1.5">
                    <span className="w-4 h-4 rounded-full bg-primary-800 text-white flex items-center justify-center text-[9px] font-bold">
                      {step.step_number || idx + 1}
                    </span>
                    <span>{step.action_title || step.action}</span>
                  </div>
                  <span className="text-[10px] font-semibold text-slate-500 flex items-center gap-1">
                    <Calendar className="w-3 h-3 text-accent-600" />
                    {step.statutory_timeline}
                  </span>
                </div>
                <p className="text-slate-600 text-[11px] mb-1 pl-5">{step.procedure_details}</p>
                <div className="text-[10px] text-primary-700 font-semibold pl-5 flex items-center gap-1">
                  <Landmark className="w-3 h-3 opacity-70" />
                  Forum: {step.forum}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
