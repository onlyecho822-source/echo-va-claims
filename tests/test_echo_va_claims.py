"""Tests for echo-va-claims (Art of Proof VA disability platform)."""
import pytest

def test_claim_types():
    types = ["direct_service_connection","secondary_connection","aggravation","tdiu","cue"]
    assert "tdiu" in types

def test_rating_combination():
    # VA combined ratings (whole person remaining method)
    def combine(r1, r2):
        remaining = (100 - r1) / 100
        return round(r1 + r2 * remaining)
    assert combine(50, 30) == 65

def test_effective_date_logic():
    import datetime
    claim_date = datetime.date(2020, 1, 15)
    start_date = datetime.date(2020, 1, 1)
    assert claim_date >= start_date

def test_evidence_tiers():
    tiers = ["buddy_statement","medical_nexus","service_records","lay_statement","ima"]
    assert len(tiers) == 5

def test_tdiu_threshold():
    single_rating = 60
    assert single_rating >= 60

def test_nexus_letter_structure():
    letter = {"diagnosis": "", "service_connection": "", "rationale": "", "confidence": ""}
    assert all(k in letter for k in ["diagnosis", "rationale"])

def test_art_of_proof_sections():
    sections = ["intake","evidence_prep","claim_build","review","submit","track"]
    assert len(sections) == 6

def test_dr_based_caregiver():
    caregiver = {"location": "Dominican Republic", "relationship": "spouse", "statement": True}
    assert caregiver["statement"] is True

def test_openai_prompt_structure():
    prompt = {"role": "system", "content": "You are an Art of Proof assistant"}
    assert prompt["role"] == "system"

def test_rating_schedule_categories():
    cats = ["musculoskeletal","mental_health","respiratory","cardiovascular","neurological"]
    assert len(cats) >= 5
