import uuid
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

from app.services.session_store import session_store
from app.services.crew_runner import CaseOrchestrationPipeline
from app.models.schemas import RawCaseIntakeSchema
from app.core.groq_pool import groq_pool
from app.core.config import settings

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

class CaseMessageResponse(BaseModel):
    status: str
    session_id: str
    reply: str

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

@router.post("/message", response_model=CaseMessageResponse)
async def send_message(req: CaseMessageRequest):
    session = session_store.get(req.session_id)
    if not session:
        # Auto-create if expired or brand new
        session_id = req.session_id or str(uuid.uuid4())
        session = {
            "session_id": session_id,
            "language": "en",
            "status": "intake_active",
            "messages": []
        }
        session_store.create(session_id, session)
    
    messages: List[Dict[str, str]] = session.get("messages", [])
    messages.append({"role": "user", "content": req.message})
    
    lang = session.get("language", "en")
    
    system_instruction = (
        "You are HaqDar's empathetic, professional legal intake specialist in Pakistan for women's inheritance rights. "
        "Your task is to interview the claimant conversationally to discover all necessary case facts: "
        "1. Deceased's full name and approximate date of death. "
        "2. Complete surviving family tree (surviving spouse, number of sons, number of daughters, whether deceased's parents or siblings are alive). "
        "3. Disputed property details (agricultural land in Kanals/Acres, urban house, city/district, mutation number). "
        "4. Details of the dispute (e.g. brother claiming fake oral Hiba, Patwari excluding female heirs, coerced signature). "
        f"Language requirement: Respond naturally in {'English' if lang == 'en' else 'conversational Roman Urdu'}. "
        "Keep your answers concise, supportive, and ask 1 or 2 clear clarifying questions at a time. "
        "When you have enough facts (deceased, all heirs, and property), let them know you are ready to launch the full 8-agent legal investigation."
    )

    try:
        client = await groq_pool.get_async_client()
        groq_messages = [{"role": "system", "content": system_instruction}]
        
        # Keep last 6 conversation turns
        for m in messages[-6:]:
            groq_messages.append({"role": m["role"], "content": m["content"]})
            
        chat_completion = await client.chat.completions.create(
            model=settings.PRIMARY_MODEL,
            messages=groq_messages,
            temperature=0.3,
            max_tokens=500,
        )
        assistant_reply = chat_completion.choices[0].message.content or "Thank you for sharing. Could you also clarify if there are any other surviving siblings or daughters?"
    except Exception as e:
        print("Groq conversational intake error:", e)
        assistant_reply = (
            "Thank you for providing these details. Can you also tell me if the deceased had any other surviving sons, daughters, or living parents?"
            if lang == "en" else
            "Shukriya ye tafseelat batane ka. Kya aap mazeed bata sakti hain ke marhoom ke koi aur betay, betiyan ya walidain hayat hain?"
        )

    messages.append({"role": "assistant", "content": assistant_reply})
    session_store.update(req.session_id, {"messages": messages})
    
    return CaseMessageResponse(
        status="success",
        session_id=req.session_id,
        reply=assistant_reply
    )

@router.post("/investigate")
async def trigger_investigation(req: InvestigateRequest, background_tasks: BackgroundTasks):
    session = session_store.get(req.session_id)
    if not session:
        session = {
            "session_id": req.session_id,
            "language": req.intake_data.claimant_language or "en",
            "status": "intake_active",
            "messages": []
        }
        session_store.create(req.session_id, session)
    
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
