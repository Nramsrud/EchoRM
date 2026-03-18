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


def build_candidate(
    *,
    score: AnomalyScore,
    transition: ClagnTransition,
) -> CandidateRecord:
    """Build a ranked candidate record."""
    category = (
        "clagn_transition"
        if transition.transition_detected
        else "continuum_lag_outlier"
    )
    return CandidateRecord(
        object_uid=score.object_uid,
        anomaly_category=category,
        rank_score=score.total_score,
        evidence_bundle={
            "score_components": score.components,
            "lag_state_change": transition.lag_state_change,
            "line_response_ratio": transition.line_response_ratio,
        },
    )
