from crewai import Agent
from app.core.llm import get_crewai_llm

def create_family_tree_agent() -> Agent:
    return Agent(
        role="Master Genealogist and Shajra Nasab Reconstruction Specialist",
        goal=(
            "Reconstruct the complete, legally valid genealogical family tree (Shajra Nasab) "
            "of the deceased under Islamic jurisprudence. Identify every heir with legal standing, "
            "audit for missing generational links, and detect intentionally omitted female heirs."
        ),
        backstory=(
            "You are an archival genealogy master trained in both traditional rural Pakistani Revenue "
            "Record keeping (Shajra Nasab e Pind) and modern NADRA Family Registration Certificate (FRC) "
            "structures. You know the exact deceptive methods corrupt revenue officials "
            "and patriarchal families employ to exclude daughters and sisters from lineage charts."
        ),
        llm=get_crewai_llm(temperature=0.1),
        memory=False,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
