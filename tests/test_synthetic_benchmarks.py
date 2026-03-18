from __future__ import annotations

from echorm.schemas import LAG_RESULT_SCHEMA, SONIFICATION_SCHEMA
from echorm.simulate.benchmarks import build_benchmark_family


def test_benchmark_families_cover_required_scenarios() -> None:
    families = ("clean", "contaminated", "state_change", "failure_case")
    realizations = [
        build_benchmark_family(family=family, seed=7)
        for family in families
    ]

    assert {realization.truth.family for realization in realizations} == set(families)
    assert all(
        LAG_RESULT_SCHEMA.validate_record(realization.lag_record) == ()
        for realization in realizations
    )
    assert all(
        SONIFICATION_SCHEMA.validate_record(realization.sonification_manifest) == ()
        for realization in realizations
    )


def test_benchmark_generation_is_deterministic_for_fixed_seed() -> None:
    first = build_benchmark_family(family="contaminated", seed=11)
    second = build_benchmark_family(family="contaminated", seed=11)

    assert first.truth == second.truth
    assert first.continuum == second.continuum
    assert first.response == second.response
    assert first.sonification_manifest == second.sonification_manifest
