"""Consensus lag object and classification logic."""

from __future__ import annotations

from dataclasses import dataclass

from .aliasing import compute_alias_risk
from .nulls import NullDiagnostic
from .serialize import SerializedLagResult


@dataclass(frozen=True, slots=True)
class ConsensusLag:
    """Consensus lag classification over multiple method results."""

    object_uid: str
    pair_id: str
    classification: str
    agreement_score: float
    alias_risk: float
    null_false_positive_rate: float
    method_results: tuple[SerializedLagResult, ...]


def build_consensus(
    results: tuple[SerializedLagResult, ...],
    *,
    null_diagnostic: NullDiagnostic,
) -> ConsensusLag:
    """Aggregate method-level lag results into the project taxonomy."""
    if not results:
        raise ValueError("consensus requires at least one method result")
    lag_medians = tuple(float(str(result.record["lag_median"])) for result in results)
    mean_lag = sum(lag_medians) / len(lag_medians)
    spread = max(lag_medians) - min(lag_medians)
    agreement_score = round(max(0.0, 1.0 - (spread / (abs(mean_lag) + 1.0))), 3)
    alias_risk = compute_alias_risk(lag_medians)
    quality_scores = [
        float(str(result.record["quality_score"])) for result in results
    ]
    mean_quality = sum(quality_scores) / len(quality_scores)
    if null_diagnostic.false_positive_rate >= 0.5:
        classification = "likely_spurious"
    elif agreement_score >= 0.75 and alias_risk <= 0.35:
        classification = "agreement_cluster"
    elif agreement_score < 0.4 and mean_quality >= 0.8:
        classification = "candidate_anomaly"
    else:
        classification = "contested"
    first = results[0].record
    return ConsensusLag(
        object_uid=str(first["object_uid"]),
        pair_id=str(first["pair_id"]),
        classification=classification,
        agreement_score=agreement_score,
        alias_risk=alias_risk,
        null_false_positive_rate=null_diagnostic.false_positive_rate,
        method_results=results,
    )
