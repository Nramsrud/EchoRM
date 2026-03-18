"""CLAGN transition analysis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ClagnTransition:
    """A candidate CLAGN transition and its evidence."""

    object_uid: str
    lag_state_change: float
    line_response_ratio: float
    transition_detected: bool


def analyze_clagn_transition(
    *,
    object_uid: str,
    pre_state_lag: float,
    post_state_lag: float,
    pre_line_flux: float,
    post_line_flux: float,
) -> ClagnTransition:
    """Analyze a candidate CLAGN transition."""
    lag_state_change = post_state_lag - pre_state_lag
    line_response_ratio = post_line_flux / max(pre_line_flux, 1e-6)
    return ClagnTransition(
        object_uid=object_uid,
        lag_state_change=lag_state_change,
        line_response_ratio=line_response_ratio,
        transition_detected=(
            abs(lag_state_change) >= 1.0
            or abs(line_response_ratio - 1.0) >= 0.5
        ),
    )
