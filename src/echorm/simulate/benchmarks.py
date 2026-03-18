"""Benchmark-family builders."""

from __future__ import annotations

from dataclasses import dataclass

from ..schemas import LAG_RESULT_SCHEMA
from ..sonify.base import MappingConfig, RenderInput
from ..sonify.echo_ensemble import build_echo_ensemble
from ..sonify.render import build_sonification_manifest
from .continuum import generate_random_walk_continuum
from .injections import apply_contamination, apply_failure_gap, apply_state_change
from .transfer import apply_delta_transfer, apply_top_hat_transfer


@dataclass(frozen=True, slots=True)
class BenchmarkTruth:
    """Immutable truth parameters for one benchmark realization."""

    family: str
    seed: int
    delay_steps: int
    contamination_level: float
    state_change_factor: float


@dataclass(frozen=True, slots=True)
class BenchmarkRealization:
    """Linked benchmark outputs for validation and sonification."""

    truth: BenchmarkTruth
    continuum: tuple[float, ...]
    response: tuple[float, ...]
    lag_record: dict[str, object]
    sonification_manifest: dict[str, object]
    annotations: dict[str, object]
    evaluation_score: float


def build_benchmark_family(*, family: str, seed: int) -> BenchmarkRealization:
    """Build one deterministic benchmark realization."""
    continuum = generate_random_walk_continuum(seed=seed, length=8)
    delay_steps = 2
    contamination_level = 0.0
    state_change_factor = 1.0
    if family == "clean":
        response = apply_delta_transfer(continuum, delay_steps=delay_steps)
    elif family == "contaminated":
        contamination_level = 0.3
        response = apply_contamination(
            apply_top_hat_transfer(continuum, delay_steps=delay_steps, width=2),
            level=contamination_level,
        )
    elif family == "state_change":
        state_change_factor = 0.6
        response = apply_state_change(
            apply_delta_transfer(continuum, delay_steps=delay_steps),
            split_index=4,
            factor=state_change_factor,
        )
    elif family == "failure_case":
        response = apply_failure_gap(
            apply_delta_transfer(continuum, delay_steps=delay_steps),
            gap_index=4,
        )
    else:
        raise ValueError(f"unsupported benchmark family: {family}")
    truth = BenchmarkTruth(
        family=family,
        seed=seed,
        delay_steps=delay_steps,
        contamination_level=contamination_level,
        state_change_factor=state_change_factor,
    )
    lag_record = LAG_RESULT_SCHEMA.ordered_record(
        {
            "object_uid": f"benchmark-{family}",
            "pair_id": "continuum->hbeta",
            "driver_channel": "continuum",
            "response_channel": "hbeta",
            "method": "truth",
            "lag_median": float(delay_steps),
            "lag_lo": float(delay_steps),
            "lag_hi": float(delay_steps),
            "significance": 1.0,
            "alias_score": 0.0,
            "quality_score": 1.0,
            "posterior_path": "",
            "method_config_hash": f"family={family}|seed={seed}",
        }
    )
    plan = build_echo_ensemble(
        RenderInput(
            object_uid=f"benchmark-{family}",
            driver_channel="continuum",
            response_channel="hbeta",
            driver_values=continuum,
            response_values=response,
            delay_steps=delay_steps,
            line_width=0.4,
            asymmetry=0.0,
            strength=0.8,
        ),
        config=MappingConfig("echo_ensemble", "science", "amplitude_wobble", 20, 1.0),
    )
    sonification_manifest = build_sonification_manifest(
        plan=plan,
        sonification_id=f"benchmark-{family}-{seed}",
        audio_path=f"audio/benchmark-{family}-{seed}.wav",
    )
    return BenchmarkRealization(
        truth=truth,
        continuum=continuum,
        response=response,
        lag_record=lag_record,
        sonification_manifest=sonification_manifest,
        annotations={"family": family, "seed": seed},
        evaluation_score=1.0 if family != "failure_case" else 0.3,
    )
