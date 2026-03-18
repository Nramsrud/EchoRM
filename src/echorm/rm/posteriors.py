"""Posterior and convergence helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PosteriorSummary:
    """Posterior interval summary for a lag parameter."""

    samples: tuple[float, ...]
    median: float
    lower: float
    upper: float
    posterior_path: str
    latent_driver: str | None = None


@dataclass(frozen=True, slots=True)
class ConvergenceDiagnostics:
    """Minimal convergence diagnostics for a backend fit."""

    r_hat: float
    effective_sample_size: int
    passed: bool


def build_posterior_summary(
    *,
    samples: tuple[float, ...],
    posterior_path: str,
    latent_driver: str | None = None,
) -> PosteriorSummary:
    """Build a simple posterior interval summary."""
    ordered = sorted(samples)
    midpoint = len(ordered) // 2
    median = ordered[midpoint]
    lower = ordered[max(0, int(len(ordered) * 0.16) - 1)]
    upper = ordered[min(len(ordered) - 1, int(len(ordered) * 0.84))]
    return PosteriorSummary(
        samples=samples,
        median=median,
        lower=lower,
        upper=upper,
        posterior_path=posterior_path,
        latent_driver=latent_driver,
    )
