"""Feature-token mapping family."""

from __future__ import annotations

from .base import MappingConfig, RenderInput, SonificationPlan
from .uncertainty import encode_uncertainty


def build_token_stream(
    render_input: RenderInput,
    *,
    config: MappingConfig,
) -> SonificationPlan:
    """Compress response features into token-like event controls."""
    event_steps = []
    for index, (driver, response) in enumerate(
        zip(render_input.driver_values, render_input.response_values, strict=False)
    ):
        event = {
            "time_index": float(index),
            "token_pitch": driver * 10.0,
            "token_duration": max(response, 0.1),
            "token_accent": render_input.strength,
            "token_pan": render_input.asymmetry,
        }
        event.update(
            encode_uncertainty(
                uncertainty_mode=config.uncertainty_mode,
                uncertainty_value=abs(driver - response),
            )
        )
        event_steps.append(event)
    return SonificationPlan(
        object_uid=render_input.object_uid,
        config=config,
        input_channels=(render_input.driver_channel, render_input.response_channel),
        event_steps=tuple(event_steps),
    )
