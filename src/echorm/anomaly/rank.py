"""Interpretable anomaly scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnomalyScore:
    """Traceable anomaly score and its components."""

    object_uid: str
    total_score: float
    components: dict[str, float]


def rank_anomaly(
    *,
    object_uid: str,
    lag_outlier: float,
    line_response_outlier: float,
    sonification_outlier: float,
    is_holdout: bool,
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
    )
