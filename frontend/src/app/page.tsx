"use client";

import React from "react";
import { useCaseStore } from "@/store/caseStore";
import { useAgentStream } from "@/hooks/useAgentStream";
import { CaseChat } from "@/components/chat/CaseChat";
import { AgentPipelineFlow } from "@/components/visualizer/AgentPipelineFlow";
import { FamilyTreeGraph } from "@/components/visualizer/FamilyTreeGraph";
import { ShareBreakdownTable } from "@/components/reports/ShareBreakdownTable";
import { FraudAndRoadmapView } from "@/components/reports/FraudAndRoadmapView";
import { ReportViewer } from "@/components/reports/ReportViewer";
import { Activity, RefreshCw } from "lucide-react";

export default function Home() {
  const { sessionId, pipelineStage, resetCase } = useCaseStore();
  const { isConnected } = useAgentStream(sessionId);

  return (
    <main className="min-h-screen bg-background flex flex-col">
      {/* Top Navigation Bar */}
      <header className="h-16 border-b border-border bg-surface/90 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-40">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary-800 text-white flex items-center justify-center font-bold text-lg shadow-xs">
            حق
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-base text-primary-900 leading-none">HaqDar</h1>
              <span className="font-bold text-accent-600 text-xs">(حقدار)</span>
              <span className="text-[10px] uppercase font-bold text-primary-800 bg-primary-50 px-2 py-0.5 rounded-full border border-primary-200">
                HEC × PakAngels AI Hackathon
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium">
              Autonomous Women&apos;s Inheritance Rights Recovery Platform
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {sessionId && (
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-slate-100 rounded-lg text-xs text-slate-600 border border-slate-200">
              <Activity className={`w-3.5 h-3.5 ${isConnected ? "text-emerald-500 animate-pulse" : "text-amber-500"}`} />
              <span className="font-mono text-[11px]">Session: {sessionId.slice(0, 8)}...</span>
              <span className="text-[10px] font-bold uppercase bg-slate-200 px-1.5 py-0.2 rounded text-slate-700">
                {pipelineStage}
              </span>
            </div>
          )}

          {sessionId && (
            <button
              onClick={resetCase}
              className="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              New Case
            </button>
          )}
        </div>
      </header>

      {/* Main Grid Workspace */}
      <div className="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-[1700px] w-full mx-auto">
        {/* Left Column (50%): Discovery, Shares & Reports */}
        <div className="lg:col-span-6 space-y-6 flex flex-col">
          <div className="h-[480px]">
            <CaseChat />
          </div>

          <ShareBreakdownTable />

          <FraudAndRoadmapView />

          <ReportViewer />
        </div>

        {/* Right Column (50%): Live Multi-Agent Visualizer & Shajra Nasab */}
        <div className="lg:col-span-6 space-y-6 flex flex-col">
          <div className="flex-1 min-h-[580px]">
            <AgentPipelineFlow />
          </div>

          <FamilyTreeGraph />
        </div>
      </div>
    </main>
  );
}
