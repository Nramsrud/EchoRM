from __future__ import annotations

from pathlib import Path

from echorm.ingest.sdss_rm import (
    build_acquisition_plan,
    build_object_manifest,
    build_photometry_records,
    build_spectral_epoch_records,
    bundle_from_payload,
    load_public_subset,
)
from echorm.schemas import (
    OBJECT_MANIFEST_SCHEMA,
    PHOTOMETRY_SCHEMA,
    SPECTRAL_EPOCH_SCHEMA,
)

FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "sdss_rm"
    / "published_lag_subset.json"
)


def test_acquisition_plan_preserves_release_and_target_subset() -> None:
    plan = build_acquisition_plan(
        release_id="sdssrm-dr16",
        catalog_url="https://sdss.example/dr16/published-lag-subset",
        raw_root="raw/sdssrm/dr16",
        object_uids=("sdssrm-101",),
    )
    assert plan.release_id == "sdssrm-dr16"
    assert plan.object_uids == ("sdssrm-101",)


def test_bundle_normalization_preserves_release_and_aliases() -> None:
    payload = load_public_subset(FIXTURE)
    bundle = bundle_from_payload(payload)
    object_record = build_object_manifest(bundle)

    assert OBJECT_MANIFEST_SCHEMA.validate_record(object_record) == ()
    assert "RMID101" in str(object_record["survey_ids"])
    assert str(object_record["literature_refs"]) == "Grier et al. 2017"


def test_raw_spectral_assets_remain_separate_from_derived_products() -> None:
    payload = load_public_subset(FIXTURE)
    bundle = bundle_from_payload(payload)
    spectral_records = build_spectral_epoch_records(bundle)
    photometry_records = build_photometry_records(bundle)

    assert SPECTRAL_EPOCH_SCHEMA.validate_record(spectral_records[0]) == ()
    assert PHOTOMETRY_SCHEMA.validate_record(photometry_records[0]) == ()
    assert str(spectral_records[0]["spec_path"]).startswith("raw/")
    assert str(photometry_records[0]["source_release"]) == bundle.release_id
