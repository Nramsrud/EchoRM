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
    conditions = [
        {
            "condition": "gold_objects_at_least_two",
            "ok": _int_value(gold_summary, "object_count") >= 2,
            "detail": f"gold_object_count={gold_summary['object_count']}",
        },
        {
            "condition": "silver_population_at_least_four",
            "ok": _int_value(silver_summary, "population_count") >= 4,
            "detail": f"silver_population_count={silver_summary['population_count']}",
        },
        {
            "condition": "continuum_cases_at_least_five",
            "ok": _int_value(continuum_summary, "case_count") >= 5,
            "detail": f"continuum_case_count={continuum_summary['case_count']}",
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
