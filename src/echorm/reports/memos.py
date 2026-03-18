"""Structured memo generation helpers."""

from __future__ import annotations

from ..eval.validation import ValidationResult


def build_mapping_comparison_memo(
    *,
    family: str,
    validation: ValidationResult,
    efficacy_summary: str,
) -> str:
    """Build a concise comparison memo."""
    return (
        f"Family: {family}\n"
        f"Lag error: {validation.lag_error:.3f}\n"
        f"Interval contains truth: {validation.interval_contains_truth}\n"
        f"Efficacy summary: {efficacy_summary}\n"
    )
