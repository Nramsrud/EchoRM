"""Normalization transforms and metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NormalizedPhotometryPoint:
    """A normalized photometry point with explicit transform metadata."""

    mjd_obs: float
    raw_flux: float
    normalized_flux: float
    normalization_mode: str
    normalization_reference: str
    transform_hash: str


def science_normalize(
    samples: tuple[tuple[float, float], ...],
    *,
    reference_flux: float,
) -> tuple[NormalizedPhotometryPoint, ...]:
    """Build science-normalized points from raw flux samples."""
    transform_hash = f"science:{reference_flux:.6f}"
    return tuple(
        NormalizedPhotometryPoint(
            mjd_obs=mjd_obs,
            raw_flux=flux,
            normalized_flux=flux / reference_flux,
            normalization_mode="science",
            normalization_reference=f"reference_flux={reference_flux:.6f}",
            transform_hash=transform_hash,
        )
        for mjd_obs, flux in samples
    )


def sonification_normalize(
    samples: tuple[tuple[float, float], ...],
) -> tuple[NormalizedPhotometryPoint, ...]:
    """Build sonification-normalized points on a unit interval."""
    flux_values = [flux for _, flux in samples]
    flux_min = min(flux_values)
    flux_span = max(flux_values) - flux_min or 1.0
    transform_hash = f"sonification:{flux_min:.6f}:{flux_span:.6f}"
    return tuple(
        NormalizedPhotometryPoint(
            mjd_obs=mjd_obs,
            raw_flux=flux,
            normalized_flux=(flux - flux_min) / flux_span,
            normalization_mode="sonification",
            normalization_reference=f"min={flux_min:.6f};span={flux_span:.6f}",
            transform_hash=transform_hash,
        )
        for mjd_obs, flux in samples
    )
