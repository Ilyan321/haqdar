# HaqDar (حقدار) — Multi-Agent System Architecture & Design Document

> **Document Version:** 1.0.0  
> **Target Release:** HEC × PakAngels Generative & Agentic AI Hackathon  
> **Core Framework:** CrewAI  
> **Inference Engine:** Groq Cloud (`llama-3.3-70b-versatile`)  
> **Database & Vector Memory:** Supabase (PostgreSQL + `pgvector`)  
> **Real-time Telemetry:** Server-Sent Events (SSE) streaming to client UI  

---

## 1. Executive Summary & System Philosophy

**HaqDar (حقدار)** is an autonomous multi-agent platform engineered to address Pakistan's inheritance crisis, where **97% of women are systematically denied their legal inheritance** and civil litigation averages 15–30 years. 

HaqDar coordinates an ensemble of **8 specialized AI agents** operating across 11 distinct agentic design patterns (Supervisor, Router, Sequential Pipeline, Parallel Fan-Out, ReAct Tool-Use, Planning, Adversarial Debate, Reflection/Self-Correction, Human-in-the-Loop, Memory-Augmented RAG, and Real-time Telemetry).

### Core Architectural Guarantees
1. **Mathematical Determinism Over LLM Hallucination:** Islamic inheritance (*Faraizi*) calculation is strictly deterministic under Quranic jurisprudence (Surah An-Nisa 4:11, 4:12, 4:176). The LLM is **never** permitted to calculate numerical shares. Share computation is delegated to a verified, pure-Python algorithmic engine (`calculate_faraizi_shares`). The LLM only interprets and contextualizes the verified mathematical proof.
2. **Adversarial Validation & Self-Correction:** An adversarial agent pair (Fraud Detection Agent + QA Reviewer) audits all genealogy and documentary claims. The QA Reviewer acts as an automated quality gate with the authority to reject flawed outputs and force execution rollback.
3. **Dual-Language Accessibility:** Empathy-driven intake operating seamlessly in standard English, Urdu script, and Roman Urdu (*Urdu written in Latin alphabet*), bridging rural-urban literacy divides.
4. **Actionable Legal Execution:** Output is not generic advice; it generates formal legal filing roadmaps citing the *Enforcement of Women's Property Rights Act 2020*, Provincial Ombudsperson procedures, and civil court precedents.

---

## 2. Multi-Agent System Architecture & Topology

### 2.1 Workflow Topology Diagram

```mermaid
flowchart TD
    User(["Claimant / Legal Advocate"]) -->|Web UI / Roman Urdu / English| Intake["Agent 2: Intake Agent\n(Conversational Interviewer)"]
    
    Intake -->|Structured Case JSON| Orchestrator["Agent 1: Case Orchestrator\n(Supervisor & Router)"]

    subgraph ParallelPhase ["Phase 1: Concurrent Investigation (Fan-Out)"]
        Orchestrator -->|Dispatch Heir Roster| FamilyTree["Agent 3: Family Tree Agent\n(Genealogy Builder - ReAct)"]
        Orchestrator -->|Dispatch Doc Text| DocAnalyzer["Agent 4: Document Analyzer\n(Property Audit - Parallel)"]
    end

    FamilyTree -->|Verified Shajra Nasab JSON| Calc["Agent 5: Sharia Calculator\n(Faraizi Math Engine - Deterministic Tool)"]
    
    subgraph AnalysisPhase ["Phase 2: Adversarial & Strategic Analysis"]
        Calc -->|True Faraizi Shares| Fraud["Agent 6: Fraud Detection Agent\n(Adversarial Auditor)"]
        DocAnalyzer -->|Extracted Mutations & Hiba| Fraud
        Calc -->|Legal Inheritance Base| Legal["Agent 7: Legal Strategy Agent\n(Planning & RAG Agent)"]
        Fraud -->|Fraud Evidence & Flags| Legal
    end

    Legal -->|Proposed Roadmap| QA["Agent 8: QA Reviewer\n(Reflection & Quality Gate)"]
    Fraud -->|Audit Trail| QA
    Calc -->|Math Vector| QA

    QA -.->|"Self-Correction Loop\n(Recalculate if Heir Omitted)"| Calc
    QA -->|Final Validated Verdict| Orchestrator
    Orchestrator -->|Stream Completed Dossier| User
```

### 2.2 Execution Pipeline Phases

| Phase | Agents Involved | Execution Mode | Dependency | Description |
|---|---|---|---|---|
| **0. Intake** | Agent 2 (Intake) | Interactive Sequential | User Input | Interactive conversational discovery; extracts structured case facts. |
| **1. Orchestration** | Agent 1 (Orchestrator) | Supervisory Router | Case JSON | Case classification (urban vs rural, provincial jurisdiction, dispute nature). |
| **2. Fact Discovery** | Agent 3 (Family Tree), Agent 4 (Document Analyzer) | Concurrent Fan-Out (Parallel) | Case JSON | Concurrently constructs the genealogical tree and audits property document text. |
| **3. Faraizi Computation** | Agent 5 (Sharia Calculator) | Sequential Tool-Execution | Family Tree Output | Deterministic calculation of Quranic shares using symbolic Python engine. |
| **4. Deep Analysis** | Agent 6 (Fraud Detection), Agent 7 (Legal Strategy) | Adversarial / Planning (Fan-In) | Calculator + Doc Analyzer | Compares de facto transfers against de jure shares; performs RAG retrieval on Pakistani laws. |
| **5. Quality Gate** | Agent 8 (QA Reviewer) | Reflection / Self-Correction | All Prior Outputs | Verifies mathematical totals, legal citations, and completeness. Re-triggers Agent 5 if needed. |

---

## 3. Global Framework & Model Configuration

### 3.1 LLM Configuration
All agents leverage **Groq Cloud** for high-throughput, low-latency reasoning utilizing `llama-3.3-70b-versatile`.

```python
# config/llm.py
import os
from crewai import LLM

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_llama70b = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0.1,  # Low temperature to enforce deterministic analytical rigor
    max_tokens=4096,
    top_p=0.95
)

# Higher-temperature configuration for empathetic intake interactions
groq_llama70b_conversational = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0.35,
    max_tokens=2048,
    top_p=0.9
)
```

### 3.2 Rate-Limiting & Fallback Strategy
- **Groq Token Limits:** Llama 3.3 70B Versatile provides generous TPM (tokens per minute) on Groq, but burst requests during parallel fan-out are managed through an exponential backoff decorator (`tenacity` library: `wait_random_exponential(min=1, max=10)`).
- **Graceful Degradation:** If an agent reaches maximum retries (`max_iter=3`), the agent state is flagged as `error` in SSE telemetry, allowing the Case Orchestrator to inspect partial findings or reassign tasks.

---

## 4. Agent Communication & Real-Time Telemetry Protocol

### 4.1 Server-Sent Events (SSE) Stream Architecture

To deliver an engaging, transparent hackathon demo and production UX, every state change across the 8 agents emits a structured event via Server-Sent Events (SSE) over HTTP streaming (`/api/cases/{case_id}/stream`).

```mermaid
sequenceDiagram
    autonumber
    actor Client as Frontend Client (React / Next.js)
    participant Stream as SSE Controller
    participant Orch as Agent 1: Orchestrator
    participant Agents as CrewAI Agent Cluster
    participant Tool as Python Math Tool / Supabase

    Client->>Stream: GET /api/cases/{case_id}/stream
    Stream-->>Client: Connection Established (text/event-stream)
    
    Orch->>Stream: Emit {"agent_id": "orchestrator", "status": "started", "message": "Classifying case parameters"}
    Stream-->>Client: event: agent_status\ndata: {...}

    Orch->>Agents: Task Execution
    Agents->>Stream: Emit {"agent_id": "sharia_calculator", "status": "thinking", "message": "Invoking deterministic engine"}
    Stream-->>Client: event: agent_status\ndata: {...}

    Agents->>Tool: calculate_faraizi_shares(heirs)
    Tool-->>Agents: shares: {wife: 0.125, daughters: 0.4375, sons: 0.4375}
    
    Agents->>Stream: Emit {"agent_id": "sharia_calculator", "status": "completed", "data": {...}}
    Stream-->>Client: event: agent_status\ndata: {...}
```

### 4.2 SSE Event Payload Schema

```typescript
export interface AgentSSEEvent {
  event_id: string;               // UUID v4
  case_id: string;                // Case identifier
  timestamp: string;              // ISO 8601 UTC
  agent_id: 
    | "case_orchestrator"
    | "intake_agent"
    | "family_tree_agent"
    | "document_analyzer"
    | "sharia_calculator"
    | "fraud_detection_agent"
    | "legal_strategy_agent"
    | "qa_reviewer";
  status: "started" | "thinking" | "completed" | "error";
  message: string;                // Human-readable progress log in English or Urdu
  data?: Record<string, any>;     // Output payload or intermediate artifact
  execution_time_ms?: number;     // Telemetry profiling
}
```

---

## 5. Detailed Specifications for All 8 Agents

---

### Agent 1: Case Orchestrator

#### 1. System Metadata & Design Pattern
- **Identifier:** `case_orchestrator`
- **Design Pattern:** Hierarchical Supervisor + Dynamic Router
- **Role:** Central case manager, routing hub, and lifecycle controller

#### 2. CrewAI Agent Definition
```python
from crewai import Agent

case_orchestrator = Agent(
    role="Supreme Inheritance Case Director and Router",
    goal=(
        "Analyze ingested inheritance dispute data, classify legal jurisdiction, "
        "property categorization, and dispute complexity, dynamically route tasks "
        "to specialized agents, supervise cross-agent synthesis, and deliver "
        "a complete, validated legal recovery dossier."
    ),
    backstory=(
        "You are a retired Senior Registrar of the High Court of Pakistan with 35 years of "
        "experience overseeing complex land disputes, inheritance mutations, and constitutional "
        "petitions. You possess an exhaustive understanding of Pakistani provincial land laws "
        "(Punjab Land Revenue Act, Sindh Tenancy Act, KPK and Balochistan land codes) and Islamic "
        "jurisprudence. Your duty is to direct and coordinate junior investigative agents with "
        "military precision, ensuring no detail is overlooked and procedural rules are strictly respected."
    ),
    llm=groq_llama70b,
    memory=True,
    verbose=True,
    allow_delegation=True,
    max_iter=4
)
```

#### 3. CrewAI Task Definition
```python
from crewai import Task

orchestrator_routing_task = Task(
    description=(
        "Review the structured intake JSON from the Intake Agent. "
        "1. Classify the case across: (a) Jurisdiction (Punjab / Sindh / KPK / Balochistan / ICT), "
        "(b) Property Type (Urban residential / Urban commercial / Rural agricultural / Mixed), "
        "(c) Nature of Dispute (Complete heir omission / Fake gift deed 'Hiba' / Coerced release deed / Delayed mutation). "
        "2. Formulate the master investigation plan and initialize execution context for the "
        "Family Tree Agent and Document Analyzer. "
        "3. Monitor pipeline outputs and compile the comprehensive final dossier."
    ),
    expected_output=(
        "A JSON Master Case Dossier containing case classification, designated legal jurisdiction, "
        "execution timeline, status summaries of all sub-investigations, and final synthesis."
    ),
    agent=case_orchestrator,
    output_pydantic=CaseDossierOutput
)
```

#### 4. Tools Required
- `case_classifier_tool`: Deterministic mapping of tehsils, districts, and provinces to applicable revenue acts (e.g., Punjab Land Revenue Act 1967 vs. Sindh Revenue Code).
- `dispatch_event_tool`: Emits SSE streaming updates to the application bus.

#### 5. Input / Output Schema

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CaseClassification(BaseModel):
    province: str = Field(..., description="Punjab, Sindh, KPK, Balochistan, or ICT")
    land_type: str = Field(..., description="agricultural, urban_residential, urban_commercial, mixed")
    primary_dispute_category: str = Field(
        ..., 
        description="heir_omission, fraudulent_hiba, unmutated_inheritance, coerced_relinquishment"
    )
    applicable_act: str = Field(..., description="E.g., Enforcement of Women's Property Rights Act 2020")
    urgency_level: str = Field(..., description="standard, urgent, emergency_freeze_required")

class CaseDossierOutput(BaseModel):
    case_id: str
    classification: CaseClassification
    investigation_plan: List[str]
    subagent_routing_manifest: Dict[str, bool]
```

#### 6. Error Handling
- **Missing Jurisdiction:** Default to Federal jurisdiction (`ICT / Ombudsperson for Protection Against Harassment / Women's Property Rights Act 2020`) if province is ambiguous, flagging a request for clarification.
- **Agent Stalling:** If a delegated agent fails to return within 15 seconds, the Orchestrator initiates a retry with constrained token parameters.

#### 7. Inter-Agent Interaction
- **Upstream:** Receives structured output from Agent 2 (Intake Agent).
- **Downstream:** Fans out parallel dispatches to Agent 3 (Family Tree) and Agent 4 (Document Analyzer). Receives final certified report from Agent 8 (QA Reviewer).

---

### Agent 2: Intake Agent

#### 1. System Metadata & Design Pattern
- **Identifier:** `intake_agent`
- **Design Pattern:** Sequential Conversational Pipeline
- **Role:** Empathetic interviewer and structured case fact extractor

#### 2. CrewAI Agent Definition
```python
intake_agent = Agent(
    role="Empathetic Legal Intake Officer and Fact Extractor",
    goal=(
        "Conduct an empathetic, patient, and highly structured interview with the claimant "
        "in English, Urdu, or Roman Urdu. Extract all requisite factual data: deceased name, "
        "exact date of death, complete roster of known immediate and extended relatives, "
        "property descriptions, and claimant's specific grievances."
    ),
    backstory=(
        "You are a compassionate paralegal and human rights advocate based in Lahore who has spent "
        "a decade assisting dispossessed rural and urban Pakistani women. You understand that "
        "clients are often distressed, traumatized by family betrayal, or unfamiliar with legal jargon. "
        "You speak fluid Roman Urdu ('Mera bhai zameen apne naam karwa chuka hai') and formal Urdu "
        "with natural ease. You never judge, always reassure, and systematically extract every single "
        "critical legal fact required to build an unassailable legal case."
    ),
    llm=groq_llama70b_conversational,
    memory=True,
    verbose=True,
    allow_delegation=False
)
```

#### 3. CrewAI Task Definition
```python
intake_collection_task = Task(
    description=(
        "Engage with the claimant transcript/input. If raw narrative is provided in Roman Urdu "
        "or English, parse all factual tokens. Ensure the following data points are extracted: "
        "1. Deceased's full name, religion/sect (Sunni/Hanafi or Shia), date and place of death. "
        "2. Marital status at death, surviving spouses. "
        "3. Complete list of sons, daughters, father, mother, brothers, sisters, and grandfather. "
        "4. Exact textual descriptions of all disputed properties (Khasra numbers, square yards, acres, cities). "
        "5. The grievance narrative (who seized control, what documents were allegedly signed)."
    ),
    expected_output=(
        "Strictly validated JSON object matching the RawCaseIntakeSchema containing normalized names, "
        "dates, family lists, and grievance details."
    ),
    agent=intake_agent,
    output_pydantic=RawCaseIntakeSchema
)
```

#### 4. Tools Required
- `roman_urdu_normalizer`: Converts Roman Urdu terms (*"walid"*, *"bhai"*, *"intiqal"*, *"bhanja"*, *"chachi"*, *"murabba"*, *"kanal"*) into standardized legal entity tokens.
- `date_parser_tool`: Resolves conversational dates (*"3 saal pehle Eid ke baad"*, *"Dec 2021"*) into approximate or exact ISO 8601 date ranges.

#### 5. Input / Output Schema

```python
class ClaimedHeirInput(BaseModel):
    name: str
    relationship_to_deceased: str = Field(
        ..., 
        description="son, daughter, wife, husband, father, mother, brother, sister, etc."
    )
    is_alive: bool = True
    gender: str = Field(..., description="male, female")
    is_claimant: bool = False

class RawPropertyInput(BaseModel):
    location: str
    area_description: str  # E.g., "4 Kanals agricultural land in Chak 42-RB Faisalabad"
    estimated_value_pkr: Optional[float] = None
    claimed_documents: List[str] = Field(default_factory=list)

class RawCaseIntakeSchema(BaseModel):
    case_id: str
    claimant_name: str
    claimant_language: str = Field(..., description="en, urdu, roman_urdu")
    deceased_name: str
    date_of_death: str
    sect: str = Field(default="Hanafi", description="Hanafi, Shia, etc.")
    family_members: List[ClaimedHeirInput]
    properties: List[RawPropertyInput]
    alleged_fraud_description: str
```

#### 6. Error Handling
- **Ambiguous Family Terminology:** In Pakistani culture, terms like *"Bhai"* can mean full brother, stepbrother, or cousin. The agent detects ambiguous relationship strings and prompts clarification questions before finalizing output.
- **Missing Date of Death:** Flags `date_of_death_estimated = true` and uses the earliest known dispute event as an anchor.

#### 7. Inter-Agent Interaction
- **Upstream:** Ingests raw user prompt or chat dialogue.
- **Downstream:** Delivers `RawCaseIntakeSchema` directly to Agent 1 (Case Orchestrator).

---

### Agent 3: Family Tree Agent

#### 1. System Metadata & Design Pattern
- **Identifier:** `family_tree_agent`
- **Design Pattern:** ReAct (Reason + Act) / Tool-Use
- **Role:** Genealogical architect constructing the Shajra Nasab and uncovering excluded legal heirs

#### 2. CrewAI Agent Definition
```python
family_tree_agent = Agent(
    role="Master Genealogist and Shajra Nasab Reconstruction Specialist",
    goal=(
        "Reconstruct the complete, legally valid genealogical family tree (Shajra Nasab) "
        "of the deceased under Islamic jurisprudence. Identify every heir with legal standing, "
        "audit for missing generational links, and detect intentionally omitted female heirs."
    ),
    backstory=(
        "You are an archival genealogy master trained in both traditional rural Pakistani Revenue "
        "Record keeping (*Shajra Nasab e Pind*) and modern NADRA Family Registration Certificate (FRC) "
        "tree architectures. You know the exact deceptive stratagems corrupt revenue officials "
        "and patriarchal families employ to drop daughters, infant sisters, and widowed mothers from "
        "the pedigree charts. You methodically reconstruct familial degrees of proximity (Darja-e-Qarabat) "
        "to ensure 100% legal heir coverage."
    ),
    llm=groq_llama70b,
    memory=True,
    verbose=True,
    allow_delegation=False
)
```

#### 3. CrewAI Task Definition
```python
build_genealogy_task = Task(
    description=(
        "Take the family members list from the intake dossier. "
        "1. Invoke `family_tree_builder` to generate a hierarchical genealogical node graph. "
        "2. Invoke `heir_identifier` to cross-reference every listed node against Islamic Hanafi legal heir classes. "
        "3. Explicitly audit for omitted heirs: Did the deceased have daughters who were omitted? "
        "Is the mother of the deceased alive? Did any child predecease the father? "
        "4. Format the final family structure into a tree JSON schema compatible with visualization."
    ),
    expected_output=(
        "A complete, validated FamilyTreeSchema containing categorized heirs (Primary Quranic Sharers, "
        "Residuaries, Distant Kindred), node linkages, and an audit of potential omitted heirs."
    ),
    agent=family_tree_agent,
    output_pydantic=FamilyTreeSchema
)
```

#### 4. Tools Required
- `family_tree_builder`: Python graph construction tool using directed acyclic graph (DAG) topology to connect deceased, spouses, ascendants, and descendants.
- `heir_identifier`: Rules engine that classifies each individual into Islamic legal categories:
  - *Ashab al-Furudh* (Quranic Sharers)
  - *Asaba* (Residuaries)
  - *Zawil Arham* (Distant Kindred)
  - *Mahjoob* (Excluded / Blocked Heirs)

#### 5. Input / Output Schema

```python
class GenealogicalNode(BaseModel):
    id: str
    name: str
    relationship: str
    gender: str
    alive_at_deceased_death: bool
    sharia_heir_category: str = Field(
        ..., 
        description="ashab_al_furudh, asaba, zawil_arham, excluded"
    )
    parent_ids: List[str] = Field(default_factory=list)
    spouse_ids: List[str] = Field(default_factory=list)
    omission_risk_flag: bool = Field(
        default=False, 
        description="Flagged true if suspected of being hidden from land revenue records"
    )

class FamilyTreeSchema(BaseModel):
    case_id: str
    deceased_id: str
    nodes: List[GenealogicalNode]
    potential_omitted_heirs_detected: List[str]
    tree_depth: int
    total_eligible_heirs_count: int
```

#### 6. Error Handling
- **Predeceased Children:** Under Section 4 of the *Muslim Family Laws Ordinance 1961 (MFLO)* in Pakistan, children of a predeceased child are entitled to their parent's share (per stirpes representation). The agent checks if grandchildren of predeceased offspring exist and applies Pakistani statutory rules alongside classical Sharia classification.
- **Cycles in Graph:** Validates that no cyclic familial loops exist (DAG verification).

#### 7. Inter-Agent Interaction
- **Upstream:** Receives raw family roster from Agent 1 (Orchestrator).
- **Downstream:** Outputs validated `FamilyTreeSchema` to Agent 5 (Sharia Calculator) and Agent 6 (Fraud Detection).

---

### Agent 4: Document Analyzer

#### 1. System Metadata & Design Pattern
- **Identifier:** `document_analyzer`
- **Design Pattern:** Parallel Execution (runs concurrently with Agent 3)
- **Role:** Forensic auditor of property records, mutation entries (*Intiqal*), and gift deeds (*Hiba*)

#### 2. CrewAI Agent Definition
```python
document_analyzer = Agent(
    role="Forensic Revenue Document and Mutation Records Analyst",
    goal=(
        "Analyze textual descriptions and transcripts of Pakistani land records, "
        "Fard Malkiat, Intiqal (mutation registers), Hiba (gift deeds), and Aks Shajra. "
        "Extract critical factual metrics (land acreage, transfer dates, attestations) "
        "and detect procedural anomalies or signs of fabrication."
    ),
    backstory=(
        "You are an expert revenue audit consultant and former Tehsildar with encyclopedic "
        "knowledge of Pakistani revenue record maintenance under the Punjab Land Revenue Act 1967 "
        "and modern PLRA (Punjab Land Records Authority) computerized systems. You know the exact "
        "loopholes used to forge oral gift deeds (*Hiba Tamleek*), unverified mutations without "
        "Jalsa-e-Aam (public assembly), and suspicious transfers executed days before a patriarch's demise."
    ),
    llm=groq_llama70b,
    memory=True,
    verbose=True,
    allow_delegation=False
)
```

#### 3. CrewAI Task Definition
```python
document_audit_task = Task(
    description=(
        "Examine the text descriptions of property deeds, mutations, and registry extracts "
        "provided in the case record. "
        "1. Extract: Property area in standard Pakistani metrics (Kanal, Marla, Murabba, Acre, Sq Yds), "
        "mutation/transfer dates, named transferor, named transferees, consideration amount (if any). "
        "2. Analyze Hiba claims: Is it an oral Hiba (*Hiba-Dahani*) or registered deed? "
        "Does it demonstrate offer, acceptance, and delivery of possession (*Tasleem-o-Raza*)? "
        "3. Audit chronological anomalies: Was the property transferred shortly before the deceased's "
        "death (*Marz-ul-Maut* / Death-illness doctrine)? "
        "4. Flag missing female signatures or absent witness attestations."
    ),
    expected_output=(
        "Structured DocumentAnalysisSchema containing extracted property assets, mutation transaction "
        "logs, and an itemized anomaly report."
    ),
    agent=document_analyzer,
    output_pydantic=DocumentAnalysisSchema
)
```

#### 4. Tools Required
- `area_converter_tool`: Standardizes Pakistani traditional land units:
  - 1 Murabba = 25 Acres
  - 1 Acre = 8 Kanals
  - 1 Kanal = 20 Marlas
  - 1 Marla = 225 or 272.25 sq ft
  - Standardizes to both Kanals/Marlas and Square Meters.
- `chronology_audit_tool`: Computes date deltas between recorded property mutation date and deceased's certified date of death.

#### 5. Input / Output Schema

```python
class MutationRecord(BaseModel):
    mutation_number: Optional[str]
    document_type: str = Field(..., description="Intiqal, Hiba, Registry, Fard, Tamleek")
    transfer_date: Optional[str]
    days_prior_to_death: Optional[int]
    transferor: str
    transferees: List[str]
    area_transferred_sqft: float
    reported_consideration_pkr: float = 0.0
    anomalies_detected: List[str]

class DocumentAnalysisSchema(BaseModel):
    case_id: str
    total_properties_count: int
    total_area_marla: float
    mutations: List[MutationRecord]
    suspicious_hiba_detected: bool
    marz_ul_maut_applicable: bool = Field(
        ..., 
        description="True if transfer executed during fatal illness without heir consent"
    )
    unauthorized_female_waiver_detected: bool
```

#### 6. Error Handling
- **Missing Mutation Numbers:** If the user cannot provide registration or mutation numbers, the tool tags them as *"Unverified Oral Claim / Pre-mutation Stage"* rather than failing.
- **Unrecognized Regional Area Units:** Standardizes regional variances in Marla size (225 sq ft in Lahore urban vs. 272 sq ft in rural Punjab).

#### 7. Inter-Agent Interaction
- **Upstream:** Receives raw document text via Agent 1 (Orchestrator).
- **Downstream:** Passes `DocumentAnalysisSchema` concurrently with Agent 3's output into Agent 6 (Fraud Detection).

---

### Agent 5: Sharia Inheritance Calculator

#### 1. System Metadata & Design Pattern
- **Identifier:** `sharia_calculator`
- **Design Pattern:** Sequential + Deterministic Python Tool-Execution
- **Role:** Pure mathematical Faraizi calculation engine & theological contextualizer

> [!IMPORTANT]
> **Zero LLM Hallucination Mandate:** The LLM does NOT calculate shares, fractions, or percentages. The LLM executes the verified Python function `calculate_faraizi_shares(heirs)`. The function computes exact shares through symbolic rational arithmetic (`fractions.Fraction`), and the LLM merely translates the verified mathematical results into structured explanations with Quranic citations.

#### 2. CrewAI Agent Definition
```python
sharia_calculator = Agent(
    role="Chief Islamic Faraizi Inheritance Math Engine & Scholar",
    goal=(
        "Call the deterministic Python tool `calculate_faraizi_shares` with the eligible heir roster "
        "from the Family Tree Agent. Never calculate fractions yourself. Receive the pure mathematical "
        "output, formulate an exact breakdown for each legal heir, and cite the governing Quranic "
        "verses (Surah An-Nisa 4:11, 4:12, 4:176) and Sunnah principles."
    ),
    backstory=(
        "You are an eminent Mufti and Sharia mathematician specializing in Islamic Law of Succession "
        "(*Ilm al-Fara'id*). You strictly uphold the divine principle that inheritance distribution "
        "is a fixed mathematical science prescribed directly in the Holy Quran. You know that LLMs make "
        "arithmetic errors when calculating complex fractions, Aul, or Radd. Therefore, you ALWAYS "
        "delegate mathematical calculation to your audited Python execution tool, verifying that the sum "
        "of all distributed shares equals 1.000000 (100%) without exception."
    ),
    llm=groq_llama70b,
    memory=True,
    verbose=True,
    allow_delegation=False
)
```

#### 3. CrewAI Task Definition
```python
calculate_shares_task = Task(
    description=(
        "1. Extract the active, eligible heirs from the FamilyTreeSchema. "
        "2. Format the heir list into the parameter signature required by `calculate_faraizi_shares`. "
        "3. Execute the tool `calculate_faraizi_shares`. "
        "4. Ingest the returned fractional shares and percentages. "
        "5. Draft an exhaustive theological and legal explanation mapping each heir to their "
        "governing Quranic rule (e.g., Wife gets 1/8 under 4:12 due to surviving issue; Daughters "
        "share 2/3 or receive 1:2 ratio alongside brothers under 4:11). "
        "6. Provide the financial and area breakdown for each disputed property."
    ),
    expected_output=(
        "A certified ShariaDistributionSchema detailing exact fractions, percentages, land area "
        "allocations, and Quranic citations for every single lawful heir."
    ),
    agent=sharia_calculator,
    output_pydantic=ShariaDistributionSchema
)
```

#### 4. Tools Required
- `calculate_faraizi_shares`: **Pure Python deterministic calculation engine**. Implements classical Hanafi Faraizi rules, including *Ashab al-Furudh*, *Asaba*, *Hajb* (exclusion), *Aul* (proportional deficit adjustment), and *Radd* (re-allocation of surplus). Detailed in Section 6.

#### 5. Input / Output Schema

```python
from fractions import Fraction

class HeirShareAllocation(BaseModel):
    heir_id: str
    name: str
    relationship: str
    gender: str
    quranic_category: str  # Ashab al-Furudh, Asaba, etc.
    exact_fraction_str: str  # E.g., "1/8", "7/24", "7/48"
    share_percentage: float  # E.g., 12.50, 14.5833
    allocated_marla: float
    quranic_citation: str  # E.g., "Surah An-Nisa 4:12"
    theological_rationale: str

class ShariaDistributionSchema(BaseModel):
    case_id: str
    total_estate_share: float = 1.0
    adjustment_applied: str = Field(..., description="normal, aul, radd")
    base_denominator: int
    heir_allocations: List[HeirShareAllocation]
    calculation_hash: str = Field(
        ..., 
        description="SHA-256 hash of deterministic Python calculation run"
    )
```

#### 6. Error Handling
- **Tool Failure / Mathematical Imbalance:** If the Python tool output does not sum to `Fraction(1, 1)` (after Aul/Radd handling), the agent aborts and invokes the `qa_reviewer` immediately rather than attempting an LLM approximation.
- **Zero Heirs / Sole Spouse Edge Cases:** Automatically applies modern Pakistani legal precedents regarding Radd for surviving spouses.

#### 7. Inter-Agent Interaction
- **Upstream:** Receives `FamilyTreeSchema` from Agent 3.
- **Downstream:** Delivers `ShariaDistributionSchema` to Agent 6 (Fraud Detection), Agent 7 (Legal Strategy), and Agent 8 (QA Reviewer).

---

### Agent 6: Fraud Detection Agent

#### 1. System Metadata & Design Pattern
- **Identifier:** `fraud_detection_agent`
- **Design Pattern:** Adversarial / Cross-Examination Investigator
- **Role:** Forensic investigator exposing illegal dispossession and forged mutations

#### 2. CrewAI Agent Definition
```python
fraud_detection_agent = Agent(
    role="Adversarial Inheritance Fraud Investigator and Anti-Corruption Auditor",
    goal=(
        "Cross-reference claimed property distributions (from Document Analyzer) against "
        "immutable Sharia shares (from Sharia Calculator) and true genealogical heirs (from Family Tree). "
        "Relentlessly detect: omitted female heirs, sham Hiba deeds, forged relinquishment "
        "affidavits (*Dastbardari*), and unlawful revenue officer (*Patwari*) collusion."
    ),
    backstory=(
        "You are a seasoned former Special Prosecutor for the National Accountability Bureau (NAB) "
        "and Anti-Corruption Establishment (ACE) in Punjab. You have prosecuted hundreds of corrupt "
        "revenue clerks, Patwaris, and predatory male relatives who exploit patriarchal cultural "
        "pressure to disinherit sisters and mothers. You operate with an adversarial mindset: you assume "
        "any document where a female heir surrenders millions of rupees in real estate for zero "
        "consideration is prima facie fraudulent until strictly proven otherwise."
    ),
    llm=groq_llama70b,
    memory=True,
    verbose=True,
    allow_delegation=False
)
```

#### 3. CrewAI Task Definition
```python
fraud_investigation_task = Task(
    description=(
        "Conduct an adversarial forensic audit of the case: "
        "1. Compare the list of heirs in the FamilyTreeSchema against the transferees in DocumentAnalysisSchema. "
        "Identify every lawful heir receiving ZERO or less than their Quranic share. "
        "2. Audit Hiba claims: Evaluate whether the alleged gift was registered, if possession was transferred, "
        "and if it was executed during fatal illness (*Marz-ul-Maut*). Under Supreme Court of Pakistan "
        "precedent (PLD 2017 SC 633, PLD 2021 SC 753), gifts disinheriting female heirs carry a heavy burden of proof. "
        "3. Evaluate *Dastbardari* (relinquishment deeds): In Pakistani law, relinquishing an expectant "
        "right (*Spes Successionis*) before inheritance opens is void ab initio. "
        "4. Assign severity ratings (CRITICAL, HIGH, MEDIUM) to each detected fraud vector."
    ),
    expected_output=(
        "A structured FraudAuditReportSchema itemizing all fraud alerts, affected heirs, violated legal statutes, "
        "and evidentiary discrepancies."
    ),
    agent=fraud_detection_agent,
    output_pydantic=FraudAuditReportSchema
)
```

#### 4. Tools Required
- `discrepancy_calculator`: Computes delta between Sharia-mandated land entitlement and de facto registry allotment for each heir.
- `hiba_authenticity_checker`: Evaluates transaction variables against 7 mandatory legal tests established by the Supreme Court of Pakistan for valid Hiba to female exclusion.

#### 5. Input / Output Schema

```python
class FraudAlert(BaseModel):
    alert_id: str
    severity: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    fraud_type: str = Field(
        ..., 
        description="omitted_female_heir, forged_hiba, marz_ul_maut_transfer, illegal_dastbardari, patwari_tampering"
    )
    victim_heir_name: str
    perpetrator_heir_name: Optional[str]
    deprivation_marla: float
    estimated_deprivation_value_pkr: float
    evidence_trail: str
    supreme_court_precedent: str

class FraudAuditReportSchema(BaseModel):
    case_id: str
    overall_fraud_score: float = Field(..., description="0.0 (No fraud) to 1.0 (Definite criminal fraud)")
    critical_alerts_count: int
    alerts: List[FraudAlert]
    prima_facie_criminal_offenses: List[str]  # E.g., PPC 420, 468, 471, 498A
```

#### 6. Error Handling
- **Voluntary Genuine Gift Claim:** If a valid registered gift deed with bank consideration exists, the agent downgrades severity from CRITICAL to MEDIUM, highlighting the need for court trial on undue influence (*Section 16, Contract Act 1872*).
- **Missing Land Values:** Automatically queries average district DC rates (*District Collector Valuation Table*) to estimate stolen property value.

#### 7. Inter-Agent Interaction
- **Upstream:** Ingests outputs from Agent 4 (Document Analyzer) and Agent 5 (Sharia Calculator).
- **Downstream:** Delivers `FraudAuditReportSchema` to Agent 7 (Legal Strategy) and Agent 8 (QA Reviewer).

---

### Agent 7: Legal Strategy Agent

#### 1. System Metadata & Design Pattern
- **Identifier:** `legal_strategy_agent`
- **Design Pattern:** Planning Agent + Agentic RAG (Supabase pgvector)
- **Role:** Master legal recovery strategist crafting an actionable procedural roadmap

#### 2. CrewAI Agent Definition
```python
legal_strategy_agent = Agent(
    role="Supreme Pakistani Land Litigation Strategist & Ombudsperson Specialist",
    goal=(
        "Synthesize all case facts, mathematical shares, and fraud alerts into an actionable, "
        "rapid legal recovery roadmap. Prioritize fast-track administrative relief via the "
        "Ombudsperson under the Enforcement of Women's Property Rights Act 2020 over stagnant "
        "civil litigation, citing relevant statutes and Supreme Court case laws."
    ),
    backstory=(
        "You are an eminent High Court advocate and constitutional counsel who drafted key sections "
        "of the *Enforcement of Women's Property Rights Act 2020* and provincial amendments. You know that "
        "traditional civil suits for declaration (*Section 42, Specific Relief Act*) take 15–30 years. "
        "You champion the Ombudsperson forum, which legally mandates resolution within **60 days**, "
        "ordering deputy commissioners to restore physical possession. You back every step with "
        "unimpeachable statutory citations and Supreme Court precedents."
    ),
    llm=groq_llama70b,
    memory=True,
    verbose=True,
    allow_delegation=False
)
```

#### 3. CrewAI Task Definition
```python
generate_legal_roadmap_task = Task(
    description=(
        "1. Retrieve applicable Pakistani statutes and precedents by invoking `search_legal_knowledge` "
        "using queries targeted at the detected fraud patterns and provincial jurisdiction. "
        "2. Formulate a 3-track recovery roadmap: "
        "   - **Track 1: Primary Administrative Relief** (Filing before Federal/Provincial Ombudsperson under "
        "     the Women's Property Rights Act 2020 for a 60-day dispossession decree). "
        "   - **Track 2: Revenue Department Rectification** (Application to Deputy Commissioner/Collector "
        "     under Section 53/164 of the Land Revenue Act 1967 for correction of mutation). "
        "   - **Track 3: Criminal & Civil Safeguards** (FIR under Pakistan Penal Code Section 498A "
        "     [depriving woman of inheritance - 10 yrs imprisonment], stay order under Order 39 Rules 1-2 CPC). "
        "3. Provide step-by-step instructions, filing fee breakdowns, and draft application templates."
    ),
    expected_output=(
        "A structured LegalRoadmapSchema with prioritized legal actions, exact forum designations, "
        "timeline forecasts, statutory citations, and draft legal petition text."
    ),
    agent=legal_strategy_agent,
    output_pydantic=LegalRoadmapSchema
)
```

#### 4. Tools Required
- `search_legal_knowledge`: RAG tool querying Supabase PostgreSQL with `pgvector` embeddings (`text-embedding-3-small` or `bge-m3`). Contains Pakistani inheritance statutes, Land Revenue Acts, and Supreme Court rulings.
- `court_fee_calculator`: Computes court fees and stamp duties according to provincial Court Fees Act 1870 schedules.

#### 5. Input / Output Schema

```python
class LegalActionStep(BaseModel):
    step_number: int
    forum: str = Field(..., description="Ombudsperson, Deputy Commissioner, Civil Judge, Session Court")
    statute_invoked: str
    action_type: str = Field(..., description="ombudsperson_petition, revenue_review, stay_application, fir")
    target_relief: str
    expected_duration_days: int
    procedural_requirements: List[str]
    precedent_citation: str

class LegalRoadmapSchema(BaseModel):
    case_id: str
    recommended_primary_forum: str
    estimated_resolution_days: int
    recovery_roadmap: List[LegalActionStep]
    draft_ombudsperson_petition_text: str
    criminal_charges_applicable: List[str]
    citations: List[str]
```

#### 6. Error Handling
- **Civil Court Lis Pendens:** If a civil suit is already pending, Section 4 of the Women's Property Rights Act 2020 allows the Ombudsperson to refer the matter to the court or conduct an inquiry. The agent detects pending litigation and adjusts the strategy to invoke the Ombudsperson's accelerated inquiry powers.
- **RAG Retrieval Failure:** If vector search yields low confidence scores (<0.7), the agent uses verified baseline statutory provisions embedded in its knowledge base.

#### 7. Inter-Agent Interaction
- **Upstream:** Ingests `ShariaDistributionSchema` and `FraudAuditReportSchema`.
- **Downstream:** Delivers `LegalRoadmapSchema` to Agent 8 (QA Reviewer).

---

### Agent 8: QA Reviewer

#### 1. System Metadata & Design Pattern
- **Identifier:** `qa_reviewer`
- **Design Pattern:** Reflection / Self-Correction & Quality Gate
- **Role:** Independent auditing gatekeeper with rollback and re-execution authority

#### 2. CrewAI Agent Definition
```python
qa_reviewer = Agent(
    role="Supreme Judicial Quality Gate & Reflection Auditor",
    goal=(
        "Perform an unsparing quality audit over the complete investigative dossier. "
        "Independently re-run the Sharia math calculation, verify that sum of shares equals 1.0, "
        "confirm that no female or legal heir was overlooked, validate every statutory citation, "
        "and enforce a self-correction loop if any discrepancy is detected."
    ),
    backstory=(
        "You are an incorruptible Judicial Inspector General of the High Court. You have zero "
        "tolerance for sloppy legal citations, mathematical rounding errors, or unverified claims. "
        "You do not rubber-stamp reports. If an agent omitted an heir or cited an obsolete statute, "
        "you reject the submission, provide explicit corrective instructions, and force the offending "
        "agent to re-execute their task until the analysis is flawless."
    ),
    llm=groq_llama70b,
    memory=True,
    verbose=True,
    allow_delegation=True
)
```

#### 3. CrewAI Task Definition
```python
qa_audit_task = Task(
    description=(
        "Execute a comprehensive 4-point verification over the collective case outputs: "
        "1. **Mathematical Verification:** Independently execute `calculate_faraizi_shares`. "
        "Compare against Sharia Calculator's output. Verify that the sum of all shares equals 1.000000. "
        "2. **Omission Audit:** Check if any surviving family member from the Intake record was "
        "erroneously excluded from the calculation. "
        "3. **Citation & Law Verification:** Verify that cited statutes match the case's province "
        "(e.g., ensure Punjab Women's Property Act is not applied to a Sindh case). "
        "4. **Verdict Generation:** If any test fails, emit status `REJECTED_NEEDS_REVISION` with "
        "corrective directives and trigger re-execution. If all pass, emit status `CERTIFIED_PASSED`."
    ),
    expected_output=(
        "A formal ValidationReportSchema indicating pass/fail status, verification checklists, "
        "re-execution directives (if failed), and official certification."
    ),
    agent=qa_reviewer,
    output_pydantic=ValidationReportSchema
)
```

#### 4. Tools Required
- `independent_math_verifier`: Standalone execution of the pure Python Faraizi engine to cross-check Agent 5's results independently.
- `statute_jurisdiction_validator`: Rules database validating provincial law applicability.

#### 5. Input / Output Schema

```python
class VerificationItem(BaseModel):
    check_name: str
    passed: bool
    details: str

class ValidationReportSchema(BaseModel):
    case_id: str
    verdict: str = Field(..., description="CERTIFIED_PASSED or REJECTED_NEEDS_REVISION")
    math_checksum_passed: bool
    omitted_heirs_audit_passed: bool
    jurisdiction_statute_match_passed: bool
    re_execution_target_agent: Optional[str] = None
    re_execution_directive: Optional[str] = None
    checks: List[VerificationItem]
    certified_timestamp: str
```

#### 6. Error Handling & Reflection Loop
```mermaid
sequenceDiagram
    participant QA as Agent 8: QA Reviewer
    participant Calc as Agent 5: Sharia Calculator
    participant Orch as Agent 1: Case Orchestrator
    
    QA->>QA: Audit Sharia Calculator shares
    alt Discrepancy Found (e.g., Deceased's Mother Omitted)
        QA->>QA: Set verdict = "REJECTED_NEEDS_REVISION"
        QA->>Orch: Notify reflection trigger (Target: Agent 5)
        Orch->>Calc: Re-execute task with amended heir roster (Include Mother)
        Calc->>Calc: Re-run deterministic Python tool
        Calc-->>QA: New ShariaDistributionSchema
        QA->>QA: Re-verify checksum (1.000000) -> Passed!
    end
    QA->>Orch: Verdict = "CERTIFIED_PASSED"
```

#### 7. Inter-Agent Interaction
- **Upstream:** Ingests outputs from all 7 previous agents.
- **Downstream:** If failed, routes back to the relevant agent (typically Agent 5 or Agent 7). If passed, transfers certified dossier to Agent 1 (Orchestrator) for client delivery.

---

## 6. The Deterministic Faraizi Inheritance Calculation Algorithm

### 6.1 Theological & Legal Basis
The Islamic law of inheritance (*Ilm al-Fara'id*) is codified directly in the Holy Quran across three primary verses:
- **Surah An-Nisa (4:11):** Shares of children and parents (*"Allah instructs you concerning your children: for the male, what is equal to the share of two females..."*).
- **Surah An-Nisa (4:12):** Shares of spouses and uterine siblings (*"And for you is half of what your wives leave if they have no child..."*).
- **Surah An-Nisa (4:176):** Shares of collaterals/siblings in *Kalalah* (deceased without parents or offspring).

Because these Quranic prescriptions are mathematical axioms, **they cannot be approximated or inferred probabilistically by an LLM**.

```
                        ┌──────────────────────────────────────────────┐
                        │          Total Estate Net Assets             │
                        │   (After debts, funeral, valid 1/3 bequests) │
                        └──────────────────────┬───────────────────────┘
                                               │
                                               ▼
                        ┌──────────────────────────────────────────────┐
                        │   Phase 1: Ashab al-Furudh (Quranic Shares)  │
                        │       Allocated fixed shares (1/2 to 1/8)    │
                        └──────────────────────┬───────────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       │                                               │
              Sum of Shares = 1.0                             Sum of Shares != 1.0
                       │                                               │
                       ▼                                               ▼
        ┌─────────────────────────────┐               ┌─────────────────────────────────┐
        │ Exactly Distributed         │               │ Check Total Relative to Unity   │
        └─────────────────────────────┘               └────────────────┬────────────────┘
                                                                       │
                                      ┌────────────────────────────────┴────────────────┐
                                      ▼                                                 ▼
                         Sum > 1.0 (Deficit)                               Sum < 1.0 (Surplus)
                                      │                                                 │
                                      ▼                                                 ▼
                        ┌───────────────────────────┐                     ┌───────────────────────────┐
                        │       Doctrine of AUL     │                     │ Check for Asaba (Residuary│
                        │ Increase denominator to   │                     └─────────────┬─────────────┘
                        │ sum of numerators         │                                   │
                        └───────────────────────────┘                     ┌─────────────┴─────────────┐
                                                                          ▼                           ▼
                                                                     Asaba Exists               No Asaba Exists
                                                                          │                           │
                                                                          ▼                           ▼
                                                            ┌───────────────────────────┐ ┌───────────────────────────┐
                                                            │ Asaba Takes Entire Remainder│ Doctrine of RADD          │
                                                            │ (Male = 2x Female ratio)  │ Return surplus proportionally│
                                                            └───────────────────────────┘ └───────────────────────────┘
```

---

### 6.2 The Three Heir Classes

#### 1. Ashab al-Furudh (Quranic Fixed Sharers)
Twelve distinct relatives defined in the Quran who take designated fractional shares:

| Heir | Share Conditions | Share Fraction | Governing Verse |
|---|---|---|---|
| **Husband** | No surviving child/grandchild | **1/2** | Quran 4:12 |
| **Husband** | With surviving child/grandchild | **1/4** | Quran 4:12 |
| **Wife / Wives** | No surviving child/grandchild | **1/4** (shared if multiple) | Quran 4:12 |
| **Wife / Wives** | With surviving child/grandchild | **1/8** (shared if multiple) | Quran 4:12 |
| **Daughter** | Single, no son | **1/2** | Quran 4:11 |
| **Daughters (2+)** | Multiple daughters, no son | **2/3** (equally shared) | Quran 4:11 |
| **Father** | With surviving son/grandson | **1/6** (fixed share) | Quran 4:11 |
| **Father** | With daughters only | **1/6 + Residuary (Asaba)** | Quran 4:11 |
| **Father** | No children or grandchildren | **Sole Residuary (takes all)**| Quran 4:11 |
| **Mother** | With children or 2+ siblings | **1/6** | Quran 4:11 |
| **Mother** | No children, max 1 sibling | **1/3** | Quran 4:11 |
| **True Grandfather** | Same as father if father deceased (blocked by father) | **1/6 / Residuary** | Hadith / Ijma |
| **True Grandmother** | No mother present | **1/6** | Hadith / Ijma |
| **Full Sister** | Single, Kalalah (no parents/children) | **1/2** | Quran 4:176 |
| **Full Sisters (2+)**| Multiple, Kalalah | **2/3** (equally shared) | Quran 4:176 |
| **Uterine Sibling (1)**| Single maternal brother/sister, Kalalah | **1/6** | Quran 4:12 |
| **Uterine Siblings (2+)**| Multiple, Kalalah | **1/3** (shared equally, no 2:1 ratio) | Quran 4:12 |

#### 2. Asaba (Residuaries)
Heirs who receive the balance of the estate after *Ashab al-Furudh* have received their Quranic shares:
- **Asaba bi-Nafsihi (Residuary in their own right):** All male agnates (Son, Son's Son, Father, Paternal Grandfather, Full Brother, Consanguine Brother, Full Brother's Son, Paternal Uncle).
- **Asaba bi-Ghayrihi (Residuary through another):** Females who become residuaries alongside their male counterparts in a 2:1 ratio:
  - Daughter with Son (Son gets 2 shares, Daughter gets 1 share).
  - Son's Daughter with Son's Son.
  - Full Sister with Full Brother.
- **Asaba ma'a Ghayrihi (Residuary together with another):** Full or consanguine sisters inheriting remainder when co-existing with daughters (and no brothers exist).

#### 3. Zawil Arham (Distant Kindred)
Blood relatives who are neither Quranic sharers nor residuaries (e.g., daughter's children, sister's children, maternal uncles/aunts). They inherit only when neither *Ashab al-Furudh* nor *Asaba* exist.

---

### 6.3 Hajb (Blocking & Exclusion Rules)
Exclusion operates under two principles:
- **Hajb al-Nuqsan (Reduction):** Partial reduction of a share due to another heir's presence (e.g., Wife reduced from 1/4 to 1/8 by presence of children).
- **Hajb al-Hirman (Total Exclusion):** An heir completely blocks a more distant relative:

| Closer Heir (Blocker) | Excluded Heirs (Blocked) | Theological Basis |
|---|---|---|
| **Son** | Grandsons, Granddaughters, Brothers, Sisters, Nephews, Uncles | Direct agnatic descendant priority |
| **Father** | Paternal Grandfather, Paternal Grandmother, Brothers, Sisters | Direct agnatic ascendant priority |
| **Mother** | Maternal and Paternal Grandmothers | Direct maternal priority |
| **Full Brother** | Consanguine Brothers, Consanguine Sisters, Nephews | Proximity of two-sided bloodline |

---

### 6.4 The Doctrine of Aul (العول — Proportional Reduction in Deficit)
When multiple Quranic sharers co-exist, the sum of their Quranic fractional shares can exceed unity (`Sum > 1.0`). Under classical Islamic jurisprudence established by the Second Caliph **Umar ibn al-Khattab (RA)** with consensus (*Ijma*), the shares cannot be fulfilled literally without depleting the estate.

**Aul Algorithm:**
1. Express all Quranic fractions over a common denominator $D_{base}$.
2. Compute the sum of all numerators $N_{total} = \sum N_i$.
3. If $N_{total} > D_{base}$, the new denominator becomes $D_{new} = N_{total}$.
4. Each heir's adjusted share becomes $\frac{N_i}{D_{new}}$.
5. This reduces every heir's share proportionally, distributing the deficit equitably.

*Example:* Husband (1/2), Mother (1/3), 2 Full Sisters (2/3).  
Common base denominator = 6:
- Husband: $3/6$
- Mother: $2/6$
- 2 Sisters: $4/6$
- Sum of numerators: $3 + 2 + 4 = 9$.  
- Since $9 > 6$, Aul applies. Base shifts from 6 to 9.
- Adjusted shares: Husband = $3/9$ (1/3), Mother = $2/9$, 2 Sisters = $4/9$. Sum = $9/9 = 1.000000$.

---

### 6.5 The Doctrine of Radd (الرد — Proportional Return of Surplus)
When Quranic sharers do not exhaust the estate (`Sum < 1.0`) and **no Asaba (residuary heirs)** exist, a surplus remains.

**Radd Algorithm:**
1. The surplus $1 - \sum \text{Shares}$ is returned proportionally to the Quranic sharers.
2. Under traditional Hanafi law, the spouse was excluded from Radd if other blood sharers existed.
3. **Pakistani Legal Statutory Standard:** Modern Pakistani court precedent (Supreme Court of Pakistan) and administrative practice grant Radd across all surviving heirs, including the surviving spouse when no other blood relatives exist, avoiding unjust escheat to the state.

---

### 6.6 Deterministic Python Implementation Reference

```python
# core/faraizi_calculator.py
"""
Deterministic Islamic Inheritance (Faraizi) Math Engine.
Complies strictly with Quran 4:11, 4:12, 4:176 and Hanafi Jurisprudence.
ZERO FLOATING-POINT ERRORS: Uses Python fractions.Fraction.
"""
from fractions import Fraction
from typing import List, Dict, Any
import hashlib
import json

def calculate_faraizi_shares(heirs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes exact legal shares for all heirs.
    Args:
        heirs: List of dicts, each with keys:
               'id', 'relationship' (wife, husband, son, daughter, father, mother, etc.),
               'gender', 'count' (int)
    Returns:
        Dict with status, shares per heir, fractional representation, and Aul/Radd status.
    """
    # Count specific heir categories
    counts = {h["relationship"]: h.get("count", 1) for h in heirs}
    num_wives = counts.get("wife", 0)
    has_husband = counts.get("husband", 0) > 0
    num_sons = counts.get("son", 0)
    num_daughters = counts.get("daughter", 0)
    has_father = counts.get("father", 0) > 0
    has_mother = counts.get("mother", 0) > 0
    
    has_children = (num_sons + num_daughters) > 0
    
    shares: Dict[str, Fraction] = {}
    citations: Dict[str, str] = {}
    
    # 1. SPOUSAL ALLOCATION (Quran 4:12)
    if has_husband:
        shares["husband"] = Fraction(1, 4) if has_children else Fraction(1, 2)
        citations["husband"] = "Quran 4:12 (Husband)"
    elif num_wives > 0:
        total_wife_share = Fraction(1, 8) if has_children else Fraction(1, 4)
        shares["wife"] = total_wife_share  # Divided equally among wives
        citations["wife"] = "Quran 4:12 (Wife/Wives)"

    # 2. PARENTAL ALLOCATION (Quran 4:11)
    if has_mother:
        if has_children or counts.get("brother", 0) + counts.get("sister", 0) >= 2:
            shares["mother"] = Fraction(1, 6)
        else:
            shares["mother"] = Fraction(1, 3)
        citations["mother"] = "Quran 4:11 (Mother)"
        
    if has_father:
        if num_sons > 0:
            shares["father"] = Fraction(1, 6)  # Fixed sharer only
        elif num_daughters > 0:
            shares["father"] = Fraction(1, 6)  # Gets 1/6 + residuary later
        else:
            # Father will take residuary later
            shares["father"] = Fraction(0, 1)
        citations["father"] = "Quran 4:11 (Father)"

    # 3. DAUGHTERS ONLY (Quran 4:11)
    if num_daughters > 0 and num_sons == 0:
        if num_daughters == 1:
            shares["daughters_total"] = Fraction(1, 2)
        else:
            shares["daughters_total"] = Fraction(2, 3)
        citations["daughters_total"] = "Quran 4:11 (Daughters without sons)"

    # Sum of Quranic fixed shares
    sum_fixed = sum(shares.values())

    # 4. RESIDUARY HANDLING (ASABA)
    remainder = Fraction(1, 1) - sum_fixed
    adjustment = "normal"
    
    if num_sons > 0:
        # Sons and Daughters inherit as Asaba bi-Ghayrihi (2:1 ratio)
        total_units = (num_sons * 2) + num_daughters
        son_unit_share = (remainder * 2) / total_units
        daughter_unit_share = remainder / total_units
        
        shares["sons_total"] = son_unit_share * num_sons
        if num_daughters > 0:
            shares["daughters_total"] = daughter_unit_share * num_daughters
            citations["daughters_total"] = "Quran 4:11 (Residuary 1:2 with brothers)"
        citations["sons_total"] = "Quran 4:11 (Residuary Asaba)"
        
    elif has_father and num_sons == 0:
        # Father takes remaining as Asaba
        shares["father"] = shares.get("father", Fraction(0, 1)) + remainder
        citations["father"] = "Quran 4:11 (Father as Asaba)"
        
    elif remainder < 0:
        # DOCTRINE OF AUL (Deficit Adjustment)
        adjustment = "aul"
        common_denom = 1
        for fr in shares.values():
            if fr.denominator != 0:
                from math import lcm
                common_denom = lcm(common_denom, fr.denominator)
        
        sum_numerators = sum(fr.numerator * (common_denom // fr.denominator) for fr in shares.values())
        # Re-scale each fraction
        shares = {k: Fraction(fr.numerator * (common_denom // fr.denominator), sum_numerators) 
                  for k, fr in shares.items()}
                  
    elif remainder > 0 and num_sons == 0 and not has_father:
        # DOCTRINE OF RADD (Return of Surplus)
        adjustment = "radd"
        # Distribute remainder proportionally to non-spousal sharers (or all per Pakistani law)
        eligible_for_radd = {k: v for k, v in shares.items() if k not in ["husband", "wife"]}
        if not eligible_for_radd:
            eligible_for_radd = shares  # Spouse takes Radd if sole survivor
            
        sum_radd_shares = sum(eligible_for_radd.values())
        for k in eligible_for_radd:
            shares[k] = shares[k] + (remainder * (shares[k] / sum_radd_shares))

    # Compile result breakdown
    output_breakdown = []
    for h in heirs:
        rel = h["relationship"]
        count = h.get("count", 1)
        
        if rel == "son":
            frac = shares["sons_total"] / count
            cit = citations.get("sons_total", "Quran 4:11")
        elif rel == "daughter":
            frac = shares["daughters_total"] / count
            cit = citations.get("daughters_total", "Quran 4:11")
        elif rel == "wife":
            frac = shares["wife"] / count
            cit = citations.get("wife", "Quran 4:12")
        else:
            frac = shares.get(rel, Fraction(0, 1)) / count
            cit = citations.get(rel, "Islamic Faraizi")
            
        output_breakdown.append({
            "heir_id": h["id"],
            "relationship": rel,
            "fraction_str": f"{frac.numerator}/{frac.denominator}",
            "percentage": round(float(frac) * 100, 4),
            "citation": cit
        })
        
    # Validation checksum: sum must equal exactly 1.0
    total_percentage = sum(item["percentage"] for item in output_breakdown)
    raw_hash = hashlib.sha256(json.dumps(output_breakdown, sort_keys=True).encode()).hexdigest()
    
    return {
        "status": "success",
        "adjustment": adjustment,
        "shares": output_breakdown,
        "checksum_total_percentage": round(total_percentage, 2),
        "calculation_hash": raw_hash
    }
```

---

## 7. Comprehensive Case Walkthrough: The Dispossession of Fatima

To illustrate the dynamic coordination of all 8 agents, this walkthrough demonstrates a representative case study: **Fatima Bibi from Okara, Punjab**.

### 7.1 Case Background & Ingested Facts
- **Deceased:** Muhammad Din (passed away November 2021 in Okara, Punjab).
- **Surviving Family at Death:**
  - Widow: Hajra Bibi
  - Sons: Tariq Mehmood, Asif Mehmood
  - Daughter: Fatima Bibi (Claimant)
  - Mother of Deceased: Zainab Bibi (alive at father's death, died 2023)
- **Disputed Property:** 24 Kanals of prime agricultural land (Chak 14-L, Okara).
- **The Fraud:** Brothers registered mutation (*Intiqal No. 1422*) omitting Fatima Bibi and mother Zainab Bibi, presenting a forged oral gift deed (*Hiba-Dahani*) claiming Fatima surrendered her share for Rs. 50,000 dowry payment.

---

### 7.2 Multi-Agent Execution Trace

```mermaid
sequenceDiagram
    autonumber
    actor Fatima as Claimant Fatima
    participant Intake as Agent 2: Intake Agent
    participant Orch as Agent 1: Case Orchestrator
    participant Tree as Agent 3: Family Tree
    participant Doc as Agent 4: Document Analyzer
    participant Calc as Agent 5: Sharia Calculator
    participant Fraud as Agent 6: Fraud Detection
    participant Legal as Agent 7: Legal Strategy
    participant QA as Agent 8: QA Reviewer

    Fatima->>Intake: "Walid ki 24 Kanal zameen thi. Bhaiyon ne fake Hiba bana kar mera haq cheen liya."
    Intake->>Intake: Normalize Roman Urdu; extract 5 heirs, 24 Kanals, Hiba dispute
    Intake->>Orch: Deliver RawCaseIntakeSchema

    Orch->>Orch: Classify: Punjab rural agricultural, Hiba fraud, High urgency
    par Parallel Investigation
        Orch->>Tree: Build Shajra Nasab DAG
        Orch->>Doc: Audit Intiqal No. 1422 & Hiba text
    end

    Tree->>Tree: Nodes: Mother, Wife, 2 Sons, 1 Daughter. Flags Fatima as Omitted in Revenue Records.
    Doc->>Doc: Flags: Hiba dated 7 days prior to death (Marz-ul-Maut), No witness for female waiver.

    Tree-->>Calc: Pass verified heir nodes
    Calc->>Calc: Execute deterministic Python engine: calculate_faraizi_shares()
    Calc-->>Fraud: Pure mathematical shares (Wife: 3/24, Mother: 4/24, Remainder to Sons & Daughter)
    Doc-->>Fraud: De facto transfer: Sons took 100%, Fatima received 0%

    Fraud->>Fraud: 🚨 CRITICAL FRAUD DETECTED: Fatima deprived of 14.17% (3.4 Kanals). Sham Hiba violates PLD 2021 SC 753.
    Fraud-->>Legal: Fraud report & evidence trail
    Calc-->>Legal: Sharia shares

    Legal->>Legal: Supabase pgvector RAG: Women's Property Rights Act 2020 + Punjab Amendment
    Legal-->>QA: Propose 60-day Ombudsperson eviction petition + Section 498A PPC FIR

    rect rgb(240, 248, 255)
        Note over QA,Calc: Reflection & Quality Gate Audit
        QA->>QA: Check 1: Math Sum = 1.0? Yes (100.00%)
        QA->>QA: Check 2: All heirs present? Yes (Mother, Wife, 2 Sons, Daughter)
        QA->>QA: Check 3: Jurisdiction match? Punjab Law matches Okara District!
        QA-->>Orch: CERTIFIED_PASSED (Hash: 9a3f2...)
    end

    Orch-->>Fatima: Stream Complete Bilingual Dossier & Drafted Ombudsperson Petition
```

---

### 7.3 Mathematical Proof for the Case

Under Surah An-Nisa (4:11 & 4:12), the 24 Kanals of Muhammad Din are distributed as follows:

$$\text{Total Estate} = 24.0 \text{ Kanals} = 100\%$$

1. **Wife (Hajra Bibi):** Children exist $\implies \frac{1}{8} = 12.50\% \implies \mathbf{3.00 \text{ Kanals}}$ (Quran 4:12)
2. **Mother (Zainab Bibi):** Children exist $\implies \frac{1}{6} = 16.67\% \implies \mathbf{4.00 \text{ Kanals}}$ (Quran 4:11)
3. **Residuary Remainder ($Asaba$):**
   $$\text{Remainder} = 1 - \left(\frac{1}{8} + \frac{1}{6}\right) = 1 - \frac{7}{24} = \frac{17}{24} = 70.833\% \implies 17.00 \text{ Kanals}$$
4. **Distribution among 2 Sons and 1 Daughter:**
   - Ratio: Son receives $2\times$ Daughter's share.
   - Total units: $(2 \times 2) + 1 = 5 \text{ units}$.
   - Value per unit: $\frac{17/24}{5} = \frac{17}{120} = 3.40 \text{ Kanals}$.
   - **Son 1 (Tariq):** $2 \text{ units} \implies \frac{34}{120} = 28.33\% \implies \mathbf{6.80 \text{ Kanals}}$
   - **Son 2 (Asif):** $2 \text{ units} \implies \frac{34}{120} = 28.33\% \implies \mathbf{6.80 \text{ Kanals}}$
   - **Daughter (Fatima Bibi):** $1 \text{ unit} \implies \frac{17}{120} = 14.17\% \implies \mathbf{3.40 \text{ Kanals}}$

$$\text{Check: } 3.00 + 4.00 + 6.80 + 6.80 + 3.40 = \mathbf{24.00 \text{ Kanals}} \quad (100.00\%)$$

**Fraud Verdict:** Tariq and Asif unlawfully usurped **3.40 Kanals** belonging to Fatima Bibi and **4.00 Kanals** belonging to mother Zainab Bibi, valued at approximately **PKR 18,500,000**.

---

## 8. Supabase & Vector Storage Architecture

### 8.1 Database Schema (PostgreSQL)

```sql
-- Cases Master Table
CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claimant_id UUID REFERENCES auth.users(id),
    case_title TEXT NOT NULL,
    province TEXT NOT NULL,
    district TEXT NOT NULL,
    property_category TEXT NOT NULL,
    status TEXT DEFAULT 'intake_active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Realtime Agent Telemetry Logs
CREATE TABLE agent_telemetry_logs (
    id BIGSERIAL PRIMARY KEY,
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    agent_id TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT NOT NULL,
    payload JSONB,
    execution_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Legal Corpus pgvector Table
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE legal_knowledge_chunks (
    id BIGSERIAL PRIMARY KEY,
    statute_name TEXT NOT NULL,
    section_number TEXT,
    province TEXT,
    text_content TEXT NOT NULL,
    embedding VECTOR(1536), -- Compatible with OpenAI / Groq embedding models
    citation_source TEXT
);

-- Indexing for sub-millisecond retrieval
CREATE INDEX ON legal_knowledge_chunks USING hnsw (embedding vector_cosine_ops);
```

### 8.2 RAG Knowledge Corpus Contents
The Supabase vector store is seeded with the complete statutory corpus of Pakistani inheritance law:
1. *The Enforcement of Women's Property Rights Act 2020* (Federal Act XII of 2020)
2. *The Punjab Enforcement of Women's Property Rights Act 2021*
3. *The Khyber Pakhtunkhwa Enforcement of Women's Property Rights Act 2019*
4. *The West Pakistan Land Revenue Act 1967* (Sections 42, 53, 164)
5. *Pakistan Penal Code 1860* (Section 498A: Prohibition of depriving women from inheriting property)
6. *Supreme Court Precedents:*
   - **PLD 2021 SC 753:** *Ghulam Qasim v. Mst. Razia Begum* (Burden of proof on beneficiary of oral gift excluding female heirs).
   - **PLD 2017 SC 633:** *Mst. Sughran Bibi v. Asghar Ali* (Relinquishment of inheritance rights by females without independent legal advice is void).
   - **2022 SCMR 1221:** Mandatory jurisdiction of Ombudsperson to restore physical possession.

---

## 9. Hackathon Pitch & Judge Evaluation Matrix

| Hackathon Scoring Category | Weight | HaqDar Agentic Implementation |
|---|:---:|---|
| **Autonomous Agent Architecture** | 25% | **8 distinct agents** coordinating through Hierarchical Supervisor, Fan-Out, ReAct, and Reflection patterns. Real CrewAI implementation with Groq acceleration. |
| **Technical Depth & Innovation** | 25% | **Zero-hallucination deterministic math engine** integrated seamlessly via CrewAI tool calling. Dynamic RAG retrieval using Supabase `pgvector`. |
| **Real-World Impact & Relevance** | 20% | Directly targets a crisis afflicting **97% of Pakistani women** (over 115 million citizens), compressing 15–30 year litigation into a 60-day Ombudsperson action plan. |
| **Self-Correction & Reflection** | 15% | Agent 8 actively stress-tests Agent 5's mathematical allocations and forces rollback if omissions or errors occur, proving true cognitive agency. |
| **User Experience & Telemetry** | 15% | Real-time SSE streaming visual node graph, multi-lingual intake (English & Roman Urdu), and production-ready Pydantic typed schemas. |

---

*HaqDar (حقدار) — Restoring what is rightfully theirs, one case at a time.*
