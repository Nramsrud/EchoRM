"""MICA2-style transfer-function adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun
from .posteriors import ConvergenceDiagnostics, PosteriorSummary


@dataclass(frozen=True, slots=True)
class Mica2Config:
    """Configuration for a MICA2-style run."""

    transfer_family: str = "gaussian"
    component_count: int = 2


def run_mica2(
    *,
    object_uid: str,
    pair_id: str,
    driver_channel: str,
    response_channel: str,
    posterior: PosteriorSummary,
    diagnostics: ConvergenceDiagnostics,
    config: Mica2Config | None = None,
) -> LagRun:
    """Wrap a posterior summary as a MICA2-style lag result."""
    config = config or Mica2Config()
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver_channel,
        response_channel=response_channel,
        method="mica2",
        lag_median=posterior.median,
        lag_lo=posterior.lower,
        lag_hi=posterior.upper,
        significance=1.0 if diagnostics.passed else 0.45,
        alias_score=0.07,
        quality_score=0.96 if diagnostics.passed else 0.57,
        diagnostics={
            "posterior_path": posterior.posterior_path,
            "latent_driver": posterior.latent_driver,
            "r_hat": diagnostics.r_hat,
            "effective_sample_size": diagnostics.effective_sample_size,
            "backend_mode": "surrogate_contract",
            "evidence_level": "tracked_wrapper",
            "transfer_family": config.transfer_family,
            "component_count": config.component_count,
        },
        runtime_metadata={
            "config": {
                "transfer_family": config.transfer_family,
                "component_count": config.component_count,
            }
        },
    )
