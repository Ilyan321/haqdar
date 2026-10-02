"use client";

import { useEffect, useRef } from "react";
import { useCaseStore } from "@/store/caseStore";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export function useAgentStream(sessionId: string | null) {
  const eventSourceRef = useRef<EventSource | null>(null);
  const {
    updateAgentStatus,
    setPipelineStage,
    setFamilyTree,
    setShariaShares,
    addFraudAlert,
    setFinalReport,
    setIsInvestigating,
  } = useCaseStore();

  useEffect(() => {
    if (!sessionId) return;

    const streamUrl = `${API_BASE}/case/stream/${sessionId}`;
    const es = new EventSource(streamUrl);
    eventSourceRef.current = es;

    es.addEventListener("agent_status", (e: MessageEvent) => {
      try {
        const payload = JSON.parse(e.data);
        updateAgentStatus(
          payload.agent_id,
          payload.status,
          payload.message,
          payload.data
        );
      } catch (err) {
        console.error("Error parsing agent_status event", err);
      }
    });

    es.addEventListener("pipeline_transition", (e: MessageEvent) => {
      try {
        const payload = JSON.parse(e.data);
        setPipelineStage(payload.stage || "RUNNING");
      } catch (err) {
        console.error("Error parsing pipeline_transition", err);
      }
    });

    es.addEventListener("family_tree_update", (e: MessageEvent) => {
      try {
        const payload = JSON.parse(e.data);
        setFamilyTree(payload);
      } catch (err) {
        console.error("Error parsing family_tree_update", err);
      }
    });

    es.addEventListener("sharia_shares_calculated", (e: MessageEvent) => {
      try {
        const payload = JSON.parse(e.data);
        setShariaShares(payload);
      } catch (err) {
        console.error("Error parsing sharia_shares_calculated", err);
      }
    });

    es.addEventListener("fraud_alert", (e: MessageEvent) => {
      try {
        const payload = JSON.parse(e.data);
        addFraudAlert(payload);
      } catch (err) {
        console.error("Error parsing fraud_alert", err);
      }
    });

    es.addEventListener("case_complete", (e: MessageEvent) => {
      try {
        setIsInvestigating(false);
        // Fetch full dossier
        fetch(`${API_BASE}/case/report/${sessionId}`)
          .then((res) => res.json())
          .then((data) => setFinalReport(data))
          .catch((err) => console.error("Error fetching report", err));
      } catch (err) {
        console.error("Error parsing case_complete", err);
      }
    });

    es.onerror = (err) => {
      console.warn("SSE connection closed or temporary error", err);
    };

    return () => {
      es.close();
      eventSourceRef.current = null;
    };
  }, [sessionId, updateAgentStatus, setPipelineStage, setFamilyTree, setShariaShares, addFraudAlert, setFinalReport, setIsInvestigating]);

  return { isConnected: !!eventSourceRef.current };
}
