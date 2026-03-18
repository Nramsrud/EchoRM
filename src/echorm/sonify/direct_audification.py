"""Direct-audification mapping family."""

from __future__ import annotations

from .base import MappingConfig, RenderInput, SonificationPlan
from .uncertainty import encode_uncertainty


def build_direct_audification(
    render_input: RenderInput,
    *,
    config: MappingConfig,
) -> SonificationPlan:
    """Map raw driver-response values directly into amplitude events."""
    event_steps = []
    for index, (driver, response) in enumerate(
        zip(render_input.driver_values, render_input.response_values, strict=False)
    ):
        event = {
            "time_index": float(index),
            "driver_level": driver,
            "response_level": response,
            "mix": (driver + response) / 2.0,
            "contrast": abs(driver - response),
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
