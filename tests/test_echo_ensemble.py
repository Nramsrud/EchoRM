from __future__ import annotations

from echorm.schemas import SONIFICATION_SCHEMA
from echorm.sonify.base import MappingConfig, RenderInput
from echorm.sonify.echo_ensemble import build_echo_ensemble
from echorm.sonify.render import build_sonification_manifest


def test_echo_ensemble_is_deterministic_and_preserves_uncertainty_mode() -> None:
    config = MappingConfig(
        mapping_family="echo_ensemble",
        normalization_mode="science",
        uncertainty_mode="amplitude_wobble",
        sample_rate_hz=10,
        time_scale=2.0,
    )
    render_input = RenderInput(
        object_uid="ngc5548",
        driver_channel="continuum",
        response_channel="hbeta",
        driver_values=(0.1, 1.0, 0.2),
        response_values=(0.0, 0.2, 0.9),
        delay_steps=2,
        line_width=0.4,
        asymmetry=0.1,
        strength=0.8,
    )
    first = build_echo_ensemble(render_input, config=config)
    second = build_echo_ensemble(render_input, config=config)

    assert first.event_steps == second.event_steps
    assert "amplitude_wobble" in first.event_steps[1]


def test_sonification_manifest_is_canonical() -> None:
    config = MappingConfig(
        mapping_family="echo_ensemble",
        normalization_mode="science",
        uncertainty_mode="timbre_spread",
        sample_rate_hz=20,
        time_scale=1.5,
    )
    render_input = RenderInput(
        object_uid="ngc5548",
        driver_channel="continuum",
        response_channel="hbeta",
        driver_values=(0.1, 1.0, 0.2),
        response_values=(0.0, 0.2, 0.9),
        delay_steps=2,
        line_width=0.4,
        asymmetry=0.1,
        strength=0.8,
    )
    plan = build_echo_ensemble(render_input, config=config)
    manifest = build_sonification_manifest(
        plan=plan,
        sonification_id="ngc5548-echo-001",
        audio_path="audio/ngc5548-echo-001.wav",
    )

    assert SONIFICATION_SCHEMA.validate_record(manifest) == ()
    assert manifest["mapping_family"] == "echo_ensemble"
    assert manifest["uncertainty_mode"] == "timbre_spread"
