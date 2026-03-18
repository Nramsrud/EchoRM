"""Line extraction and metric builders."""

from __future__ import annotations

from ..schemas import LINE_METRICS_SCHEMA
from .continuum import ContinuumFit
from .diagnostics import residual_rms
from .preprocess import ProcessedSpectrum


def extract_line_metrics(
    *,
    object_uid: str,
    epoch_uid: str,
    line_name: str,
    spectrum: ProcessedSpectrum,
    fit: ContinuumFit,
    line_window: tuple[float, float],
) -> dict[str, object]:
    """Extract canonical line metrics inside a rest-frame line window."""
    selected = [
        (wave, residual)
        for wave, residual in zip(
            spectrum.wavelength_rest,
            fit.residuals,
            strict=False,
        )
        if line_window[0] <= wave <= line_window[1]
    ]
    if not selected:
        raise ValueError("line window does not overlap the spectrum")
    residuals = [residual for _, residual in selected]
    line_flux = sum(residuals)
    peak = max(residuals)
    half_peak = peak / 2.0 if peak else 0.0
    fwhm_points = [wave for wave, residual in selected if residual >= half_peak]
    fwhm = max(fwhm_points) - min(fwhm_points) if fwhm_points else 0.0
    centroid = (
        sum(wave * residual for wave, residual in selected)
        / max(line_flux, 1e-6)
    )
    sigma_line = (
        sum(((wave - centroid) ** 2) * residual for wave, residual in selected)
        / max(line_flux, 1e-6)
    ) ** 0.5
    midpoint = len(residuals) // 2
    blue_flux = sum(residuals[:midpoint])
    red_flux = sum(residuals[midpoint:])
    asymmetry = blue_flux - red_flux
    record = {
        "object_uid": object_uid,
        "epoch_uid": epoch_uid,
        "line_name": line_name,
        "line_flux": line_flux,
        "line_flux_err": abs(line_flux) * 0.05,
        "ew": line_flux / max(sum(fit.continuum) / len(fit.continuum), 1e-6),
        "ew_err": abs(line_flux) * 0.02,
        "fwhm": fwhm,
        "fwhm_err": fwhm * 0.05,
        "sigma_line": sigma_line,
        "sigma_line_err": sigma_line * 0.05,
        "centroid": centroid,
        "centroid_err": 0.1,
        "skew": asymmetry / max(abs(line_flux), 1e-6),
        "kurtosis": peak / max(abs(line_flux), 1e-6),
        "blue_red_asymmetry": asymmetry,
        "fit_model_id": fit.fit_model_id,
        "continuum_variant": fit.variant,
        "calibration_confidence": fit.calibration_confidence,
        "residual_rms": residual_rms(fit),
    }
    return LINE_METRICS_SCHEMA.ordered_record(record)
