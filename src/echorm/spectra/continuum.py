"""Continuum-subtraction variants."""

from __future__ import annotations

from dataclasses import dataclass

from .preprocess import ProcessedSpectrum


@dataclass(frozen=True, slots=True)
class ContinuumFit:
    """A continuum estimate and its residuals."""

    variant: str
    continuum: tuple[float, ...]
    residuals: tuple[float, ...]
    calibration_confidence: float
    fit_model_id: str


def _build_fit(
    spectrum: ProcessedSpectrum,
    *,
    variant: str,
    continuum: tuple[float, ...],
    calibration_confidence: float,
) -> ContinuumFit:
    residuals = tuple(
        flux - baseline
        for flux, baseline in zip(spectrum.flux, continuum, strict=False)
    )
    return ContinuumFit(
        variant=variant,
        continuum=continuum,
        residuals=residuals,
        calibration_confidence=calibration_confidence,
        fit_model_id=f"{variant}:{spectrum.calibration_state}",
    )


def fit_local_continuum(spectrum: ProcessedSpectrum) -> ContinuumFit:
    """Fit a flat local continuum."""
    baseline = sum(spectrum.flux) / len(spectrum.flux)
    continuum = tuple(baseline for _ in spectrum.flux)
    return _build_fit(
        spectrum,
        variant="local",
        continuum=continuum,
        calibration_confidence=0.9,
    )


def fit_pseudo_continuum(spectrum: ProcessedSpectrum) -> ContinuumFit:
    """Fit a moving-average pseudo-continuum."""
    continuum = []
    for index, _ in enumerate(spectrum.flux):
        neighbors = spectrum.flux[
            max(0, index - 1) : min(len(spectrum.flux), index + 2)
        ]
        continuum.append(sum(neighbors) / len(neighbors))
    return _build_fit(
        spectrum,
        variant="pseudo_continuum",
        continuum=tuple(continuum),
        calibration_confidence=0.8,
    )


def fit_full_decomposition(spectrum: ProcessedSpectrum) -> ContinuumFit:
    """Fit a simple sloped full-decomposition baseline."""
    start = spectrum.flux[0]
    stop = spectrum.flux[-1]
    step = (stop - start) / max(len(spectrum.flux) - 1, 1)
    continuum = tuple(start + index * step for index, _ in enumerate(spectrum.flux))
    return _build_fit(
        spectrum,
        variant="full_decomposition",
        continuum=continuum,
        calibration_confidence=0.85,
    )
