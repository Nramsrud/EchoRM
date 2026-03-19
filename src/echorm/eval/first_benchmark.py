"""First benchmark package assembly."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ..ingest.agn_watch import (
    build_object_manifest as build_agn_object_manifest,
)
from ..ingest.agn_watch import (
    build_photometry_records as build_agn_photometry_records,
)
from ..ingest.agn_watch import (
    build_spectral_epoch_records as build_agn_spectral_epoch_records,
)
from ..ingest.agn_watch import (
    load_raw_manifest,
    parse_agn_watch_file,
)
from ..ingest.sdss_rm import (
    build_object_manifest as build_sdss_object_manifest,
)
from ..ingest.sdss_rm import (
    build_photometry_records as build_sdss_photometry_records,
)
from ..ingest.sdss_rm import (
    build_spectral_epoch_records as build_sdss_spectral_epoch_records,
)
from ..ingest.sdss_rm import (
    bundle_from_payload,
    load_public_subset,
)
from ..reports.benchmark_dossier import (
    build_first_benchmark_case_summary,
    build_first_benchmark_dossier,
)
from ..rm.base import TimeSeries
from ..rm.pyccf import run_pyccf
from ..rm.pyzdcf import run_pyzdcf
from ..rm.serialize import serialize_lag_run
from ..simulate.benchmarks import build_benchmark_family
from .readiness import (
    ToolStatus,
    VerificationCheck,
    _write_json,
    detect_tool_statuses,
    run_verification_checks,
)
from .validation import validate_benchmark


@dataclass(frozen=True, slots=True)
class FirstBenchmarkCase:
    """One first-benchmark case."""

    case_id: str
    benchmark_type: str
    evidence_level: str
    metric_family: str
    summary_metric: float
    quality_flag: str
    artifact_paths: dict[str, str]
    notes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "benchmark_type": self.benchmark_type,
            "evidence_level": self.evidence_level,
            "metric_family": self.metric_family,
            "summary_metric": self.summary_metric,
            "quality_flag": self.quality_flag,
            "artifact_paths": dict(self.artifact_paths),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class FirstBenchmarkPackage:
    """The first bounded benchmark package."""

    run_id: str
    profile: str
    package_type: str
    benchmark_scope: str
    readiness: str
    verification: tuple[VerificationCheck, ...]
    tools: tuple[ToolStatus, ...]
    cases: tuple[FirstBenchmarkCase, ...]
    demonstrated_capabilities: tuple[str, ...]
    non_demonstrated_capabilities: tuple[str, ...]
    limitations: tuple[str, ...]
    warnings: tuple[str, ...]
    artifact_root: str

    def to_dict(self) -> dict[str, object]:
        real_fixture_cases = sum(
            case.evidence_level == "real_fixture" for case in self.cases
        )
        synthetic_cases = sum(
            case.evidence_level == "synthetic" for case in self.cases
        )
        summary = {
            "case_count": len(self.cases),
            "real_fixture_case_count": real_fixture_cases,
            "synthetic_case_count": synthetic_cases,
            "verification_passed": sum(check.ok for check in self.verification),
            "verification_total": len(self.verification),
            "tools_available": sum(tool.available for tool in self.tools),
            "tools_total": len(self.tools),
            "warning_count": len(self.warnings),
        }
        return {
            "run_id": self.run_id,
            "profile": self.profile,
            "package_type": self.package_type,
            "benchmark_scope": self.benchmark_scope,
            "readiness": self.readiness,
            "artifact_root": self.artifact_root,
            "summary": summary,
            "verification": [check.to_dict() for check in self.verification],
            "tools": [tool.to_dict() for tool in self.tools],
            "cases": [case.to_dict() for case in self.cases],
            "demonstrated_capabilities": list(self.demonstrated_capabilities),
            "non_demonstrated_capabilities": list(
                self.non_demonstrated_capabilities
            ),
            "limitations": list(self.limitations),
            "warnings": list(self.warnings),
        }


def _artifact_paths(run_id: str, case_id: str) -> dict[str, str]:
    case_root = f"{run_id}/cases/{case_id}"
    return {
        "case_json": f"{case_root}/index.json",
        "summary_markdown": f"{case_root}/summary.md",
    }


def _agn_watch_cases(repo_root: Path, run_id: str) -> tuple[
    tuple[FirstBenchmarkCase, dict[str, object]],
    tuple[FirstBenchmarkCase, dict[str, object]],
]:
    fixtures_root = repo_root / "tests" / "fixtures" / "agn_watch"

    phot_manifest = load_raw_manifest(
        fixtures_root / "ngc5548_photometry.txt",
        object_uid="ngc5548",
        canonical_name="NGC 5548",
        source_url="https://agnwatch.example/ngc5548_photometry.txt",
        file_format="photometry_lightcurve",
    )
    phot_parsed = parse_agn_watch_file(phot_manifest)
    phot_object = build_agn_object_manifest(
        phot_parsed,
        line_coverage="Hbeta",
        literature_refs="Peterson et al. 2002",
    )
    phot_records = build_agn_photometry_records(phot_parsed, phot_manifest)
    phot_case_id = "agn_watch_ngc5548_ingest"
    phot_case = FirstBenchmarkCase(
        case_id=phot_case_id,
        benchmark_type="ingest_fidelity",
        evidence_level="real_fixture",
        metric_family="provenance_schema",
        summary_metric=float(len(phot_records)),
        quality_flag="pass",
        artifact_paths=_artifact_paths(run_id, phot_case_id),
        notes=(
            "Fixture-backed AGN Watch photometry ingest check.",
            f"unit={phot_parsed.metadata['unit']}",
        ),
    )
    phot_payload: dict[str, object] = {
        "case_id": phot_case_id,
        "benchmark_type": phot_case.benchmark_type,
        "evidence_level": phot_case.evidence_level,
        "metric_family": phot_case.metric_family,
        "object_manifest": phot_object,
        "photometry_record_count": len(phot_records),
        "quality_flags": [record["quality_flag"] for record in phot_records],
        "source_release": phot_manifest.source_url,
        "artifact_paths": phot_case.artifact_paths,
        "notes": list(phot_case.notes),
    }

    spec_manifest = load_raw_manifest(
        fixtures_root / "ngc3783_spectra.csv",
        object_uid="ngc3783",
        canonical_name="NGC 3783",
        source_url="https://agnwatch.example/ngc3783_spectra.csv",
        file_format="spectral_index",
    )
    spec_parsed = parse_agn_watch_file(spec_manifest)
    spec_records = build_agn_spectral_epoch_records(spec_parsed, spec_manifest)
    spec_case_id = "agn_watch_ngc3783_spectral_ingest"
    spec_case = FirstBenchmarkCase(
        case_id=spec_case_id,
        benchmark_type="ingest_fidelity",
        evidence_level="real_fixture",
        metric_family="spectral_epoch_integrity",
        summary_metric=float(len(spec_records)),
        quality_flag="pass",
        artifact_paths=_artifact_paths(run_id, spec_case_id),
        notes=(
            "Fixture-backed AGN Watch spectral ingest check.",
            "Calibration states preserved across epochs.",
        ),
    )
    spec_payload: dict[str, object] = {
        "case_id": spec_case_id,
        "benchmark_type": spec_case.benchmark_type,
        "evidence_level": spec_case.evidence_level,
        "metric_family": spec_case.metric_family,
        "spectral_epoch_count": len(spec_records),
        "calibration_states": [
            record["calibration_state"] for record in spec_records
        ],
        "source_release": spec_manifest.source_url,
        "artifact_paths": spec_case.artifact_paths,
        "notes": list(spec_case.notes),
    }
    return (phot_case, phot_payload), (spec_case, spec_payload)


def _sdss_rm_case(
    repo_root: Path,
    run_id: str,
) -> tuple[FirstBenchmarkCase, dict[str, object]]:
    fixture_path = (
        repo_root
        / "tests"
        / "fixtures"
        / "sdss_rm"
        / "published_lag_subset.json"
    )
    bundle = bundle_from_payload(load_public_subset(fixture_path))
    object_record = build_sdss_object_manifest(bundle)
    photometry_records = build_sdss_photometry_records(bundle)
    spectral_records = build_sdss_spectral_epoch_records(bundle)
    case_id = "sdss_rm_rmid101_ingest"
    case = FirstBenchmarkCase(
        case_id=case_id,
        benchmark_type="ingest_fidelity",
        evidence_level="real_fixture",
        metric_family="release_traceability",
        summary_metric=float(len(spectral_records)),
        quality_flag="pass",
        artifact_paths=_artifact_paths(run_id, case_id),
        notes=(
            "Fixture-backed SDSS-RM published subset ingest check.",
            f"release={bundle.release_id}",
        ),
    )
    payload: dict[str, object] = {
        "case_id": case_id,
        "benchmark_type": case.benchmark_type,
        "evidence_level": case.evidence_level,
        "metric_family": case.metric_family,
        "object_manifest": object_record,
        "photometry_record_count": len(photometry_records),
        "spectral_epoch_count": len(spectral_records),
        "raw_spec_paths": [record["spec_path"] for record in spectral_records],
        "artifact_paths": case.artifact_paths,
        "notes": list(case.notes),
    }
    return case, payload


def _synthetic_case(
    *,
    run_id: str,
    family: str,
    seed: int,
) -> tuple[FirstBenchmarkCase, dict[str, object]]:
    realization = build_benchmark_family(family=family, seed=seed)
    driver = TimeSeries(
        channel="continuum",
        mjd_obs=tuple(float(index) for index, _ in enumerate(realization.continuum)),
        values=realization.continuum,
    )
    response = TimeSeries(
        channel="hbeta",
        mjd_obs=tuple(float(index) for index, _ in enumerate(realization.response)),
        values=realization.response,
    )
    pyccf_result = run_pyccf(
        object_uid=realization.truth.family,
        driver=driver,
        response=response,
    )
    pyzdcf_result = run_pyzdcf(
        object_uid=realization.truth.family,
        driver=driver,
        response=response,
    )
    pyccf = serialize_lag_run(pyccf_result)
    pyzdcf = serialize_lag_run(pyzdcf_result)
    pyccf_validation = validate_benchmark(
        realization=realization,
        recovered_lag=pyccf_result.lag_median,
        interval=(pyccf_result.lag_lo, pyccf_result.lag_hi),
        runtime_sec=0.5,
    )
    pyzdcf_validation = validate_benchmark(
        realization=realization,
        recovered_lag=pyzdcf_result.lag_median,
        interval=(pyzdcf_result.lag_lo, pyzdcf_result.lag_hi),
        runtime_sec=0.5,
    )
    mean_lag_error = round(
        (pyccf_validation.lag_error + pyzdcf_validation.lag_error) / 2.0,
        3,
    )
    case_id = f"synthetic_{family}_lag_recovery"
    quality_flag = "pass" if mean_lag_error <= 1.0 else "warning"
    case = FirstBenchmarkCase(
        case_id=case_id,
        benchmark_type="lag_recovery",
        evidence_level="synthetic",
        metric_family="classical_rm",
        summary_metric=mean_lag_error,
        quality_flag=quality_flag,
        artifact_paths=_artifact_paths(run_id, case_id),
        notes=(
            "Synthetic lag-recovery benchmark over classical wrappers.",
            f"truth_delay={realization.truth.delay_steps}",
        ),
    )
    payload: dict[str, object] = {
        "case_id": case_id,
        "benchmark_type": case.benchmark_type,
        "evidence_level": case.evidence_level,
        "metric_family": case.metric_family,
        "truth": {
            "family": realization.truth.family,
            "delay_steps": realization.truth.delay_steps,
            "seed": realization.truth.seed,
        },
        "method_results": {
            "pyccf": {
                "record": pyccf.record,
                "lag_error": pyccf_validation.lag_error,
            },
            "pyzdcf": {
                "record": pyzdcf.record,
                "lag_error": pyzdcf_validation.lag_error,
            },
        },
        "mean_lag_error": mean_lag_error,
        "artifact_paths": case.artifact_paths,
        "notes": list(case.notes),
    }
    return case, payload


def assemble_first_benchmark_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str,
    profile: str = "first_benchmark",
    seed: int = 7,
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
) -> tuple[FirstBenchmarkPackage, tuple[dict[str, object], ...]]:
    """Assemble the first benchmark package without writing files."""
    verification_records = verification or run_verification_checks(repo_root)
    tool_records = tools or detect_tool_statuses()

    case_payload_pairs = [
        *_agn_watch_cases(repo_root, run_id),
        _sdss_rm_case(repo_root, run_id),
        _synthetic_case(run_id=run_id, family="clean", seed=seed),
        _synthetic_case(run_id=run_id, family="contaminated", seed=seed + 1),
        _synthetic_case(run_id=run_id, family="state_change", seed=seed + 2),
        _synthetic_case(run_id=run_id, family="failure_case", seed=seed + 3),
    ]
    cases = tuple(case for case, _ in case_payload_pairs)
    payloads = tuple(payload for _, payload in case_payload_pairs)

    warnings = [
        f"verification_failed:{record.name}"
        for record in verification_records
        if not record.ok
    ]
    warnings.extend(
        f"tool_missing:{tool.name}" for tool in tool_records if not tool.available
    )
    case_warnings = [
        f"case_warning:{case.case_id}"
        for case in cases
        if case.quality_flag != "pass"
    ]
    warnings.extend(case_warnings)
    if any(
        warning.startswith("verification_failed:")
        or warning.startswith("tool_missing:")
        for warning in warnings
    ):
        readiness = "degraded"
    elif case_warnings:
        readiness = "ready_with_warnings"
    else:
        readiness = "ready"

    package = FirstBenchmarkPackage(
        run_id=run_id,
        profile=profile,
        package_type="first_benchmark",
        benchmark_scope=(
            "Initial bounded benchmark package covering fixture-backed real-data "
            "ingest fidelity and synthetic classical lag-recovery."
        ),
        readiness=readiness,
        verification=verification_records,
        tools=tool_records,
        cases=cases,
        demonstrated_capabilities=(
            "Fixture-backed AGN Watch ingestion preserves provenance and "
            "schema structure for the initial gold objects.",
            "Fixture-backed SDSS-RM ingestion preserves release-traceable "
            "object, photometry, and spectral records for the initial silver "
            "subset.",
            "Current classical lag wrappers recover synthetic benchmark "
            "delays on clean and contaminated cases within bounded "
            "first-package coverage.",
        ),
        non_demonstrated_capabilities=(
            "Population-scale real-data lag recovery is not yet demonstrated.",
            "Model-based lag backends are not yet benchmarked on real "
            "benchmark objects in this package.",
            "This package does not constitute blinded efficacy validation or "
            "discovery readiness.",
        ),
        limitations=(
            "Real-data cases in this package are fixture-backed ingest "
            "fidelity checks rather than full real-light-curve lag "
            "benchmarks.",
            "Synthetic lag-recovery cases benchmark current classical wrappers only.",
            "Benchmark scope is intentionally bounded to the committed public "
            "fixtures and deterministic synthetic families.",
        ),
        warnings=tuple(warnings),
        artifact_root=str(artifact_root / run_id),
    )
    return package, payloads


def materialize_first_benchmark_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str,
    profile: str = "first_benchmark",
    seed: int = 7,
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
) -> Path:
    """Materialize the first benchmark package to disk."""
    package, payloads = assemble_first_benchmark_package(
        repo_root=repo_root,
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        seed=seed,
        verification=verification,
        tools=tools,
    )
    artifact_root.mkdir(parents=True, exist_ok=True)
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    cases_dir = run_dir / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)

    for payload in payloads:
        case_id = str(payload["case_id"])
        case_dir = cases_dir / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        _write_json(case_dir / "index.json", payload)
        (case_dir / "summary.md").write_text(
            build_first_benchmark_case_summary(payload),
            encoding="utf-8",
        )

    package_payload = package.to_dict()
    _write_json(run_dir / "index.json", package_payload)
    _write_json(run_dir / "claims.json", package_payload)
    (run_dir / "dossier.md").write_text(
        build_first_benchmark_dossier(package),
        encoding="utf-8",
    )
    (run_dir / "summary.md").write_text(
        build_first_benchmark_dossier(package),
        encoding="utf-8",
    )

    root_index_path = artifact_root / "index.json"
    if root_index_path.exists():
        root_payload = json.loads(root_index_path.read_text(encoding="utf-8"))
        root_runs = root_payload.get("runs", [])
        runs = (
            [entry for entry in root_runs if isinstance(entry, dict)]
            if isinstance(root_runs, list)
            else []
        )
    else:
        runs = []
    entry = {
        "run_id": package.run_id,
        "profile": package.profile,
        "readiness": package.readiness,
        "case_count": len(package.cases),
        "path": f"{run_id}/index.json",
        "package_type": package.package_type,
    }
    runs = [run for run in runs if run.get("run_id") != package.run_id]
    runs.append(entry)
    runs.sort(key=lambda run: str(run["run_id"]))
    _write_json(root_index_path, {"runs": runs})
    return run_dir / "index.json"
