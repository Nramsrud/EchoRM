"""Ranked candidate builders."""

from __future__ import annotations

from dataclasses import dataclass

from .clagn import ClagnTransition
from .rank import AnomalyScore


@dataclass(frozen=True, slots=True)
class CandidateRecord:
    """A ranked anomaly candidate with evidence."""

    object_uid: str
    anomaly_category: str
    rank_score: float
    evidence_bundle: dict[str, object]
    canonical_name: str = ""
    review_priority: str = "medium"
    method_support_count: int = 0
    limitations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Serialize the candidate record."""
        return {
            "object_uid": self.object_uid,
            "canonical_name": self.canonical_name,
            "anomaly_category": self.anomaly_category,
            "rank_score": self.rank_score,
            "evidence_bundle": self.evidence_bundle,
            "review_priority": self.review_priority,
            "method_support_count": self.method_support_count,
            "limitations": list(self.limitations),
        }


def build_candidate(
    *,
    score: AnomalyScore,
    transition: ClagnTransition,
    canonical_name: str = "",
    benchmark_links: tuple[str, ...] = (),
    limitations: tuple[str, ...] = (),
) -> CandidateRecord:
    """Build a ranked candidate record."""
    if transition.transition_detected:
        category = "clagn_transition"
    elif transition.alignment_eligible and not transition.state_transition_supported:
        category = "clagn_precursor_context"
    else:
        category = "continuum_lag_outlier"
    return CandidateRecord(
        object_uid=score.object_uid,
        anomaly_category=category,
        rank_score=score.total_score,
        evidence_bundle={
            "score_components": score.components,
            "lag_state_change": transition.lag_state_change,
            "line_response_ratio": transition.line_response_ratio,
            "alignment_eligible": transition.alignment_eligible,
            "state_transition_supported": transition.state_transition_supported,
            "alignment_status": transition.alignment_status,
            "evidence_level": score.evidence_level,
            "benchmark_links": list(benchmark_links),
        },
        canonical_name=canonical_name,
        review_priority=score.review_priority,
        method_support_count=score.method_support_count,
        limitations=limitations,
    )
