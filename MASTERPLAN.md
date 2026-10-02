# HaqDar (حقدار) - Master Implementation Plan

> **Note:** This document contains exact, step-by-step instructions for coding the HaqDar platform. It defines the modular architecture, library dependencies, and execution phases. **No actual implementation code is written here; this is the blueprint for the coding phase.**

---

## 1. Tech Stack & Exact Versions
Ensure the following library versions are used during initialization to prevent compatibility issues:

**Frontend:**
- `next`: ^14.2.0 (App Router) - Using 14.x for stability, though 16.3.8 is latest, 14/15 is most common for stable React Flow integration.
- `react`, `react-dom`: ^18.2.0
- `reactflow` (now `@xyflow/react`): ^12.0.0 (For Pipeline and Family Tree visualization)
- `tailwindcss`: ^3.4.0
- `lucide-react`: Latest (Icons)
- `zustand`: Latest (State management for SSE streams)

**Backend:**
- `python`: >=3.11, <3.14
- `fastapi`: ^0.142.2
- `uvicorn`: ^0.30.0
- `crewai`: ^1.15.23
- `crewai-tools`: Latest
- `groq`: ^1.7.0 (Official Groq SDK)
  - Primary Model: `llama-3.3-70b-versatile` (Non-deprecated, active, 128k context, excellent reasoning)
  - Fallback/Formatting Model: `llama3-8b-8192` (For simple tasks to save tokens/rate limits)
- `langchain-groq`: Latest
- `supabase`: ^2.3.0 (For pgvector RAG)
- `pydantic`: ^2.7.0
- `sse-starlette`: Latest (For Server-Sent Events)

---

## 2. Directory Structure (Highly Modular)
The codebase MUST be organized strictly into a monorepo structure. Each agent MUST have its own dedicated file to ensure maintainability.

```text
/home/ilyan/og/
├── frontend/                  # Next.js App
│   ├── src/
│   │   ├── app/               # App Router pages and layouts
│   │   ├── components/
│   │   │   ├── chat/          # Intake chat components
│   │   │   ├── visualizer/    # React Flow (Pipeline & Family Tree)
│   │   │   ├── reports/       # Share breakdown & PDF viewer
│   │   │   └── ui/            # Reusable Tailwind components
│   │   ├── hooks/             # SSE stream listener (useAgentStream)
│   │   └── store/             # Zustand case state store
│   └── tailwind.config.ts     # Adheres to DESIGN-SYSTEM.md
│
├── backend/                   # FastAPI + CrewAI App
│   ├── app/
│   │   ├── api/               # FastAPI routers (case, stream, report)
│   │   ├── core/              # Config, Groq API key rotation pool
│   │   ├── agents/            # ONE FILE PER AGENT
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py
│   │   │   ├── intake_agent.py
│   │   │   ├── family_tree_agent.py
│   │   │   ├── document_analyzer.py
│   │   │   ├── sharia_calculator.py
│   │   │   ├── fraud_detection.py
│   │   │   ├── legal_strategy.py
│   │   │   └── qa_reviewer.py
│   │   ├── tasks/             # Task definitions corresponding to agents
│   │   ├── tools/             # Custom tools
│   │   │   ├── sharia_math.py # Deterministic Faraizi engine (Pure Python)
│   │   │   ├── supabase_rag.py# pgvector search
│   │   │   └── validators.py
│   │   ├── models/            # Pydantic schemas (I/O contracts)
│   │   ├── services/          # Ephemeral session store, SSE broadcaster
│   │   └── main.py            # FastAPI entry point
│   └── requirements.txt
│
└── docs/                      # Generated architecture and specs
```

---

## 3. Step-by-Step Implementation Instructions

### Phase 1: Foundation & Backend Scaffold
1. **Initialize Environments:**
   - Create the `backend/` directory, initialize a Python virtual environment (`python -m venv venv`), and install dependencies (`fastapi`, `crewai`, `groq`, etc.).
   - Create the `frontend/` directory using `npx create-next-app@latest frontend --typescript --tailwind --eslint --app`.
2. **Implement the Sharia Math Engine (`backend/app/tools/sharia_math.py`):**
   - **Crucial:** Build the deterministic Faraizi calculator using `fractions.Fraction`.
   - Implement logic for *Ashab al-Furudh* (Quranic sharers), *Asaba* (residuaries), *Hajb* (exclusion), *Aul*, and *Radd*.
   - Add comprehensive unit tests to prove 100% mathematical accuracy before moving on.
3. **Setup Core Services:**
   - Implement `backend/app/core/groq_pool.py` for rotating the 5 Groq API keys with rate-limit circuit breaking.
   - Implement `backend/app/services/session_store.py` for in-memory TTL state management (no database).
   - Implement `backend/app/services/event_broadcaster.py` using `asyncio.Queue` for SSE.

### Phase 2: CrewAI Agents Implementation (1 File Per Agent)
Follow the exact specifications in `docs/AGENT-DESIGN.md`.
1. **Intake & Orchestrator:** Create `intake_agent.py` and `orchestrator.py`. Ensure Intake uses the conversational LLM config and outputs Pydantic models.
2. **Parallel Discovery:** Create `family_tree_agent.py` and `document_analyzer.py`.
3. **Calculation & Analysis:** Create `sharia_calculator.py` (wrapping the `sharia_math.py` tool), `fraud_detection.py`, and `legal_strategy.py`.
4. **QA & Output:** Create `qa_reviewer.py` with reflection logic to trigger loops if math mismatches. Create `output_agent.py` (in `tasks` or `agents`) for bilingual synthesis.
5. **Crew Coordinator:** In `backend/app/services/crew_runner.py`, assemble the Crew. Use CrewAI's `Crew` class to wire the tasks. Implement step callbacks to push state changes to the SSE broadcaster.

### Phase 3: FastAPI Endpoints & SSE
1. Create `POST /api/case/start` to initialize a session UUID.
2. Create `POST /api/case/message` to pass user text to the Intake Agent.
3. Create `GET /api/case/stream/{id}` utilizing `sse-starlette` to stream agent statuses (`started`, `thinking`, `completed`, `error`) and intermediate JSON payloads.
4. Create `GET /api/case/report/{id}` to fetch the final dossier.

### Phase 4: Frontend Development
Follow `docs/DESIGN-SYSTEM.md` for aesthetics (Light Professional, Deep Teal/Sovereign Amber, Inter font).
1. **State Management:** Setup a Zustand store (`useCaseState`) to handle the SSE connection and store pipeline state.
2. **Chat Component (`CaseChat.tsx`):** Build the conversational UI for the Intake phase.
3. **Pipeline Visualizer (`AgentPipelineFlow.tsx`):** Use `@xyflow/react`. Create custom nodes for the 8 agents. Map the SSE statuses to node colors (e.g., pulsing blue for 'thinking', green for 'completed').
4. **Family Tree (`FamilyTreeGraph.tsx`):** Use `@xyflow/react` to render the `FamilyTreeSchema` JSON. Color-code omitted heirs in red.
5. **Share Breakdown (`ShareBreakdownTable.tsx`):** Render the fractions and percentages using a tabular monospace font.
6. **Bilingual Report (`ReportViewer.tsx`):** Build the final document view with a toggle switch for English/Roman Urdu.

### Phase 5: Integration & "Hero Moment" Verification
1. Connect the Next.js frontend to the FastAPI backend.
2. Run an end-to-end test using the scenario: "Haji Ghulam died leaving 1 widow, 2 sons, 1 daughter. Brother forged Hiba deed."
3. **Verify the Hero Moment:** Ensure that if the Sharia Calculator drops the widow, the QA Reviewer catches it, emits an SSE reflection event, and forces a recalculation.
4. Finalize UI polish and prepare deployment scripts for Vercel and Railway/Render.

---

## 4. Execution Rules
- **No Direct LLM Math:** The LLM MUST NOT calculate fractions. It must parse the output of `calculate_faraizi_shares`.
- **Strict Typing:** All CrewAI tasks must use `output_pydantic` mapping to the schemas defined in `AGENT-DESIGN.md`.
- **Telemetry:** Every agent transition must emit an SSE event for the frontend React Flow graph to react instantly.
- **Absolute Rate Limit Resilience:** The Groq API can trigger 429s. The `groq_pool.py` MUST implement aggressive exponential backoff (e.g., using `tenacity`), rotate keys smoothly, and handle timeouts without crashing the agent pipeline. Never allow the app to fail mid-processing due to a 429.
- **Report Size & Output Token Management:** Do NOT generate massive, verbose reports that abruptly end mid-sentence due to output token limits. Instruct the `output_agent` to use concise bullet points, executive summaries, and strict length bounds. If necessary, chunk report generation into multiple small tasks rather than one huge completion.

> Proceed to code generation phase by starting with Phase 1 (Foundation).
