"""Human-readable benchmark readiness summaries."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..eval.readiness import BenchmarkReadinessRun


def build_benchmark_readiness_summary(run: BenchmarkReadinessRun) -> str:
    """Build a concise markdown summary for one readiness run."""
    tool_summary = ", ".join(
        f"{tool.name}={'ok' if tool.available else 'missing'}" for tool in run.tools
    )
    verification_summary = ", ".join(
        f"{check.name}={'ok' if check.ok else 'fail'}" for check in run.verification
    )
    case_lines = "\n".join(
        f"- {case.case_id}: family={case.family}, lag_error={case.lag_error:.3f}, "
        f"false_positive={case.false_positive}"
        for case in run.cases
    )
    warnings = ", ".join(run.warnings) if run.warnings else "none"
    return (
        f"# Benchmark Readiness {run.run_id}\n\n"
        f"- Profile: {run.profile}\n"
        f"- Readiness: {run.readiness}\n"
        f"- Verification: {verification_summary}\n"
        f"- Tools: {tool_summary}\n"
        f"- Warnings: {warnings}\n\n"
        "## Cases\n\n"
        f"{case_lines}\n"
    )


def build_benchmark_case_summary(case_payload: Mapping[str, object]) -> str:
    """Build a concise markdown summary for one benchmark case."""
    validation_object = case_payload["validation"]
    if not isinstance(validation_object, Mapping):
        raise ValueError("case payload validation section must be a mapping")
    return (
        f"# Case {case_payload['case_id']}\n\n"
        f"- Family: {case_payload['family']}\n"
        f"- Lag error: {validation_object['lag_error']}\n"
        f"- Interval contains truth: {validation_object['interval_contains_truth']}\n"
        f"- False positive: {validation_object['false_positive']}\n"
    )
