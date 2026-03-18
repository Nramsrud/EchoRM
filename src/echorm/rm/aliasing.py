"""Alias-risk calculations."""

from __future__ import annotations


def compute_alias_risk(lag_medians: tuple[float, ...]) -> float:
    """Estimate alias risk from method-to-method lag dispersion."""
    if not lag_medians:
        return 1.0
    spread = max(lag_medians) - min(lag_medians)
    center = sum(lag_medians) / len(lag_medians)
    return round(min(1.0, spread / (abs(center) + 1.0)), 3)
