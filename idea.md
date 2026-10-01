# HaqDar (حقدار) — AI-Powered Women's Inheritance Rights Recovery Platform

> *"Restoring what is rightfully theirs, one case at a time."*

---

## The Problem

**97% of Pakistani women never receive their lawful landed inheritance.**

Despite Pakistan's constitution AND explicit Islamic Sharia mandates guaranteeing women's inheritance rights, female land ownership stands at approximately **2%**. This is not a minor issue — it is a systemic crisis affecting over **50% of Pakistan's population**.

### How the Fraud Works

1. A father dies, leaving land and property
2. Male heirs (brothers, uncles) collude with the local **Patwari** (village revenue officer)
3. The Patwari **omits** the daughters from the handwritten family tree (*Shajra Nasab*)
4. Or they fabricate a fake "voluntary gift" document (*Hiba*) claiming the woman "gave up" her share
5. Civil courts take **15–30 YEARS** to resolve such cases
6. Result: Women lose everything. 97% never recover their rights.

### Why This Problem is Unique

- **Islamic law (Sharia) explicitly MANDATES women's inheritance** — Quran verses 4:11, 4:12, 4:176 define exact mathematical fractions
- The **Faraizi inheritance calculation** is deterministic — an algorithm can compute exact shares perfectly
- Pakistan passed the **Women's Property Rights Act 2020** but enforcement is near-zero
- The problem spans ALL provinces, ALL economic classes, rural AND urban
- **Nobody has ever built a technology solution for this**

---

## The Solution: HaqDar

HaqDar is a **multi-agent AI platform** that automates the entire inheritance rights investigation, calculation, fraud detection, and legal recovery process.

A woman (or her advocate) enters her case details. **8 specialized AI agents** coordinate in real-time to:

1. Conduct a structured case intake interview
2. Build the complete family tree (genealogy)
3. Analyze property documents for suspicious transfers
4. Calculate the **exact Sharia-mandated share** for every heir
5. Detect fraud (omitted heirs, fake gift deeds, suspicious mutations)
6. Generate a step-by-step legal recovery roadmap
7. Self-validate the entire analysis for errors
8. Output everything in accessible Urdu

### What Makes It Special

- **Not a chatbot.** It's 8 agents working together with observable decision-making.
- **Mathematical proof.** The inheritance shares are computed using Faraizi formulas — deterministic, not hallucinated.
- **Self-correcting.** A QA agent reviews the analysis and catches errors before finalizing.
- **Fraud detection.** Cross-references claimed distributions against legal distributions to flag theft.
- **Actionable output.** Generates a legal roadmap citing specific Pakistani laws and filing procedures.

---

## Multi-Agent Architecture

```
                    ┌─────────────────────────┐
                    │   🎯 CASE ORCHESTRATOR   │  ← Router + Supervisor
                    │   (Main Coordinator)     │
                    └────────┬────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │ 📋 INTAKE  │ │ 👨‍👩‍👧‍👦 FAMILY │ │ 📄 DOCUMENT│   ← Parallel Execution
     │   AGENT    │ │ TREE AGENT │ │  ANALYZER  │
     └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
           │               │              │
           └───────────────┼──────────────┘
                           ▼
              ┌─────────────────────────┐
              │ ⚖️ SHARIA CALCULATOR    │  ← Sequential (needs family tree)
              │ (Faraizi Math Engine)   │
              └────────┬────────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
     ┌────────────┐    ┌────────────┐
     │ 🔍 FRAUD   │    │ 📜 LEGAL   │  ← Parallel (independent analysis)
     │ DETECTION  │    │ STRATEGY   │
     └─────┬──────┘    └─────┬──────┘
           │                 │
           └────────┬────────┘
                    ▼
           ┌────────────────┐
           │ 🛡️ QA REVIEWER │  ← Reflection / Self-Correction
           │ (Debate Agent) │
           └────────┬───────┘
                    ▼
           ┌────────────────┐
           │ 🗣️ URDU OUTPUT │  ← Final Communication
           │    AGENT       │
           └────────────────┘
```

---

## The 8 Agents

### Agent 1: 🎯 Case Orchestrator (Supervisor + Router)
- **Role:** Central case manager that receives new cases and orchestrates the entire investigation
- **Workflow Pattern:** Supervisor + Router
- **What it does:** Classifies case type (urban/rural, property type, province), delegates to specialized agents, monitors progress, requests human approval at critical points

### Agent 2: 📋 Intake Agent
- **Role:** Conducts structured interviews with claimants
- **Workflow Pattern:** Sequential (first step in pipeline)
- **What it does:** Gathers deceased's name, date of death, property details, list of known heirs, nature of dispute — in Urdu or English

### Agent 3: 👨‍👩‍👧‍👦 Family Tree Agent
- **Role:** Constructs the complete genealogical tree (Shajra Nasab)
- **Workflow Pattern:** Tool-Use (ReAct) — iteratively builds and validates
- **What it does:** Identifies ALL legal heirs under Islamic law, including those who may have been deliberately omitted

### Agent 4: 📄 Document Analyzer
- **Role:** Processes property documents and extracts key facts
- **Workflow Pattern:** Parallel (runs alongside Family Tree Agent)
- **What it does:** Analyzes registry extracts, gift deeds (Hiba), mutation records; flags anomalies like transfers dated near death

### Agent 5: ⚖️ Sharia Inheritance Calculator
- **Role:** Expert in Islamic Faraizi inheritance law
- **Workflow Pattern:** Sequential (depends on Family Tree Agent)
- **What it does:** Computes the EXACT fractional share for every legal heir according to Quran and Sunnah

#### Faraizi Calculation Example:
```
Father dies, leaving behind:
├── Wife         → Gets 1/8 of estate
├── Mother       → Gets 1/6 of estate
├── Son (x2)     → Each gets 2x daughter's share
└── Daughter     → Gets 1x share (from remaining)

These fractions are DETERMINISTIC — computed from Quran 4:11, 4:12, 4:176
The AI doesn't guess — it mathematically PROVES each heir's exact share.
```

### Agent 6: 🔍 Fraud Detection Agent
- **Role:** Cross-references claimed vs. legal distribution
- **Workflow Pattern:** Debate (challenges other agents' findings)
- **What it does:** Detects omitted female heirs, suspicious Hiba documents, irregular mutation timings, coerced signatures

### Agent 7: 📜 Legal Strategy Agent
- **Role:** Creates step-by-step legal recovery roadmap
- **Workflow Pattern:** Planning Agent + Agentic RAG
- **What it does:** Recommends filing with Ombudsperson (Women's Property Rights Act 2020), civil court, or mediation; retrieves relevant legal precedents

### Agent 8: 🛡️ QA Reviewer (Reflection Agent)
- **Role:** Final quality gate
- **Workflow Pattern:** Reflection / Self-Correction — loops back if errors found
- **What it does:** Reviews mathematical accuracy, checks for missed heirs, validates legal citations, challenges assumptions

---

## Agentic Workflow Types Demonstrated

| # | Workflow Type | Where It Appears |
|---|---|---|
| 1 | **Sequential Pipeline** | Intake → Family Tree → Sharia Calc → Strategy |
| 2 | **Parallel / Fan-Out** | Document Analyzer + Family Tree run simultaneously |
| 3 | **Hierarchical / Supervisor** | Orchestrator manages all agents |
| 4 | **Router / Orchestrator** | Case classification and routing |
| 5 | **Reflection / Self-Correction** | QA Reviewer catches errors, sends back for revision |
| 6 | **Tool-Use (ReAct)** | Sharia Calculator uses math tools |
| 7 | **Planning Agent** | Legal Strategy creates step-by-step roadmap |
| 8 | **Collaborative / Debate** | Fraud Detection challenges Legal Strategy |
| 9 | **Human-in-the-Loop** | User confirms family details, approves filing strategy |
| 10 | **Memory-Augmented** | Case history stored in vector DB for precedent |
| 11 | **Agentic RAG** | Legal provisions retrieved and self-validated |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Gemini 2.5 Flash / GPT-4o |
| **Agent Framework** | CrewAI or LangGraph |
| **Vector DB** | ChromaDB / FAISS (for legal knowledge base) |
| **Backend** | Supabase (auth, case storage, real-time) |
| **Frontend** | Streamlit (rapid) or Next.js (polished) |
| **Agent Visualization** | React Flow / streamlit-agraph |
| **Urdu NLP** | OpenAI Whisper + Gemini |
| **Deployment** | Streamlit Cloud / Vercel |

---

## Demo Flow (3-Minute Pitch)

### 0:00–0:30 — THE PAIN
"97% of Pakistani women never receive their legal inheritance. Despite the Quran explicitly commanding fair distribution, corrupt Patwaris and male heirs systematically erase women from property records. Civil courts take 15-30 YEARS. Meet Fatima — her father died, her brothers took everything."

### 0:30–2:00 — THE LIVE DEMO
- Screen shows the agent workflow graph lighting up in real-time
- User enters case details (Urdu or English)
- Intake Agent conducts interview
- Family Tree Agent builds genealogy (animated tree appears)
- Document Analyzer + Family Tree run in PARALLEL (both nodes glow)
- Sharia Calculator computes exact shares (table appears with fractions)
- 🚨 Fraud Detection FIRES: "ALERT: Daughter Fatima is MISSING from the Shajra Nasab. A Hiba document dated 2 days before death is highly suspicious."
- Legal Strategy generates recovery roadmap
- QA Reviewer validates (shows self-correction loop catching an error)
- HITL Moment: "Do you approve this legal strategy? [Approve] [Modify]"
- User clicks Approve → Final Urdu report generated

### 2:00–2:30 — THE HARD ENGINEERING
"This isn't a ChatGPT wrapper. This is 8 specialized AI agents using sequential, parallel, hierarchical, reflection, debate, planning, and human-in-the-loop workflows — the full spectrum of agentic AI architecture."

### 2:30–3:00 — IMPACT
"HaqDar can be deployed to every Union Council in Pakistan. It processes cases in minutes that take courts 15 years. It gives women a mathematical, legally-backed weapon to reclaim what Islam already promised them."

---

## The "Hero Moment" (Self-Correction Demo)

During the demo, the Sharia Calculator initially computes shares with a MISSING HEIR (the deceased's mother). The QA Reviewer catches this:

```
🛡️ QA Reviewer: "ERROR: The calculation omits the deceased's mother.
   Under Islamic law, the mother receives 1/6 when there are children.
   Sending back for recalculation..."

⚖️ Sharia Calculator: "Acknowledged. Recalculating with mother included..."
[Shares update live on screen]

🛡️ QA Reviewer: "✅ VALIDATED — All heirs accounted for, fractions sum to 1.0"
```

This proves genuine AI agency and scores highest with judges.

---

## Key Legal References

- **Quran 4:11** — Shares of children (son gets 2x daughter's share)
- **Quran 4:12** — Shares of spouses
- **Quran 4:176** — Shares of siblings (Kalalah)
- **Pakistan Women's Property Rights Act 2020** — Enforcement mechanism
- **Punjab Land Records Authority (PLRA)** — Digitized records
- **NADRA Family Registration Certificate (FRC)** — True genealogical data

---

## Why This Wins

| Factor | HaqDar | Typical Submission |
|---|---|---|
| Novelty | Never attempted | "Another medical chatbot" |
| Agents | 8 specialized | 1-2 generic |
| Workflow types | 11 different patterns | Just prompt chaining |
| Community impact | 97% of women affected | Niche problem |
| Islamic alignment | Quran-mandated math | No cultural resonance |
| Demo wow factor | Live graph + self-correction | Text chat box |
| Output | Actionable legal roadmap | "Consult a lawyer" |

---

*HaqDar — Because every woman deserves her Haq (right).*
