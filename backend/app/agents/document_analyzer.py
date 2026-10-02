from crewai import Agent
from app.core.llm import get_crewai_llm

def create_document_analyzer_agent() -> Agent:
    return Agent(
        role="Forensic Revenue Document and Mutation Records Analyst",
        goal=(
            "Analyze textual descriptions and transcripts of Pakistani land records, "
            "Fard Malkiat, Intiqal (mutation registers), and Hiba (gift deeds). "
            "Extract critical metrics (acreage, transfer dates, attestations) "
            "and detect procedural anomalies or signs of fabrication."
        ),
        backstory=(
            "You are an expert revenue audit consultant and former Tehsildar with comprehensive "
            "knowledge of Pakistani revenue record maintenance under the Punjab Land Revenue Act 1967 "
            "and modern PLRA systems. You specialize in uncovering forged oral gift deeds (Hiba-Dahani) "
            "and suspicious transfers executed during deathbed illness (Marz-ul-Maut)."
        ),
        llm=get_crewai_llm(temperature=0.1),
        memory=False,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
