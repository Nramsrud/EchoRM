"""EzTao-style DRW and CARMA simulation adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun
from .posteriors import ConvergenceDiagnostics, PosteriorSummary


@dataclass(frozen=True, slots=True)
class EztaoConfig:
    """Configuration for an EzTao-style run."""

    process_family: str = "drw"
    simulation_grid: int = 128


def run_eztao(
    *,
    object_uid: str,
    pair_id: str,
    driver_channel: str,
    response_channel: str,
    posterior: PosteriorSummary,
    diagnostics: ConvergenceDiagnostics,
    config: EztaoConfig | None = None,
) -> LagRun:
    """Wrap a posterior summary as an EzTao-style lag result."""
    config = config or EztaoConfig()
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver_channel,
        response_channel=response_channel,
        method="eztao",
        lag_median=posterior.median,
        lag_lo=posterior.lower,
        lag_hi=posterior.upper,
        significance=1.0 if diagnostics.passed else 0.4,
        alias_score=0.09,
        quality_score=0.94 if diagnostics.passed else 0.56,
        diagnostics={
            "posterior_path": posterior.posterior_path,
            "latent_driver": posterior.latent_driver,
            "r_hat": diagnostics.r_hat,
            "effective_sample_size": diagnostics.effective_sample_size,
            "backend_mode": "surrogate_contract",
            "evidence_level": "tracked_wrapper",
            "process_family": config.process_family,
        },
        runtime_metadata={
            "config": {
                "process_family": config.process_family,
                "simulation_grid": config.simulation_grid,
            }
        },
    )
