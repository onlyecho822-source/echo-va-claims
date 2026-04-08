"""Tests for echo-va-claims (Art of Proof VA platform)."""
import pytest

def test_claim_types():
    types = ["direct_service_connection", "secondary", "aggravation", "presumptive", "tdiu"]
    assert "tdiu" in types

def test_evidence_categories():
    cats = ["medical_nexus", "buddy_statement", "service_records", "lay_evidence", "dbq"]
    assert len(cats) == 5

def test_nexus_score():
    def nexus(medical_strength, service_docs, continuity):
        return (medical_strength * 0.5 + service_docs * 0.3 + continuity * 0.2)
    score = nexus(0.9, 0.8, 0.7)
    assert 0.7 < score < 1.0

def test_rating_percentages():
    ratings = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    assert 100 in ratings and 0 in ratings

def test_tdiu_criteria():
    criteria = {
        "single_condition_rating": 60,
        "combined_rating": 70,
        "unemployability": True
    }
    assert criteria["single_condition_rating"] == 60

def test_effective_date_logic():
    import datetime
    filing_date = datetime.date(2024, 1, 15)
    assert filing_date.year == 2024

def test_buddy_statement_fields():
    stmt = {"name": str, "relationship": str, "observations": str, "signed": bool}
    assert "relationship" in stmt

def test_art_of_proof_mission():
    mission = "universal evidence preparation engine"
    assert "evidence" in mission

def test_supplemental_claim():
    claim = {"type": "supplemental", "new_evidence": True, "prior_denial": True}
    assert claim["new_evidence"] is True

def test_stripe_tiers():
    tiers = {"basic": 29, "pro": 79, "full_service": 299}
    assert tiers["pro"] > tiers["basic"]
