# HaqDar (حقدار) — AI-Powered Women's Inheritance Rights Recovery Platform

<div align="center">

![HaqDar Banner](https://img.shields.io/badge/%D8%AD%D9%82%D8%AF%D8%A7%D8%B1-HaqDar-d4a853?style=for-the-badge)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent%20Swarm-FF4B4B?style=for-the-badge)](https://crewai.com)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B%20%2F%20Qwen-f55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**"Restoring what is rightfully theirs through deterministic law and autonomous agentic AI."**

*An 8-Agent Autonomous Legal Tech Platform built for the HEC × PakAngels Generative & Agentic AI Hackathon.*

[🌐 Live Brief](http://haqdar-idea.aenox.me/) • [📕 Project Brief PDF](./HaqDar-Project-Brief.pdf) • [📄 Masterplan](./MASTERPLAN.md) • [📐 Architecture Doc](./docs/ARCHITECTURE.md) • [📋 PRD](./docs/PRD.md)

</div>

---

## 📌 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [The Systemic Crisis & The Law](#-the-systemic-crisis--the-law)
3. [Core Capabilities & Innovation](#-core-capabilities--innovation)
4. [8-Agent Autonomous Swarm Architecture](#-8-agent-autonomous-swarm-architecture)
5. [Deterministic Sharia Calculation Engine](#-deterministic-sharia-calculation-engine)
6. [Conversational Discovery & Fact Locking](#-conversational-discovery--fact-locking)
7. [Technology Stack](#-technology-stack)
8. [Project Structure](#-project-structure)
9. [Quick Start & Local Setup](#-quick-start--local-setup)
10. [Running Tests](#-running-tests)
11. [Live Hackathon Demo Flow](#-live-hackathon-demo-flow)
12. [API Reference](#-api-reference)

---

## 🏛️ Executive Summary

In Pakistan, **over 97% of women never receive their lawful landed inheritance**, and female land ownership nationwide stands at approximately **2%**. When women attempt to claim their rightful estate, traditional civil court suits (*Dewani Muqadma*) take an average of **15 to 30 years**, paralyzing claimants with corrupt revenue gatekeeping and extortionate legal fees.

**HaqDar (حقدار)** is an autonomous multi-agent legal intelligence platform that resolves this multi-decade litigation bottleneck into an instantaneous, mathematically proven, and legally actionable recovery package.

HaqDar combines:
- **Zero-Hallucination Faraizi Math Engine:** Computes exact fractional shares (`fractions.Fraction`) according to Quranic Sharia jurisprudence (Surah An-Nisa 4:11, 4:12, 4:176).
- **8 Autonomous CrewAI Agents:** Coordinates specialized intake, genealogical reconstruction, document auditing, fraud detection, legal strategy, and quality assurance.
- **Bilingual Conversational Discovery:** Engages claimants naturally in **English and Roman Urdu** with real-time fact locking and automated follow-up questioning.
- **Fast-Track Statutory Enforcement:** Drafts expedited 60-day recovery petitions under the **Enforcement of Women's Property Rights Act 2020** before the Provincial Women Ombudsperson.

---

## ⚡ The Systemic Crisis & The Law

```
                         THE INHERITANCE DISPOSSESSION CYCLE
 ┌────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
 │ Patriarch Dies │ ───> │ Male Relatives  │ ───> │ Revenue Records │ ───> │ 15-30 Years in  │
 │ Leaves Property│      │ Bribe Patwari   │      │ Erase Daughters │      │ Civil Court Grid│
 └────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────┘
                                                            │                        │
                                                            ▼                        ▼
                                                  ┌──────────────────┐     ┌──────────────────┐
                                                  │ Forged Gift Deed │     │ 97% Women Give   │
                                                  │ (Hiba / Tamleek) │     │ Up Rights Entirely│
                                                  └──────────────────┘     └──────────────────┘
```

### Statutory Shields Invoked by HaqDar:
- **Enforcement of Women's Property Rights Act 2020:** Bypasses sluggish civil courts by empowering the Provincial Ombudsperson to order direct revenue rectification and police eviction within **60 days**.
- **Pakistan Penal Code (PPC) Section 498-A:** Criminalizes deceitful deprivation of female inheritance with **5 to 10 years rigorous imprisonment** and a PKR 1,000,000 fine.
- **Supreme Court of Pakistan Precedents (PLD 1990 SC 1 / 2021 SCMR 1351):** Affirm that inheritance rights vest automatically at the exact second of the estate owner's death; adverse possession cannot run against female co-heirs.

---

## 🌟 Core Capabilities & Innovation

| Feature | What HaqDar Delivers | Traditional Approach |
|---|---|---|
| **Mathematical Precision** | **Exact symbolic fractions (`fractions.Fraction`)** with verified 100% closure (`Awl`, `Radd`, `Kalalah`). | Hallucinated LLM math or corrupt manual Patwari calculations. |
| **Investigation Speed** | **Under 2 minutes** end-to-end multi-agent diagnostic and petition drafting. | 15–30 years of civil court deadlock. |
| **Language Support** | Seamless **English & Roman Urdu** intake with auto-detection and targeted missing-fact elicitation. | Inaccessible legal jargon only understandable by high-priced attorneys. |
| **Live Observability** | Real-time **SSE event stream** and **React Flow** interactive agent pipeline & family tree graphs. | Black-box processes with zero visibility. |
| **Fraud Triage** | Automated detection of suspicious oral gifts (*Hiba*), proximity-to-death transfers, and revenue mutation tampering. | Undetected forgery buried in handwritten Urdu revenue ledgers. |

---

## 🤖 8-Agent Autonomous Swarm Architecture

HaqDar coordinates 8 specialized autonomous agents orchestrated through CrewAI with sequential, parallel fan-out, adversarial debate, and self-correcting reflection topologies:

```
                            ┌─────────────────────────┐
                            │   🎯 CASE ORCHESTRATOR   │  ← Supervisor & State Router
                            │   (Workflow Controller) │
                            └────────────┬────────────┘
                                         │
                   ┌─────────────────────┼─────────────────────┐
                   │                     │                     │
                   ▼                     ▼                     ▼
          ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
          │ 📋 INTAKE      │    │ 👨‍👩‍👧‍👦 FAMILY     │    │ 📄 DOCUMENT    │  ← Fan-Out (Parallel)
          │    OFFICER     │    │    TREE AGENT  │    │    ANALYZER    │
          └────────┬───────┘    └────────┬───────┘    └────────┬───────┘
                   │                     │                     │
                   └─────────────────────┼─────────────────────┘
                                         ▼
                            ┌─────────────────────────┐
                            │ ⚖️ SHARIA CALCULATOR    │  ← Deterministic Faraizi Engine
                            │ (Symbolic Math Core)    │
                            └────────────┬────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
          ┌────────────────┐                          ┌────────────────┐
          │ 🔍 FRAUD       │                          │ 📜 LEGAL       │  ← Parallel Legal Audit
          │    DETECTION   │                          │    STRATEGIST  │
          └────────┬───────┘                          └────────┬───────┘
                   │                                           │
                   └─────────────────────┬─────────────────────┘
                                         ▼
                            ┌─────────────────────────┐
                            │ 🛡️ QA REVIEWER          │  ← Reflection & Self-Correction Gate
                            │ (Closure Verification)  │
                            └────────────┬────────────┘
                                         ▼
                            ┌─────────────────────────┐
                            │ 📡 NOTIFIER & EXPORTER  │  ← Real-Time SSE / Slack Alert Hub
                            │ (Client Telemetry)      │
                            └─────────────────────────┘
```

### Agent Roles & Workflows:
1. **Case Orchestrator (🎯 Supervisor + Router):** Manages session lifecycle, assigns agent workloads, aggregates intermediate JSON state, and routes execution.
2. **Intake Officer (📋 Empathetic Fact Extractor):** Interviews the claimant in English or Roman Urdu, extracts verified facts, locks verified criteria, and prompts for missing data.
3. **Family Tree Agent (👨‍👩‍👧‍👦 Genealogical Mapper):** Reconstructs the complete family hierarchy, identifying living heirs and flagging omitted female heirs.
4. **Document Analyzer (📄 Forensic Revenue Auditor):** Scans mutation documents (*Intiqal*), registry deeds, and extracts transaction dates, Patwari signatures, and transfer types.
5. **Sharia Calculator (⚖️ Quranic Math Engine):** Executes deterministic Faraizi inheritance allocation using Python `fractions.Fraction` with zero LLM math hallucination.
6. **Fraud Detection Agent (🔍 Adversarial Auditor):** Cross-examines document dates against date of death, detects illegal oral *Hiba* gift deeds, and flags violations of Section 498-A PPC.
7. **Legal Strategist (📜 Fast-Track Petition Drafter):** Formulates step-by-step statutory recovery roadmaps under the *Enforcement of Women's Property Rights Act 2020*.
8. **QA Reviewer (🛡️ Mathematical Closure & Gatekeeper):** Validates that all fractional shares sum strictly to `1/1` (100%), enforces female heir inclusion, and verifies statutory citations.

---

## 📐 Deterministic Sharia Calculation Engine

Islamic inheritance law (Faraizi) is governed by strict mathematical axioms. HaqDar embeds these rules directly into Python symbolic rational arithmetic (`backend/app/tools/sharia_math.py`):

```python
# Quranic Faraizi Standard Allocation Example (Surah An-Nisa 4:11-12)
Deceased Estate Owner: Father
Total Estate Value: 100% (16 Kanals / PKR 32,000,000)

Surviving Heirs:
├── 1 Widow (Mother):      1/8  (15/120  = 12.50%)   [Quran 4:12]
├── 1 Mother (Grandmother): 1/6  (20/120  = 16.67%)   [Quran 4:11]
└── Residue (Asaba):       17/24 (85/120 = 70.83%)   [Quran 4:11 (Son = 2x Daughter)]
    ├── Son 1 (Tariq):     2/5 of Residue = 34/120 = 17/60 (28.33%)
    ├── Son 2 (Rashid):    2/5 of Residue = 34/120 = 17/60 (28.33%)
    └── Daughter (Fatima): 1/5 of Residue = 17/120         (14.17%)

Total Sum: 15/120 + 20/120 + 34/120 + 34/120 + 17/120 = 120/120 = 1.0000 (100% Exact)
```

### Supported Special Cases:
- **Awl (Proportional Reduction):** Automatically expands base denominator when fixed Quranic shares exceed 1.0 (e.g. Husband + 2 Daughters + Parents).
- **Radd (Surplus Re-distribution):** Re-distributes remainder proportionally among Sharia heirs when no residuary (*Asaba*) heirs exist.
- **Kalalah (Estates without Offspring or Father):** Accurately routes shares to germane, consanguine, and uterine siblings under Quran 4:12 & 4:176.

---

## 💬 Conversational Discovery & Fact Locking

HaqDar features a resilient, multi-turn conversational intake engine:

1. **Dual-Language Fluency:** Seamlessly processes natural English and Roman Urdu (e.g., *"Mera walid marhoom ho gaye hain aur mere bhaiyon ne saari zameen apne naam karwa li"*).
2. **Instant Fact Locking:** Automatically extracts and locks:
   - Deceased Name & Date of Death
   - Verified Heir Counts (Sons, Daughters, Widow, Mother, Father)
   - Property Measurement (Kanals, Marlas, Acres, Valuation)
   - Property Location (Tehsil, District, Province)
   - Nature of Grievance & Fraud
3. **Smart Questioning Safety Guard:** Dynamically asks targeted single-question follow-ups for any missing legal fact until all criteria are met.
4. **Token Rate-Limit Governance:** Governed with Groq-optimized token limits (`max_tokens: 400` fact extraction, `max_tokens: 200` conversational agent) ensuring continuous zero-rate-limit operation.

---

## 🛠️ Technology Stack

```
Frontend (Next.js 14)          Backend (FastAPI)             AI & LLM Services
┌───────────────────────┐      ┌───────────────────────┐     ┌───────────────────────┐
│ • Next.js 14 App Router│ <──> │ • FastAPI (Python 3.12)│ <─> │ • Groq Multi-Key Pool │
│ • React 18            │ SSE  │ • CrewAI Swarm        │     │   - Llama 3.3 70B     │
│ • @xyflow/react Flow  │      │ • SSE Starlette       │     │   - Qwen 3.8 27B      │
│ • Tailwind CSS        │      │ • Pydantic v2         │     │ • Sharia Math Core    │
│ • Zustand State Store │      │ • Ephemeral Session   │     │ • Slack Alert Webhook │
└───────────────────────┘      └───────────────────────┘     └───────────────────────┘
```

---

## 📁 Project Structure

```text
/home/ilyan/og/
├── backend/                        # FastAPI & CrewAI Backend
│   ├── app/
│   │   ├── agents/                 # 8 Autonomous CrewAI Agents
│   │   │   ├── orchestrator.py     # Central Coordinator
│   │   │   ├── intake_agent.py     # Empathetic Intake Officer
│   │   │   ├── family_tree_agent.py# Genealogical Tree Builder
│   │   │   ├── document_analyzer.py# Revenue Record Scanner
│   │   │   ├── sharia_calculator.py# Islamic Share Distributor
│   │   │   ├── fraud_detection.py  # Anomaly & Fraud Detector
│   │   │   ├── legal_strategy.py   # Statutory Ombudsperson Strategist
│   │   │   └── qa_reviewer.py      # Closure & Verification Gate
│   │   ├── api/                    # API Endpoints (case, stream)
│   │   │   ├── case.py             # Intake, Message & Investigation API
│   │   │   └── stream.py           # Real-Time SSE Streamer
│   │   ├── core/                   # Configuration & LLM Infrastructure
│   │   │   ├── config.py           # Environment & Model Settings
│   │   │   ├── groq_pool.py        # Multi-Key Groq Rotation Pool
│   │   │   └── llm.py              # LLM Initializer
│   │   ├── models/                 # Pydantic Data Contracts
│   │   │   └── schemas.py          # Case, Heir & Report Schemas
│   │   ├── services/               # Infrastructure Services
│   │   │   ├── crew_runner.py      # CrewAI Pipeline Runner
│   │   │   ├── event_broadcaster.py# Real-Time Event Dispatcher
│   │   │   ├── notifier.py         # Slack & Incident Webhook Alerting
│   │   │   └── session_store.py    # Ephemeral TTL Session Memory
│   │   ├── tasks/                  # CrewAI Task Definitions
│   │   │   └── case_tasks.py       # Sequential & Parallel Task Graph
│   │   └── tools/                  # Deterministic Computation Tools
│   │       └── sharia_math.py      # Symbolic Quranic Faraizi Math Core
│   ├── tests/                      # Automated Pytest Suite
│   │   └── test_sharia_math.py     # Exact Fraction & Law Unit Tests
│   └── requirements.txt            # Python Dependencies
│
├── frontend/                       # Next.js 14 Presentation Tier
│   ├── src/
│   │   ├── app/                    # Next.js App Router (Home, Terms, Privacy)
│   │   ├── components/
│   │   │   ├── chat/               # Conversational Intake Chat
│   │   │   ├── visualizer/         # React Flow Agent & Family Tree Graphs
│   │   │   ├── reports/            # Share Breakdown Table & Legal Reports
│   │   │   └── common/             # Navigation & Responsive Footer
│   │   ├── hooks/                  # SSE Stream Hook (useAgentStream)
│   │   └── store/                  # Zustand Global Case Store
│   ├── package.json
│   └── tailwind.config.ts
│
├── docs/                           # Architecture, PRD & Agent Specifications
│   ├── AGENT-DESIGN.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN-SYSTEM.md
│   └── PRD.md
│
├── docker-compose.yml              # Local Multi-Service Orchestration
├── render.yaml                     # Render Cloud Deployment Spec
├── vercel.json                     # Vercel Frontend Deployment Spec
├── start.sh                        # One-Click Local Startup Script
└── MASTERPLAN.md                   # Platform Implementation Blueprint
```

---

## 🚀 Quick Start & Local Setup

### Prerequisites
- **Node.js** >= 18.x
- **Python** >= 3.11 (< 3.14)
- **Groq API Key** (Free tier available at [console.groq.com](https://console.groq.com))

### 1. Clone & Configure Environment
```bash
git clone https://github.com/your-org/haqdar.git
cd haqdar

# Configure backend environment
cp .env.example backend/.env
# Add your GROQ_API_KEY inside backend/.env
```

### 2. Option A: One-Click Startup Script
```bash
chmod +x start.sh
./start.sh
```

### 3. Option B: Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 🧪 Running Tests

HaqDar includes automated unit and integration tests covering the deterministic Sharia calculation engine (standard cases, Awl, Radd, Kalalah, and complex family structures):

```bash
# From project root
PYTHONPATH=backend backend/venv/bin/pytest backend/tests/ -v
```

Output:
```text
backend/tests/test_sharia_math.py::test_standard_case_fatima PASSED   [ 25%]
backend/tests/test_sharia_math.py::test_awl_case PASSED                [ 50%]
backend/tests/test_sharia_math.py::test_kalalah_case PASSED            [ 75%]
backend/tests/test_sharia_math.py::test_widow_two_sons_two_daughters PASSED [100%]

============================== 4 passed in 0.03s ===============================
```

---

## 🎬 Live Hackathon Demo Flow

To demonstrate HaqDar's end-to-end multi-agent capabilities on video or to judges:

### 1. Conversational Intake (Roman Urdu or English)
Enter the following opening prompt:
> *"Mera walid marhoom ho gaye hain aur mere bhaiyon ne Lahore ki saari zameen apne naam karwa li hai aur mujhe hissa nahi de rahe."*

### 2. Answer Clarifying Questions
- **Deceased:** *"Chaudhry Muhammad Din, 14 March 2023"*
- **Heirs:** *"2 betay (Tariq, Rashid), 1 beti (Fatima - me), aur meri walida (widow Kulsoom) hayat hain"*
- **Land Size:** *"16 Kanal agricultural land in Raiwind Lahore"*

### 3. Launch Investigation
Click **"Launch 8-Agent Autonomous Investigation"**:
1. **Live Pipeline Flow:** React Flow highlights each agent as it activates over SSE.
2. **Family Tree Visualization:** Dynamic interactive genealogy renders on screen.
3. **Share Breakdown:** Displays exact fractions (Fatima: 17/120 = 14.17%, Mother: 1/8 = 12.5%, Sons: 17/60 each).
4. **Forensic Fraud Alert:** Flags fraudulent oral *Hiba* and Section 498-A PPC violation.
5. **Actionable Roadmap:** Outputs ready-to-file fast-track petition before the Punjab Women Ombudsperson.

---

## 📡 API Reference

### Core Endpoints

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/case/start` | Initializes a new case session and returns intake greeting. |
| `POST` | `/api/case/message` | Handles conversational discovery, updates locked facts, and guides user. |
| `POST` | `/api/case/investigate` | Triggers the 8-agent autonomous CrewAI investigation in the background. |
| `GET` | `/api/case/stream/{sessionId}` | Server-Sent Events (SSE) stream for live agent execution telemetry. |
| `GET` | `/api/case/report/{sessionId}` | Retrieves the aggregated legal investigation report and share matrix. |

---

## ⚖️ Legal & Ethical Disclaimer

HaqDar is an autonomous legal intelligence and procedural aid system. It provides computational Sharia inheritance calculations and statutory petition drafts under Pakistani law (Enforcement of Women's Property Rights Act 2020). HaqDar does not replace formal judicial adjudication, and petitions generated by the platform are submitted directly to competent statutory authorities (Provincial Ombudspersons and Civil Courts).

---

<div align="center">

**HaqDar (حقدار) Team** — HEC × PakAngels Generative & Agentic AI Hackathon

*"Restoring what is rightfully theirs, one case at a time."*

</div>
