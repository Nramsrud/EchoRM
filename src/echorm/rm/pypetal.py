"""pyPETaL-style orchestration adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun
from .posteriors import ConvergenceDiagnostics, PosteriorSummary


@dataclass(frozen=True, slots=True)
class PypetalConfig:
    """Configuration for a pyPETaL-style orchestration run."""

    detrending: str = "median_filter"
    alias_weighting: str = "enabled"
    outlier_rejection: str = "mad_clip"


def run_pypetal(
    *,
    object_uid: str,
    pair_id: str,
    driver_channel: str,
    response_channel: str,
    posterior: PosteriorSummary,
    diagnostics: ConvergenceDiagnostics,
    config: PypetalConfig | None = None,
) -> LagRun:
    """Wrap a posterior summary as a pyPETaL-style lag result."""
    config = config or PypetalConfig()
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver_channel,
        response_channel=response_channel,
        method="pypetal",
        lag_median=posterior.median,
        lag_lo=posterior.lower,
        lag_hi=posterior.upper,
        significance=1.0 if diagnostics.passed else 0.55,
        alias_score=0.08,
        quality_score=0.97 if diagnostics.passed else 0.62,
        diagnostics={
            "posterior_path": posterior.posterior_path,
            "latent_driver": posterior.latent_driver,
            "r_hat": diagnostics.r_hat,
            "effective_sample_size": diagnostics.effective_sample_size,
            "backend_mode": "surrogate_contract",
            "evidence_level": "tracked_wrapper",
        },
        runtime_metadata={
            "config": {
                "detrending": config.detrending,
                "alias_weighting": config.alias_weighting,
                "outlier_rejection": config.outlier_rejection,
            }
        },
    )
