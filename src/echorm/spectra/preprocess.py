"""Spectral preprocessing helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProcessedSpectrum:
    """A preprocessed spectrum in observed and rest-frame coordinates."""

    wavelength_obs: tuple[float, ...]
    wavelength_rest: tuple[float, ...]
    flux: tuple[float, ...]
    calibration_state: str


def preprocess_spectrum(
    *,
    wavelength_obs: tuple[float, ...],
    flux: tuple[float, ...],
    redshift: float,
    calibration_state: str,
    extinction_scale: float = 1.0,
) -> ProcessedSpectrum:
    """Validate a spectrum and convert it into rest-frame coordinates."""
    if len(wavelength_obs) != len(flux):
        raise ValueError("wavelength and flux arrays must have equal length")
    if tuple(sorted(wavelength_obs)) != wavelength_obs:
        raise ValueError("wavelength grid must be monotonic")
    wavelength_rest = tuple(wave / (1.0 + redshift) for wave in wavelength_obs)
    corrected_flux = tuple(value * extinction_scale for value in flux)
    return ProcessedSpectrum(
        wavelength_obs=wavelength_obs,
        wavelength_rest=wavelength_rest,
        flux=corrected_flux,
        calibration_state=calibration_state,
    )
