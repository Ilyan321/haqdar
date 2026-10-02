import uuid
import json
import re
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

from app.services.session_store import session_store
from app.services.crew_runner import CaseOrchestrationPipeline
from app.models.schemas import RawCaseIntakeSchema, ClaimedHeirInput, RawPropertyInput
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
    options: List[str] = Field(default_factory=list)

class CaseMessageRequest(BaseModel):
    session_id: str
    message: str

class CaseMessageResponse(BaseModel):
    status: str
    session_id: str
    reply: str
    extracted_facts: Dict[str, Any] = Field(default_factory=dict)
    options: List[str] = Field(default_factory=list)
    ready_to_launch: bool = False

class InvestigateRequest(BaseModel):
    session_id: str
    intake_data: Optional[RawCaseIntakeSchema] = None


def extract_quick_facts_from_text(text: str, current_facts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lightweight rule-based fact extractor to guarantee facts are never forgotten across conversation turns.
    """
    facts = dict(current_facts)
    lower = text.lower()

    # Deceased Name
    name_match = re.search(r'(?:name is|marhoom ka naam|walid ka naam|father(?: is|\'s name is)?)\s+([A-Za-z\s]+?)(?:,|\.|\band\b|\bhe\b|\bwho\b|\bdied\b|\bpassed\b|$)', text, re.I)
    if name_match and not facts.get("deceased_name"):
        facts["deceased_name"] = name_match.group(1).strip().title()

    # Heirs - Sons
    sons_match = re.search(r'(\d+)\s*(?:sons?|bhai|betay)', lower)
    if sons_match:
        facts["sons_count"] = int(sons_match.group(1))

    # Heirs - Daughters
    daughters_match = re.search(r'(\d+)\s*(?:daughters?|sisters?|behne?|betiyan?)', lower)
    if daughters_match:
        facts["daughters_count"] = int(daughters_match.group(1))

    # Mother / Widow status
    if any(w in lower for w in ["mother died", "mother passed", "walida faut", "walida ka inteqal", "mothers died", "no mother", "no widow"]):
        facts["mother_alive"] = False
        facts["widow_alive"] = False
    elif any(w in lower for w in ["mother is alive", "widow is alive", "walida hayat"]):
        facts["mother_alive"] = True
        facts["widow_alive"] = True

    # Property size / Area
    area_match = re.search(r'(\d+\s*(?:acres?|kanals?|marlas?|bigha|sq\s*ft|sq\s*yards?)(?:\s+of\s+[a-z\s]+)?)', lower)
    if area_match:
        facts["property_area"] = area_match.group(1).strip()

    # Location
    for loc_keyword in ["in lahore", "in sindh", "in punjab", "in karachi", "in gujranwala", "in kamber", "in shahdadkot", "in warah", "warah", "kamber", "lahore", "gujranwala", "rawalpindi", "faisalabad", "multan"]:
        if loc_keyword in lower and not facts.get("location"):
            facts["location"] = text.strip()

    # Dispute / Fraud type
    if any(w in lower for w in ["oral gift", "hiba", "fake gift", "jaali hiba"]):
        facts["dispute_type"] = "Forged Deathbed Oral Gift (Hiba)"
    elif any(w in lower for w in ["omitted", "left out", "naam nikal", "naam nahi"]):
        facts["dispute_type"] = "Omission from Revenue Mutation (Intiqal)"
    elif any(w in lower for w in ["coerced", "forced", "dastbardari", "signed"]):
        facts["dispute_type"] = "Coerced Relinquishment (Dastbardari)"
    elif any(w in lower for w in ["brothers are not giving", "seize", "qabza", "dispossessed", "refusing"]):
        facts["dispute_type"] = "Unlawful Dispossession & Deprivation (PPC 498A)"

    return facts


@router.post("/start", response_model=StartCaseResponse)
async def start_case(req: StartCaseRequest):
    session_id = str(uuid.uuid4())
    is_urdu = req.preferred_language == "roman_urdu"
    
    greeting = (
        "As-salamu alaykum. I am HaqDar's intake specialist. "
        "I am here to protect your lawful inheritance under Sharia and Pakistani Law (Women's Property Rights Act 2020). "
        "To get started, what was the deceased's name, and who are the surviving family members?"
        if not is_urdu else
        "As-salamu alaykum. Main HaqDar ka intake officer hoon. "
        "Aap ki wirasat ka sharia aur Pakistani qanoon ke mutabiq haq dilwane mein aap ki poori madad ki jaye gi. "
        "Barah-e-karam batayein marhoom ka naam kya tha aur kon kon se wariseen hayat hain?"
    )
    
    initial_options = [
        "Load Fatima's Case (120 Kanals)",
        "My father died leaving agricultural land",
        "Dispute over an urban family house",
        "Brothers forged a fake oral gift (Hiba)"
    ] if not is_urdu else [
        "Fatima ka benchmark case load karein",
        "Walid ka inteqal hua aur zameen chori",
        "Shehri ghar ka tanaza hai",
        "Bhaiyon ne jaali Hiba deed banwaya"
    ]
    
    session_store.create(session_id, {
        "session_id": session_id,
        "language": req.preferred_language,
        "status": "intake_active",
        "messages": [{"role": "assistant", "content": greeting}],
        "extracted_facts": {}
    })
    
    return StartCaseResponse(
        session_id=session_id,
        status="intake_active",
        greeting=greeting,
        options=initial_options
    )


@router.post("/message", response_model=CaseMessageResponse)
async def send_message(req: CaseMessageRequest):
    session = session_store.get(req.session_id)
    if not session:
        session_id = req.session_id or str(uuid.uuid4())
        session = {
            "session_id": session_id,
            "language": "en",
            "status": "intake_active",
            "messages": [],
            "extracted_facts": {}
        }
        session_store.create(session_id, session)

    messages: List[Dict[str, str]] = session.get("messages", [])
    messages.append({"role": "user", "content": req.message})
    
    lang = session.get("language", "en")
    is_urdu = lang == "roman_urdu"

    # 1. Update structured facts state
    current_facts = session.get("extracted_facts", {})
    updated_facts = extract_quick_facts_from_text(req.message, current_facts)
    session_store.update(req.session_id, {"extracted_facts": updated_facts})

    # 2. Check completeness
    has_deceased = bool(updated_facts.get("deceased_name"))
    has_heirs = ("sons_count" in updated_facts or "daughters_count" in updated_facts)
    has_property = bool(updated_facts.get("property_area") or updated_facts.get("location"))
    has_dispute = bool(updated_facts.get("dispute_type"))
    
    ready_to_launch = (has_deceased and has_heirs and has_property) or (has_heirs and has_property)

    # 3. Formulate dynamic prompt with LOCKED facts
    known_summary = []
    if updated_facts.get("deceased_name"):
        known_summary.append(f"Deceased: {updated_facts['deceased_name']}")
    if "sons_count" in updated_facts or "daughters_count" in updated_facts:
        known_summary.append(f"Heirs: {updated_facts.get('sons_count', 0)} Sons, {updated_facts.get('daughters_count', 0)} Daughters")
    if updated_facts.get("property_area"):
        known_summary.append(f"Property Area: {updated_facts['property_area']}")
    if updated_facts.get("location"):
        known_summary.append(f"Location: {updated_facts['location']}")
    if updated_facts.get("dispute_type"):
        known_summary.append(f"Dispute: {updated_facts['dispute_type']}")

    system_instruction = (
        "You are HaqDar's empathetic legal intake officer for Pakistani inheritance rights. "
        f"FACTS ALREADY CONFIRMED AND LOCKED (DO NOT ASK FOR THESE AGAIN):\n" + "\n".join(f"- {k}" for k in known_summary) + "\n\n"
        "STRICT RULES:\n"
        "1. Never ask for a fact that is already locked above.\n"
        "2. Do NOT drill down obsessively into sub-tehsils or mutation numbers. General location (e.g. 'Warah, Sindh' or 'Lahore') is sufficient.\n"
        "3. If deceased, heirs, and property are known, warmly state that all key facts are gathered and invite the user to launch the 8-agent investigation.\n"
        f"4. Respond naturally in {'English' if not is_urdu else 'conversational Roman Urdu'}.\n"
        "5. Keep response to maximum 2-3 short, clear sentences."
    )

    try:
        client = await groq_pool.get_async_client()
        groq_messages = [{"role": "system", "content": system_instruction}]
        for m in messages[-6:]:
            groq_messages.append({"role": m["role"], "content": m["content"]})
            
        chat_completion = await client.chat.completions.create(
            model=settings.PRIMARY_MODEL,
            messages=groq_messages,
            temperature=0.3,
            max_tokens=250,
        )
        assistant_reply = chat_completion.choices[0].message.content or "Thank you for these details."
    except Exception as e:
        print("Groq conversational intake error:", e)
        if ready_to_launch:
            assistant_reply = (
                "Thank you! I have gathered the essential facts for your case. We are ready to launch the 8-agent forensic investigation."
                if not is_urdu else
                "Shukriya! Tamam zaroori maloomat darj ho chuki hain. Ab 8-agent legal investigation shuru karne ke liye tayyar hain."
            )
        else:
            assistant_reply = (
                "Understood. Could you also mention the nature of the dispute (e.g. brothers claiming an oral gift or refusing partition)?"
                if not is_urdu else
                "Theek hai. Kya aap bata sakti hain ke bhaiyon ka kya moaqaf hai (kya wo kisi jaali Hiba ka daawa kar rahe hain ya taqseem se inkaar)?"
            )

    # Dynamic options to offer one-click responses
    options = []
    if ready_to_launch:
        options = [
            "🚀 Launch 8-Agent Autonomous Investigation",
            "Brothers claim fake oral Hiba deed",
            "Excluded from revenue mutation record"
        ] if not is_urdu else [
            "🚀 8-Agent Investigation Shuru Karein",
            "Bhai jaali Hiba deed ka daawa kar rahe hain",
            "Intiqal se naam nikaal diya gaya hai"
        ]
    elif not has_dispute:
        options = [
            "Fake Oral Gift (Hiba) claimed by brothers",
            "Omitted from revenue mutation",
            "Brothers refusing partition of estate"
        ] if not is_urdu else [
            "Bhaiyon ne jaali Hiba ka daawa kiya",
            "Intiqal se naam nikaal diya",
            "Wirasat taqseem karne se inkaar hai"
        ]

    messages.append({"role": "assistant", "content": assistant_reply})
    session_store.update(req.session_id, {"messages": messages, "extracted_facts": updated_facts})

    return CaseMessageResponse(
        status="success",
        session_id=req.session_id,
        reply=assistant_reply,
        extracted_facts=updated_facts,
        options=options,
        ready_to_launch=ready_to_launch
    )


@router.post("/investigate")
async def trigger_investigation(req: InvestigateRequest, background_tasks: BackgroundTasks):
    session = session_store.get(req.session_id)
    if not session:
        session = {
            "session_id": req.session_id,
            "language": "en",
            "status": "intake_active",
            "messages": [],
            "extracted_facts": {}
        }
        session_store.create(req.session_id, session)

    facts = session.get("extracted_facts", {})
    
    # Build structured intake from cumulative facts or fallback
    intake = req.intake_data
    if not intake:
        deceased = facts.get("deceased_name", "Ilyan Khan")
        sons = facts.get("sons_count", 2)
        daughters = facts.get("daughters_count", 3)
        mother_alive = facts.get("mother_alive", False)
        area = facts.get("property_area", "17 Acres Farm Land")
        location = facts.get("location", "Warah, Kamber Shahdadkot, Sindh")
        dispute = facts.get("dispute_type", "Brothers unlawfully dispossessing sisters of inheritance")

        family_list = []
        if mother_alive:
            family_list.append(ClaimedHeirInput(name="Widow / Mother", relationship_to_deceased="wife", is_alive=True, gender="female"))
        for s in range(sons):
            family_list.append(ClaimedHeirInput(name=f"Brother #{s+1}", relationship_to_deceased="son", is_alive=True, gender="male"))
        for d in range(daughters):
            family_list.append(ClaimedHeirInput(name=f"Sister #{d+1}" if d > 0 else "Claimant (Daughter)", relationship_to_deceased="daughter", is_alive=True, gender="female", is_claimant=(d==0)))

        intake = RawCaseIntakeSchema(
            case_id=req.session_id,
            claimant_name="Claimant Daughter",
            claimant_language=session.get("language", "en"),
            deceased_name=deceased,
            date_of_death="2023-01-14",
            sect="Hanafi",
            family_members=family_list,
            properties=[RawPropertyInput(location=location, area_description=area)],
            alleged_fraud_description=dispute
        )

    # Run full multi-agent pipeline in background
    background_tasks.add_task(
        CaseOrchestrationPipeline.run_full_investigation,
        req.session_id,
        intake
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
