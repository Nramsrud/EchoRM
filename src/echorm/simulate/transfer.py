"""Transfer-function families."""

from __future__ import annotations


def apply_delta_transfer(
    continuum: tuple[float, ...],
    *,
    delay_steps: int,
) -> tuple[float, ...]:
    """Apply a delta transfer function."""
    return tuple(
        continuum[index - delay_steps] if index >= delay_steps else 0.0
        for index in range(len(continuum))
    )


def apply_top_hat_transfer(
    continuum: tuple[float, ...],
    *,
    delay_steps: int,
    width: int,
) -> tuple[float, ...]:
    """Apply a top-hat transfer function."""
    response = []
    for index in range(len(continuum)):
        window = [
            continuum[offset]
            for offset in range(
                max(0, index - delay_steps - width + 1),
                index - delay_steps + 1,
            )
            if 0 <= offset < len(continuum)
        ]
        response.append(sum(window) / max(len(window), 1))
    return tuple(response)
