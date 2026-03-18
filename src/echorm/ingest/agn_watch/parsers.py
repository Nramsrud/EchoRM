"""Parser families for AGN Watch light curves and spectral indexes."""

from __future__ import annotations

from dataclasses import dataclass

from .manifests import RawSourceManifest


@dataclass(frozen=True, slots=True)
class ParsedPhotometryRow:
    """One AGN Watch photometry sample."""

    mjd_obs: float
    flux: float
    flux_err: float
    quality_flag: str


@dataclass(frozen=True, slots=True)
class ParsedSpectralEpoch:
    """One AGN Watch spectral epoch index row."""

    epoch_uid: str
    mjd_obs: float
    wave_min: float
    wave_max: float
    median_snr: float
    calibration_state: str
    spec_path: str


@dataclass(frozen=True, slots=True)
class ParsedAgnWatchFile:
    """Parsed AGN Watch content plus preserved metadata."""

    object_uid: str
    canonical_name: str
    file_format: str
    metadata: dict[str, str]
    comments: tuple[str, ...]
    photometry_rows: tuple[ParsedPhotometryRow, ...] = ()
    spectral_epochs: tuple[ParsedSpectralEpoch, ...] = ()


def _parse_metadata(text: str) -> tuple[dict[str, str], tuple[str, ...], list[str]]:
    metadata: dict[str, str] = {}
    comments: list[str] = []
    data_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            comment = line[1:].strip()
            comments.append(comment)
            if ":" in comment:
                key, value = comment.split(":", 1)
                metadata[key.strip().lower()] = value.strip()
            continue
        data_lines.append(line)
    return metadata, tuple(comments), data_lines


def _parse_lightcurve_rows(lines: list[str]) -> tuple[ParsedPhotometryRow, ...]:
    rows: list[ParsedPhotometryRow] = []
    for line in lines:
        mjd_obs, flux, flux_err, quality_flag = line.split()
        rows.append(
            ParsedPhotometryRow(
                mjd_obs=float(mjd_obs),
                flux=float(flux),
                flux_err=float(flux_err),
                quality_flag=quality_flag,
            )
        )
    return tuple(rows)


def _parse_spectral_rows(lines: list[str]) -> tuple[ParsedSpectralEpoch, ...]:
    header = lines[0].split(",")
    expected_header = [
        "epoch_uid",
        "mjd_obs",
        "wave_min",
        "wave_max",
        "median_snr",
        "calibration_state",
        "spec_path",
    ]
    if header != expected_header:
        raise ValueError("unsupported AGN Watch spectral header")
    rows: list[ParsedSpectralEpoch] = []
    for line in lines[1:]:
        (
            epoch_uid,
            mjd_obs,
            wave_min,
            wave_max,
            median_snr,
            calibration_state,
            spec_path,
        ) = line.split(",")
        rows.append(
            ParsedSpectralEpoch(
                epoch_uid=epoch_uid,
                mjd_obs=float(mjd_obs),
                wave_min=float(wave_min),
                wave_max=float(wave_max),
                median_snr=float(median_snr),
                calibration_state=calibration_state,
                spec_path=spec_path,
            )
        )
    return tuple(rows)


def parse_agn_watch_file(manifest: RawSourceManifest) -> ParsedAgnWatchFile:
    """Dispatch to the supported AGN Watch parser family."""
    metadata, comments, data_lines = _parse_metadata(manifest.raw_text)
    if manifest.file_format == "photometry_lightcurve":
        return ParsedAgnWatchFile(
            object_uid=manifest.object_uid,
            canonical_name=manifest.canonical_name,
            file_format=manifest.file_format,
            metadata=metadata,
            comments=comments,
            photometry_rows=_parse_lightcurve_rows(data_lines),
        )
    if manifest.file_format == "spectral_index":
        return ParsedAgnWatchFile(
            object_uid=manifest.object_uid,
            canonical_name=manifest.canonical_name,
            file_format=manifest.file_format,
            metadata=metadata,
            comments=comments,
            spectral_epochs=_parse_spectral_rows(data_lines),
        )
    raise ValueError(f"unsupported AGN Watch format: {manifest.file_format}")
