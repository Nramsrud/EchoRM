"""Fit and calibration diagnostics."""

from __future__ import annotations

from .continuum import ContinuumFit


def residual_rms(fit: ContinuumFit) -> float:
    """Compute the RMS of continuum residuals."""
    squared = [value * value for value in fit.residuals]
    rms = (sum(squared) / max(len(squared), 1)) ** 0.5
    return float(rms)
