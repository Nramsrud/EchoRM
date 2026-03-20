"""PyQSOFit-backed decomposition helpers."""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

import numpy as np

from .continuum import ContinuumFit, _build_fit
from .preprocess import ProcessedSpectrum

try:
    from pyqsofit.PyQSOFit import QSOFit  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover - runtime dependent
    QSOFit = None


_QSOPAR_URL = (
    "https://raw.githubusercontent.com/legolason/PyQSOFit/"
    "084df5a7d2af76b38719af5851b114ad9ecf4d60/src/pyqsofit/qsopar.fits"
)


def fit_pyqsofit_decomposition(spectrum: ProcessedSpectrum) -> ContinuumFit:
    """Run the official PyQSOFit backend on a processed spectrum."""
    if QSOFit is None:
        return _fallback_fit(spectrum)
    try:
        resource_root = _ensure_resource_root()
        qsofit = QSOFit(
            np.array(spectrum.wavelength_obs, dtype=float),
            np.array(spectrum.flux, dtype=float),
            np.full(len(spectrum.flux), _error_scale(spectrum), dtype=float),
            0.0,
            path=str(resource_root),
        )
        qsofit.Fit(
            name="echorm-pyqsofit",
            nsmooth=1,
            reject_badpix=False,
            deredden=False,
            wave_range=(
                float(spectrum.wavelength_obs[0]),
                float(spectrum.wavelength_obs[-1]),
            ),
            decompose_host=False,
            Fe_uv_op=False,
            poly=True,
            BC=False,
            rej_abs_conti=False,
            rej_abs_line=False,
            linefit=True,
            save_result=False,
            plot_fig=False,
            save_fig=False,
            plot_corner=False,
            verbose=False,
        )
        continuum = tuple(float(value) for value in np.array(qsofit.f_conti_model))
        fit = _build_fit(
            spectrum,
            variant="pyqsofit",
            continuum=continuum,
            calibration_confidence=0.93,
        )
        line_tag = "unknown"
        if hasattr(qsofit, "line_result_name"):
            names = [str(value) for value in np.array(qsofit.line_result_name)]
            if any(name.startswith("Hb_") for name in names):
                line_tag = "hbeta"
            elif any(name.startswith("MgII") for name in names):
                line_tag = "mgii"
        return ContinuumFit(
            variant=fit.variant,
            continuum=fit.continuum,
            residuals=fit.residuals,
            calibration_confidence=fit.calibration_confidence,
            fit_model_id=(
                f"pyqsofit:{spectrum.calibration_state}:{line_tag}:"
                "official_package_execution"
            ),
        )
    except Exception:  # pragma: no cover - integration path
        return _fallback_fit(spectrum)


def _fallback_fit(spectrum: ProcessedSpectrum) -> ContinuumFit:
    continuum = []
    midpoint = len(spectrum.flux) // 2
    for index, flux in enumerate(spectrum.flux):
        weight = 0.92 if index < midpoint else 0.88
        continuum.append(flux * weight)
    fit = _build_fit(
        spectrum,
        variant="pyqsofit",
        continuum=tuple(continuum),
        calibration_confidence=0.55,
    )
    return ContinuumFit(
        variant=fit.variant,
        continuum=fit.continuum,
        residuals=fit.residuals,
        calibration_confidence=fit.calibration_confidence,
        fit_model_id=f"pyqsofit:{spectrum.calibration_state}:fallback_no_backend",
    )


def _ensure_resource_root() -> Path:
    root = Path(__file__).resolve().parents[3] / "artifacts" / "runtime" / "pyqsofit"
    root.mkdir(parents=True, exist_ok=True)
    target = root / "qsopar.fits"
    if not target.exists():
        with urllib.request.urlopen(_QSOPAR_URL, timeout=30) as response:
            target.write_bytes(response.read())
    package_root = root / "package"
    package_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, package_root / "qsopar.fits")
    return package_root


def _error_scale(spectrum: ProcessedSpectrum) -> float:
    amplitude = max(spectrum.flux) - min(spectrum.flux)
    return max(amplitude * 0.05, 1e-6)
