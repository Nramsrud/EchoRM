"""Synthetic continuum generators."""

from __future__ import annotations

import random


def generate_random_walk_continuum(*, seed: int, length: int) -> tuple[float, ...]:
    """Generate a deterministic random-walk continuum."""
    rng = random.Random(seed)
    values = [0.0]
    for _ in range(length - 1):
        values.append(values[-1] + rng.uniform(-0.5, 0.5))
    minimum = min(values)
    return tuple(value - minimum + 0.1 for value in values)
