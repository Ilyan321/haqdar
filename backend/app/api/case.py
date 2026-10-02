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


async def extract_facts_with_llm(messages: List[Dict[str, str]], current_facts: Dict[str, Any]) -> Dict[str, Any]:
    """
    LLM-based structured extraction to robustly handle complex conversational inputs.
    """
    history_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])
    
    system_prompt = f"""You are an expert legal fact extractor for Pakistani Islamic inheritance (Faraizi) law.
Extract case facts from the conversation accurately. Return a JSON object with EXACTLY these keys. If a fact is not mentioned or unknown, set it to null.

Keys:
- "deceased_name": (string) Full name of the deceased person (e.g. 'Ilyan Khan').
- "date_of_death": (string) Date or approximate time of death (e.g. '31-09-2026').
- "sons_count": (integer) Number of surviving sons (including the claimant if claimant is a son).
- "daughters_count": (integer) Number of surviving daughters (including the claimant if claimant is a daughter).
- "widow_alive": (boolean) Is the widow / wife of the deceased alive? (e.g. true if user mentions 1 widow, mother of children, or wife).
- "wives_count": (integer) Number of surviving wives/widows (typically 1).
- "mother_alive": (boolean) Is the mother of the deceased alive?
- "father_alive": (boolean) Is the father of the deceased alive?
- "property_type": (string) Type of property (e.g. 'agricultural farmlands', 'residential house', 'commercial shop', 'cash / bank savings').
- "property_area": (string) Specific size/measurement or value of the property (e.g. '120 Kanals', '17 Acres', '10 Marlas', 'Rs. 25,000,000'). If only generic description given without size (e.g. 'farmlands'), record 'farmlands (size unstated)'.
- "has_quantitative_measurement": (boolean) TRUE if user provided explicit numerical size or units (e.g. Kanals, Marlas, Acres, Murabba, Sq Yards, PKR/Rs amount). FALSE if user only gave a vague label like 'farmlands', 'house', 'zameen' without quantity.
- "location": (string) Location of the property (city, town, district, village, e.g. 'Lahore, near old Lahore, village').
- "debts_or_liabilities": (string or null) Any outstanding unpaid debts or funeral expenses of the deceased.
- "wills_or_bequests": (string or null) Any valid will / wasiyyat (up to 1/3) left by the deceased.
- "dispute_type": (string) The nature of the dispute (e.g. 'brothers refusing to give lawful share', 'fraudulent oral gift Hiba', 'omitted from mutation').

Previous facts state:
{json.dumps(current_facts)}

Respond with ONLY valid JSON containing the merged and updated facts.
"""
    groq_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": history_text}
    ]
    
    for attempt in range(3):
        try:
            client = await groq_pool.get_async_client()
            chat_completion = await client.chat.completions.create(
                model=settings.PRIMARY_MODEL,
                messages=groq_messages,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            content = chat_completion.choices[0].message.content
            if content:
                new_facts = json.loads(content)
                merged = dict(current_facts)
                for k, v in new_facts.items():
                    if v is not None:
                        merged[k] = v
                return merged
        except Exception as e:
            print(f"Error extracting facts with LLM (attempt {attempt+1}):", e)
            if attempt < 2:
                if hasattr(client, 'api_key'):
                    groq_pool.mark_rate_limited(client.api_key)
                await asyncio.sleep(1)
            else:
                pass
                
    return current_facts


@router.post("/start", response_model=StartCaseResponse)
async def start_case(req: StartCaseRequest):
    session_id = str(uuid.uuid4())
    is_urdu = req.preferred_language == "roman_urdu"
    
    greeting = (
        "As-salamu alaykum. I am HaqDar's intake specialist. "
        "I am here to protect your lawful inheritance under Sharia and Pakistani Law (Women's Property Rights Act 2020). "
        "To get started, what was the deceased's full name, approximate date of death, and who are all surviving heirs (sons, daughters, widow, parents)?"
        if not is_urdu else
        "As-salamu alaykum. Main HaqDar ka intake officer hoon. "
        "Aap ki wirasat ka sharia aur Pakistani qanoon ke mutabiq haq dilwane mein aap ki poori madad ki jaye gi. "
        "Barah-e-karam batayein marhoom ka mukammal naam kya tha, tareekh-e-inteqal, aur kon kon se wariseen (betay, betiyan, bewa, waldain) hayat hain?"
    )
    
    initial_options = [
        "Load Fatima's Case (120 Kanals)"
    ] if not is_urdu else [
        "Fatima ka benchmark case load karein"
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


def is_property_quantified(facts: Dict[str, Any]) -> bool:
    """Helper to verify if property size or financial value has been quantified."""
    if facts.get("has_quantitative_measurement") is True:
        return True
    prop = str(facts.get("property_area", "")).lower()
    # Check for unit keywords or digits with unit
    has_units = bool(re.search(r'\d+\s*(kanal|marla|acre|ekad|bigha|sq\s*ft|sq\s*yard|yard|gaz|pkr|rs|rupee|lac|lakh|crore|k\b|m\b)', prop))
    return has_units


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
    updated_facts = await extract_facts_with_llm(messages, current_facts)
    session_store.update(req.session_id, {"extracted_facts": updated_facts})

    # 2. Check completeness with strict criteria (ALL essential inheritance pillars)
    has_deceased = bool(updated_facts.get("deceased_name"))
    has_heirs = ("sons_count" in updated_facts or "daughters_count" in updated_facts or "widow_alive" in updated_facts or "mother_alive" in updated_facts)
    has_quant_property = is_property_quantified(updated_facts)
    has_location = bool(updated_facts.get("location"))
    has_dispute = bool(updated_facts.get("dispute_type"))
    
    # Ready only when all key facts including exact property measurement/value are established
    ready_to_launch = (
        has_deceased and
        has_heirs and
        has_quant_property and
        has_location and
        has_dispute
    )

    # 3. Formulate dynamic prompt with LOCKED facts and MISSING facts
    known_summary = []
    if updated_facts.get("deceased_name"):
        known_summary.append(f"Deceased Name: {updated_facts['deceased_name']}")
    if updated_facts.get("date_of_death"):
        known_summary.append(f"Date of Death: {updated_facts['date_of_death']}")
    
    heir_parts = []
    if updated_facts.get("sons_count") is not None:
        heir_parts.append(f"{updated_facts.get('sons_count')} Sons")
    if updated_facts.get("daughters_count") is not None:
        heir_parts.append(f"{updated_facts.get('daughters_count')} Daughters")
    if updated_facts.get("widow_alive"):
        heir_parts.append(f"{updated_facts.get('wives_count', 1)} Widow(s)")
    if updated_facts.get("mother_alive"):
        heir_parts.append("Mother")
    if updated_facts.get("father_alive"):
        heir_parts.append("Father")
        
    if heir_parts:
        known_summary.append(f"Surviving Heirs: {', '.join(heir_parts)}")

    if updated_facts.get("property_area"):
        quant_note = " (Exact Size Verified)" if has_quant_property else " (Needs size/units e.g. Kanals/Acres)"
        known_summary.append(f"Property: {updated_facts['property_area']}{quant_note}")
    if updated_facts.get("location"):
        known_summary.append(f"Location: {updated_facts['location']}")
    if updated_facts.get("dispute_type"):
        known_summary.append(f"Dispute Nature: {updated_facts['dispute_type']}")

    missing_items = []
    if not has_deceased:
        missing_items.append("Deceased's full name and approximate date of death")
    if not has_heirs:
        missing_items.append("Surviving heirs breakdown (number of sons, daughters, and whether widow/mother/father are alive)")
    if not has_quant_property:
        if updated_facts.get("property_area") and not has_quant_property:
            missing_items.append("Exact total size or measurement of the property to be partitioned (e.g. how many Kanals, Marlas, or Acres, or estimated PKR valuation)")
        else:
            missing_items.append("Property size, unit of measurement (e.g. 120 Kanals, 15 Acres, 10 Marlas) and property type")
    if not has_location:
        missing_items.append("City, tehsil, or village where property is located")
    if not has_dispute:
        missing_items.append("Specific dispute or grievance (e.g. brothers refusing to give share, forged Hiba gift deed, or omission from mutation)")

    assistant_reply = ""
    if ready_to_launch:
        deceased = updated_facts.get("deceased_name", "the deceased")
        heirs_str = ", ".join(heir_parts) if heir_parts else "the surviving heirs"
        prop_str = updated_facts.get("property_area", "the family estate")
        loc_str = updated_facts.get("location", "Pakistan")
        
        if not is_urdu:
            assistant_reply = (
                f"Thank you. I have recorded the key case facts: {deceased}'s estate ({prop_str} in {loc_str}), "
                f"surviving heirs ({heirs_str}), and the unlawful dispossession dispute. "
                "All required estate and heir details are established. You can now launch the 8-agent autonomous investigation."
            )
        else:
            assistant_reply = (
                f"Shukriya. Tamam zaroori maloomat darj ho chuki hain: {deceased} ki wirasat ({prop_str}, {loc_str}), "
                f"wariseen ({heirs_str}), aur wirasat ka tanaza. "
                "Ab aap 8-agent autonomous investigation shuru kar sakti hain."
            )
    else:
        system_instruction = f"""You are HaqDar's empathetic legal intake agent. Your goal is to gather MISSING FACTS to accurately calculate Islamic inheritance shares and build a recovery petition.
        
LOCKED FACTS SO FAR:
{', '.join(known_summary) if known_summary else 'None'}

CRITICAL MISSING FACTS NEEDED:
{', '.join(missing_items)}

IMPORTANT RULES:
1. Be empathetic and professional.
2. Ask exactly ONE clear question focusing on the highest priority missing fact.
3. If the user mentioned a property category like 'farmlands' or 'house' without size/units, specifically ask: 'What is the total size or measurement of the property (e.g., how many Kanals, Marlas, or Acres, or its estimated value)?'
4. Do not re-ask for facts already locked.
5. Keep your reply concise (under 2 sentences).
6. If the user language is Roman Urdu, reply in Roman Urdu. Otherwise reply in English.
7. DO NOT prefix with 'LOCKED FACTS SO FAR' or dump internal tags in the visible reply.
"""
        
        groq_messages = [{"role": "system", "content": system_instruction}]
        for m in messages[-4:]:
            groq_messages.append({"role": m["role"], "content": m["content"]})
            
        for attempt in range(3):
            try:
                client = await groq_pool.get_async_client()
                chat_completion = await client.chat.completions.create(
                    model=settings.PRIMARY_MODEL,
                    messages=groq_messages,
                    temperature=0.3,
                    max_tokens=250,
                )
                assistant_reply = chat_completion.choices[0].message.content or "Thank you for these details."
                break
            except Exception as e:
                print(f"Groq conversational intake error (attempt {attempt+1}):", e)
                if attempt < 2:
                    if hasattr(client, 'api_key'):
                        groq_pool.mark_rate_limited(client.api_key)
                    await asyncio.sleep(1)
                else:
                    if not has_heirs:
                        assistant_reply = (
                            "Could you please clarify who the surviving heirs are (number of sons, daughters, and if his widow or mother is alive)?"
                            if not is_urdu else
                            "Barah-e-karam batayein kitne betay, betiyan aur kya marhoom ki bewa ya walida hayat hain?"
                        )
                    elif not has_quant_property:
                        assistant_reply = (
                            "To calculate the exact shares, what is the total size or measurement of the property (e.g., how many Kanals, Marlas, or Acres, or estimated value)?"
                            if not is_urdu else
                            "Hissa nikalne ke liye, barah-e-karam zameen ki paimaish batayein (kitne Kanal, Marla, ya Acre zameen hai ya andazan qeemat kya hai)?"
                        )
                    elif not has_location:
                        assistant_reply = (
                            "Where is this property located (which city, tehsil, or village)?"
                            if not is_urdu else
                            "Yeh jaidad kahan waqia hai (shehr, tehsil ya gaon ka naam batayein)?"
                        )
                    else:
                        assistant_reply = (
                            "Thank you. Could you describe how you are being excluded or denied your share?"
                            if not is_urdu else
                            "Shukriya. Barah-e-karam batayein ke bhaiyon ne kis tarah wirasat se bay-dakhal kiya?"
                        )

    # Options only for launch when case facts are ready
    options = []
    if ready_to_launch:
        options = [
            "🚀 Launch 8-Agent Autonomous Investigation"
        ] if not is_urdu else [
            "🚀 8-Agent Investigation Shuru Karein"
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
        deceased = facts.get("deceased_name", "Late Deceased")
        date_of_death = facts.get("date_of_death", "2023-01-14")
        sons = facts.get("sons_count", 0)
        daughters = facts.get("daughters_count", 0)
        widow_alive = facts.get("widow_alive", False)
        wives_count = facts.get("wives_count", 1 if widow_alive else 0)
        mother_alive = facts.get("mother_alive", False)
        father_alive = facts.get("father_alive", False)
        area = facts.get("property_area", "120 Kanals Agricultural Land")
        location = facts.get("location", "Lahore, Punjab")
        dispute = facts.get("dispute_type", "Unlawful Dispossession & Deprivation of Inheritance (PPC 498A)")

        family_list = []
        if widow_alive or wives_count > 0:
            for w in range(max(1, wives_count)):
                name = "Widow" if wives_count == 1 else f"Widow #{w+1}"
                family_list.append(ClaimedHeirInput(name=name, relationship_to_deceased="wife", is_alive=True, gender="female"))
        if mother_alive:
            family_list.append(ClaimedHeirInput(name="Mother", relationship_to_deceased="mother", is_alive=True, gender="female"))
        if father_alive:
            family_list.append(ClaimedHeirInput(name="Father", relationship_to_deceased="father", is_alive=True, gender="male"))
        for s in range(sons):
            family_list.append(ClaimedHeirInput(name=f"Brother #{s+1}" if sons > 1 else "Brother", relationship_to_deceased="son", is_alive=True, gender="male"))
        for d in range(daughters):
            is_claimant = (d == 0)
            name = "Claimant (Daughter)" if is_claimant else f"Sister #{d}"
            family_list.append(ClaimedHeirInput(name=name, relationship_to_deceased="daughter", is_alive=True, gender="female", is_claimant=is_claimant))

        intake = RawCaseIntakeSchema(
            case_id=req.session_id,
            claimant_name="Claimant Daughter",
            claimant_language=session.get("language", "en"),
            deceased_name=deceased,
            date_of_death=date_of_death,
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
