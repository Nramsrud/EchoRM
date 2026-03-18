"""Null-control and shuffled-pair helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .serialize import SerializedLagResult


@dataclass(frozen=True, slots=True)
class NullDiagnostic:
    """Null-control summary for one consensus evaluation."""

    false_positive_rate: float
    null_pair_count: int


def evaluate_null_controls(results: tuple[SerializedLagResult, ...]) -> NullDiagnostic:
    """Estimate null false-positive rate from low-significance lag runs."""
    null_like = sum(
        float(str(result.record["significance"])) < 0.6
        for result in results
    )
    count = len(results)
    return NullDiagnostic(
        false_positive_rate=round(null_like / max(count, 1), 3),
        null_pair_count=count,
    )
