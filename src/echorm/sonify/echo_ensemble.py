"""Echo-ensemble mapping family."""

from __future__ import annotations

from .base import MappingConfig, RenderInput, SonificationPlan
from .uncertainty import encode_uncertainty


def build_echo_ensemble(
    render_input: RenderInput,
    *,
    config: MappingConfig,
) -> SonificationPlan:
    """Map driver and delayed response channels into deterministic events."""
    event_steps = []
    for index, (driver, response) in enumerate(
        zip(render_input.driver_values, render_input.response_values, strict=False)
    ):
        base_event = {
            "time_index": float(index),
            "driver_level": driver,
            "response_level": response,
            "delay_index": float(index + render_input.delay_steps),
            "brightness": render_input.line_width,
            "pan": render_input.asymmetry,
            "strength": render_input.strength,
        }
        base_event.update(
            encode_uncertainty(
                uncertainty_mode=config.uncertainty_mode,
                uncertainty_value=abs(driver - response),
            )
        )
        event_steps.append(base_event)
    return SonificationPlan(
        object_uid=render_input.object_uid,
        config=config,
        input_channels=(render_input.driver_channel, render_input.response_channel),
        event_steps=tuple(event_steps),
    )
