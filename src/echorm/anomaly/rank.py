"""Interpretable anomaly scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnomalyScore:
    """Traceable anomaly score and its components."""

    object_uid: str
    total_score: float
    components: dict[str, float]
    evidence_level: str = "derived"
    method_support_count: int = 0
    review_priority: str = "medium"

    def to_dict(self) -> dict[str, object]:
        """Serialize the score."""
        return {
            "object_uid": self.object_uid,
            "total_score": self.total_score,
            "components": self.components,
            "evidence_level": self.evidence_level,
            "method_support_count": self.method_support_count,
            "review_priority": self.review_priority,
        }


def rank_anomaly(
    *,
    object_uid: str,
    lag_outlier: float,
    line_response_outlier: float,
    sonification_outlier: float,
    is_holdout: bool,
    evidence_level: str = "derived",
    method_support_count: int = 0,
    review_priority: str = "medium",
) -> AnomalyScore:
    """Rank one object by interpretable anomaly components."""
    if not is_holdout:
        raise ValueError("discovery ranking requires hold-out inputs")
    components = {
        "lag_outlier": lag_outlier,
        "line_response_outlier": line_response_outlier,
        "sonification_outlier": sonification_outlier,
    }
    total_score = round(sum(components.values()) / len(components), 3)
    return AnomalyScore(
        object_uid=object_uid,
        total_score=total_score,
        components=components,
        evidence_level=evidence_level,
        method_support_count=method_support_count,
        review_priority=review_priority,
    )
