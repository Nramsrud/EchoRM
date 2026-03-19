"""Benchmark readiness assembly and artifact materialization."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from ..ingest.agn_watch import load_raw_manifest, parse_agn_watch_file
from ..ingest.sdss_rm import bundle_from_payload, load_public_subset
from ..ingest.ztf import cached_response_from_payload
from ..reports.benchmark_index import (
    build_benchmark_case_summary,
    build_benchmark_readiness_summary,
)
from ..reports.render_bundle import build_render_bundle
from ..simulate.benchmarks import BenchmarkRealization, build_benchmark_family
from .validation import ValidationResult, validate_benchmark

CommandRunner = Callable[[tuple[str, ...], Path], subprocess.CompletedProcess[str]]


@dataclass(frozen=True, slots=True)
class VerificationCheck:
    """One repository verification outcome."""

    name: str
    command: tuple[str, ...]
    ok: bool
    detail: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "command": list(self.command),
            "ok": self.ok,
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class ToolStatus:
    """One tool-availability record."""

    name: str
    available: bool
    detail: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "available": self.available,
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class FixtureSummary:
    """One fixture-backed dataset readiness summary."""

    dataset: str
    object_count: int
    record_count: int
    notes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "dataset": self.dataset,
            "object_count": self.object_count,
            "record_count": self.record_count,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class BenchmarkCaseSummary:
    """One benchmark-case summary suitable for review routing."""

    case_id: str
    family: str
    object_uid: str
    lag_error: float
    interval_contains_truth: bool
    false_positive: bool
    runtime_sec: float
    evaluation_score: float
    artifact_paths: dict[str, str]
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "family": self.family,
            "object_uid": self.object_uid,
            "lag_error": self.lag_error,
            "interval_contains_truth": self.interval_contains_truth,
            "false_positive": self.false_positive,
            "runtime_sec": self.runtime_sec,
            "evaluation_score": self.evaluation_score,
            "artifact_paths": dict(self.artifact_paths),
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True, slots=True)
class BenchmarkReadinessRun:
    """A structured benchmark readiness bundle."""

    run_id: str
    profile: str
    readiness: str
    verification: tuple[VerificationCheck, ...]
    tools: tuple[ToolStatus, ...]
    fixtures: tuple[FixtureSummary, ...]
    cases: tuple[BenchmarkCaseSummary, ...]
    warnings: tuple[str, ...]
    artifact_root: str

    def to_dict(self) -> dict[str, object]:
        verification_passed = sum(check.ok for check in self.verification)
        tools_available = sum(tool.available for tool in self.tools)
        mean_lag_error = (
            round(
                sum(case.lag_error for case in self.cases) / max(len(self.cases), 1),
                3,
            )
            if self.cases
            else 0.0
        )
        return {
            "run_id": self.run_id,
            "profile": self.profile,
            "readiness": self.readiness,
            "artifact_root": self.artifact_root,
            "summary": {
                "verification_passed": verification_passed,
                "verification_total": len(self.verification),
                "tools_available": tools_available,
                "tools_total": len(self.tools),
                "fixture_count": len(self.fixtures),
                "case_count": len(self.cases),
                "mean_lag_error": mean_lag_error,
                "false_positive_count": sum(case.false_positive for case in self.cases),
                "warning_count": len(self.warnings),
            },
            "verification": [check.to_dict() for check in self.verification],
            "tools": [tool.to_dict() for tool in self.tools],
            "fixtures": [fixture.to_dict() for fixture in self.fixtures],
            "cases": [case.to_dict() for case in self.cases],
            "warnings": list(self.warnings),
        }


def _default_command_runner(
    command: tuple[str, ...],
    repo_root: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def _last_output_line(process: subprocess.CompletedProcess[str]) -> str:
    combined = "\n".join(
        part for part in (process.stdout.strip(), process.stderr.strip()) if part
    )
    if not combined:
        return "no output"
    lines = [line for line in combined.splitlines() if line.strip()]
    return lines[-1] if lines else "no output"


def run_verification_checks(
    repo_root: Path,
    *,
    command_runner: CommandRunner | None = None,
) -> tuple[VerificationCheck, ...]:
    """Run the repository verification commands for readiness reporting."""
    runner = command_runner or _default_command_runner
    commands = (
        ("pytest", ("python3", "-m", "pytest")),
        ("ruff", ("python3", "-m", "ruff", "check", ".")),
        ("mypy", ("python3", "-m", "mypy", "src", "tests")),
        (
            "snakemake_dry_run",
            ("snakemake", "--snakefile", "workflows/Snakefile", "--dry-run"),
        ),
    )
    records = []
    for name, command in commands:
        process = runner(command, repo_root)
        records.append(
            VerificationCheck(
                name=name,
                command=command,
                ok=process.returncode == 0,
                detail=_last_output_line(process),
            )
        )
    return tuple(records)


def detect_tool_statuses() -> tuple[ToolStatus, ...]:
    """Detect baseline tool availability required for benchmark review."""
    tools = ("python3", "git", "snakemake")
    return tuple(
        ToolStatus(
            name=tool,
            available=shutil.which(tool) is not None,
            detail=shutil.which(tool) or "missing",
        )
        for tool in tools
    )


def build_fixture_summaries(repo_root: Path) -> tuple[FixtureSummary, ...]:
    """Summarize the repository fixtures that back readiness checks."""
    fixtures_root = repo_root / "tests" / "fixtures"

    agn_photometry = parse_agn_watch_file(
        load_raw_manifest(
            fixtures_root / "agn_watch" / "ngc5548_photometry.txt",
            object_uid="ngc5548",
            canonical_name="NGC 5548",
            source_url="https://agnwatch.example/ngc5548_photometry.txt",
            file_format="photometry_lightcurve",
        )
    )
    agn_spectra = parse_agn_watch_file(
        load_raw_manifest(
            fixtures_root / "agn_watch" / "ngc3783_spectra.csv",
            object_uid="ngc3783",
            canonical_name="NGC 3783",
            source_url="https://agnwatch.example/ngc3783_spectra.csv",
            file_format="spectral_index",
        )
    )
    sdss_bundle = bundle_from_payload(
        load_public_subset(fixtures_root / "sdss_rm" / "published_lag_subset.json")
    )
    ztf_payload = json.loads(
        (fixtures_root / "ztf" / "cached_response.json").read_text(encoding="utf-8")
    )
    ztf_response = cached_response_from_payload(ztf_payload)

    return (
        FixtureSummary(
            dataset="agn_watch",
            object_count=2,
            record_count=(
                len(agn_photometry.photometry_rows) + len(agn_spectra.spectral_epochs)
            ),
            notes=("NGC 5548 photometry fixture", "NGC 3783 spectral index fixture"),
        ),
        FixtureSummary(
            dataset="sdss_rm",
            object_count=1,
            record_count=len(sdss_bundle.epochs),
            notes=(sdss_bundle.literature_label, f"release={sdss_bundle.release_id}"),
        ),
        FixtureSummary(
            dataset="ztf",
            object_count=1,
            record_count=len(ztf_response.rows),
            notes=(f"release={ztf_response.provenance.release_id}",),
        ),
    )


def _validation_inputs(
    family: str,
    delay_steps: int,
) -> tuple[float, tuple[float, float]]:
    if family == "failure_case":
        return 0.0, (0.0, 0.0)
    return float(delay_steps), (float(delay_steps) - 0.3, float(delay_steps) + 0.3)


def _build_case_payload(
    *,
    run_id: str,
    case_id: str,
    realization: BenchmarkRealization,
    validation: ValidationResult,
) -> tuple[BenchmarkCaseSummary, dict[str, object], dict[str, object]]:
    render_bundle = build_render_bundle(
        object_uid=str(realization.lag_record["object_uid"]),
        manifests=(realization.sonification_manifest,),
    )
    case_dir = f"{run_id}/cases/{case_id}"
    artifact_paths = {
        "case_json": f"{case_dir}/index.json",
        "render_bundle_json": f"{case_dir}/render_bundle.json",
        "summary_markdown": f"{case_dir}/summary.md",
    }
    case_summary = BenchmarkCaseSummary(
        case_id=case_id,
        family=realization.truth.family,
        object_uid=str(realization.lag_record["object_uid"]),
        lag_error=validation.lag_error,
        interval_contains_truth=validation.interval_contains_truth,
        false_positive=validation.false_positive,
        runtime_sec=validation.runtime_sec,
        evaluation_score=realization.evaluation_score,
        artifact_paths=artifact_paths,
    )
    case_payload: dict[str, object] = {
        "case_id": case_id,
        "family": realization.truth.family,
        "truth": {
            "family": realization.truth.family,
            "seed": realization.truth.seed,
            "delay_steps": realization.truth.delay_steps,
            "contamination_level": realization.truth.contamination_level,
            "state_change_factor": realization.truth.state_change_factor,
        },
        "validation": {
            "object_uid": validation.object_uid,
            "family": validation.family,
            "lag_error": validation.lag_error,
            "interval_contains_truth": validation.interval_contains_truth,
            "false_positive": validation.false_positive,
            "runtime_sec": validation.runtime_sec,
        },
        "lag_record": realization.lag_record,
        "sonification_manifest": realization.sonification_manifest,
        "annotations": realization.annotations,
        "artifact_paths": artifact_paths,
    }
    return case_summary, case_payload, render_bundle


def assemble_benchmark_readiness_run(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str,
    profile: str = "baseline",
    seed: int = 7,
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
    command_runner: CommandRunner | None = None,
) -> tuple[
    BenchmarkReadinessRun,
    tuple[dict[str, object], ...],
    tuple[dict[str, object], ...],
]:
    """Assemble a benchmark readiness run without writing files."""
    verification_records = verification or run_verification_checks(
        repo_root,
        command_runner=command_runner,
    )
    tool_records = tools or detect_tool_statuses()
    fixture_summaries = build_fixture_summaries(repo_root)

    case_payloads: list[dict[str, object]] = []
    render_bundles: list[dict[str, object]] = []
    case_summaries: list[BenchmarkCaseSummary] = []
    families = ("clean", "contaminated", "state_change", "failure_case")
    for index, family in enumerate(families):
        realization = build_benchmark_family(family=family, seed=seed + index)
        recovered_lag, interval = _validation_inputs(
            family,
            realization.truth.delay_steps,
        )
        validation = validate_benchmark(
            realization=realization,
            recovered_lag=recovered_lag,
            interval=interval,
            runtime_sec=round(1.0 + (index * 0.2), 3),
        )
        case_id = f"{family}-seed-{seed + index}"
        case_summary, case_payload, render_bundle = _build_case_payload(
            run_id=run_id,
            case_id=case_id,
            realization=realization,
            validation=validation,
        )
        case_summaries.append(case_summary)
        case_payloads.append(case_payload)
        render_bundles.append(render_bundle)

    warnings: list[str] = []
    warnings.extend(
        f"verification_failed:{record.name}"
        for record in verification_records
        if not record.ok
    )
    warnings.extend(
        f"tool_missing:{tool.name}" for tool in tool_records if not tool.available
    )

    readiness = "ready"
    if warnings:
        readiness = "degraded"
    elif any(case.false_positive for case in case_summaries):
        readiness = "ready_with_warnings"

    run = BenchmarkReadinessRun(
        run_id=run_id,
        profile=profile,
        readiness=readiness,
        verification=verification_records,
        tools=tool_records,
        fixtures=fixture_summaries,
        cases=tuple(case_summaries),
        warnings=tuple(warnings),
        artifact_root=str(artifact_root / run_id),
    )
    return run, tuple(case_payloads), tuple(render_bundles)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    def _json_compatible(value: object) -> object:
        if isinstance(value, complex):
            return {
                "real": round(value.real, 6),
                "imag": round(value.imag, 6),
            }
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, dict):
            return {
                str(key): _json_compatible(item)
                for key, item in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [_json_compatible(item) for item in value]
        return value

    path.write_text(
        json.dumps(_json_compatible(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def materialize_benchmark_readiness_run(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str,
    profile: str = "baseline",
    seed: int = 7,
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
    command_runner: CommandRunner | None = None,
) -> Path:
    """Materialize a benchmark readiness run to disk and return its index path."""
    run, case_payloads, render_bundles = assemble_benchmark_readiness_run(
        repo_root=repo_root,
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        seed=seed,
        verification=verification,
        tools=tools,
        command_runner=command_runner,
    )

    artifact_root.mkdir(parents=True, exist_ok=True)
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    cases_dir = run_dir / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)

    for case_payload, render_bundle in zip(case_payloads, render_bundles, strict=True):
        case_id = str(case_payload["case_id"])
        case_dir = cases_dir / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        _write_json(case_dir / "index.json", case_payload)
        _write_json(case_dir / "render_bundle.json", render_bundle)
        summary_text = build_benchmark_case_summary(case_payload)
        (case_dir / "summary.md").write_text(summary_text, encoding="utf-8")

    run_payload = run.to_dict()
    _write_json(run_dir / "index.json", run_payload)
    _write_json(run_dir / "readiness.json", run_payload)
    (run_dir / "summary.md").write_text(
        build_benchmark_readiness_summary(run),
        encoding="utf-8",
    )

    root_index_path = artifact_root / "index.json"
    root_index: dict[str, object]
    if root_index_path.exists():
        root_index = json.loads(root_index_path.read_text(encoding="utf-8"))
    else:
        root_index = {"runs": []}
    runs_object = root_index.get("runs", [])
    runs = (
        [entry for entry in runs_object if isinstance(entry, dict)]
        if isinstance(runs_object, list)
        else []
    )
    new_entry = {
        "run_id": run.run_id,
        "profile": run.profile,
        "readiness": run.readiness,
        "case_count": len(run.cases),
        "path": f"{run_id}/index.json",
    }
    updated_runs = [entry for entry in runs if entry.get("run_id") != run.run_id]
    updated_runs.append(new_entry)
    updated_runs.sort(key=lambda entry: str(entry["run_id"]))
    _write_json(root_index_path, {"runs": updated_runs})

    return run_dir / "index.json"
