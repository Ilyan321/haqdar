"use client";

import React, { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Node,
  Edge,
  Position,
  ReactFlowProvider,
  useReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useCaseStore } from "@/store/caseStore";
import { AlertTriangle, CheckCircle, User, Focus } from "lucide-react";

function FamilyTreeGraphInner() {
  const { familyTree } = useCaseStore();
  const { fitView } = useReactFlow();

  const handleRecenter = () => {
    fitView({ padding: 0.2, duration: 400 });
  };

  const { nodes, edges } = useMemo(() => {
    if (!familyTree || !familyTree.nodes) {
      return { nodes: [], edges: [] };
    }

    const flowNodes: Node[] = [];
    const flowEdges: Edge[] = [];

    // Root node: Deceased
    const rootId = "deceased-root";
    flowNodes.push({
      id: rootId,
      position: { x: 300, y: 30 },
      data: {
        label: (
          <div className="p-3 bg-slate-800 text-white rounded-xl border border-slate-700 shadow-md text-center w-56">
            <div className="text-[10px] uppercase tracking-wider text-accent-500 font-bold">Deceased Estate Owner</div>
            <div className="font-bold text-sm truncate">{familyTree.deceased_name || "Deceased"}</div>
          </div>
        ),
      },
      sourcePosition: Position.Bottom,
    });

    const heirList = familyTree.nodes || [];
    const spacing = 220;
    const startX = Math.max(20, 300 - ((heirList.length - 1) * spacing) / 2);

    heirList.forEach((heir: any, idx: number) => {
      const isOmitted = heir.omission_risk_flag;
      const heirId = `heir-${heir.id || idx}`;

      flowNodes.push({
        id: heirId,
        position: { x: startX + idx * spacing, y: 180 },
        data: {
          label: (
            <div
              className={`p-3 rounded-xl border transition-all text-left w-52 shadow-xs ${
                isOmitted
                  ? "bg-danger-50 border-danger-600 text-danger-900 ring-2 ring-danger-600/30"
                  : "bg-white border-success-600 text-slate-800"
              }`}
            >
              <div className="flex items-center justify-between gap-1 mb-1">
                <span className="font-bold text-xs truncate">{heir.name}</span>
                {isOmitted ? (
                  <span className="flex items-center gap-0.5 text-[9px] bg-danger-600 text-white px-1.5 py-0.5 rounded font-bold uppercase">
                    <AlertTriangle className="w-2.5 h-2.5" /> Omitted
                  </span>
                ) : (
                  <span className="flex items-center gap-0.5 text-[9px] bg-success-600 text-white px-1.5 py-0.5 rounded font-bold uppercase">
                    <CheckCircle className="w-2.5 h-2.5" /> Heir
                  </span>
                )}
              </div>
              <div className="text-[11px] font-semibold text-slate-600 capitalize">
                {heir.relationship} ({heir.gender})
              </div>
              <div className="text-[10px] text-slate-500 mt-1">
                Category: <span className="font-mono">{heir.sharia_heir_category}</span>
              </div>
            </div>
          ),
        },
        targetPosition: Position.Top,
      });

      flowEdges.push({
        id: `e-root-${heirId}`,
        source: rootId,
        target: heirId,
        animated: isOmitted,
        style: {
          stroke: isOmitted ? "#DC2626" : "#059669",
          strokeWidth: 2,
        },
      });
    });

    return { nodes: flowNodes, edges: flowEdges };
  }, [familyTree]);

  if (!familyTree || !familyTree.nodes || familyTree.nodes.length === 0) {
    return (
      <div className="p-8 text-center text-slate-400 bg-white rounded-xl border border-dashed border-slate-300">
        <User className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm font-medium">Genealogical tree will appear here during investigation.</p>
      </div>
    );
  }

  return (
    <div className="w-full h-80 bg-slate-50 rounded-2xl border border-border shadow-sm overflow-hidden relative">
      <div className="absolute top-3 left-4 z-10 bg-white/90 backdrop-blur px-3 py-1.5 rounded-lg border border-border shadow-xs text-xs font-semibold text-primary-800">
        Reconstructed Shajra Nasab (Genealogical Tree)
      </div>

      <button
        onClick={handleRecenter}
        title="Recenter & Fit View"
        className="absolute top-3 right-4 z-10 bg-white/95 hover:bg-slate-100 text-primary-900 px-3 py-1.5 rounded-lg border border-border shadow-xs text-xs font-bold flex items-center gap-1.5 transition-all active:scale-95"
      >
        <Focus className="w-3.5 h-3.5 text-accent-600" />
        <span>Recenter View</span>
      </button>

      <ReactFlow nodes={nodes} edges={edges} fitView attributionPosition="bottom-right">
        <Background color="#cbd5e1" gap={16} size={1} />
        <Controls />
      </ReactFlow>
    </div>
  );
}

export function FamilyTreeGraph() {
  return (
    <ReactFlowProvider>
      <FamilyTreeGraphInner />
    </ReactFlowProvider>
  );
}
