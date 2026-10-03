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

export interface ExtractedFacts {
  deceased_name?: string;
  date_of_death?: string;
  sons_count?: number;
  daughters_count?: number;
  widow_alive?: boolean;
  wives_count?: number;
  mother_alive?: boolean;
  father_alive?: boolean;
  brothers_count?: number;
  sisters_count?: number;
  property_area?: string;
  property_type?: string;
  has_quantitative_measurement?: boolean;
  location?: string;
  debts_or_liabilities?: string;
  wills_or_bequests?: string;
  dispute_type?: string;
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
  extractedFacts: ExtractedFacts;
  suggestedOptions: string[];
  isReadyToLaunch: boolean;

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
  setExtractedFacts: (facts: ExtractedFacts) => void;
  setSuggestedOptions: (opts: string[]) => void;
  setIsReadyToLaunch: (ready: boolean) => void;
  resetCase: () => void;
}

const INITIAL_AGENT_STATUSES: Record<string, AgentStatus> = {
  orchestrator: { agent_id: "orchestrator", status: "idle", message: "Awaiting case assignment" },
  intake_agent: { agent_id: "intake_agent", status: "idle", message: "Ready for claimant interview" },
  family_tree_agent: { agent_id: "family_tree_agent", status: "idle", message: "Awaiting genealogy roster" },
  document_analyzer: { agent_id: "document_analyzer", status: "idle", message: "Awaiting property deeds" },
  sharia_calculator: { agent_id: "sharia_calculator", status: "idle", message: "Faraizi engine standby" },
  fraud_detection_agent: { agent_id: "fraud_detection_agent", status: "idle", message: "Anti-corruption audit standby" },
  legal_strategy_agent: { agent_id: "legal_strategy_agent", status: "idle", message: "Ombudsperson roadmap ready" },
  qa_reviewer: { agent_id: "qa_reviewer", status: "idle", message: "Judicial review gatekeeper active" },
};

export const useCaseStore = create<CaseState>((set) => ({
  sessionId: null,
  language: "en",
  messages: [],
  agentStatuses: INITIAL_AGENT_STATUSES,
  pipelineStage: "IDLE",
  familyTree: null,
  shariaShares: null,
  fraudAlerts: [],
  legalRoadmap: null,
  finalReport: null,
  isInvestigating: false,
  extractedFacts: {},
  suggestedOptions: [],
  isReadyToLaunch: false,

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
  setExtractedFacts: (facts) =>
    set((state) => ({ extractedFacts: { ...state.extractedFacts, ...facts } })),
  setSuggestedOptions: (opts) => set({ suggestedOptions: opts }),
  setIsReadyToLaunch: (ready) => set({ isReadyToLaunch: ready }),
  resetCase: () =>
    set({
      sessionId: null,
      messages: [],
      agentStatuses: INITIAL_AGENT_STATUSES,
      pipelineStage: "IDLE",
      familyTree: null,
      shariaShares: null,
      fraudAlerts: [],
      legalRoadmap: null,
      finalReport: null,
      isInvestigating: false,
      extractedFacts: {},
      suggestedOptions: [],
      isReadyToLaunch: false,
    }),
}));
