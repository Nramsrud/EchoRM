"""JAVELIN-style adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun
from .posteriors import ConvergenceDiagnostics, PosteriorSummary


@dataclass(frozen=True, slots=True)
class JavelinConfig:
    """Configuration for a JAVELIN-style fit."""

    chain_length: int = 2000
    burn_in: int = 500


def run_javelin(
    *,
    object_uid: str,
    pair_id: str,
    driver_channel: str,
    response_channel: str,
    posterior: PosteriorSummary,
    diagnostics: ConvergenceDiagnostics,
    config: JavelinConfig | None = None,
) -> LagRun:
    """Wrap a posterior summary as a JAVELIN-style lag result."""
    config = config or JavelinConfig()
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver_channel,
        response_channel=response_channel,
        method="javelin",
        lag_median=posterior.median,
        lag_lo=posterior.lower,
        lag_hi=posterior.upper,
        significance=1.0 if diagnostics.passed else 0.5,
        alias_score=0.1,
        quality_score=0.95 if diagnostics.passed else 0.6,
        diagnostics={
            "posterior_path": posterior.posterior_path,
            "latent_driver": posterior.latent_driver,
            "r_hat": diagnostics.r_hat,
            "effective_sample_size": diagnostics.effective_sample_size,
        },
        runtime_metadata={
            "config": {
                "chain_length": config.chain_length,
                "burn_in": config.burn_in,
            }
        },
    )
