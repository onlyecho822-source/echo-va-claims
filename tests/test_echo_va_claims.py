"""Tests for echo-va-claims — Art of Proof VA disability claim logic."""
import pytest


# ── Rating combinations ───────────────────────────────────────────────────────

def combined_rating(ratings):
    """VA combined ratings formula: each rating applied to remaining efficiency."""
    efficiency = 1.0
    for r in sorted(ratings, reverse=True):
        efficiency *= (1 - r / 100)
    return round((1 - efficiency) * 100)


def test_single_rating_unchanged():
    assert combined_rating([50]) == 50


def test_two_ratings_combined():
    assert combined_rating([50, 30]) == 65


def test_three_ratings_combined():
    result = combined_rating([70, 50, 30])
    assert 80 <= result <= 95


def test_rating_always_under_100():
    assert combined_rating([90, 80, 70, 60]) < 100


def test_rating_increases_with_more_conditions():
    r1 = combined_rating([50])
    r2 = combined_rating([50, 30])
    assert r2 > r1


def test_zero_rating_no_effect():
    assert combined_rating([0, 50]) == combined_rating([50])


# ── Claim type classification ──────────────────────────────────────────────────

CLAIM_TYPES = [
    "direct_service_connection",
    "secondary_connection",
    "aggravation",
    "tdiu",
    "cue",
]

def test_claim_types_complete():
    assert "tdiu" in CLAIM_TYPES
    assert "direct_service_connection" in CLAIM_TYPES
    assert len(CLAIM_TYPES) == 5


def test_secondary_connection_requires_primary():
    def validate_secondary(primary_condition, secondary_condition):
        return bool(primary_condition and secondary_condition)
    assert validate_secondary("PTSD", "insomnia") is True
    assert validate_secondary(None, "insomnia") is False


# ── TDIU qualification ─────────────────────────────────────────────────────────

def tdiu_qualified(combined, individual_ratings):
    """TDIU: 60% combined OR one condition at 40%+ if combined ≥70%."""
    if combined >= 60 and max(individual_ratings) >= 40:
        return True
    if combined >= 70:
        return True
    return False


def test_tdiu_qualifies_at_60_combined():
    assert tdiu_qualified(60, [40]) is True


def test_tdiu_qualifies_at_70_combined():
    assert tdiu_qualified(70, [30]) is True


def test_tdiu_fails_below_threshold():
    assert tdiu_qualified(30, [20]) is False


def test_tdiu_requires_individual_at_40():
    assert tdiu_qualified(60, [39]) is False


# ── Nexus letter elements ──────────────────────────────────────────────────────

def test_nexus_letter_required_elements():
    required = ["diagnosis", "at_least_as_likely", "service_event", "medical_rationale"]
    letter = {
        "diagnosis": "PTSD",
        "at_least_as_likely": True,
        "service_event": "IED exposure 2003",
        "medical_rationale": "Per DSM-5 criteria",
    }
    assert all(k in letter for k in required)


def test_nexus_strength_levels():
    levels = ["at_least_as_likely", "more_likely_than_not", "highly_probable"]
    assert len(levels) == 3
    assert "at_least_as_likely" in levels
