from __future__ import annotations

from echorm.reports.render_bundle import build_render_bundle
from echorm.sonify.base import SUPPORTED_FAMILIES, MappingConfig, RenderInput
from echorm.sonify.direct_audification import build_direct_audification
from echorm.sonify.echo_ensemble import build_echo_ensemble
from echorm.sonify.render import build_sonification_manifest
from echorm.sonify.token_stream import build_token_stream


def _render_input() -> RenderInput:
    return RenderInput(
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


def test_mapping_families_share_the_same_core_contract() -> None:
    render_input = _render_input()
    echo_plan = build_echo_ensemble(
        render_input,
        config=MappingConfig("echo_ensemble", "science", "amplitude_wobble", 20, 1.0),
    )
    direct_plan = build_direct_audification(
        render_input,
        config=MappingConfig(
            "direct_audification",
            "science",
            "amplitude_wobble",
            20,
            1.0,
        ),
    )
    token_plan = build_token_stream(
        render_input,
        config=MappingConfig("token_stream", "science", "amplitude_wobble", 20, 1.0),
    )

    assert SUPPORTED_FAMILIES == (
        "echo_ensemble",
        "direct_audification",
        "token_stream",
    )
    assert (
        echo_plan.input_channels
        == direct_plan.input_channels
        == token_plan.input_channels
    )
    assert (
        echo_plan.config.time_scale
        == direct_plan.config.time_scale
        == token_plan.config.time_scale
    )


def test_render_bundle_is_complete_and_provenance_aware() -> None:
    render_input = _render_input()
    manifests = (
        build_sonification_manifest(
            plan=build_echo_ensemble(
                render_input,
                config=MappingConfig(
                    "echo_ensemble",
                    "science",
                    "timbre_spread",
                    20,
                    1.0,
                ),
            ),
            sonification_id="ngc5548-echo",
            audio_path="audio/ngc5548-echo.wav",
        ),
        build_sonification_manifest(
            plan=build_direct_audification(
                render_input,
                config=MappingConfig(
                    "direct_audification",
                    "science",
                    "timbre_spread",
                    20,
                    1.0,
                ),
            ),
            sonification_id="ngc5548-direct",
            audio_path="audio/ngc5548-direct.wav",
        ),
        build_sonification_manifest(
            plan=build_token_stream(
                render_input,
                config=MappingConfig(
                    "token_stream",
                    "science",
                    "timbre_spread",
                    20,
                    1.0,
                ),
            ),
            sonification_id="ngc5548-token",
            audio_path="audio/ngc5548-token.wav",
        ),
    )
    bundle = build_render_bundle(object_uid="ngc5548", manifests=manifests)

    stems_text = str(bundle["audio_stems"])
    provenance_text = str(bundle["provenance_records"])
    assert "ngc5548-echo.wav" in stems_text
    assert "ngc5548-direct.wav" in stems_text
    assert "ngc5548-token.wav" in stems_text
    assert str(bundle["visualization_path"]) == "reports/ngc5548/timeline.svg"
    assert provenance_text.count("sonification_id") == 3
