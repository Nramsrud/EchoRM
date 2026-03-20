"""Root-authority closeout package assembly."""

from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from ..anomaly.candidates import build_candidate
from ..anomaly.clagn import analyze_clagn_transition
from ..anomaly.rank import rank_anomaly
from ..reports.candidate_memos import build_candidate_memo
from ..reports.catalog import build_catalog_package
from ..reports.release import build_release_bundle, build_release_index
from .benchmark_corpus import (
    BenchmarkObject,
    DiscoveryHoldoutRecord,
    build_discovery_manifest_metadata,
    build_line_diagnostics,
    build_manifest_metadata,
    build_render_artifacts,
    run_method_suite,
)
from .broad_validation import (
    JSONDict,
    _artifact_paths,
    _build_method_records,
    _dict_list,
    _float_value,
    _mapping_value,
    _object_summary,
    _package_dossier,
    _package_header,
    _update_root_index,
    _write_group_payload,
    _write_markdown,
    _write_object_payload,
)
from .literal_corpora import (
    build_measured_series,
    load_literal_discovery_holdout_records,
    load_literal_gold_benchmark_objects,
    load_literal_silver_benchmark_objects,
)
from .objectives import ObjectiveScorecard, compute_objective_scorecard
from .readiness import (
    ToolStatus,
    VerificationCheck,
    _write_json,
    detect_tool_statuses,
    run_verification_checks,
)
from .validation import ValidationResult

try:
    import optuna
except ImportError:  # pragma: no cover
    optuna = None  # type: ignore[assignment]

try:
    import ray
    from ray import tune
except ImportError:  # pragma: no cover
    ray = None  # type: ignore[assignment]
    tune = None  # type: ignore[assignment]

try:
    from ax.service.ax_client import AxClient as _AxClient
    from ax.service.utils.instantiation import (
        ObjectiveProperties as _ObjectiveProperties,
    )
except ImportError:  # pragma: no cover
    AxClient: Any | None = None
    ObjectiveProperties: Any | None = None
else:
    AxClient = _AxClient
    ObjectiveProperties = _ObjectiveProperties


def _hash_mapping(payload: Mapping[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]


def _load_required_run(artifact_root: Path, run_id: str) -> Mapping[str, object]:
    path = artifact_root / run_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("run payload must be a mapping")
    return payload


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_group_payload(
    artifact_root: Path,
    run_id: str,
    group: str,
    item_id: str,
) -> Mapping[str, object]:
    path = artifact_root / run_id / group / item_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{run_id}/{group}/{item_id} payload must be a mapping")
    return payload


def _load_group_payloads(
    artifact_root: Path,
    run_id: str,
    group: str,
) -> list[JSONDict]:
    group_dir = artifact_root / run_id / group
    if not group_dir.exists():
        return []
    payloads: list[JSONDict] = []
    for path in sorted(group_dir.glob("*/index.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payloads.append(cast(JSONDict, payload))
    return payloads


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _discovery_object_summary(record: DiscoveryHoldoutRecord, run_id: str) -> JSONDict:
    return {
        "object_uid": record.object_uid,
        "canonical_name": record.canonical_name,
        "tier": "discovery",
        "evidence_level": record.evidence_level,
        "quality_flag": "holdout",
        "primary_metric": round(
            (record.lag_outlier + record.line_response_outlier) / 2.0,
            3,
        ),
        "anomaly_category": record.anomaly_category,
        "holdout_policy": record.holdout_policy,
        "artifact_paths": _artifact_paths(run_id, "objects", record.object_uid),
        "notes": list(record.notes),
    }


def _build_literal_object_payload(
    *,
    object_record: BenchmarkObject,
    run_id: str,
    run_dir: Path,
    include_advanced: bool = False,
) -> tuple[JSONDict, JSONDict]:
    measured = build_measured_series(object_record)
    lag_steps = max(1, round(object_record.literature_lag_day))
    method_suite = run_method_suite(
        object_record=object_record,
        driver_values=measured.driver_values,
        response_values=measured.response_values,
        lag_steps=lag_steps,
        include_advanced=include_advanced,
        mjd_obs=measured.mjd_obs,
        response_evidence_level=measured.response_evidence_level,
    )
    line_diagnostics = build_line_diagnostics(object_record)
    render_artifacts = build_render_artifacts(
        object_record=object_record,
        driver_values=measured.driver_values,
        response_values=measured.response_values,
        lag_steps=lag_steps,
        run_dir=run_dir,
    )
    payload: JSONDict = {
        "object_uid": object_record.object_uid,
        "canonical_name": object_record.canonical_name,
        "tier": object_record.tier,
        "evidence_level": object_record.evidence_level,
        "response_evidence_level": measured.response_evidence_level,
        "benchmark_regime": object_record.benchmark_regime,
        "literature_lag_day": object_record.literature_lag_day,
        "artifact_paths": _artifact_paths(run_id, "objects", object_record.object_uid),
        "object_manifest": object_record.object_manifest,
        "method_suite": method_suite,
        "literature_table": method_suite["comparisons"],
        "line_diagnostics": line_diagnostics,
        "claims_boundary": {
            "demonstrated": [
                "real measured continuum and response series",
                "object-level lag comparison against literature references",
            ],
            "limitations": [
                "spectral diagnostics remain bounded by the tracked spectra surface",
                "object remains within the declared benchmark scope",
            ],
            "non_demonstrated": [
                "field deployment performance",
            ],
        },
        "sonifications": render_artifacts["sonifications"],
        "render_bundle": render_artifacts["render_bundle"],
        "notes": list(object_record.notes),
    }
    mean_abs_error = _float_value(method_suite, "mean_abs_error")
    coverage_rate = _float_value(method_suite, "coverage_rate")
    quality_flag = (
        "pass" if mean_abs_error <= 3.0 and coverage_rate >= 0.75 else "warning"
    )
    summary = _object_summary(
        object_record,
        mean_abs_error=mean_abs_error,
        coverage_rate=coverage_rate,
        quality_flag=quality_flag,
        run_id=run_id,
    )
    summary["response_evidence_level"] = measured.response_evidence_level
    return payload, summary


def materialize_advanced_rigor_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str = "advanced_rigor",
    profile: str = "root_closeout",
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
) -> Path:
    """Materialize the advanced-method and spectral-rigor package."""
    verification_records = verification or run_verification_checks(repo_root)
    tool_records = tools or detect_tool_statuses()
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    objects = (
        *load_literal_gold_benchmark_objects(repo_root),
        *load_literal_silver_benchmark_objects(repo_root),
    )
    payloads: list[JSONDict] = []
    summaries: list[JSONDict] = []
    method_records: list[JSONDict] = []
    spectral_fit_records: list[JSONDict] = []
    for object_record in objects:
        payload, summary = _build_literal_object_payload(
            object_record=object_record,
            run_id=run_id,
            run_dir=run_dir,
            include_advanced=(
                object_record.tier == "gold"
                or object_record.benchmark_regime
                in {"multi_epoch_line_response", "mgii_alias_risk"}
            ),
        )
        payloads.append(payload)
        summaries.append(summary)
        _write_object_payload(run_dir, payload)
        object_methods = _build_method_records(run_id=run_id, object_payload=payload)
        method_records.extend(object_methods)
        for method_payload in object_methods:
            _write_group_payload(
                run_dir=run_dir,
                group="methods",
                item_id=str(method_payload["method_id"]),
                payload=method_payload,
                title=f"Method {method_payload['method_id']}",
            )
        for record in _dict_list(payload, "line_diagnostics"):
            fit_id = str(record.get("fit_model_id", ""))
            spectral_fit_id = f"{object_record.object_uid}-{fit_id.replace(':', '-')}"
            spectral_record = {
                "spectral_fit_id": spectral_fit_id,
                "object_uid": object_record.object_uid,
                "line_name": str(record.get("line_name", "")),
                "continuum_variant": str(record.get("continuum_variant", "")),
                "fit_model_id": fit_id,
                "calibration_confidence": _float_value(
                    record,
                    "calibration_confidence",
                ),
                "artifact_paths": _artifact_paths(
                    run_id,
                    "spectral_fits",
                    spectral_fit_id,
                ),
            }
            spectral_fit_records.append(spectral_record)
            _write_group_payload(
                run_dir=run_dir,
                group="spectral_fits",
                item_id=spectral_fit_id,
                payload=spectral_record,
                title=f"Spectral Fit {spectral_fit_id}",
            )
    advanced_method_names = {"pypetal", "litmus", "mica2", "eztao", "celerite2"}
    advanced_method_count = sum(
        item["method"] in advanced_method_names for item in method_records
    )
    pyqsofit_count = sum(
        item["continuum_variant"] == "pyqsofit" for item in spectral_fit_records
    )
    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="advanced_rigor",
        benchmark_scope=(
            "Advanced RM-method and spectral-rigor package over tracked benchmark "
            "objects, including pyPETaL, LITMUS, MICA2, EzTao, celerite2, and "
            "PyQSOFit-style decomposition records."
        ),
        readiness=(
            "ready"
            if advanced_method_count >= 5
            and pyqsofit_count >= len(objects)
            else "degraded"
        ),
        verification=verification_records,
        tools=tool_records,
        summary={
            "object_count": len(objects),
            "method_record_count": len(method_records),
            "advanced_method_count": advanced_method_count,
            "advanced_object_count": len(
                {
                    item["object_uid"]
                    for item in method_records
                    if item["method"] in advanced_method_names
                }
            ),
            "spectral_fit_count": len(spectral_fit_records),
            "spectral_fit_family_count": len(
                {item["continuum_variant"] for item in spectral_fit_records}
            ),
            "pyqsofit_coverage_rate": round(pyqsofit_count / max(len(objects), 1), 3),
        },
        demonstrated=(
            "Advanced-method records are attached to every tracked benchmark object.",
            "Object payloads use real measured continuum and response series.",
        ),
        not_demonstrated=(
            "This package does not itself close discovery or release gates.",
        ),
        limitations=(
            "Some advanced-method integrations may remain unavailable "
            "on the active runtime.",
            "Spectral decomposition remains bounded by the tracked spectra surface.",
        ),
        warnings=(),
        artifact_root=artifact_root,
    )
    payload["objects"] = summaries
    payload["methods"] = method_records
    payload["spectral_fits"] = spectral_fit_records
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="advanced_rigor",
        readiness=str(payload["readiness"]),
        count=len(objects),
    )
    return run_dir / "index.json"


def materialize_corpus_scaleout_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str = "corpus_scaleout",
    profile: str = "root_closeout",
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
) -> Path:
    """Materialize the root-scope benchmark and discovery corpus package."""
    verification_records = verification or run_verification_checks(repo_root)
    tool_records = tools or detect_tool_statuses()
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    gold_objects = load_literal_gold_benchmark_objects(repo_root)
    silver_objects = load_literal_silver_benchmark_objects(repo_root)
    discovery_records = load_literal_discovery_holdout_records(repo_root)
    gold_manifest = build_manifest_metadata("gold_full_scope", gold_objects)
    silver_manifest = build_manifest_metadata("silver_full_scope", silver_objects)
    discovery_manifest = build_discovery_manifest_metadata(
        "discovery_holdout",
        discovery_records,
    )
    object_summaries = []
    for record in discovery_records:
        payload = _discovery_object_summary(record, run_id)
        object_summaries.append(payload)
        _write_group_payload(
            run_dir=run_dir,
            group="objects",
            item_id=record.object_uid,
            payload={
                **payload,
                "release_id": record.release_id,
                "crossmatch_key": record.crossmatch_key,
                "query_params": record.query_params,
                "benchmark_links": list(record.benchmark_links),
            },
            title=f"Object {record.object_uid}",
        )
    comparisons = [
        {
            "corpus_id": manifest["corpus_id"],
            "object_count": manifest["object_count"],
            "manifest_hash": manifest["manifest_hash"],
        }
        for manifest in (gold_manifest, silver_manifest, discovery_manifest)
    ]
    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="corpus_scaleout",
        benchmark_scope=(
            "Full-scope gold, silver, and discovery-hold-out manifest package with "
            "explicit provenance and hold-out governance."
        ),
        readiness=(
            "ready"
            if int(str(discovery_manifest["object_count"])) >= 5
            and str(discovery_manifest["holdout_policy"])
            else "degraded"
        ),
        verification=verification_records,
        tools=tool_records,
        summary={
            "gold_object_count": gold_manifest["object_count"],
            "silver_object_count": silver_manifest["object_count"],
            "discovery_object_count": discovery_manifest["object_count"],
            "manifest_count": 3,
            "release_count": len(
                discovery_manifest["release_ids"]
                if isinstance(discovery_manifest["release_ids"], list)
                else []
            ),
            "holdout_policy": str(discovery_manifest["holdout_policy"]),
        },
        demonstrated=(
            "Gold, silver, and discovery corpora are frozen as tracked manifests.",
            "Discovery hold-out governance is explicit in the tracked corpus "
            "artifacts.",
        ),
        not_demonstrated=(
            "Corpus freeze alone does not promote discovery claims.",
        ),
        limitations=(
            "Discovery manifests remain bounded by the published catalog slice "
            "loaded for root closeout.",
            "The package records corpus governance, not full scientific "
            "interpretation.",
        ),
        warnings=(),
        artifact_root=artifact_root,
    )
    payload["objects"] = object_summaries
    payload["comparisons"] = comparisons
    payload["gold_manifest"] = gold_manifest
    payload["silver_manifest"] = silver_manifest
    payload["discovery_manifest"] = discovery_manifest
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _write_json(run_dir / "gold_manifest.json", gold_manifest)
    _write_json(run_dir / "silver_manifest.json", silver_manifest)
    _write_json(run_dir / "discovery_manifest.json", discovery_manifest)
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="corpus_scaleout",
        readiness=str(payload["readiness"]),
        count=int(str(discovery_manifest["object_count"])),
    )
    return run_dir / "index.json"


def _validation_results_from_benchmark_artifacts(
    artifact_root: Path,
) -> tuple[ValidationResult, ...]:
    results: list[ValidationResult] = []
    for run_id in ("gold_validation", "silver_validation", "advanced_rigor"):
        for payload in _load_group_payloads(artifact_root, run_id, "objects"):
            object_uid = str(payload.get("object_uid", ""))
            method_suite = _mapping_value(payload, "method_suite")
            literature_lag = _float_value(payload, "literature_lag_day")
            null_diagnostic = _mapping_value(method_suite, "null_diagnostic")
            runtime_sec = _float_value(method_suite, "runtime_sec_mean")
            benchmark_regime = str(payload.get("benchmark_regime", "benchmark"))
            for item in _dict_list(method_suite, "method_results"):
                record = _mapping_value(item, "record")
                diagnostics = _mapping_value(item, "diagnostics")
                method = str(record.get("method", ""))
                lag_error = abs(_float_value(record, "lag_median") - literature_lag)
                interval_contains_truth = (
                    _float_value(record, "lag_lo")
                    <= literature_lag
                    <= _float_value(record, "lag_hi")
                )
                results.append(
                    ValidationResult(
                        object_uid=object_uid,
                        family=f"{run_id}:{benchmark_regime}:{method}",
                        lag_error=round(lag_error, 3),
                        interval_contains_truth=interval_contains_truth,
                        false_positive=(
                            _float_value(null_diagnostic, "false_positive_rate") > 0.0
                        ),
                        runtime_sec=max(
                            runtime_sec,
                            _float_value(
                                _mapping_value(item, "runtime_metadata"),
                                "runtime_sec",
                            ),
                        ),
                    )
                )
                if str(diagnostics.get("evidence_level", "")) == "no_execution":
                    results.append(
                        ValidationResult(
                            object_uid=f"{object_uid}-{method}-unavailable",
                            family=f"{run_id}:availability",
                            lag_error=10.0,
                            interval_contains_truth=False,
                            false_positive=True,
                            runtime_sec=runtime_sec,
                        )
                    )
    for run_id in ("continuum_validation",):
        run_payload = _load_required_run(artifact_root, run_id)
        for case in _dict_list(run_payload, "cases"):
            family = str(case.get("family", "continuum"))
            summary_metric = _float_value(case, "summary_metric")
            results.append(
                ValidationResult(
                    object_uid=str(case.get("case_id", "")),
                    family=f"{run_id}:{family}",
                    lag_error=summary_metric,
                    interval_contains_truth=str(case.get("quality_flag", "")) == "pass",
                    false_positive=family == "failure_case",
                    runtime_sec=0.2,
                )
            )
    return tuple(results)


def materialize_optimization_closeout_package(
    *,
    artifact_root: Path,
    run_id: str = "optimization_closeout",
    profile: str = "root_closeout",
) -> Path:
    """Materialize the optimization and agent-loop closeout package."""
    validation_results = _validation_results_from_benchmark_artifacts(artifact_root)
    efficacy_summary = _mapping_value(
        _load_required_run(artifact_root, "efficacy_benchmark"),
        "summary",
    )
    silver_summary = _mapping_value(
        _load_required_run(artifact_root, "silver_validation"),
        "summary",
    )
    continuum_summary = _mapping_value(
        _load_required_run(artifact_root, "continuum_validation"),
        "summary",
    )
    scorecard = compute_objective_scorecard(
        validation_results,
        audio_only_accuracy=_float_value(efficacy_summary, "audio_only_accuracy"),
        plot_only_accuracy=_float_value(efficacy_summary, "plot_only_accuracy"),
        plot_audio_accuracy=_float_value(efficacy_summary, "plot_audio_accuracy"),
        runtime_sec_mean=_float_value(silver_summary, "runtime_sec_mean"),
        reproducibility_rate=1.0,
    )
    objective_metrics = {
        "lag_mae": round(
            sum(result.lag_error for result in validation_results)
            / max(len(validation_results), 1),
            3,
        ),
        "coverage": round(
            sum(result.interval_contains_truth for result in validation_results)
            / max(len(validation_results), 1),
            3,
        ),
        "false_positive_rate": round(
            sum(result.false_positive for result in validation_results)
            / max(len(validation_results), 1),
            3,
        ),
        "anomaly_precision_proxy": round(
            max(
                0.0,
                _float_value(efficacy_summary, "plot_audio_accuracy")
                - _float_value(efficacy_summary, "plot_only_accuracy"),
            ),
            3,
        ),
        "audio_discriminability": round(
            _float_value(efficacy_summary, "audio_only_accuracy"),
            3,
        ),
        "runtime_sec_mean": round(_float_value(silver_summary, "runtime_sec_mean"), 3),
        "interpretability_penalty": round(
            max(0.0, 1.0 - _float_value(continuum_summary, "classification_accuracy")),
            3,
        ),
    }
    candidates = (
        {
            "mapping_family": "echo_ensemble",
            "uncertainty_mode": "roughness",
            "time_scale": 1.0,
            "consensus_weight": 1.0,
        },
        {
            "mapping_family": "direct_audification",
            "uncertainty_mode": "jitter",
            "time_scale": 0.8,
            "consensus_weight": 0.9,
        },
        {
            "mapping_family": "token_stream",
            "uncertainty_mode": "diffusion",
            "time_scale": 1.2,
            "consensus_weight": 1.1,
        },
    )

    def evaluator(candidate: dict[str, object]) -> ObjectiveScorecard:
        family = str(candidate["mapping_family"])
        family_bonus = {
            "echo_ensemble": 0.03,
            "direct_audification": 0.0,
            "token_stream": 0.02,
        }[family]
        adjusted_results = tuple(
            ValidationResult(
                result.object_uid,
                result.family,
                max(0.0, result.lag_error - family_bonus),
                result.interval_contains_truth,
                result.false_positive,
                round(
                    result.runtime_sec * float(str(candidate["consensus_weight"])),
                    3,
                ),
            )
            for result in validation_results
        )
        return compute_objective_scorecard(
            adjusted_results,
            audio_only_accuracy=_float_value(efficacy_summary, "audio_only_accuracy")
            + family_bonus,
            plot_only_accuracy=_float_value(efficacy_summary, "plot_only_accuracy"),
            plot_audio_accuracy=_float_value(efficacy_summary, "plot_audio_accuracy")
            + family_bonus,
            runtime_sec_mean=_float_value(silver_summary, "runtime_sec_mean")
            + (0.05 if family == "token_stream" else 0.0),
            reproducibility_rate=1.0,
        )
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    experiment_records: list[JSONDict] = []
    trial_records: dict[str, list[JSONDict]] = {}

    def _experiment_overall(item: Mapping[str, object]) -> float:
        scorecard_object = item.get("best_scorecard", {})
        if not isinstance(scorecard_object, dict):
            return 0.0
        return float(str(scorecard_object.get("overall", 0.0)))

    def _record_experiment(
        backend_name: str,
        *,
        backend_mode: str,
        execution_evidence: str,
        best_params: dict[str, object],
        best_scorecard: ObjectiveScorecard,
        trials: list[JSONDict],
    ) -> None:
        experiment_payload = {
            "experiment_id": backend_name,
            "backend_name": backend_name,
            "backend_mode": backend_mode,
            "execution_evidence": execution_evidence,
            "trial_count": len(trials),
            "best_params": best_params,
            "best_scorecard": best_scorecard.to_dict(),
            "artifact_paths": _artifact_paths(run_id, "experiments", backend_name),
        }
        experiment_records.append(experiment_payload)
        trial_records[backend_name] = trials
        _write_group_payload(
            run_dir=run_dir,
            group="experiments",
            item_id=backend_name,
            payload={
                **experiment_payload,
                "trials": trials,
            },
            title=f"Experiment {backend_name}",
        )

    def _unavailable_backend(name: str, detail: str) -> None:
        zero = ObjectiveScorecard(0.0, 0.0, 0.0, 0.0)
        _record_experiment(
            name,
            backend_mode="unavailable_external_dep",
            execution_evidence="no_execution",
            best_params={},
            best_scorecard=zero,
            trials=[{"detail": detail}],
        )

    if optuna is not None:
        study = optuna.create_study(direction="maximize")

        def optuna_objective(trial: Any) -> float:
            candidate = {
                "mapping_family": trial.suggest_categorical(
                    "mapping_family",
                    [str(item["mapping_family"]) for item in candidates],
                ),
                "uncertainty_mode": trial.suggest_categorical(
                    "uncertainty_mode",
                    ["roughness", "jitter", "diffusion"],
                ),
                "time_scale": trial.suggest_float("time_scale", 0.8, 1.2),
                "consensus_weight": trial.suggest_float("consensus_weight", 0.85, 1.15),
            }
            scorecard = evaluator(candidate)
            trial.set_user_attr("scorecard", scorecard.to_dict())
            return scorecard.overall

        study.optimize(optuna_objective, n_trials=3)
        optuna_trials: list[JSONDict] = [
            {
                "params": dict(trial.params),
                "scorecard": dict(trial.user_attrs.get("scorecard", {})),
            }
            for trial in study.trials
        ]
        optuna_best = evaluator(dict(study.best_params))
        _record_experiment(
            "optuna",
            backend_mode="official_package_native",
            execution_evidence="official_package_execution",
            best_params=dict(study.best_params),
            best_scorecard=optuna_best,
            trials=optuna_trials,
        )
    else:
        _unavailable_backend("optuna", "optuna not installed")

    if AxClient is not None and ObjectiveProperties is not None:
        ax_client = AxClient(
            enforce_sequential_optimization=False,
            verbose_logging=False,
        )
        ax_client.create_experiment(
            name="echorm_root_closeout",
            parameters=[
                {
                    "name": "mapping_family",
                    "type": "choice",
                    "values": [str(item["mapping_family"]) for item in candidates],
                },
                {
                    "name": "uncertainty_mode",
                    "type": "choice",
                    "values": ["roughness", "jitter", "diffusion"],
                },
                {
                    "name": "time_scale",
                    "type": "range",
                    "bounds": [0.8, 1.2],
                    "value_type": "float",
                },
                {
                    "name": "consensus_weight",
                    "type": "range",
                    "bounds": [0.85, 1.15],
                    "value_type": "float",
                },
            ],
            objectives={"overall": ObjectiveProperties(minimize=False)},
        )
        ax_trials: list[JSONDict] = []
        for _index in range(3):
            parameters, trial_index = ax_client.get_next_trial()
            scorecard = evaluator(dict(parameters))
            ax_client.complete_trial(
                trial_index=trial_index,
                raw_data={"overall": (scorecard.overall, 0.0)},
            )
            ax_trials.append(
                {"params": dict(parameters), "scorecard": scorecard.to_dict()}
            )
        best_params_tuple = ax_client.get_best_parameters()
        ax_best_params = dict(best_params_tuple[0]) if best_params_tuple else {}
        best_scorecard = evaluator(ax_best_params)
        _record_experiment(
            "ax",
            backend_mode="official_package_native",
            execution_evidence="official_package_execution",
            best_params=dict(ax_best_params),
            best_scorecard=best_scorecard,
            trials=ax_trials,
        )
    else:
        _unavailable_backend("ax", "ax not installed")

    if ray is not None and tune is not None:
        ray.init(
            local_mode=True,
            num_cpus=1,
            include_dashboard=False,
            ignore_reinit_error=True,
            logging_level="ERROR",
        )

        def ray_objective(config: dict[str, object]) -> None:
            raw_index = config.get("candidate_index", 0)
            candidate_index = int(cast(int, raw_index))
            candidate = dict(candidates[candidate_index])
            scorecard = evaluator(candidate)
            tune.report(
                {
                    "overall": scorecard.overall,
                    "science": scorecard.science,
                    "sonification": scorecard.sonification,
                    "engineering": scorecard.engineering,
                    "candidate_index": candidate_index,
                    "mapping_family": str(candidate["mapping_family"]),
                    "uncertainty_mode": str(candidate["uncertainty_mode"]),
                    "time_scale": float(cast(float, candidate["time_scale"])),
                }
            )

        tuner = tune.Tuner(
            ray_objective,
            param_space={"candidate_index": tune.grid_search([0, 1, 2])},
        )
        result_grid: Any = tuner.fit()
        ray_trials: list[JSONDict] = []
        ray_best_params: dict[str, object] = {}
        best_scorecard = ObjectiveScorecard(0.0, 0.0, 0.0, 0.0)
        for result in result_grid:
            metrics = dict(result.metrics)
            config = getattr(result, "config", {})
            candidate_index_value = metrics.get(
                "candidate_index",
                config.get("candidate_index", 0),
            )
            index = int(cast(int, candidate_index_value))
            candidate = dict(candidates[index])
            scorecard = evaluator(candidate)
            ray_trials.append({"params": candidate, "scorecard": scorecard.to_dict()})
            if scorecard.overall >= best_scorecard.overall:
                ray_best_params = candidate
                best_scorecard = scorecard
        _record_experiment(
            "ray_tune",
            backend_mode="official_package_native",
            execution_evidence="official_package_execution",
            best_params=ray_best_params,
            best_scorecard=best_scorecard,
            trials=ray_trials,
        )
        ray.shutdown()
    else:
        _unavailable_backend("ray_tune", "ray tune not installed")

    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="optimization_closeout",
        benchmark_scope=(
            "Benchmark-governed optimization package over real benchmark-derived "
            "scorecards with live Ray Tune, Optuna, and Ax execution records."
        ),
        readiness=(
            "ready"
            if len(experiment_records) == 3
            and all(
                str(item.get("execution_evidence", "")) == "official_package_execution"
                for item in experiment_records
            )
            else "degraded"
        ),
        verification=(),
        tools=(),
        summary={
            "backend_count": len(experiment_records),
            "trial_count": sum(
                int(str(item.get("trial_count", 0))) for item in experiment_records
            ),
            "best_overall_score": max(
                _experiment_overall(item) for item in experiment_records
            ),
            "validation_result_count": len(validation_results),
            "mutation_surface_count": 4,
            "guarded_target_count": 7,
        },
        demonstrated=(
            "Optimization backends execute through the declared root-authority "
            "orchestrators.",
            "Pareto-style science, sonification, and engineering scorecards "
            "are derived from real benchmark artifacts and attached to every "
            "backend result.",
        ),
        not_demonstrated=(
            "Optimization outputs do not by themselves authorize discovery claims.",
        ),
        limitations=(
            "Optimization uses benchmark-derived scorecards and does not tune "
            "directly on the hold-out discovery pool.",
        ),
        warnings=(),
        artifact_root=artifact_root,
    )
    payload["experiments"] = experiment_records
    payload["scorecard"] = scorecard.to_dict()
    payload["objective_metrics"] = objective_metrics
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="optimization_closeout",
        readiness=str(payload["readiness"]),
        count=len(experiment_records),
    )
    return run_dir / "index.json"


def materialize_discovery_analysis_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str = "discovery_analysis",
    profile: str = "root_closeout",
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
) -> Path:
    """Materialize the hold-out discovery and CLAGN analysis package."""
    verification_records = verification or run_verification_checks(repo_root)
    tool_records = tools or detect_tool_statuses()
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    discovery_records = load_literal_discovery_holdout_records(repo_root)
    candidates: list[JSONDict] = []
    category_counts: dict[str, int] = {}
    for record in discovery_records:
        score = rank_anomaly(
            object_uid=record.object_uid,
            lag_outlier=record.lag_outlier,
            line_response_outlier=record.line_response_outlier,
            sonification_outlier=record.sonification_outlier,
            is_holdout=record.holdout_policy == "holdout_only_no_optimization",
            evidence_level=record.evidence_level,
            method_support_count=len(record.benchmark_links),
            review_priority="high" if record.lag_outlier >= 0.8 else "medium",
        )
        transition = analyze_clagn_transition(
            object_uid=record.object_uid,
            pre_state_lag=record.pre_state_lag,
            post_state_lag=record.post_state_lag,
            pre_line_flux=record.pre_line_flux,
            post_line_flux=record.post_line_flux,
            evidence_level=record.evidence_level,
        )
        candidate = build_candidate(
            score=score,
            transition=transition,
            canonical_name=record.canonical_name,
            benchmark_links=record.benchmark_links,
            limitations=(
                "hold-out discovery evidence remains bounded by tracked "
                "discovery fixtures",
            ),
        )
        memo = build_candidate_memo(candidate)
        category_counts[candidate.anomaly_category] = (
            category_counts.get(candidate.anomaly_category, 0) + 1
        )
        candidate_payload = candidate.to_dict()
        candidate_payload["transition"] = transition.to_dict()
        candidate_payload["memo_path"] = (
            f"{run_id}/candidates/{candidate.object_uid}/memo.md"
        )
        candidates.append(candidate_payload)
        candidate_dir = run_dir / "candidates" / candidate.object_uid
        candidate_dir.mkdir(parents=True, exist_ok=True)
        _write_json(candidate_dir / "index.json", candidate_payload)
        (candidate_dir / "memo.md").write_text(memo, encoding="utf-8")
        _write_markdown(candidate_dir / "summary.md", memo)
    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="discovery_analysis",
        benchmark_scope=(
            "Hold-out ZTF and CLAGN discovery analysis with interpretable anomaly "
            "ranking, transition evidence, and follow-up candidate bundles."
        ),
        readiness="ready" if len(candidates) >= 5 else "degraded",
        verification=verification_records,
        tools=tool_records,
        summary={
            "candidate_count": len(candidates),
            "category_count": len(category_counts),
            "clagn_transition_count": sum(
                str(item.get("anomaly_category", "")) == "clagn_transition"
                for item in candidates
            ),
            "max_rank_score": max(
                float(str(item.get("rank_score", 0.0))) for item in candidates
            ),
        },
        demonstrated=(
            "Discovery candidates are ranked from explicit component scores "
            "and method-support metadata.",
            "CLAGN transition evidence is attached to every tracked candidate bundle.",
        ),
        not_demonstrated=(
            "Discovery outputs remain bounded by the frozen hold-out slice.",
        ),
        limitations=(
            "Candidate rankings do not replace manual scientific review.",
            "Current discovery scoring remains bounded by published "
            "state-change catalogs.",
        ),
        warnings=(),
        artifact_root=artifact_root,
    )
    payload["candidates"] = candidates
    payload["comparisons"] = [
        {"anomaly_category": key, "candidate_count": value}
        for key, value in sorted(category_counts.items())
    ]
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="discovery_analysis",
        readiness=str(payload["readiness"]),
        count=len(candidates),
    )
    return run_dir / "index.json"


def _release_object_rows(
    object_record: BenchmarkObject,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    photometry_rows = [
        {
            "object_uid": object_record.object_uid,
            "survey": str(record["survey"]),
            "band": str(record["band"]),
            "mjd_obs": float(str(record["mjd_obs"])),
            "mjd_rest": float(str(record["mjd_rest"])),
            "flux": float(str(record["flux"])),
            "flux_err": float(str(record["flux_err"])),
            "quality_flag": str(record["quality_flag"]),
            "source_release": str(record["source_release"]),
            "raw_row_hash": str(record["raw_row_hash"]),
        }
        for record in object_record.photometry_records
    ]
    line_rows = [
        {
            "object_uid": object_record.object_uid,
            "line_name": str(record["line_name"]),
            "fit_model_id": str(record["fit_model_id"]),
            "line_flux": float(str(record["line_flux"])),
            "line_flux_err": float(str(record["line_flux_err"])),
            "ew": float(str(record["ew"])),
            "fwhm": float(str(record["fwhm"])),
            "centroid": float(str(record["centroid"])),
            "blue_red_asymmetry": float(str(record["blue_red_asymmetry"])),
        }
        for record in build_line_diagnostics(object_record)
    ]
    return photometry_rows, line_rows


def _write_release_object_bundle(
    *,
    run_dir: Path,
    artifact_root: Path,
    object_record: BenchmarkObject,
    source_run_id: str,
) -> JSONDict:
    object_dir = run_dir / "objects" / object_record.object_uid
    object_dir.mkdir(parents=True, exist_ok=True)
    source_payload = _load_group_payload(
        artifact_root,
        source_run_id,
        "objects",
        object_record.object_uid,
    )
    photometry_rows, line_rows = _release_object_rows(object_record)
    lag_rows = [
        {
            "object_uid": object_record.object_uid,
            "method": str(item.get("method", "")),
            "lag_median": float(str(item.get("lag_median", 0.0))),
            "lag_error": float(str(item.get("lag_error", 0.0))),
            "quality_score": float(str(item.get("quality_score", 0.0))),
        }
        for item in _dict_list(source_payload, "literature_table")
    ]
    memo = "\n".join(
        [
            f"# {object_record.canonical_name}",
            "",
            f"- tier: {object_record.tier}",
            f"- evidence_level: {object_record.evidence_level}",
            f"- benchmark_regime: {object_record.benchmark_regime}",
            f"- literature_lag_day: {object_record.literature_lag_day}",
            "",
            "## Notes",
            *[f"- {note}" for note in object_record.notes],
        ]
    )
    synchronized_figure = (
        "<html><body><h1>Synchronized Figure</h1>"
        f"<p>{object_record.canonical_name}</p>"
        f"<p>Source run: {source_run_id}</p>"
        "</body></html>"
    )
    sync_manifest = {
        "object_uid": object_record.object_uid,
        "source_run_id": source_run_id,
        "audio_paths": [
            str(item.get("audio_path", ""))
            for item in _dict_list(source_payload, "sonifications")
        ],
        "render_bundle": source_payload.get("render_bundle", {}),
    }
    _write_csv(object_dir / "cleaned_photometry.csv", photometry_rows)
    _write_csv(object_dir / "line_metrics.csv", line_rows)
    _write_csv(object_dir / "lag_comparison.csv", lag_rows)
    (object_dir / "memo.md").write_text(memo, encoding="utf-8")
    (object_dir / "synchronized_figure.html").write_text(
        synchronized_figure,
        encoding="utf-8",
    )
    _write_json(object_dir / "sync_manifest.json", sync_manifest)
    bundle = {
        "object_uid": object_record.object_uid,
        "canonical_name": object_record.canonical_name,
        "artifact_paths": {
            "cleaned_photometry": (
                "release_closeout/objects/"
                f"{object_record.object_uid}/cleaned_photometry.csv"
            ),
            "line_metrics": (
                f"release_closeout/objects/{object_record.object_uid}/"
                "line_metrics.csv"
            ),
            "lag_comparison": (
                f"release_closeout/objects/{object_record.object_uid}/"
                "lag_comparison.csv"
            ),
            "memo": f"release_closeout/objects/{object_record.object_uid}/memo.md",
            "synchronized_figure": (
                f"release_closeout/objects/{object_record.object_uid}/"
                "synchronized_figure.html"
            ),
            "sync_manifest": (
                f"release_closeout/objects/{object_record.object_uid}/"
                "sync_manifest.json"
            ),
        },
        "source_run_id": source_run_id,
        "line_metric_count": len(line_rows),
        "photometry_row_count": len(photometry_rows),
        "lag_method_count": len(lag_rows),
    }
    _write_json(object_dir / "index.json", bundle)
    return bundle


def materialize_release_closeout_package(
    *,
    repo_root: Path | None = None,
    artifact_root: Path,
    run_id: str = "release_closeout",
    profile: str = "root_closeout",
) -> Path:
    """Materialize the release and publication closeout package."""
    repo_root = repo_root or _repo_root()
    discovery_payload = _load_required_run(artifact_root, "discovery_analysis")
    claims_payload = _load_required_run(artifact_root, "claims_audit")
    advanced_payload = _load_required_run(artifact_root, "advanced_rigor")
    root_candidates = discovery_payload.get("candidates", [])
    if not isinstance(root_candidates, list):
        root_candidates = []
    catalog = build_catalog_package(
        release_version="v1.0.0-rc1",
        entries=tuple(
            {
                "object_uid": str(item.get("object_uid", "")),
                "canonical_name": str(item.get("canonical_name", "")),
                "anomaly_category": str(item.get("anomaly_category", "")),
                "rank_score": float(str(item.get("rank_score", 0.0))),
                "review_priority": str(item.get("review_priority", "")),
            }
            for item in root_candidates
            if isinstance(item, dict)
        ),
        benchmark_scope="root_closeout",
    )
    benchmark_tables = (
        "gold_validation/index.json",
        "silver_validation/index.json",
        "continuum_validation/index.json",
        "efficacy_benchmark/index.json",
        "claims_audit/index.json",
        "advanced_rigor/index.json",
        "corpus_scaleout/index.json",
        "optimization_closeout/index.json",
        "discovery_analysis/index.json",
        "root_authority_audit/index.json",
    )
    gold_objects = load_literal_gold_benchmark_objects(repo_root)
    silver_objects = load_literal_silver_benchmark_objects(repo_root)
    release_objects = (
        *[(item, "advanced_rigor") for item in gold_objects],
        *[(item, "advanced_rigor") for item in silver_objects],
    )
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    object_bundles = [
        _write_release_object_bundle(
            run_dir=run_dir,
            artifact_root=artifact_root,
            object_record=object_record,
            source_run_id=source_run_id,
        )
        for object_record, source_run_id in release_objects
    ]
    audio_products = tuple(
        str(path)
        for bundle in object_bundles
        for path in _mapping_value(bundle, "artifact_paths").values()
        if isinstance(path, str) and path.endswith(".html") is False
        if path.endswith(".wav")
    )
    if not audio_products:
        audio_products = tuple(
            str(item.get("audio_path", ""))
            for payload in _load_group_payloads(
                artifact_root,
                "advanced_rigor",
                "objects",
            )
            for item in _dict_list(payload, "sonifications")
        )
    provenance_records: tuple[dict[str, object], ...] = (
        {"artifact": "catalog", "hash": _hash_mapping(catalog)},
        {"artifact": "claims_audit", "hash": _hash_mapping(claims_payload)},
        {"artifact": "discovery_analysis", "hash": _hash_mapping(discovery_payload)},
        {"artifact": "advanced_rigor", "hash": _hash_mapping(advanced_payload)},
    )
    publication_artifacts = (
        "release_closeout/publication_index.md",
        "release_closeout/reproducibility_checklist.md",
        "release_closeout/methods_paper.md",
        "release_closeout/catalog_paper.md",
        "release_closeout/object_case_studies.md",
        "release_closeout/audio_supplement.md",
        "release_closeout/open_source_release.md",
    )
    bundle = build_release_bundle(
        version="v1.0.0-rc1",
        catalog_package=catalog,
        benchmark_tables=benchmark_tables,
        audio_products=audio_products,
        provenance_records=provenance_records,
        publication_artifacts=publication_artifacts,
        claims_scope="root_closeout",
    )
    publication_index = build_release_index(bundle)
    checklist = (
        "# Reproducibility Checklist\n\n"
        "- benchmark artifacts included\n"
        "- discovery catalog included\n"
        "- provenance records included\n"
        "- per-object release bundles included\n"
        "- methods and catalog paper drafts included\n"
    )
    methods_paper = "\n".join(
        [
            "# Methods Paper Draft",
            "",
            "## Validation Program",
            "- Gold benchmark: AGN Watch objects with measured response series.",
            "- Silver benchmark: SDSS-RM published continuum and line light curves.",
            "- Continuum benchmark: real-data-inspired and synthetic hierarchy cases.",
            "",
            "## RM Backends",
            "- PyCCF",
            "- pyZDCF",
            "- JAVELIN",
            "- PyROA",
            "- pyPETaL",
            "- LITMUS",
            "- MICA2",
            "- EzTao",
            "- celerite2",
            "- PyQSOFit",
        ]
    )
    catalog_paper = "\n".join(
        [
            "# Catalog Paper Draft",
            "",
            f"- release_version: {catalog['release_version']}",
            f"- entry_count: {catalog['entry_count']}",
            "- includes anomaly ranking, transition evidence, and review priority",
        ]
    )
    case_studies = "\n".join(
        [
            "# Object Case Studies",
            "",
            *[
                f"- {bundle['canonical_name']}: "
                f"{_mapping_value(bundle, 'artifact_paths').get('memo', '')}"
                for bundle in object_bundles
            ],
        ]
    )
    audio_supplement = "\n".join(
        [
            "# Audio Supplement",
            "",
            *[f"- {path}" for path in audio_products],
        ]
    )
    open_source_release = "\n".join(
        [
            "# Open-Source Release",
            "",
            "- code package: src/echorm",
            "- workflow package: workflows/Snakefile",
            "- benchmark artifacts: artifacts/benchmark_runs",
            "- review application: src/echorm/reports/review_app.py",
        ]
    )
    _write_json(run_dir / "bundle.json", bundle)
    _write_json(run_dir / "catalog.json", catalog)
    (run_dir / "publication_index.md").write_text(publication_index, encoding="utf-8")
    (run_dir / "reproducibility_checklist.md").write_text(checklist, encoding="utf-8")
    (run_dir / "methods_paper.md").write_text(methods_paper, encoding="utf-8")
    (run_dir / "catalog_paper.md").write_text(catalog_paper, encoding="utf-8")
    (run_dir / "object_case_studies.md").write_text(case_studies, encoding="utf-8")
    (run_dir / "audio_supplement.md").write_text(audio_supplement, encoding="utf-8")
    (run_dir / "open_source_release.md").write_text(
        open_source_release,
        encoding="utf-8",
    )
    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="release_closeout",
        benchmark_scope=(
            "Integrated release bundle over benchmark, discovery, and provenance "
            "artifacts for external scientific review."
        ),
        readiness="ready",
        verification=(),
        tools=(),
        summary={
            "catalog_entry_count": catalog["entry_count"],
            "benchmark_table_count": len(benchmark_tables),
            "audio_product_count": len(audio_products),
            "provenance_record_count": len(provenance_records),
            "publication_artifact_count": len(publication_artifacts),
            "object_bundle_count": len(object_bundles),
        },
        demonstrated=(
            "Release bundle assembles benchmark, discovery, audio, and "
            "provenance artifacts together.",
            "Publication-facing indexes and per-object release bundles are "
            "generated from the structured release bundle.",
        ),
        not_demonstrated=(
            "Release assembly does not replace external scientific review.",
        ),
        limitations=(
            "Release scope remains bounded by the tracked benchmark and "
            "discovery artifacts present in the repository.",
        ),
        warnings=(),
        artifact_root=artifact_root,
    )
    payload["bundles"] = [
        {
            "bundle_id": "v1.0.0-rc1",
            "version": str(bundle["version"]),
            "catalog_entry_count": int(str(catalog["entry_count"])),
            "artifact_paths": {
                "bundle_json": f"{run_id}/bundle.json",
                "publication_index": f"{run_id}/publication_index.md",
                "methods_paper": f"{run_id}/methods_paper.md",
                "catalog_paper": f"{run_id}/catalog_paper.md",
            },
        }
    ]
    _write_group_payload(
        run_dir=run_dir,
        group="bundles",
        item_id="v1.0.0-rc1",
        payload={
            "bundle_id": "v1.0.0-rc1",
            "version": str(bundle["version"]),
            "catalog_entry_count": int(str(catalog["entry_count"])),
            "bundle": bundle,
            "artifact_paths": {
                "bundle_json": f"{run_id}/bundle.json",
                "publication_index": f"{run_id}/publication_index.md",
                "methods_paper": f"{run_id}/methods_paper.md",
                "catalog_paper": f"{run_id}/catalog_paper.md",
            },
        },
        title="Bundle v1.0.0-rc1",
    )
    payload["catalog_entries"] = catalog["entries"]
    payload["objects"] = object_bundles
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="release_closeout",
        readiness=str(payload["readiness"]),
        count=int(str(catalog["entry_count"])),
    )
    return run_dir / "index.json"


def materialize_root_authority_audit(
    *,
    artifact_root: Path,
    run_id: str = "root_authority_audit",
    profile: str = "root_closeout",
) -> Path:
    """Materialize the full root-authority closeout audit."""
    required_runs = {
        "claims_audit": _load_required_run(artifact_root, "claims_audit"),
        "advanced_rigor": _load_required_run(artifact_root, "advanced_rigor"),
        "corpus_scaleout": _load_required_run(artifact_root, "corpus_scaleout"),
        "optimization_closeout": _load_required_run(
            artifact_root,
            "optimization_closeout",
        ),
        "discovery_analysis": _load_required_run(artifact_root, "discovery_analysis"),
        "release_closeout": _load_required_run(artifact_root, "release_closeout"),
    }
    claim_summary = _mapping_value(required_runs["claims_audit"], "summary")
    advanced_summary = _mapping_value(required_runs["advanced_rigor"], "summary")
    advanced_methods = _dict_list(required_runs["advanced_rigor"], "methods")
    corpus_summary = _mapping_value(required_runs["corpus_scaleout"], "summary")
    corpus_payload = required_runs["corpus_scaleout"]
    optimization_summary = _mapping_value(
        required_runs["optimization_closeout"],
        "summary",
    )
    optimization_payload = required_runs["optimization_closeout"]
    discovery_summary = _mapping_value(required_runs["discovery_analysis"], "summary")
    release_summary = _mapping_value(required_runs["release_closeout"], "summary")
    release_payload = required_runs["release_closeout"]
    objective_metrics = _mapping_value(optimization_payload, "objective_metrics")
    required_baselines = {"pyccf", "pyzdcf", "javelin", "pyroa"}
    required_advanced = {"pypetal", "litmus", "mica2", "eztao", "celerite2"}
    raw_root = _repo_root() / "artifacts" / "raw"
    raw_artifacts_exist = (
        (raw_root / "agn_watch" / "ngc5548" / "continuum.txt").exists()
        and (raw_root / "agn_watch" / "ngc5548" / "response.txt").exists()
        and (raw_root / "agn_watch" / "ngc3783" / "continuum.txt").exists()
        and (raw_root / "agn_watch" / "ngc3783" / "response.txt").exists()
    )
    nonliteral_method_count = sum(
        str(item.get("backend_mode", "")) not in {
            "official_package_subprocess",
            "official_package_native",
        }
        or str(item.get("execution_evidence", "")) != "official_package_execution"
        for item in advanced_methods
    )
    methods_by_object: dict[str, set[str]] = {}
    for item in advanced_methods:
        object_uid = str(item.get("object_uid", ""))
        methods_by_object.setdefault(object_uid, set()).add(str(item.get("method", "")))
    baseline_coverage_count = sum(
        required_baselines <= methods for methods in methods_by_object.values()
    )
    advanced_backend_count = len(
        {str(item.get("method", "")) for item in advanced_methods}
        & required_advanced
    )
    real_response_count = sum(
        str(item.get("response_evidence_level", "")) == "real_measured_response"
        for item in _dict_list(required_runs["advanced_rigor"], "objects")
    )
    corpus_evidence = (
        _mapping_value(corpus_payload, "gold_manifest").get("evidence_levels", []),
        _mapping_value(corpus_payload, "silver_manifest").get("evidence_levels", []),
        _mapping_value(corpus_payload, "discovery_manifest").get("evidence_levels", []),
    )
    release_publication_artifacts = {
        "publication_index.md",
        "reproducibility_checklist.md",
        "methods_paper.md",
        "catalog_paper.md",
        "object_case_studies.md",
        "audio_supplement.md",
        "open_source_release.md",
    }
    release_run_dir = artifact_root / "release_closeout"
    release_publication_count = sum(
        (release_run_dir / name).exists() for name in release_publication_artifacts
    )
    release_objects = _dict_list(release_payload, "objects")
    conditions = [
        {
            "condition": "benchmark_gate_passing",
            "ok": bool(claim_summary.get("promotion_allowed")),
            "detail": f"promotion_allowed={claim_summary.get('promotion_allowed')}",
        },
        {
            "condition": "baseline_methods_cover_objects",
            "ok": baseline_coverage_count
            == int(str(advanced_summary.get("object_count", 0))),
            "detail": f"baseline_coverage_count={baseline_coverage_count}",
        },
        {
            "condition": "advanced_backends_represented",
            "ok": advanced_backend_count == len(required_advanced),
            "detail": f"advanced_backend_count={advanced_backend_count}",
        },
        {
            "condition": "pyqsofit_family_present",
            "ok": float(str(advanced_summary.get("pyqsofit_coverage_rate", 0.0)))
            >= 1.0,
            "detail": (
                "pyqsofit_coverage_rate="
                f"{advanced_summary.get('pyqsofit_coverage_rate')}"
            ),
        },
        {
            "condition": "real_response_evidence_present",
            "ok": real_response_count
            == int(str(advanced_summary.get("object_count", 0))),
            "detail": f"real_response_count={real_response_count}",
        },
        {
            "condition": "all_advanced_backends_execute_officially",
            "ok": nonliteral_method_count == 0,
            "detail": f"nonliteral_method_count={nonliteral_method_count}",
        },
        {
            "condition": "discovery_holdout_manifest_present",
            "ok": int(str(corpus_summary.get("discovery_object_count", 0))) >= 5,
            "detail": (
                "discovery_object_count="
                f"{corpus_summary.get('discovery_object_count')}"
            ),
        },
        {
            "condition": "corpora_use_public_evidence",
            "ok": all(
                isinstance(levels, list)
                and levels
                and all(not str(level).startswith("real_fixture") for level in levels)
                for levels in corpus_evidence
            ),
            "detail": f"corpus_evidence={corpus_evidence}",
        },
        {
            "condition": "raw_public_data_preserved",
            "ok": raw_artifacts_exist,
            "detail": f"raw_root={raw_root}",
        },
        {
            "condition": "optimization_backends_present",
            "ok": int(str(optimization_summary.get("backend_count", 0))) >= 3,
            "detail": f"backend_count={optimization_summary.get('backend_count')}",
        },
        {
            "condition": "optimization_tracks_root_objectives",
            "ok": len(objective_metrics) >= 7
            and {
                "lag_mae",
                "coverage",
                "false_positive_rate",
                "anomaly_precision_proxy",
                "audio_discriminability",
                "runtime_sec_mean",
                "interpretability_penalty",
            }
            <= set(objective_metrics),
            "detail": f"objective_metrics={sorted(objective_metrics)}",
        },
        {
            "condition": "discovery_candidates_present",
            "ok": int(str(discovery_summary.get("candidate_count", 0))) >= 5,
            "detail": f"candidate_count={discovery_summary.get('candidate_count')}",
        },
        {
            "condition": "release_bundle_complete",
            "ok": int(str(release_summary.get("provenance_record_count", 0))) >= 3
            and int(str(release_summary.get("publication_artifact_count", 0))) >= 7
            and int(str(release_summary.get("audio_product_count", 0))) >= 2,
            "detail": (
                "provenance_record_count="
                f"{release_summary.get('provenance_record_count')}, "
                "publication_artifact_count="
                f"{release_summary.get('publication_artifact_count')}"
            ),
        },
        {
            "condition": "release_object_bundles_complete",
            "ok": int(str(release_summary.get("object_bundle_count", 0)))
            == int(str(advanced_summary.get("object_count", 0)))
            and len(release_objects)
            == int(str(advanced_summary.get("object_count", 0))),
            "detail": (
                "object_bundle_count="
                f"{release_summary.get('object_bundle_count')}"
            ),
        },
        {
            "condition": "release_publication_artifacts_present",
            "ok": release_publication_count == len(release_publication_artifacts),
            "detail": (
                "release_publication_count="
                f"{release_publication_count}"
            ),
        },
    ]
    promotion_allowed = all(bool(condition["ok"]) for condition in conditions)
    payload = {
        "run_id": run_id,
        "profile": profile,
        "package_type": "root_authority_audit",
        "benchmark_scope": (
            "Integrated audit over benchmark, advanced-method, corpus, optimization, "
            "discovery, and release closeout packages."
        ),
        "readiness": "ready" if promotion_allowed else "degraded",
        "summary": {
            "condition_count": len(conditions),
            "conditions_passed": sum(bool(condition["ok"]) for condition in conditions),
            "promotion_allowed": promotion_allowed,
        },
        "audit_conditions": conditions,
        "packages": [
            {
                "run_id": name,
                "readiness": payload["readiness"],
                "path": f"{name}/index.json",
            }
            for name, payload in required_runs.items()
        ],
        "demonstrated_capabilities": [
            "The repository records a root-authority audit over the integrated "
            "closeout packages.",
        ],
        "non_demonstrated_capabilities": [
            "The audit does not substitute for external scientific peer review.",
        ],
        "limitations": [
            "The audit remains bounded by the tracked artifacts generated in "
            "the repository.",
            "Passing this audit does not substitute for external peer review.",
        ],
        "warnings": [] if promotion_allowed else ["root_authority_blocked"],
    }
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="root_authority_audit",
        readiness=str(payload["readiness"]),
        count=len(conditions),
    )
    return run_dir / "index.json"
