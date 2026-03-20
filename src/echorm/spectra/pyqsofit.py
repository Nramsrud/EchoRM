"""PyQSOFit-style decomposition helpers."""

from __future__ import annotations

from .continuum import ContinuumFit, _build_fit
from .preprocess import ProcessedSpectrum


def fit_pyqsofit_decomposition(spectrum: ProcessedSpectrum) -> ContinuumFit:
    """Build a PyQSOFit-style pseudo decomposition record."""
    continuum = []
    midpoint = len(spectrum.flux) // 2
    for index, flux in enumerate(spectrum.flux):
        weight = 0.92 if index < midpoint else 0.88
        continuum.append(flux * weight)
    fit = _build_fit(
        spectrum,
        variant="pyqsofit",
        continuum=tuple(continuum),
        calibration_confidence=0.87,
    )
    return ContinuumFit(
        variant=fit.variant,
        continuum=fit.continuum,
        residuals=fit.residuals,
        calibration_confidence=fit.calibration_confidence,
        fit_model_id=f"pyqsofit:{spectrum.calibration_state}:feii_balmer_host",
    )
