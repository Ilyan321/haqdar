from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ==========================================
# 1. Intake & Classification Schemas
# ==========================================

class ClaimedHeirInput(BaseModel):
    name: str = Field(..., description="Name of family member")
    relationship_to_deceased: str = Field(
        ..., 
        description="wife, husband, mother, father, son, daughter, brother, sister, etc."
    )
    is_alive: bool = True
    gender: str = Field(..., description="male or female")
    is_claimant: bool = False
    notes: Optional[str] = None

class RawPropertyInput(BaseModel):
    location: str = Field(..., description="Village, Tehsil, District, or City")
    area_description: str = Field(..., description="e.g. 4 Kanals agricultural land or 10 Marla house")
    estimated_value_pkr: Optional[float] = None
    claimed_documents: List[str] = Field(default_factory=list)

class RawCaseIntakeSchema(BaseModel):
    case_id: str
    claimant_name: str
    claimant_language: str = Field(default="en", description="en, urdu, or roman_urdu")
    deceased_name: str
    date_of_death: str
    sect: str = Field(default="Hanafi", description="Hanafi, Shia, etc.")
    family_members: List[ClaimedHeirInput]
    properties: List[RawPropertyInput]
    alleged_fraud_description: str

class CaseClassification(BaseModel):
    province: str = Field(default="Punjab", description="Punjab, Sindh, KPK, Balochistan, or ICT")
    land_type: str = Field(default="agricultural", description="agricultural, urban_residential, urban_commercial, mixed")
    primary_dispute_category: str = Field(
        default="heir_omission", 
        description="heir_omission, fraudulent_hiba, unmutated_inheritance, coerced_relinquishment"
    )
    applicable_act: str = Field(
        default="Enforcement of Women's Property Rights Act 2020",
        description="Statutory framework governing recovery"
    )
    urgency_level: str = Field(default="urgent", description="standard, urgent, emergency_freeze_required")


# ==========================================
# 2. Family Tree & Genealogy Schemas
# ==========================================

class GenealogicalNode(BaseModel):
    id: str
    name: str
    relationship: str
    gender: str
    alive_at_deceased_death: bool = True
    sharia_heir_category: str = Field(
        default="Zawil-Furooz", 
        description="Zawil-Furooz (Sharer), Asaba (Residuary), Zawil-Arham, or Excluded"
    )
    omission_risk_flag: bool = Field(
        default=False, 
        description="Flagged true if suspected of being hidden from land revenue records"
    )
    parent_ids: List[str] = Field(default_factory=list)
    spouse_ids: List[str] = Field(default_factory=list)

class FamilyTreeSchema(BaseModel):
    case_id: str
    deceased_id: str
    deceased_name: str
    nodes: List[GenealogicalNode]
    potential_omitted_heirs_detected: List[str] = Field(default_factory=list)
    total_eligible_heirs_count: int


# ==========================================
# 3. Document Analysis Schemas
# ==========================================

class MutationRecord(BaseModel):
    mutation_number: Optional[str] = None
    document_type: str = Field(..., description="Intiqal, Hiba, Registry, Fard, Tamleek")
    transfer_date: Optional[str] = None
    days_prior_to_death: Optional[int] = None
    transferor: str
    transferees: List[str]
    area_transferred_description: str
    anomalies_detected: List[str] = Field(default_factory=list)

class DocumentAnalysisSchema(BaseModel):
    case_id: str
    total_properties_count: int
    mutations: List[MutationRecord]
    suspicious_hiba_detected: bool = False
    marz_ul_maut_applicable: bool = Field(
        default=False, 
        description="True if transfer executed during deathbed illness without heir consent"
    )
    unauthorized_female_waiver_detected: bool = False
    summary_of_findings: str


# ==========================================
# 4. Sharia Distribution Schemas
# ==========================================

class HeirShareAllocation(BaseModel):
    heir_id: str
    name: str
    relationship: str
    gender: str
    quranic_category: str
    exact_fraction_str: str  # e.g. "1/8", "17/120"
    share_percentage: float  # e.g. 12.5, 14.1667
    allocated_area: Optional[str] = None
    quranic_citation: str  # e.g. "Surah An-Nisa 4:11"
    theological_rationale: str

class ShariaDistributionSchema(BaseModel):
    case_id: str
    total_estate_share: float = 1.0
    adjustment_applied: str = Field(default="normal", description="normal, aul, radd")
    base_denominator: int
    heir_allocations: List[HeirShareAllocation]
    mathematical_proof: str


# ==========================================
# 5. Fraud Detection Schemas
# ==========================================

class FraudAlert(BaseModel):
    alert_id: str
    severity: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    fraud_type: str = Field(
        ..., 
        description="omitted_female_heir, forged_hiba, marz_ul_maut_transfer, illegal_dastbardari, patwari_tampering"
    )
    victim_heir_name: str
    perpetrator_heir_name: Optional[str] = None
    deprivation_summary: str
    evidence_trail: str
    supreme_court_precedent: str

class FraudAuditReportSchema(BaseModel):
    case_id: str
    overall_fraud_score: float = Field(..., description="0.0 to 1.0")
    critical_alerts_count: int
    alerts: List[FraudAlert]
    prima_facie_criminal_offenses: List[str] = Field(default_factory=list)  # e.g., PPC 498A, PPC 420


# ==========================================
# 6. Legal Strategy & Recovery Schemas
# ==========================================

class LegalActionStep(BaseModel):
    step_number: int
    forum: str = Field(..., description="e.g. Provincial Ombudsperson, Deputy Commissioner, Civil Court")
    action_title: str
    procedure_details: str
    statutory_timeline: str  # e.g. "60 days mandatory"
    governing_law: str  # e.g. "Section 4, Enforcement of Women's Property Rights Act 2020"

class LegalRoadmapSchema(BaseModel):
    case_id: str
    primary_strategy: str
    priority_forum: str
    action_steps: List[LegalActionStep]
    statutory_precedents: List[str]
    estimated_recovery_time_days: int = 60


# ==========================================
# 7. QA Reviewer & Output Schemas
# ==========================================

class QAReviewVerdictSchema(BaseModel):
    case_id: str
    status: str = Field(..., description="APPROVED or REVISE")
    mathematical_integrity_verified: bool
    all_female_heirs_accounted_for: bool
    critique_notes: str
    target_agent_for_revision: Optional[str] = None

class BilingualReportSchema(BaseModel):
    case_id: str
    executive_summary_en: str
    executive_summary_roman_urdu: str
    family_tree_summary: str
    sharia_shares_summary: str
    fraud_alerts_summary: str
    legal_action_plan_en: str
    legal_action_plan_roman_urdu: str
    quranic_proof_text: str
