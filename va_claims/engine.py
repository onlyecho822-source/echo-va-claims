"""
va_claims/engine.py — Art of Proof™ VA Disability Evidence Scoring Engine.
Implements CFR 38 Part 4 rating math, TDIU threshold logic,
nexus confidence levels, and evidence completeness scoring.
∇θ Operator — Echo Universe T2 Revenue
"""
from __future__ import annotations
import hashlib, time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class DischargeType(Enum):
    HONORABLE           = "Honorable"
    GENERAL             = "General Under Honorable"
    OTHER_THAN_HONORABLE = "Other Than Honorable"
    BAD_CONDUCT         = "Bad Conduct Discharge"
    DISHONORABLE        = "Dishonorable"


class ClaimType(Enum):
    DISABILITY  = "disability"
    PENSION     = "pension"
    EDUCATION   = "education"
    HOUSING     = "housing"
    HEALTHCARE  = "healthcare"


class NexusConfidence(Enum):
    AT_LEAST_AS_LIKELY  = 0.50   # "at least as likely as not"
    MORE_LIKELY         = 0.51   # "more likely than not"
    HIGHLY_PROBABLE     = 0.75   # "highly probable"
    WITHOUT_DOUBT       = 0.95   # "without reasonable doubt"


EVIDENCE_WEIGHTS: Dict[str, float] = {
    "nexus_letter":     0.40,
    "medical_records":  0.30,
    "service_records":  0.25,
    "buddy_statement":  0.15,
    "lay_statement":    0.10,
    "dbq_form":         0.35,
}

VALID_RATINGS = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100}


@dataclass
class EvidencePackage:
    veteran_id: str
    condition: str
    evidence_types: List[str] = field(default_factory=list)
    nexus_confidence: Optional[NexusConfidence] = None
    submitted_at: float = field(default_factory=time.time)

    def completeness_score(self) -> float:
        """Weighted evidence completeness 0.0–1.0."""
        max_possible = sum(EVIDENCE_WEIGHTS.values())
        score = sum(EVIDENCE_WEIGHTS.get(e, 0) for e in self.evidence_types)
        return min(1.0, score / max_possible)

    def is_service_connected(self) -> bool:
        return (self.nexus_confidence is not None and
                self.nexus_confidence.value >= NexusConfidence.AT_LEAST_AS_LIKELY.value)

    def fingerprint(self) -> str:
        data = f"{self.veteran_id}:{self.condition}:{sorted(self.evidence_types)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


class RatingEngine:
    """
    Implements CFR 38 Part 4 combined ratings table (whole person theory).
    Ratings are applied in descending order to the remaining efficiency.
    """

    @staticmethod
    def round_to_valid(raw: float) -> int:
        """Round raw combined rating to nearest 10 (VA rounding rules)."""
        if raw % 10 >= 5:
            return int((raw // 10 + 1) * 10)
        return int((raw // 10) * 10)

    @staticmethod
    def combine(ratings: List[int]) -> int:
        """Combine multiple disability ratings using whole person theory."""
        if not ratings:
            return 0
        remaining = 100.0
        for r in sorted(ratings, reverse=True):
            remaining -= remaining * (r / 100)
        raw = 100 - remaining
        return RatingEngine.round_to_valid(raw)

    @staticmethod
    def tdiu_eligible(ratings: List[int]) -> bool:
        """
        TDIU eligibility: single rating ≥60% OR combined ≥70% with one ≥40%.
        38 CFR 4.16(a)
        """
        if not ratings:
            return False
        if max(ratings) >= 60:
            return True
        combined = RatingEngine.combine(ratings)
        if combined >= 70 and max(ratings) >= 40:
            return True
        return False

    @staticmethod
    def effective_date(intent_to_file, claim_date) -> object:
        """Effective date is earliest of intent-to-file or claim date."""
        return min(intent_to_file, claim_date)


class ClaimProcessor:
    """End-to-end claim intake, scoring, and status tracking."""

    DISCHARGE_ELIGIBLE = {DischargeType.HONORABLE, DischargeType.GENERAL}
    MIN_SERVICE_DAYS = 90

    def __init__(self):
        self._claims: Dict[str, dict] = {}
        self._counter = 0

    def submit(self, veteran_id: str, condition: str, evidence: EvidencePackage,
               discharge: DischargeType, service_days: int) -> str:
        """Submit a claim. Returns reference number."""
        self._counter += 1
        ref = f"AOP-{int(time.time())}-{self._counter:04d}"
        self._claims[ref] = {
            "ref": ref, "veteran_id": veteran_id, "condition": condition,
            "evidence": evidence, "discharge": discharge, "service_days": service_days,
            "status": "SUBMITTED", "submitted_at": time.time(),
        }
        return ref

    def is_eligible(self, ref: str) -> bool:
        c = self._claims.get(ref)
        if not c:
            return False
        return (c["discharge"] in self.DISCHARGE_ELIGIBLE and
                c["service_days"] >= self.MIN_SERVICE_DAYS)

    def get_status(self, ref: str) -> str:
        return self._claims.get(ref, {}).get("status", "NOT_FOUND")

    def advance_status(self, ref: str, new_status: str) -> bool:
        if ref not in self._claims:
            return False
        self._claims[ref]["status"] = new_status
        return True

    def claim_count(self) -> int:
        return len(self._claims)

    def summary(self) -> Dict:
        statuses = {}
        for c in self._claims.values():
            statuses[c["status"]] = statuses.get(c["status"], 0) + 1
        return {"total": len(self._claims), "by_status": statuses}
