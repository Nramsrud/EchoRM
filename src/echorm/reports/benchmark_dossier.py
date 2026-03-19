"""First benchmark dossier rendering."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..eval.first_benchmark import FirstBenchmarkPackage


def build_first_benchmark_dossier(package: FirstBenchmarkPackage) -> str:
    """Build the first benchmark dossier."""
    demonstrated = "\n".join(
        f"- {item}" for item in package.demonstrated_capabilities
    )
    not_demonstrated = "\n".join(
        f"- {item}" for item in package.non_demonstrated_capabilities
    )
    limitations = "\n".join(f"- {item}" for item in package.limitations)
    case_lines = "\n".join(
        f"- {case.case_id}: type={case.benchmark_type}, "
        f"evidence={case.evidence_level}, metric={case.metric_family}, "
        f"summary_metric={case.summary_metric:.3f}, quality={case.quality_flag}"
        for case in package.cases
    )
    warnings = ", ".join(package.warnings) if package.warnings else "none"
    return (
        f"# First Benchmark Dossier {package.run_id}\n\n"
        f"- Profile: {package.profile}\n"
        f"- Package type: {package.package_type}\n"
        f"- Readiness: {package.readiness}\n"
        f"- Scope: {package.benchmark_scope}\n"
        f"- Warnings: {warnings}\n\n"
        "## Demonstrated Capability\n\n"
        f"{demonstrated}\n\n"
        "## Not Yet Demonstrated\n\n"
        f"{not_demonstrated}\n\n"
        "## Limitations\n\n"
        f"{limitations}\n\n"
        "## Cases\n\n"
        f"{case_lines}\n"
    )


def build_first_benchmark_case_summary(case_payload: Mapping[str, object]) -> str:
    """Build a concise markdown summary for one first benchmark case."""
    return (
        f"# Case {case_payload['case_id']}\n\n"
        f"- Benchmark type: {case_payload['benchmark_type']}\n"
        f"- Evidence level: {case_payload['evidence_level']}\n"
        f"- Metric family: {case_payload['metric_family']}\n"
        f"- Notes: {case_payload['notes']}\n"
    )
