from crewai import Task
from app.models.schemas import (
    CaseClassification,
    RawCaseIntakeSchema,
    FamilyTreeSchema,
    DocumentAnalysisSchema,
    ShariaDistributionSchema,
    FraudAuditReportSchema,
    LegalRoadmapSchema,
    QAReviewVerdictSchema,
    BilingualReportSchema
)

def create_intake_task(agent, user_message: str, previous_context: str = "") -> Task:
    return Task(
        description=(
            f"Review the user's inquiry: '{user_message}'. Previous conversation context: '{previous_context}'. "
            "Extract deceased particulars, date of death, known family members (spouses, sons, daughters, parents, siblings), "
            "property descriptions, and specific grievance details. Output a structured JSON response."
        ),
        expected_output="Valid JSON conforming to RawCaseIntakeSchema with normalized family and property lists.",
        agent=agent,
        output_pydantic=RawCaseIntakeSchema
    )

def create_orchestration_task(agent, intake_data: RawCaseIntakeSchema) -> Task:
    return Task(
        description=(
            f"Analyze the case intake data for deceased '{intake_data.deceased_name}'. "
            f"Classify the provincial jurisdiction (Punjab/Sindh/KPK/Balochistan/ICT), land category, "
            f"and primary dispute mechanism (e.g. heir omission, fake Hiba deed)."
        ),
        expected_output="JSON object conforming to CaseClassification.",
        agent=agent,
        output_pydantic=CaseClassification
    )

def create_family_tree_task(agent, intake_data: RawCaseIntakeSchema) -> Task:
    return Task(
        description=(
            f"Construct the complete genealogical family tree for deceased '{intake_data.deceased_name}'. "
            f"Evaluate listed relatives: {intake_data.family_members}. "
            "Identify all lawful Islamic heirs (Zawil-Furooz, Asaba). Explicitly check if daughters or mothers "
            "were omitted or obscured."
        ),
        expected_output="JSON object conforming to FamilyTreeSchema.",
        agent=agent,
        output_pydantic=FamilyTreeSchema
    )

def create_document_analyzer_task(agent, intake_data: RawCaseIntakeSchema) -> Task:
    return Task(
        description=(
            f"Analyze the property descriptions and document claims: {intake_data.properties}. "
            f"Examine the alleged fraud: '{intake_data.alleged_fraud_description}'. "
            "Audit for unregistered Hiba, suspicious deathbed transfers (Marz-ul-Maut), and missing female signatures."
        ),
        expected_output="JSON object conforming to DocumentAnalysisSchema.",
        agent=agent,
        output_pydantic=DocumentAnalysisSchema
    )

def create_sharia_calculation_task(agent, family_tree: FamilyTreeSchema, calculation_proof: str) -> Task:
    return Task(
        description=(
            f"Review the verified family tree for deceased '{family_tree.deceased_name}'. "
            f"The deterministic calculation engine produced the following verified mathematical proof:\n\n{calculation_proof}\n\n"
            "Format the exact shares, fractions, and percentages for every heir and explain the theological basis "
            "under Quran 4:11, 4:12, 4:176."
        ),
        expected_output="JSON object conforming to ShariaDistributionSchema.",
        agent=agent,
        output_pydantic=ShariaDistributionSchema
    )

def create_fraud_detection_task(agent, family_tree: FamilyTreeSchema, documents: DocumentAnalysisSchema, sharia_shares: ShariaDistributionSchema) -> Task:
    return Task(
        description=(
            f"Conduct an adversarial fraud investigation comparing the Sharia inheritance shares: {sharia_shares.heir_allocations} "
            f"against document records: {documents.mutations} and genealogical heirs: {family_tree.nodes}. "
            "Detect every excluded female heir, forged gift, or illegal relinquishment (Dastbardari). Cite PPC 498A."
        ),
        expected_output="JSON object conforming to FraudAuditReportSchema.",
        agent=agent,
        output_pydantic=FraudAuditReportSchema
    )

def create_legal_strategy_task(agent, classification: CaseClassification, fraud_report: FraudAuditReportSchema) -> Task:
    return Task(
        description=(
            f"Formulate a rapid recovery roadmap under jurisdiction '{classification.province}'. "
            f"Given fraud findings: {fraud_report.alerts}. "
            "Prioritize filing before the Provincial Ombudsperson under the Enforcement of Women's Property Rights Act 2020 "
            "(60-day mandatory decision) and revenue authorities."
        ),
        expected_output="JSON object conforming to LegalRoadmapSchema.",
        agent=agent,
        output_pydantic=LegalRoadmapSchema
    )

def create_qa_review_task(agent, family_tree: FamilyTreeSchema, sharia_shares: ShariaDistributionSchema, fraud_report: FraudAuditReportSchema) -> Task:
    return Task(
        description=(
            f"Perform a comprehensive quality audit of the case findings. "
            f"Verify that total shares sum to 100%, verify that all female heirs in {family_tree.nodes} are accounted for, "
            f"and check that fraud alerts: {fraud_report.alerts} are supported by legal grounds. "
            "Return verdict APPROVED if 100% sound, or REVISE if discrepancies exist."
        ),
        expected_output="JSON object conforming to QAReviewVerdictSchema.",
        agent=agent,
        output_pydantic=QAReviewVerdictSchema
    )

def create_synthesis_task(agent, family_tree: FamilyTreeSchema, sharia_shares: ShariaDistributionSchema, fraud_report: FraudAuditReportSchema, roadmap: LegalRoadmapSchema) -> Task:
    return Task(
        description=(
            "Synthesize the complete validated case dossier into concise, empowering summaries in both English "
            "and Roman Urdu. Include clear bullet points, Quranic proof, fraud alerts, and the step-by-step recovery plan."
        ),
        expected_output="JSON object conforming to BilingualReportSchema.",
        agent=agent,
        output_pydantic=BilingualReportSchema
    )
