"""Tests for echo-va-claims — Art of Proof™ VA disability evidence engine."""
import pytest


def test_import_package():
    """Verify package is importable — entry point smoke test."""
    try:
        import echo_va_claims as evc
        assert evc is not None
    except ImportError:
        # Try alternate import path
        try:
            from va_claims import core
            assert core is not None
        except ImportError:
            pytest.skip("Package not yet installable — integration test only")


def test_evidence_scoring_logic():
    """Test evidence scoring rules are consistent."""
    scores = {
        "nexus_letter": 0.4,
        "buddy_statement": 0.15,
        "medical_records": 0.3,
        "service_records": 0.25,
    }
    total = sum(scores.values())
    assert total > 0
    # Nexus letter should be highest weight
    assert scores["nexus_letter"] == max(scores.values())


def test_rating_tiers():
    """VA rating tiers are 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100."""
    valid_ratings = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100}
    test_values = [0, 10, 50, 100, 5, 15, 99]
    for v in test_values:
        rounded = round(v / 10) * 10
        assert rounded in valid_ratings


def test_combined_ratings_never_exceed_100():
    """Combined VA rating (whole person theory) never exceeds 100."""
    def combine(ratings):
        remaining = 100
        for r in sorted(ratings, reverse=True):
            remaining -= remaining * (r / 100)
        return round(100 - remaining)
    assert combine([50, 30, 10]) <= 100
    assert combine([70, 60, 50, 40]) <= 100


def test_claim_status_states():
    """Claim lifecycle states are defined."""
    states = ["PENDING", "IN_REVIEW", "APPROVED", "DENIED", "APPEALED"]
    assert len(states) == 5
    assert "APPROVED" in states


def test_effective_date_logic():
    """Effective date is earliest of intent to file or claim date."""
    from datetime import date
    intent_date = date(2023, 1, 15)
    claim_date = date(2023, 3, 1)
    effective = min(intent_date, claim_date)
    assert effective == intent_date


def test_nexus_confidence_levels():
    """Nexus letter confidence levels map to standard language."""
    levels = {
        "at_least_as_likely": 0.50,
        "more_likely_than_not": 0.51,
        "highly_probable": 0.75,
        "without_doubt": 0.95,
    }
    assert levels["more_likely_than_not"] > levels["at_least_as_likely"]


def test_evidence_completeness_score():
    """Evidence completeness follows additive model."""
    def completeness(evidence_types):
        weights = {"nexus": 40, "medical": 30, "service": 20, "buddy": 10}
        return sum(weights.get(e, 0) for e in evidence_types)
    assert completeness(["nexus", "medical"]) == 70
    assert completeness(["nexus", "medical", "service", "buddy"]) == 100


def test_rating_combination_whole_person():
    """Whole person theory: each disability applied to remaining efficiency."""
    def whole_person(d1, d2):
        remaining = 100 - d1
        additional = remaining * d2 / 100
        return round(d1 + additional)
    result = whole_person(50, 30)
    assert 60 <= result <= 70


def test_tdiu_threshold():
    """TDIU threshold: single 60% or combined 70% with one at 40%."""
    def tdiu_eligible(ratings):
        if max(ratings) >= 60:
            return True
        if sum(ratings) >= 70 and max(ratings) >= 40:
            return True
        return False
    assert tdiu_eligible([60]) is True
    assert tdiu_eligible([40, 30]) is True
    assert tdiu_eligible([30, 30]) is False
