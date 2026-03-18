from __future__ import annotations

import json
from pathlib import Path

from echorm.ingest.ztf import (
    build_api_plan,
    build_bulk_plan,
    build_photometry_records,
    cached_response_from_payload,
)
from echorm.schemas import PHOTOMETRY_SCHEMA

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "ztf" / "cached_response.json"


def test_access_plans_support_api_and_bulk_modes() -> None:
    api_plan = build_api_plan(
        release_id="ztf-dr22",
        target_id="ztf-target-001",
        ra_deg=214.7341,
        dec_deg=53.4031,
        radius_arcsec=1.0,
        bad_flag_policy="drop-catflags-above-0",
        crossmatch_key="lsid-123",
    )
    bulk_plan = build_bulk_plan(
        release_id="ztf-dr22",
        target_id="ztf-target-001",
        parquet_uri="s3://ztf/dr22/lightcurves.parquet",
        filters={"field": 123},
        crossmatch_key="lsid-123",
    )

    assert api_plan.mode == "api"
    assert bulk_plan.mode == "bulk"
    assert bulk_plan.query["parquet_uri"] == "s3://ztf/dr22/lightcurves.parquet"


def test_cached_response_preserves_query_provenance() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    response = cached_response_from_payload(payload)

    assert response.provenance.release_id == "ztf-dr22"
    assert response.provenance.crossmatch_key == "lsid-123"
    assert response.provenance.query_params["radius_arcsec"] == 1.0


def test_normalization_preserves_quality_flags() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    response = cached_response_from_payload(payload)
    records = build_photometry_records(response)

    assert PHOTOMETRY_SCHEMA.validate_record(records[0]) == ()
    assert str(records[1]["quality_flag"]) == "catflags=1"
    assert str(records[0]["source_release"]) == "ztf-dr22"
