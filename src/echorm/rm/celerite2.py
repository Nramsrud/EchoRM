"""celerite2-style GP baseline adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun
from .posteriors import ConvergenceDiagnostics, PosteriorSummary


@dataclass(frozen=True, slots=True)
class Celerite2Config:
    """Configuration for a celerite2-style run."""

    kernel_family: str = "matern32"
    solver_mode: str = "jax_like"


def run_celerite2(
    *,
    object_uid: str,
    pair_id: str,
    driver_channel: str,
    response_channel: str,
    posterior: PosteriorSummary,
    diagnostics: ConvergenceDiagnostics,
    config: Celerite2Config | None = None,
) -> LagRun:
    """Wrap a posterior summary as a celerite2-style lag result."""
    config = config or Celerite2Config()
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver_channel,
        response_channel=response_channel,
        method="celerite2",
        lag_median=posterior.median,
        lag_lo=posterior.lower,
        lag_hi=posterior.upper,
        significance=1.0 if diagnostics.passed else 0.42,
        alias_score=0.06,
        quality_score=0.95 if diagnostics.passed else 0.59,
        diagnostics={
            "posterior_path": posterior.posterior_path,
            "latent_driver": posterior.latent_driver,
            "r_hat": diagnostics.r_hat,
            "effective_sample_size": diagnostics.effective_sample_size,
            "backend_mode": "surrogate_contract",
            "evidence_level": "tracked_wrapper",
            "kernel_family": config.kernel_family,
        },
        runtime_metadata={
            "config": {
                "kernel_family": config.kernel_family,
                "solver_mode": config.solver_mode,
            }
        },
    )
