import uuid
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from app.services.session_store import session_store
from app.services.crew_runner import CaseOrchestrationPipeline
from app.models.schemas import RawCaseIntakeSchema

router = APIRouter(prefix="/case", tags=["Case Management"])

class StartCaseRequest(BaseModel):
    initial_notes: Optional[str] = ""
    preferred_language: str = "en"  # "en" or "roman_urdu"

class StartCaseResponse(BaseModel):
    session_id: str
    status: str
    greeting: str

class CaseMessageRequest(BaseModel):
    session_id: str
    message: str

class InvestigateRequest(BaseModel):
    session_id: str
    intake_data: RawCaseIntakeSchema

@router.post("/start", response_model=StartCaseResponse)
async def start_case(req: StartCaseRequest):
    session_id = str(uuid.uuid4())
    greeting = (
        "As-salamu alaykum. I am HaqDar's intake specialist. "
        "I am here to help ensure your rightful inheritance is calculated and restored according to Sharia and Pakistan law. "
        "Can you share who the deceased was, when they passed away, and who their surviving family members are?"
        if req.preferred_language == "en" else
        "As-salamu alaykum. Main HaqDar ka intake officer hoon. "
        "Aap ki wirasat ka sharia aur Pakistani qanoon ke mutabiq haq dilwane mein aap ki poori madad ki jaye gi. "
        "Barah-e-karam batayein marhoom ka naam kya tha, kab inteqal hua, aur unke kitne bachay ya rishtedar hain?"
    )
    
    session_store.create(session_id, {
        "session_id": session_id,
        "language": req.preferred_language,
        "status": "intake_active",
        "messages": [
            {"role": "assistant", "content": greeting}
        ]
    })
    
    return StartCaseResponse(
        session_id=session_id,
        status="intake_active",
        greeting=greeting
    )

@router.post("/message")
async def send_message(req: CaseMessageRequest):
    session = session_store.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    
    messages = session.get("messages", [])
    messages.append({"role": "user", "content": req.message})
    session_store.update(req.session_id, {"messages": messages})
    
    return {
        "status": "received",
        "session_id": req.session_id,
        "message_count": len(messages)
    }

@router.post("/investigate")
async def trigger_investigation(req: InvestigateRequest, background_tasks: BackgroundTasks):
    session = session_store.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    
    # Run full multi-agent pipeline in background
    background_tasks.add_task(
        CaseOrchestrationPipeline.run_full_investigation,
        req.session_id,
        req.intake_data
    )
    
    return {
        "status": "investigation_queued",
        "session_id": req.session_id,
        "message": "8-agent pipeline investigation started. Connect to SSE stream for live updates."
    }

@router.get("/report/{session_id}")
async def get_report(session_id: str):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    
    dossier = session.get("dossier")
    if not dossier:
        return {
            "session_id": session_id,
            "status": session.get("status", "in_progress"),
            "message": "Investigation still in progress or not yet triggered."
        }
    
    return dossier
