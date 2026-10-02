from fractions import Fraction
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class HeirInput(BaseModel):
    relation: str = Field(..., description="wife, husband, mother, father, son, daughter, brother, sister, grandfather, grandmother")
    count: int = Field(default=1, ge=1)
    name: Optional[str] = None
    is_claimant: bool = False

class HeirShareDetail(BaseModel):
    relation: str
    count: int
    name: Optional[str] = None
    is_claimant: bool = False
    individual_fraction_str: str
    individual_fraction_value: float
    total_group_fraction_str: str
    individual_percentage: float
    category: str  # 'Zawil-Furooz' (Sharer) or 'Asaba' (Residuary) or 'Radd-Adjusted'
    quranic_basis: str
    theological_rationale: str

class ShariaCalculationOutput(BaseModel):
    heir_shares: List[HeirShareDetail]
    total_distributed_fraction: str
    total_percentage: float
    base_denominator: int
    awl_applied: bool
    radd_applied: bool
    mathematical_proof: str


def calculate_faraizi_shares(heirs: List[HeirInput], deceased_gender: str = "male") -> ShariaCalculationOutput:
    """
    Deterministic Islamic Faraizi Inheritance calculation engine under Sunni Hanafi jurisprudence.
    Uses exact rational arithmetic (fractions.Fraction) to prevent floating point drift.
    """
    # Group counts
    counts: Dict[str, int] = {}
    names_map: Dict[str, List[HeirInput]] = {}
    for h in heirs:
        rel = h.relation.lower().strip()
        counts[rel] = counts.get(rel, 0) + h.count
        if rel not in names_map:
            names_map[rel] = []
        names_map[rel].append(h)

    num_wives = counts.get("wife", 0)
    num_husbands = counts.get("husband", 0)
    num_mothers = min(counts.get("mother", 0), 1)
    num_fathers = min(counts.get("father", 0), 1)
    num_sons = counts.get("son", 0)
    num_daughters = counts.get("daughter", 0)
    num_brothers = counts.get("brother", 0)
    num_sisters = counts.get("sister", 0)

    has_children = (num_sons > 0 or num_daughters > 0)
    total_siblings = num_brothers + num_sisters

    # Dictionary to store exact fractions for each group
    group_shares: Dict[str, Fraction] = {}
    group_categories: Dict[str, str] = {}
    group_basis: Dict[str, str] = {}
    group_rationale: Dict[str, str] = {}

    # 1. Spouse
    if num_wives > 0:
        share = Fraction(1, 8) if has_children else Fraction(1, 4)
        group_shares["wife"] = share
        group_categories["wife"] = "Zawil-Furooz (Quranic Sharer)"
        group_basis["wife"] = "Quran 4:12"
        group_rationale["wife"] = f"Wife/wives receive {'1/8' if has_children else '1/4'} because deceased {'has' if has_children else 'does not have'} surviving children."

    if num_husbands > 0:
        share = Fraction(1, 4) if has_children else Fraction(1, 2)
        group_shares["husband"] = share
        group_categories["husband"] = "Zawil-Furooz (Quranic Sharer)"
        group_basis["husband"] = "Quran 4:12"
        group_rationale["husband"] = f"Husband receives {'1/4' if has_children else '1/2'} because deceased {'has' if has_children else 'does not have'} surviving children."

    # 2. Mother
    if num_mothers > 0:
        if has_children or total_siblings >= 2:
            share = Fraction(1, 6)
            reason = "1/6 due to presence of children or multiple siblings"
        else:
            share = Fraction(1, 3)
            reason = "1/3 due to absence of children and multiple siblings"
        group_shares["mother"] = share
        group_categories["mother"] = "Zawil-Furooz (Quranic Sharer)"
        group_basis["mother"] = "Quran 4:11"
        group_rationale["mother"] = f"Mother receives {reason}."

    # 3. Father
    if num_fathers > 0:
        if num_sons > 0:
            group_shares["father"] = Fraction(1, 6)
            group_categories["father"] = "Zawil-Furooz (Quranic Sharer)"
            group_basis["father"] = "Quran 4:11"
            group_rationale["father"] = "Father receives fixed 1/6 due to presence of male descendant (son)."
        elif num_daughters > 0:
            # 1/6 fixed + will take residual later if any
            group_shares["father"] = Fraction(1, 6)
            group_categories["father"] = "Zawil-Furooz + Asaba"
            group_basis["father"] = "Quran 4:11"
            group_rationale["father"] = "Father receives fixed 1/6 plus residual entitlement due to presence of only female descendants."
        else:
            # Pure residuary if no children
            group_categories["father"] = "Asaba (Residuary)"
            group_basis["father"] = "Quran 4:11"
            group_rationale["father"] = "Father inherits as pure residuary in absence of children."

    # 4. Daughters (without sons)
    if num_daughters > 0 and num_sons == 0:
        if num_daughters == 1:
            share = Fraction(1, 2)
            reason = "1/2 for single daughter in absence of sons"
        else:
            share = Fraction(2, 3)
            reason = "2/3 shared equally among multiple daughters in absence of sons"
        group_shares["daughter"] = share
        group_categories["daughter"] = "Zawil-Furooz (Quranic Sharer)"
        group_basis["daughter"] = "Quran 4:11"
        group_rationale["daughter"] = f"Daughters receive {reason}."

    # 5. Siblings (Kalalah: when no children and no father)
    if not has_children and num_fathers == 0:
        if num_brothers == 0 and num_sisters > 0:
            if num_sisters == 1:
                share = Fraction(1, 2)
                reason = "1/2 for single full sister under Kalalah"
            else:
                share = Fraction(2, 3)
                reason = "2/3 shared equally among multiple sisters under Kalalah"
            group_shares["sister"] = share
            group_categories["sister"] = "Zawil-Furooz (Quranic Sharer)"
            group_basis["sister"] = "Quran 4:176"
            group_rationale["sister"] = reason

    # Calculate sum of fixed sharers
    fixed_sum = sum(group_shares.values())
    remainder = Fraction(1, 1) - fixed_sum

    # Handle Residuaries (Asaba)
    if num_sons > 0:
        # Sons and Daughters share the remainder in 2:1 ratio
        total_parts = (num_sons * 2) + num_daughters
        if remainder > 0:
            son_total_share = remainder * Fraction(num_sons * 2, total_parts)
            daughter_total_share = remainder * Fraction(num_daughters, total_parts)
            
            group_shares["son"] = son_total_share
            group_categories["son"] = "Asaba (Residuary - 2x Share)"
            group_basis["son"] = "Quran 4:11"
            group_rationale["son"] = f"Sons inherit remainder in 2:1 ratio relative to daughters ({num_sons} sons receive {son_total_share})."
            
            if num_daughters > 0:
                group_shares["daughter"] = daughter_total_share
                group_categories["daughter"] = "Asaba bil-Ghayr (Residuary with Brother - 1x Share)"
                group_basis["daughter"] = "Quran 4:11"
                group_rationale["daughter"] = f"Daughters inherit remainder in 1:2 ratio alongside brothers ({num_daughters} daughters receive {daughter_total_share})."
    elif num_fathers > 0 and num_sons == 0:
        # If father has residual entitlement
        if remainder > 0:
            current_father = group_shares.get("father", Fraction(0, 1))
            group_shares["father"] = current_father + remainder
            group_rationale["father"] += f" Plus took remainder of {remainder} as residuary."
    elif not has_children and num_fathers == 0 and num_brothers > 0:
        # Full brothers (and sisters) as Asaba under Kalalah (Quran 4:176)
        total_parts = (num_brothers * 2) + num_sisters
        if remainder > 0:
            brother_total = remainder * Fraction(num_brothers * 2, total_parts)
            group_shares["brother"] = brother_total
            group_categories["brother"] = "Asaba (Residuary Brother - 2x)"
            group_basis["brother"] = "Quran 4:176"
            group_rationale["brother"] = f"Brothers inherit remainder in 2:1 ratio under Kalalah ({brother_total})."
            
            if num_sisters > 0:
                sister_total = remainder * Fraction(num_sisters, total_parts)
                group_shares["sister"] = sister_total
                group_categories["sister"] = "Asaba bil-Ghayr (Sister with Brother - 1x)"
                group_basis["sister"] = "Quran 4:176"
                group_rationale["sister"] = f"Sisters inherit remainder in 1:2 ratio alongside brothers ({sister_total})."

    # Check total sum for Awl or Radd
    total_distributed = sum(group_shares.values())
    awl_applied = False
    radd_applied = False

    # Awl: Sum > 1
    if total_distributed > Fraction(1, 1):
        awl_applied = True
        # Scale down all shares proportionally
        adjusted_shares = {}
        for rel, sh in group_shares.items():
            adjusted_shares[rel] = sh / total_distributed
        group_shares = adjusted_shares
        total_distributed = Fraction(1, 1)

    # Radd: Sum < 1 and no residuary
    elif total_distributed < Fraction(1, 1) and len(group_shares) > 0:
        radd_applied = True
        # Under Pakistani statutory law and contemporary Hanafi judicial application,
        # surplus returns proportionally to all sharers
        adjusted_shares = {}
        for rel, sh in group_shares.items():
            adjusted_shares[rel] = sh / total_distributed
        group_shares = adjusted_shares
        total_distributed = Fraction(1, 1)

    # Build individual heir details
    details: List[HeirShareDetail] = []
    proof_lines = ["=== MATHEMATICAL INHERITANCE PROOF (Faraizi) ==="]

    for rel, group_share in group_shares.items():
        count = counts.get(rel, 1)
        individual_share = group_share / count
        heir_inputs = names_map.get(rel, [])

        proof_lines.append(
            f"• {rel.title()} (x{count}): Total Group Share = {group_share} ({float(group_share)*100:.4f}%), "
            f"Per Individual = {individual_share} ({float(individual_share)*100:.4f}%) [{group_basis.get(rel, '')}]"
        )

        for i, h_input in enumerate(heir_inputs):
            # If multiple heirs in input object
            h_count = h_input.count
            for j in range(h_count):
                name = h_input.name or f"{rel.title()} #{len(details) + 1}"
                details.append(
                    HeirShareDetail(
                        relation=rel,
                        count=1,
                        name=name,
                        is_claimant=h_input.is_claimant if (i == 0 and j == 0) else False,
                        individual_fraction_str=f"{individual_share.numerator}/{individual_share.denominator}",
                        individual_fraction_value=float(individual_share),
                        total_group_fraction_str=f"{group_share.numerator}/{group_share.denominator}",
                        individual_percentage=round(float(individual_share) * 100, 4),
                        category=group_categories.get(rel, "Sharer"),
                        quranic_basis=group_basis.get(rel, "Quran 4:11-12"),
                        theological_rationale=group_rationale.get(rel, ""),
                    )
                )

    proof_lines.append(f"Total Distribution Sum: {total_distributed} (100.0%)")
    if awl_applied:
        proof_lines.append("[!] Awl (Proportional Deficit Adjustment) applied due to total shares exceeding 1.0.")
    if radd_applied:
        proof_lines.append("[!] Radd (Surplus Return) applied due to unallocated residue with no residuary heirs.")

    return ShariaCalculationOutput(
        heir_shares=details,
        total_distributed_fraction=f"{total_distributed.numerator}/{total_distributed.denominator}",
        total_percentage=round(float(total_distributed) * 100, 4),
        base_denominator=total_distributed.denominator,
        awl_applied=awl_applied,
        radd_applied=radd_applied,
        mathematical_proof="\n".join(proof_lines),
    )
