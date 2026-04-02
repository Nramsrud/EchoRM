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
    pre_state_lag: float
    post_state_lag: float
    evidence_level: str = "derived"

    def to_dict(self) -> dict[str, object]:
        """Serialize the transition record."""
        return {
            "object_uid": self.object_uid,
            "lag_state_change": self.lag_state_change,
            "line_response_ratio": self.line_response_ratio,
            "transition_detected": self.transition_detected,
            "pre_state_lag": self.pre_state_lag,
            "post_state_lag": self.post_state_lag,
            "evidence_level": self.evidence_level,
        }


def analyze_clagn_transition(
    *,
    object_uid: str,
    pre_state_lag: float,
    post_state_lag: float,
    pre_line_flux: float,
    post_line_flux: float,
    evidence_level: str = "derived",
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
        pre_state_lag=pre_state_lag,
        post_state_lag=post_state_lag,
        evidence_level=evidence_level,
    )
