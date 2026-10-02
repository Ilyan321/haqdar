import { create } from "zustand";

export interface AgentStatus {
  agent_id: string;
  status: "idle" | "started" | "thinking" | "completed" | "error" | "reflecting";
  message: string;
  data?: any;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
}

export interface CaseState {
  sessionId: string | null;
  language: "en" | "roman_urdu";
  messages: ChatMessage[];
  agentStatuses: Record<string, AgentStatus>;
  pipelineStage: string;
  familyTree: any | null;
  shariaShares: any | null;
  fraudAlerts: any[];
  legalRoadmap: any | null;
  finalReport: any | null;
  isInvestigating: boolean;

  setSessionId: (id: string) => void;
  setLanguage: (lang: "en" | "roman_urdu") => void;
  addMessage: (msg: Omit<ChatMessage, "id" | "timestamp">) => void;
  updateAgentStatus: (agent_id: string, status: AgentStatus["status"], message: string, data?: any) => void;
  setPipelineStage: (stage: string) => void;
  setFamilyTree: (tree: any) => void;
  setShariaShares: (shares: any) => void;
  addFraudAlert: (alert: any) => void;
  setLegalRoadmap: (roadmap: any) => void;
  setFinalReport: (report: any) => void;
  setIsInvestigating: (inv: boolean) => void;
  resetCase: () => void;
}

export const useCaseStore = create<CaseState>((set) => ({
  sessionId: null,
  language: "en",
  messages: [],
  agentStatuses: {
    orchestrator: { agent_id: "orchestrator", status: "idle", message: "Awaiting case assignment" },
    intake_agent: { agent_id: "intake_agent", status: "idle", message: "Ready for claimant interview" },
    family_tree_agent: { agent_id: "family_tree_agent", status: "idle", message: "Awaiting genealogy roster" },
    document_analyzer: { agent_id: "document_analyzer", status: "idle", message: "Awaiting property deeds" },
    sharia_calculator: { agent_id: "sharia_calculator", status: "idle", message: "Faraizi engine standby" },
    fraud_detection_agent: { agent_id: "fraud_detection_agent", status: "idle", message: "Anti-corruption audit standby" },
    legal_strategy_agent: { agent_id: "legal_strategy_agent", status: "idle", message: "Ombudsperson roadmap ready" },
    qa_reviewer: { agent_id: "qa_reviewer", status: "idle", message: "Judicial review gatekeeper active" },
  },
  pipelineStage: "IDLE",
  familyTree: null,
  shariaShares: null,
  fraudAlerts: [],
  legalRoadmap: null,
  finalReport: null,
  isInvestigating: false,

  setSessionId: (id) => set({ sessionId: id }),
  setLanguage: (lang) => set({ language: lang }),
  addMessage: (msg) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...msg,
          id: Math.random().toString(36).substring(7),
          timestamp: new Date().toLocaleTimeString(),
        },
      ],
    })),
  updateAgentStatus: (agent_id, status, message, data) =>
    set((state) => ({
      agentStatuses: {
        ...state.agentStatuses,
        [agent_id]: { agent_id, status, message, data },
      },
    })),
  setPipelineStage: (stage) => set({ pipelineStage: stage }),
  setFamilyTree: (tree) => set({ familyTree: tree }),
  setShariaShares: (shares) => set({ shariaShares: shares }),
  addFraudAlert: (alert) =>
    set((state) => {
      const exists = state.fraudAlerts.some(
        (a) => a.alert_id === alert.alert_id || a.fraud_type === alert.fraud_type
      );
      if (exists) return state;
      return { fraudAlerts: [...state.fraudAlerts, alert] };
    }),
  setLegalRoadmap: (roadmap) => set({ legalRoadmap: roadmap }),
  setFinalReport: (report) => set({ finalReport: report }),
  setIsInvestigating: (inv) => set({ isInvestigating: inv }),
  resetCase: () =>
    set({
      sessionId: null,
      messages: [],
      pipelineStage: "IDLE",
      familyTree: null,
      shariaShares: null,
      fraudAlerts: [],
      legalRoadmap: null,
      finalReport: null,
      isInvestigating: false,
    }),
}));
