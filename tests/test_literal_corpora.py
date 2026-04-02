from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from echorm.eval.benchmark_corpus import BenchmarkObject
from echorm.eval.literal_corpora import (
    _download_ztf_lightcurve,
    _read_ztf_rows,
    _select_discovery_state_alignment,
    build_interpolated_series,
    build_measured_series,
)


def _benchmark_object() -> BenchmarkObject:
    object_manifest = {
        "object_uid": "test-object",
        "canonical_name": "Test Object",
        "redshift": 0.01,
    }
    photometry_records = (
        {
            "mjd_obs": 1.00,
            "flux": 10.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 2.00,
            "flux": 20.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 3.00,
            "flux": 30.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 4.00,
            "flux": 40.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 5.00,
            "flux": 50.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 6.00,
            "flux": 60.0,
            "normalization_mode": "raw",
        },
    )
    response_records = (
        {
            "mjd_obs": 1.08,
            "flux": 100.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 2.04,
            "flux": 110.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 3.11,
            "flux": 120.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 4.07,
            "flux": 130.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 5.02,
            "flux": 140.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 6.04,
            "flux": 150.0,
            "normalization_mode": "raw",
        },
    )
    return BenchmarkObject(
        object_uid="test-object",
        canonical_name="Test Object",
        tier="gold",
        evidence_level="test",
        object_manifest=object_manifest,
        photometry_records=photometry_records,
        response_records=response_records,
        spectral_epoch_records=(),
        literature_lag_day=2.0,
        line_name="Hbeta",
        benchmark_regime="test",
        notes=(),
    )


def test_build_measured_series_matches_nearest_response_points() -> None:
    pair = build_measured_series(_benchmark_object())

    assert pair.response_evidence_level == "real_measured_response"
    assert pair.mjd_obs == (1.04, 2.02, 3.055, 4.035, 5.01, 6.02)
    assert pair.driver_values == (10.0, 20.0, 30.0, 40.0, 50.0, 60.0)
    assert pair.response_values == (100.0, 110.0, 120.0, 130.0, 140.0, 150.0)


def test_build_interpolated_series_interpolates_onto_continuum_cadence() -> None:
    pair = build_interpolated_series(_benchmark_object())

    assert pair.response_evidence_level == "real_interpolated_response"
    assert pair.mjd_obs == (2.0, 3.0, 4.0, 5.0, 6.0)
    assert pair.driver_values == (20.0, 30.0, 40.0, 50.0, 60.0)
    assert pair.response_values == pytest.approx(
        (
            109.58333333333333,
            118.97196261682244,
            129.27083333333334,
            139.78947368421052,
            149.60784313725492,
        )
    )


def test_ztf_download_falls_back_to_offline_rows_on_timeout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise_timeout(*args: object, **kwargs: object) -> object:
        raise TimeoutError("simulated timeout")

    monkeypatch.setattr("urllib.request.urlopen", _raise_timeout)

    raw_path, used_offline_fallback = _download_ztf_lightcurve(
        tmp_path,
        object_uid="ci-fallback-target",
        ra_deg=214.0,
        dec_deg=53.0,
        fallback_split_mjd=59000.0,
    )

    rows = _read_ztf_rows(raw_path)

    assert used_offline_fallback is True
    assert raw_path.exists()
    assert len(rows) == 8
    assert min(float(str(row["mjd"])) for row in rows) < 59000.0
    assert max(float(str(row["mjd"])) for row in rows) > 59000.0


def test_discovery_alignment_prefers_supported_changing_state_pair() -> None:
    state_rows = [
        {
            "state": "A",
            "mjd": 10,
            "zspec": 0.1,
            "l5100": 1.0,
            "lhb": 2.0,
            "lmgii": 3.0,
        },
        {
            "state": "B",
            "mjd": 20,
            "zspec": 0.1,
            "l5100": 1.1,
            "lhb": 2.1,
            "lmgii": 3.1,
        },
        {
            "state": "C",
            "mjd": 30,
            "zspec": 0.1,
            "l5100": 1.2,
            "lhb": 2.2,
            "lmgii": 3.2,
        },
    ]
    raw_rows = [
        {"mjd": 12.0, "mag": 18.0, "magerr": 0.1, "filtercode": "zg"},
        {"mjd": 13.0, "mag": 18.1, "magerr": 0.1, "filtercode": "zr"},
        {"mjd": 18.0, "mag": 18.2, "magerr": 0.1, "filtercode": "zg"},
        {"mjd": 19.0, "mag": 18.3, "magerr": 0.1, "filtercode": "zr"},
        {"mjd": 22.0, "mag": 18.4, "magerr": 0.1, "filtercode": "zg"},
        {"mjd": 23.0, "mag": 18.5, "magerr": 0.1, "filtercode": "zr"},
        {"mjd": 26.0, "mag": 18.6, "magerr": 0.1, "filtercode": "zg"},
        {"mjd": 27.0, "mag": 18.7, "magerr": 0.1, "filtercode": "zr"},
        {"mjd": 28.0, "mag": 18.8, "magerr": 0.1, "filtercode": "zg"},
        {"mjd": 29.0, "mag": 18.9, "magerr": 0.1, "filtercode": "zr"},
    ]

    alignment = _select_discovery_state_alignment(state_rows, raw_rows)
    selected_pair = cast(dict[str, object], alignment["selected_pair"])
    pre_epoch = cast(dict[str, object], selected_pair["pre_epoch"])
    post_epoch = cast(dict[str, object], selected_pair["post_epoch"])

    assert alignment["alignment_eligible"] is True
    assert alignment["state_transition_supported"] is True
    assert alignment["alignment_status"] == "changing_state_supported"
    assert pre_epoch["mjd"] == 20
    assert post_epoch["mjd"] == 30
    assert selected_pair["support_score"] == 2


def test_discovery_alignment_falls_back_to_same_state_supported_pair() -> None:
    state_rows = [
        {
            "state": "A",
            "mjd": 10,
            "zspec": 0.1,
            "l5100": 1.0,
            "lhb": 2.0,
            "lmgii": 3.0,
        },
        {
            "state": "A",
            "mjd": 20,
            "zspec": 0.1,
            "l5100": 1.1,
            "lhb": 2.1,
            "lmgii": 3.1,
        },
        {
            "state": "B",
            "mjd": 30,
            "zspec": 0.1,
            "l5100": 1.2,
            "lhb": 2.2,
            "lmgii": 3.2,
        },
    ]
    raw_rows = [
        {"mjd": 12.0, "mag": 18.0, "magerr": 0.1, "filtercode": "zg"},
        {"mjd": 13.0, "mag": 18.1, "magerr": 0.1, "filtercode": "zr"},
        {"mjd": 18.0, "mag": 18.2, "magerr": 0.1, "filtercode": "zg"},
        {"mjd": 19.0, "mag": 18.3, "magerr": 0.1, "filtercode": "zr"},
    ]

    alignment = _select_discovery_state_alignment(state_rows, raw_rows)
    selected_pair = cast(dict[str, object], alignment["selected_pair"])
    pre_epoch = cast(dict[str, object], selected_pair["pre_epoch"])
    post_epoch = cast(dict[str, object], selected_pair["post_epoch"])

    assert alignment["alignment_eligible"] is True
    assert alignment["state_transition_supported"] is False
    assert alignment["alignment_status"] == "same_state_supported"
    assert alignment["state_transition_exclusion_reason"] == (
        "no_eligible_adjacent_changing_state_pair"
    )
    assert pre_epoch["mjd"] == 10
    assert post_epoch["mjd"] == 20
