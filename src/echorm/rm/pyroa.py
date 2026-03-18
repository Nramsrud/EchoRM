"""PyROA-style adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun
from .posteriors import ConvergenceDiagnostics, PosteriorSummary


@dataclass(frozen=True, slots=True)
class PyroaConfig:
    """Configuration for a PyROA-style fit."""

    chain_length: int = 3000
    walkers: int = 32


def run_pyroa(
    *,
    object_uid: str,
    pair_id: str,
    driver_channel: str,
    response_channel: str,
    posterior: PosteriorSummary,
    diagnostics: ConvergenceDiagnostics,
    config: PyroaConfig | None = None,
) -> LagRun:
    """Wrap a posterior summary as a PyROA-style lag result."""
    config = config or PyroaConfig()
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver_channel,
        response_channel=response_channel,
        method="pyroa",
        lag_median=posterior.median,
        lag_lo=posterior.lower,
        lag_hi=posterior.upper,
        significance=1.0 if diagnostics.passed else 0.4,
        alias_score=0.15,
        quality_score=0.93 if diagnostics.passed else 0.55,
        diagnostics={
            "posterior_path": posterior.posterior_path,
            "latent_driver": posterior.latent_driver,
            "r_hat": diagnostics.r_hat,
            "effective_sample_size": diagnostics.effective_sample_size,
            "multi_light_curve_context": True,
        },
        runtime_metadata={
            "config": {
                "chain_length": config.chain_length,
                "walkers": config.walkers,
            }
        },
    )
