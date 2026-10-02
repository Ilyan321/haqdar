"use client";

import React, { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Node,
  Edge,
  Position,
  MarkerType,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useCaseStore } from "@/store/caseStore";

const AGENT_CONFIGS = [
  { id: "orchestrator", label: "🎯 Case Orchestrator", role: "Supervisor & Router", x: 250, y: 20 },
  { id: "intake_agent", label: "📋 Intake Agent", role: "Guided Fact Discovery", x: 50, y: 130 },
  { id: "family_tree_agent", label: "👨‍👩‍👧‍👦 Family Tree", role: "Genealogy & Heirs", x: 250, y: 130 },
  { id: "document_analyzer", label: "📄 Document Analyzer", role: "Mutation & Deed Audit", x: 450, y: 130 },
  { id: "sharia_calculator", label: "⚖️ Sharia Calculator", role: "Deterministic Math (Quran 4:11)", x: 250, y: 250 },
  { id: "fraud_detection_agent", label: "🔍 Fraud Detection", role: "Adversarial PPC 498A Audit", x: 120, y: 370 },
  { id: "legal_strategy_agent", label: "📜 Legal Strategy", role: "60-Day Ombudsperson Plan", x: 380, y: 370 },
  { id: "qa_reviewer", label: "🛡️ QA Reviewer", role: "Judicial Reflection Gate", x: 250, y: 490 },
];

export function AgentPipelineFlow() {
  const { agentStatuses } = useCaseStore();

  const nodes: Node[] = useMemo(() => {
    return AGENT_CONFIGS.map((cfg) => {
      const statusObj = agentStatuses[cfg.id] || { status: "idle", message: "" };
      const status = statusObj.status;

      let borderClass = "border-slate-300 bg-white text-slate-800";
      let badgeClass = "bg-slate-100 text-slate-600";
      let pulse = false;

      if (status === "thinking" || status === "started") {
        borderClass = "border-info-600 bg-info-50 text-primary-900 shadow-md ring-2 ring-info-600/30";
        badgeClass = "bg-info-600 text-white animate-pulse";
        pulse = true;
      } else if (status === "completed") {
        borderClass = "border-success-600 bg-success-50 text-slate-900 shadow-sm";
        badgeClass = "bg-success-600 text-white";
      } else if (status === "error") {
        borderClass = "border-danger-600 bg-danger-50 text-danger-900";
        badgeClass = "bg-danger-600 text-white";
      }

      return {
        id: cfg.id,
        position: { x: cfg.x, y: cfg.y },
        data: {
          label: (
            <div className={`p-3 rounded-xl border transition-all duration-300 w-52 text-left ${borderClass}`}>
              <div className="flex items-center justify-between gap-1 mb-1">
                <span className="font-bold text-xs truncate">{cfg.label}</span>
                <span className={`text-[9px] uppercase px-1.5 py-0.5 rounded font-semibold tracking-wider ${badgeClass}`}>
                  {status}
                </span>
              </div>
              <div className="text-[11px] font-medium text-slate-500 mb-1">{cfg.role}</div>
              {statusObj.message && (
                <div className="text-[10px] text-slate-600 border-t border-slate-200/60 pt-1 mt-1 line-clamp-2 italic">
                  {statusObj.message}
                </div>
              )}
            </div>
          ),
        },
        sourcePosition: Position.Bottom,
        targetPosition: Position.Top,
      };
    });
  }, [agentStatuses]);

  const edges: Edge[] = useMemo(() => [
    { id: "e-orch-intake", source: "orchestrator", target: "intake_agent", animated: true },
    { id: "e-orch-tree", source: "orchestrator", target: "family_tree_agent", animated: true },
    { id: "e-orch-doc", source: "orchestrator", target: "document_analyzer", animated: true },
    { id: "e-tree-calc", source: "family_tree_agent", target: "sharia_calculator", animated: true },
    { id: "e-doc-calc", source: "document_analyzer", target: "sharia_calculator", animated: true },
    { id: "e-calc-fraud", source: "sharia_calculator", target: "fraud_detection_agent", animated: true },
    { id: "e-calc-legal", source: "sharia_calculator", target: "legal_strategy_agent", animated: true },
    { id: "e-fraud-qa", source: "fraud_detection_agent", target: "qa_reviewer", animated: true },
    { id: "e-legal-qa", source: "legal_strategy_agent", target: "qa_reviewer", animated: true },
  ], []);

  return (
    <div className="w-full h-full min-h-[580px] bg-slate-50 rounded-2xl border border-border shadow-sm overflow-hidden relative">
      <div className="absolute top-3 left-4 z-10 bg-white/90 backdrop-blur px-3 py-1.5 rounded-lg border border-border shadow-xs text-xs font-semibold text-primary-800 flex items-center gap-2">
        <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
        Live Multi-Agent Orchestration Topology
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        attributionPosition="bottom-right"
      >
        <Background color="#cbd5e1" gap={16} size={1} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
