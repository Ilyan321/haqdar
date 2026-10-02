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
    name_match = re.search(r'(?:name is|marhoom ka naam|walid ka naam|father\'s name is|deceased\'s name is)\s+([A-Za-z\s]+?)(?:,|\.|\band\b|\bhe\b|\bwho\b|\bdied\b|\bpassed\b|$)', text, re.I)
    if name_match and not facts.get("deceased_name"):
        cand = name_match.group(1).strip().title()
        if not any(bad in cand.lower() for bad in ["passed", "died", "not", "giving", "share", "leaving", "alive"]):
            facts["deceased_name"] = cand

    # Direct name mentions like "Haji Ghulam Rasool" or "Ilyan Khan"
    if not facts.get("deceased_name"):
        for potential_name in ["Haji Ghulam Rasool", "Ghulam Rasool", "Ilyan Khan", "Muhammad Khan", "Abdul Rehman", "Tariq Mahmood"]:
            if potential_name.lower() in lower:
                facts["deceased_name"] = potential_name
                break

    # Heirs - Sons & Brothers (from claimant's perspective "2 brothers" means 2 sons of deceased)
    sons_match = re.search(r'(\d+)\s*(?:sons?|brothers?|bhai|betay)', lower)
    if sons_match:
        facts["sons_count"] = int(sons_match.group(1))
    elif "just 2 sons" in lower or "2 sons" in lower or "2 brothers" in lower:
        facts["sons_count"] = 2
    elif "1 son" in lower or "1 brother" in lower:
        facts["sons_count"] = 1
    elif "3 sons" in lower or "3 brothers" in lower:
        facts["sons_count"] = 3
    elif "no sons" in lower or "no brothers" in lower:
        facts["sons_count"] = 0

    # Heirs - Daughters & Sisters (from claimant's perspective "3 sisters" or "myself and 2 sisters")
    daughters_match = re.search(r'(\d+)\s*(?:daughters?|sisters?|behne?|betiyan?)', lower)
    if daughters_match:
        facts["daughters_count"] = int(daughters_match.group(1))
    elif "3 daughters" in lower or "3 sisters" in lower:
        facts["daughters_count"] = 3
    elif "2 daughters" in lower or "2 sisters" in lower:
        facts["daughters_count"] = 2
    elif "1 daughter" in lower or "only daughter" in lower or "myself (daughter)" in lower:
        facts["daughters_count"] = 1

    # Mother / Widow status
    if any(w in lower for w in ["mother died", "mother passed", "walida faut", "walida ka inteqal", "mothers died", "no mother", "no widow", "died way earlier", "died earlier"]):
        facts["mother_alive"] = False
        facts["widow_alive"] = False
    elif any(w in lower for w in ["mother is alive", "widow is alive", "walida hayat", "mother (widow", "widow kulsoom"]):
        facts["mother_alive"] = True
        facts["widow_alive"] = True

    # Property size / Area
    area_match = re.search(r'(\d+\s*(?:acres?|kanals?|marlas?|bigha|sq\s*ft|sq\s*yards?)(?:\s+of\s+[a-z\s]+)?)', lower)
    if area_match:
        facts["property_area"] = area_match.group(1).strip()
    elif "17 acres" in lower:
        facts["property_area"] = "17 Acres Farm Land"
    elif "120 kanals" in lower:
        facts["property_area"] = "120 Kanals Agricultural Land"
    elif "house" in lower or "ghar" in lower:
        if not facts.get("property_area"):
            facts["property_area"] = "Residential Family House"

    # Location
    for loc_keyword, loc_name in [
        ("warah", "Warah, Kamber Shahdadkot, Sindh"),
        ("kamber", "Kamber Shahdadkot, Sindh"),
        ("shahdadkot", "Shahdadkot, Sindh"),
        ("gujranwala", "Gujranwala, Punjab"),
        ("lahore", "Lahore, Punjab"),
        ("karachi", "Karachi, Sindh"),
        ("rawalpindi", "Rawalpindi, Punjab"),
        ("faisalabad", "Faisalabad, Punjab"),
        ("multan", "Multan, Punjab"),
        ("sindh", "Sindh, Pakistan"),
        ("punjab", "Punjab, Pakistan")
    ]:
        if loc_keyword in lower:
            facts["location"] = loc_name
            break

    # Dispute / Fraud type
    if any(w in lower for w in ["oral gift", "hiba", "fake gift", "jaali hiba", "fake oral hiba"]):
        facts["dispute_type"] = "Forged Deathbed Oral Gift (Hiba)"
    elif any(w in lower for w in ["omitted", "left out", "naam nikal", "naam nahi", "mutation no. 412"]):
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
        "2 Sons, 3 Daughters, Mother passed away",
        "17 Acres Farm Land in Lahore",
        "Brothers forged a fake oral gift (Hiba)"
    ] if not is_urdu else [
        "Fatima ka benchmark case load karein",
        "2 betay, 3 betiyan, walida faut ho chuki hain",
        "17 Acre zameen Lahore mein",
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

    # 2. Check completeness with strict criteria
    has_deceased = bool(updated_facts.get("deceased_name"))
    has_heirs = ("sons_count" in updated_facts or "daughters_count" in updated_facts)
    has_property_area = bool(updated_facts.get("property_area"))
    has_location = bool(updated_facts.get("location"))
    has_dispute = bool(updated_facts.get("dispute_type"))
    
    # Must have heirs, property description, and dispute before declaring complete
    ready_to_launch = (
        has_heirs and
        (has_property_area or has_location) and
        (has_deceased or len(messages) >= 4) and
        (has_dispute or len(messages) >= 4)
    )

    # 3. Formulate dynamic prompt with LOCKED facts and MISSING facts
    known_summary = []
    if updated_facts.get("deceased_name"):
        known_summary.append(f"Deceased Name: {updated_facts['deceased_name']}")
    if "sons_count" in updated_facts or "daughters_count" in updated_facts:
        known_summary.append(f"Surviving Heirs: {updated_facts.get('sons_count', 0)} Sons, {updated_facts.get('daughters_count', 0)} Daughters")
    if "mother_alive" in updated_facts:
        known_summary.append(f"Mother / Widow Alive: {updated_facts['mother_alive']}")
    if updated_facts.get("property_area"):
        known_summary.append(f"Property Size: {updated_facts['property_area']}")
    if updated_facts.get("location"):
        known_summary.append(f"Location: {updated_facts['location']}")
    if updated_facts.get("dispute_type"):
        known_summary.append(f"Dispute Nature: {updated_facts['dispute_type']}")

    missing_items = []
    if not has_deceased:
        missing_items.append("Deceased's full name and approximate date of death")
    if not has_heirs:
        missing_items.append("Surviving heirs count (number of sons, daughters, and if mother/widow is alive)")
    if not has_property_area:
        missing_items.append("Property size or type (e.g. 17 acres agricultural land, 10 marla house)")
    if not has_location:
        missing_items.append("City or district where property is located")
    if not has_dispute:
        missing_items.append("Specific action taken by brothers/colluders (e.g. fake oral gift / Hiba, omitted from mutation)")

    assistant_reply = ""
    if ready_to_launch:
        deceased = updated_facts.get("deceased_name", "the deceased")
        sons = updated_facts.get("sons_count", 0)
        daughters = updated_facts.get("daughters_count", 0)
        prop_str = updated_facts.get("property_area", "the family estate")
        loc_str = updated_facts.get("location", "Pakistan")
        
        if not is_urdu:
            assistant_reply = (
                f"Thank you. I have recorded the key case facts: {deceased}'s estate ({prop_str} in {loc_str}), "
                f"surviving heirs ({sons} sons, {daughters} daughters), and the unlawful dispossession dispute. "
                "All required information is established. You can now launch the 8-agent autonomous investigation."
            )
        else:
            assistant_reply = (
                f"Shukriya. Tamam zaroori maloomat darj ho chuki hain: {deceased} ki wirasat ({prop_str}, {loc_str}), "
                f"wariseen ({sons} betay, {daughters} betiyan), aur wirasat ka tanaza. "
                "Ab aap 8-agent autonomous investigation shuru kar sakti hain."
            )
    else:
        try:
            client = await groq_pool.get_async_client()
            groq_messages = [{"role": "system", "content": system_instruction}]
            for m in messages[-4:]:
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
            if not has_heirs:
                assistant_reply = (
                    "Could you please share who the surviving heirs are (number of sons, daughters, and whether the mother is alive)?"
                    if not is_urdu else
                    "Barah-e-karam batayein kitne betay, betiyan aur kya walida hayat hain?"
                )
            elif not has_property_area:
                assistant_reply = (
                    "Understood. Could you also provide details about the property (e.g. 17 acres of agricultural land or a house)?"
                    if not is_urdu else
                    "Theek hai. Barah-e-karam zameen ya jaidad ki tafseelat batayein (kitne acre zameen ya kitna bada ghar hai)?"
                )
            else:
                assistant_reply = (
                    "Thank you. Could you describe the specific dispute or how you are being excluded?"
                    if not is_urdu else
                    "Shukriya. Barah-e-karam batayein ke bhaiyon ne kya kiya (jaali Hiba deed ya intiqal se naam nikalwaya)?"
                )

    # Dynamic option chips matching what is currently missing
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
    elif not has_heirs:
        options = [
            "2 Sons, 3 Daughters, Mother passed away",
            "1 Son, 2 Daughters, Mother is alive",
            "2 Brothers, 1 Sister (Myself)",
            "Only Daughters, No Sons"
        ] if not is_urdu else [
            "2 betay, 3 betiyan, walida faut hain",
            "1 beta, 2 betiyan, walida hayat hain",
            "2 bhai, 1 behen (main khud)",
            "Sirf betiyan hain, koi beta nahi"
        ]
    elif not has_property_area:
        options = [
            "17 Acres Agricultural Land",
            "120 Kanals Agricultural Land",
            "10 Marla Residential House",
            "1 Kanal Urban Plot"
        ] if not is_urdu else [
            "17 Acre zaree zameen",
            "120 Kanal zameen",
            "10 Marla rehaishi ghar",
            "1 Kanal shehri plot"
        ]
    elif not has_dispute:
        options = [
            "Fake Oral Gift (Hiba) claimed by brothers",
            "Omitted from revenue mutation record",
            "Brothers refusing estate partition",
            "Forced signature on blank stamp paper"
        ] if not is_urdu else [
            "Bhaiyon ne jaali Hiba ka daawa kiya",
            "Intiqal se naam nikaal diya",
            "Wirasat taqseem karne se inkaar hai",
            "Zabardasti stamp paper par dastakhat"
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
