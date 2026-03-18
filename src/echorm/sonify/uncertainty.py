"""Uncertainty-encoding implementations."""

from __future__ import annotations


def encode_uncertainty(
    *,
    uncertainty_mode: str,
    uncertainty_value: float,
) -> dict[str, float]:
    """Encode uncertainty into deterministic audio-control parameters."""
    if uncertainty_mode == "amplitude_wobble":
        return {"amplitude_wobble": round(uncertainty_value, 3)}
    if uncertainty_mode == "timbre_spread":
        return {"timbre_spread": round(uncertainty_value, 3)}
    raise ValueError(f"unsupported uncertainty mode: {uncertainty_mode}")
