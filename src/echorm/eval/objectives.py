"""Optimization objectives and constraints."""

from __future__ import annotations

from ..eval.validation import ValidationResult


def compute_mean_validation_score(
    results: tuple[ValidationResult, ...],
) -> float:
    """Compute a benchmark-locked validation objective."""
    if not results:
        return 0.0
    penalty = sum(result.lag_error + float(result.false_positive) for result in results)
    return round(max(0.0, 1.0 - (penalty / len(results))), 3)


def enforce_mutation_guard(
    *,
    candidate: dict[str, object],
    allowed_fields: tuple[str, ...],
    prohibited_targets: tuple[str, ...],
) -> None:
    """Reject mutation candidates that reach prohibited surfaces."""
    for key in candidate:
        if key in prohibited_targets:
            raise ValueError(f"prohibited optimization target: {key}")
        if key not in allowed_fields:
            raise ValueError(f"non-mutable optimization field: {key}")
