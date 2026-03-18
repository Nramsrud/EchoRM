"""Contamination and complexity injections."""

from __future__ import annotations


def apply_contamination(
    values: tuple[float, ...],
    *,
    level: float,
) -> tuple[float, ...]:
    """Inject diffuse-continuum contamination."""
    return tuple(value + level for value in values)


def apply_state_change(
    values: tuple[float, ...],
    *,
    split_index: int,
    factor: float,
) -> tuple[float, ...]:
    """Inject a state change after a split index."""
    return tuple(
        value if index < split_index else value * factor
        for index, value in enumerate(values)
    )


def apply_failure_gap(
    values: tuple[float, ...],
    *,
    gap_index: int,
) -> tuple[float, ...]:
    """Inject a failure-case gap."""
    return tuple(
        value if index != gap_index else 0.0
        for index, value in enumerate(values)
    )
