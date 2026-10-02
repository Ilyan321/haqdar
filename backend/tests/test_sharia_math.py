import pytest
from app.tools.sharia_math import calculate_faraizi_shares, HeirInput

def test_standard_case_fatima():
    """
    Fatima's Case:
    Deceased leaves:
    - 1 Wife (Mother of children) -> 1/8
    - 1 Mother of deceased -> 1/6
    - 2 Sons -> 2x share each
    - 1 Daughter (Fatima) -> 1x share
    
    Total fixed = 1/8 + 1/6 = 3/24 + 4/24 = 7/24
    Remainder = 17/24
    Total parts for children = (2 sons * 2) + (1 daughter * 1) = 5 parts
    Daughter share = (17/24) * (1/5) = 17/120 (~14.1667%)
    Each son share = (17/24) * (2/5) = 34/120 = 17/60 (~28.3333%)
    Wife share = 1/8 = 15/120 (12.5%)
    Mother share = 1/6 = 20/120 (~16.6667%)
    Sum = 15 + 20 + 34 + 34 + 17 = 120/120 = 1.0 (100%)
    """
    heirs = [
        HeirInput(relation="wife", count=1, name="Kulsoom Bibi"),
        HeirInput(relation="mother", count=1, name="Jannat Bibi"),
        HeirInput(relation="son", count=2, name="Tariq & Rashid"),
        HeirInput(relation="daughter", count=1, name="Fatima Bibi", is_claimant=True),
    ]

    res = calculate_faraizi_shares(heirs)

    assert res.total_distributed_fraction == "1/1"
    assert res.total_percentage == 100.0
    assert not res.awl_applied
    assert not res.radd_applied

    # Check shares map
    shares = {h.name: h.individual_fraction_str for h in res.heir_shares}
    
    wife_share = next(h for h in res.heir_shares if h.relation == "wife")
    mother_share = next(h for h in res.heir_shares if h.relation == "mother")
    daughter_share = next(h for h in res.heir_shares if h.relation == "daughter")
    son_shares = [h for h in res.heir_shares if h.relation == "son"]

    assert wife_share.individual_fraction_str == "1/8"
    assert mother_share.individual_fraction_str == "1/6"
    assert daughter_share.individual_fraction_str == "17/120"
    assert son_shares[0].individual_fraction_str == "17/60"
    assert son_shares[1].individual_fraction_str == "17/60"

def test_awl_case():
    """
    Awl Scenario:
    - Husband -> 1/4 (due to children)
    - 2 Daughters -> 2/3
    - Mother -> 1/6
    - Father -> 1/6
    Sum = 3/12 + 8/12 + 2/12 + 2/12 = 15/12 > 1.0
    Base denominator expands from 12 to 15.
    Husband: 3/15 = 1/5
    2 Daughters: 8/15 (4/15 each)
    Mother: 2/15
    Father: 2/15
    """
    heirs = [
        HeirInput(relation="husband", count=1),
        HeirInput(relation="daughter", count=2),
        HeirInput(relation="mother", count=1),
        HeirInput(relation="father", count=1),
    ]
    res = calculate_faraizi_shares(heirs)
    assert res.awl_applied is True
    assert res.total_distributed_fraction == "1/1"
    assert res.total_percentage == 100.0

def test_kalalah_case():
    """
    Kalalah Scenario (No children, no father):
    - 1 Wife -> 1/4
    - 1 Brother -> Asaba (2x)
    - 1 Sister -> Asaba (1x)
    Remainder = 3/4
    Parts = 2 + 1 = 3 parts
    Brother = 3/4 * 2/3 = 2/4 = 1/2
    Sister = 3/4 * 1/3 = 1/4
    """
    heirs = [
        HeirInput(relation="wife", count=1),
        HeirInput(relation="brother", count=1),
        HeirInput(relation="sister", count=1),
    ]
    res = calculate_faraizi_shares(heirs)
    assert not res.awl_applied
    assert res.total_distributed_fraction == "1/1"
    
    wife_share = next(h for h in res.heir_shares if h.relation == "wife")
    brother_share = next(h for h in res.heir_shares if h.relation == "brother")
    sister_share = next(h for h in res.heir_shares if h.relation == "sister")

    assert wife_share.individual_fraction_str == "1/4"
    assert brother_share.individual_fraction_str == "1/2"
    assert sister_share.individual_fraction_str == "1/4"

def test_widow_two_sons_two_daughters():
    """
    Case with 1 Widow, 2 Sons, 2 Daughters:
    - Widow: 1/8 (6/48)
    - Remainder: 7/8
    - 2 Sons (2 parts each) + 2 Daughters (1 part each) = 6 parts
    - Each Son: (7/8) * (2/6) = 7/24 (14/48)
    - Each Daughter: (7/8) * (1/6) = 7/48
    - Sum: 6/48 + 14/48 + 14/48 + 7/48 + 7/48 = 48/48 = 1.0
    """
    heirs = [
        HeirInput(relation="wife", count=1, name="Widow"),
        HeirInput(relation="son", count=2, name="Son 1 & Son 2"),
        HeirInput(relation="daughter", count=2, name="Daughter 1 & Daughter 2", is_claimant=True),
    ]
    res = calculate_faraizi_shares(heirs)
    assert res.total_distributed_fraction == "1/1"
    assert res.total_percentage == 100.0

    wife_share = next(h for h in res.heir_shares if h.relation == "wife")
    son_shares = [h for h in res.heir_shares if h.relation == "son"]
    daughter_shares = [h for h in res.heir_shares if h.relation == "daughter"]

    assert wife_share.individual_fraction_str == "1/8"
    assert son_shares[0].individual_fraction_str == "7/24"
    assert son_shares[1].individual_fraction_str == "7/24"
    assert daughter_shares[0].individual_fraction_str == "7/48"
    assert daughter_shares[1].individual_fraction_str == "7/48"
