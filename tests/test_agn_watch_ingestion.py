from __future__ import annotations

from pathlib import Path

from echorm.ingest.agn_watch import (
    build_object_manifest,
    build_photometry_records,
    build_spectral_epoch_records,
    load_raw_manifest,
    parse_agn_watch_file,
)
from echorm.schemas import (
    OBJECT_MANIFEST_SCHEMA,
    PHOTOMETRY_SCHEMA,
    SPECTRAL_EPOCH_SCHEMA,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "agn_watch"


def test_lightcurve_parser_preserves_metadata_and_raw_text() -> None:
    manifest = load_raw_manifest(
        FIXTURES / "ngc5548_photometry.txt",
        object_uid="ngc5548",
        canonical_name="NGC 5548",
        source_url="https://agnwatch.example/ngc5548_photometry.txt",
        file_format="photometry_lightcurve",
    )
    parsed = parse_agn_watch_file(manifest)

    assert "# note: preserved legacy continuum comments" in manifest.raw_text
    assert parsed.metadata["unit"] == "mJy"
    assert parsed.photometry_rows[1].quality_flag == "review"


def test_lightcurve_normalization_builds_canonical_records() -> None:
    manifest = load_raw_manifest(
        FIXTURES / "ngc5548_photometry.txt",
        object_uid="ngc5548",
        canonical_name="NGC 5548",
        source_url="https://agnwatch.example/ngc5548_photometry.txt",
        file_format="photometry_lightcurve",
    )
    parsed = parse_agn_watch_file(manifest)

    object_record = build_object_manifest(
        parsed,
        line_coverage="Hbeta",
        literature_refs="Peterson et al. 2002",
    )
    photometry_records = build_photometry_records(parsed, manifest)

    assert OBJECT_MANIFEST_SCHEMA.validate_record(object_record) == ()
    assert PHOTOMETRY_SCHEMA.validate_record(photometry_records[0]) == ()
    assert object_record["tier"] == "gold"
    assert photometry_records[0]["source_release"] == manifest.source_url


def test_spectral_index_normalization_supports_second_gold_object() -> None:
    manifest = load_raw_manifest(
        FIXTURES / "ngc3783_spectra.csv",
        object_uid="ngc3783",
        canonical_name="NGC 3783",
        source_url="https://agnwatch.example/ngc3783_spectra.csv",
        file_format="spectral_index",
    )
    parsed = parse_agn_watch_file(manifest)
    spectral_records = build_spectral_epoch_records(parsed, manifest)

    assert parsed.spectral_epochs[0].spec_path.endswith(".fits")
    assert SPECTRAL_EPOCH_SCHEMA.validate_record(spectral_records[0]) == ()
    assert spectral_records[1]["calibration_state"] == "recalibrated"
