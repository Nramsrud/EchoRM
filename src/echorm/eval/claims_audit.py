"""Cross-package claims audit for broad validation."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

from .readiness import _write_json


def _mapping_field(payload: Mapping[str, object], key: str) -> Mapping[str, object]:
    value = payload.get(key, {})
    return value if isinstance(value, dict) else {}


def _int_value(payload: Mapping[str, object], key: str, default: int = 0) -> int:
    return int(str(payload.get(key, default)))


def _float_value(
    payload: Mapping[str, object],
    key: str,
    default: float = 0.0,
) -> float:
    return float(str(payload.get(key, default)))


def _list_length(payload: Mapping[str, object], key: str) -> int:
    value = payload.get(key, [])
    return len(value) if isinstance(value, list) else 0


def materialize_claims_audit(
    *,
    artifact_root: Path,
    run_id: str = "claims_audit",
    profile: str = "broad_validation",
) -> Path:
    """Materialize a broad-validation claims audit over generated packages."""
    required_runs = {
        "gold_validation": artifact_root / "gold_validation" / "index.json",
        "silver_validation": artifact_root / "silver_validation" / "index.json",
        "continuum_validation": artifact_root / "continuum_validation" / "index.json",
        "efficacy_benchmark": artifact_root / "efficacy_benchmark" / "index.json",
    }
    run_payloads = {
        name: json.loads(path.read_text(encoding="utf-8"))
        for name, path in required_runs.items()
    }
    gold_summary = _mapping_field(run_payloads["gold_validation"], "summary")
    silver_summary = _mapping_field(run_payloads["silver_validation"], "summary")
    continuum_summary = _mapping_field(run_payloads["continuum_validation"], "summary")
    efficacy_summary = _mapping_field(run_payloads["efficacy_benchmark"], "summary")
    rerun_payloads = [
        run_payloads["gold_validation"],
        run_payloads["silver_validation"],
        run_payloads["continuum_validation"],
        run_payloads["efficacy_benchmark"],
    ]
    rerun_stability_ok = all(
        all(
            bool(rerun.get("passed"))
            for rerun in payload.get("reruns", [])
            if isinstance(rerun, dict)
        )
        for payload in rerun_payloads
    )
    claims_metadata_ok = all(
        _list_length(payload, "demonstrated_capabilities") > 0
        and _list_length(payload, "non_demonstrated_capabilities") > 0
        and _list_length(payload, "limitations") > 0
        for payload in rerun_payloads
    )
    conditions = [
        {
            "condition": "gold_objects_at_least_two",
            "ok": _int_value(gold_summary, "object_count") >= 2,
            "detail": f"gold_object_count={gold_summary['object_count']}",
        },
        {
            "condition": "gold_mean_abs_error_at_or_below_3d",
            "ok": _float_value(gold_summary, "mean_abs_error") <= 3.0,
            "detail": f"gold_mean_abs_error={gold_summary['mean_abs_error']}",
        },
        {
            "condition": "gold_coverage_at_or_above_0_75",
            "ok": _float_value(gold_summary, "coverage_rate") >= 0.75,
            "detail": f"gold_coverage_rate={gold_summary['coverage_rate']}",
        },
        {
            "condition": "silver_population_at_least_four",
            "ok": _int_value(silver_summary, "population_count") >= 4,
            "detail": f"silver_population_count={silver_summary['population_count']}",
        },
        {
            "condition": "silver_coverage_at_or_above_0_75",
            "ok": _float_value(silver_summary, "coverage_rate") >= 0.75,
            "detail": f"silver_coverage_rate={silver_summary['coverage_rate']}",
        },
        {
            "condition": "silver_false_positive_at_or_below_0_10",
            "ok": _float_value(silver_summary, "false_positive_rate") <= 0.10,
            "detail": (
                "silver_false_positive_rate="
                f"{silver_summary['false_positive_rate']}"
            ),
        },
        {
            "condition": "silver_disagreement_at_or_below_0_50",
            "ok": _float_value(silver_summary, "disagreement_rate") <= 0.50,
            "detail": f"silver_disagreement_rate={silver_summary['disagreement_rate']}",
        },
        {
            "condition": "continuum_cases_at_least_five",
            "ok": _int_value(continuum_summary, "case_count") >= 5,
            "detail": f"continuum_case_count={continuum_summary['case_count']}",
        },
        {
            "condition": "continuum_classification_at_or_above_0_75",
            "ok": _float_value(continuum_summary, "classification_accuracy") >= 0.75,
            "detail": (
                "continuum_classification_accuracy="
                f"{continuum_summary['classification_accuracy']}"
            ),
        },
        {
            "condition": "continuum_stability_at_or_above_0_75",
            "ok": _float_value(continuum_summary, "cadence_stability_score") >= 0.75,
            "detail": (
                "continuum_cadence_stability_score="
                f"{continuum_summary['cadence_stability_score']}"
            ),
        },
        {
            "condition": "audio_beats_plot_baseline",
            "ok": _float_value(efficacy_summary, "audio_only_accuracy")
            >= _float_value(efficacy_summary, "plot_only_accuracy"),
            "detail": (
                "audio_only_accuracy="
                f"{efficacy_summary['audio_only_accuracy']}, "
                "plot_only_accuracy="
                f"{efficacy_summary['plot_only_accuracy']}"
            ),
        },
        {
            "condition": "combined_beats_plot_baseline",
            "ok": _float_value(efficacy_summary, "plot_audio_accuracy")
            >= _float_value(efficacy_summary, "plot_only_accuracy"),
            "detail": (
                "plot_audio_accuracy="
                f"{efficacy_summary['plot_audio_accuracy']}, "
                "plot_only_accuracy="
                f"{efficacy_summary['plot_only_accuracy']}"
            ),
        },
        {
            "condition": "efficacy_calibration_at_or_below_0_20",
            "ok": _float_value(efficacy_summary, "calibration_error") <= 0.20,
            "detail": (
                "efficacy_calibration_error="
                f"{efficacy_summary['calibration_error']}"
            ),
        },
        {
            "condition": "efficacy_agreement_at_or_above_0_60",
            "ok": _float_value(efficacy_summary, "inter_rater_agreement") >= 0.60,
            "detail": (
                "efficacy_inter_rater_agreement="
                f"{efficacy_summary['inter_rater_agreement']}"
            ),
        },
        {
            "condition": "rerun_stability_passes",
            "ok": rerun_stability_ok,
            "detail": f"rerun_stability_passes={rerun_stability_ok}",
        },
        {
            "condition": "claims_metadata_present",
            "ok": claims_metadata_ok,
            "detail": f"claims_metadata_present={claims_metadata_ok}",
        },
    ]
    promotion_allowed = all(bool(condition["ok"]) for condition in conditions)
    warnings = () if promotion_allowed else ("promotion_blocked",)
    payload: dict[str, object] = {
        "run_id": run_id,
        "profile": profile,
        "package_type": "claims_audit",
        "benchmark_scope": (
            "Cross-package audit over gold, silver, continuum, and efficacy "
            "validation packages."
        ),
        "readiness": "ready" if promotion_allowed else "degraded",
        "artifact_root": str(artifact_root / run_id),
        "summary": {
            "condition_count": len(conditions),
            "conditions_passed": sum(bool(condition["ok"]) for condition in conditions),
            "promotion_allowed": promotion_allowed,
        },
        "audit_conditions": conditions,
        "packages": [
            {
                "run_id": name,
                "readiness": run_payloads[name]["readiness"],
                "path": f"{name}/index.json",
            }
            for name in required_runs
        ],
        "demonstrated_capabilities": [
            "The audit evaluates the declared gate conditions from tracked "
            "validation artifacts.",
            "Promotion is blocked automatically when any required condition fails.",
        ],
        "non_demonstrated_capabilities": [
            "The audit does not replace package-level scientific interpretation.",
        ],
        "limitations": [
            "Audit conclusions remain bounded by the declared benchmark scope of "
            "the generated packages.",
        ],
        "warnings": list(warnings),
    }
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    _write_json(run_dir / "index.json", payload)
    dossier = (
        f"# claims_audit {run_id}\n\n"
        f"- Readiness: {payload['readiness']}\n"
        f"- Promotion allowed: {promotion_allowed}\n\n"
        "## Conditions\n\n"
        + "\n".join(
            f"- {condition['condition']}: {condition['ok']} ({condition['detail']})"
            for condition in conditions
        )
        + "\n"
    )
    (run_dir / "summary.md").write_text(dossier, encoding="utf-8")
    (run_dir / "dossier.md").write_text(dossier, encoding="utf-8")

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
    runs = [run for run in runs if run.get("run_id") != run_id]
    runs.append(
        {
            "run_id": run_id,
            "profile": profile,
            "readiness": payload["readiness"],
            "case_count": len(conditions),
            "path": f"{run_id}/index.json",
            "package_type": "claims_audit",
        }
    )
    runs.sort(key=lambda run: str(run["run_id"]))
    _write_json(root_index_path, {"runs": runs})
    return run_dir / "index.json"
