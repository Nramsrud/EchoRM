"""Benchmark review loaders and read-only web rendering."""

from __future__ import annotations

import json
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


def load_root_index(artifact_root: Path) -> dict[str, object]:
    """Load the root benchmark-run index."""
    index_path = artifact_root / "index.json"
    if not index_path.exists():
        return {"runs": []}
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("root benchmark index must be a mapping")
    return payload


def load_run_detail(artifact_root: Path, run_id: str) -> dict[str, object]:
    """Load one run-detail payload."""
    path = artifact_root / run_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("run detail must be a mapping")
    return payload


def load_case_detail(
    artifact_root: Path,
    run_id: str,
    case_id: str,
) -> dict[str, object]:
    """Load one benchmark-case payload."""
    path = artifact_root / run_id / "cases" / case_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("case detail must be a mapping")
    return payload


def load_group_detail(
    artifact_root: Path,
    run_id: str,
    group: str,
    item_id: str,
) -> dict[str, object]:
    """Load one grouped benchmark payload."""
    path = artifact_root / run_id / group / item_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("group detail must be a mapping")
    return payload


def _html_page(title: str, body: str) -> str:
    return (
        "<!doctype html>"
        "<html><head><meta charset='utf-8'>"
        f"<title>{escape(title)}</title>"
        "<style>"
        "body{font-family:Georgia,serif;margin:2rem;background:#f5f1e8;color:#1e2a26;}"
        "a{color:#1a5a5a;text-decoration:none;} a:hover{text-decoration:underline;}"
        "table{border-collapse:collapse;width:100%;margin:1rem 0;}"
        "th,td{border:1px solid #c7bda9;padding:0.5rem;text-align:left;"
        "vertical-align:top;}"
        "pre{background:#fff;border:1px solid #c7bda9;padding:1rem;overflow:auto;}"
        ".banner{padding:0.75rem 1rem;background:#dfe8d3;border:1px solid #aab89c;}"
        ".warn{background:#f7dfc2;border-color:#c28f52;}"
        "</style></head><body>"
        f"{body}</body></html>"
    )


def render_root_index_html(root_index: dict[str, object]) -> str:
    """Render the benchmark-run index page."""
    runs = root_index.get("runs", [])
    rows = []
    for run in runs if isinstance(runs, list) else []:
        if not isinstance(run, dict):
            continue
        run_id = escape(str(run.get("run_id", "")))
        rows.append(
            "<tr>"
            f"<td><a href='/runs/{run_id}'>{run_id}</a></td>"
            f"<td>{escape(str(run.get('profile', '')))}</td>"
            f"<td>{escape(str(run.get('package_type', 'readiness')))}</td>"
            f"<td>{escape(str(run.get('readiness', '')))}</td>"
            f"<td>{escape(str(run.get('case_count', '')))}</td>"
            "</tr>"
        )
    body = (
        "<h1>Benchmark Review</h1>"
        "<div class='banner'>Read-only review surface over benchmark "
        "artifacts.</div>"
        "<p><a href='/api/runs'>JSON index</a></p>"
        "<table><thead><tr><th>Run</th><th>Profile</th><th>Type</th>"
        "<th>Readiness</th><th>Cases</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )
    return _html_page("Benchmark Review", body)


def render_run_detail_html(run: dict[str, object]) -> str:
    """Render one run-detail page."""
    summary = run.get("summary", {})
    benchmark_scope = run.get("benchmark_scope")
    package_type = run.get("package_type")
    verification = run.get("verification", [])
    tools = run.get("tools", [])
    cases = run.get("cases", [])
    objects = run.get("objects", [])
    tasks = run.get("tasks", [])
    cohorts = run.get("cohorts", [])
    comparisons = run.get("comparisons", [])
    audit_conditions = run.get("audit_conditions", [])
    warnings_object = run.get("warnings", [])
    warnings = (
        [str(value) for value in warnings_object]
        if isinstance(warnings_object, list)
        else []
    )
    warning_text = ", ".join(warnings) or "none"

    verification_rows = []
    for record in verification if isinstance(verification, list) else []:
        if not isinstance(record, dict):
            continue
        verification_rows.append(
            "<tr>"
            f"<td>{escape(str(record.get('name', '')))}</td>"
            f"<td>{escape(str(record.get('ok', '')))}</td>"
            f"<td>{escape(str(record.get('detail', '')))}</td>"
            "</tr>"
        )

    tool_rows = []
    for tool in tools if isinstance(tools, list) else []:
        if not isinstance(tool, dict):
            continue
        tool_rows.append(
            "<tr>"
            f"<td>{escape(str(tool.get('name', '')))}</td>"
            f"<td>{escape(str(tool.get('available', '')))}</td>"
            f"<td>{escape(str(tool.get('detail', '')))}</td>"
            "</tr>"
        )

    case_rows = []
    for case in cases if isinstance(cases, list) else []:
        if not isinstance(case, dict):
            continue
        case_id = escape(str(case.get("case_id", "")))
        case_type = escape(
            str(case.get("benchmark_type", case.get("family", "")))
        )
        case_evidence = escape(
            str(case.get("evidence_level", case.get("lag_error", "")))
        )
        case_quality = escape(
            str(case.get("quality_flag", case.get("false_positive", "")))
        )
        case_rows.append(
            "<tr>"
            f"<td><a href='/runs/{escape(str(run.get('run_id', '')))}"
            f"/cases/{case_id}'>{case_id}</a></td>"
            f"<td>{case_type}</td>"
            f"<td>{case_evidence}</td>"
            f"<td>{case_quality}</td>"
            "</tr>"
        )

    object_rows = []
    for item in objects if isinstance(objects, list) else []:
        if not isinstance(item, dict):
            continue
        object_id = escape(str(item.get("object_uid", "")))
        object_rows.append(
            "<tr>"
            f"<td><a href='/runs/{escape(str(run.get('run_id', '')))}"
            f"/objects/{object_id}'>{object_id}</a></td>"
            f"<td>{escape(str(item.get('tier', '')))}</td>"
            f"<td>{escape(str(item.get('evidence_level', '')))}</td>"
            f"<td>{escape(str(item.get('quality_flag', '')))}</td>"
            f"<td>{escape(str(item.get('primary_metric', '')))}</td>"
            "</tr>"
        )

    task_rows = []
    for item in tasks if isinstance(tasks, list) else []:
        if not isinstance(item, dict):
            continue
        task_id = escape(str(item.get("task_id", "")))
        task_rows.append(
            "<tr>"
            f"<td><a href='/runs/{escape(str(run.get('run_id', '')))}"
            f"/tasks/{task_id}'>{task_id}</a></td>"
            f"<td>{escape(str(item.get('mode', '')))}</td>"
            f"<td>{escape(str(item.get('benchmark_type', '')))}</td>"
            "</tr>"
        )

    cohort_rows = []
    for item in cohorts if isinstance(cohorts, list) else []:
        if not isinstance(item, dict):
            continue
        cohort_id = escape(str(item.get("cohort_id", "")))
        cohort_rows.append(
            "<tr>"
            f"<td><a href='/runs/{escape(str(run.get('run_id', '')))}"
            f"/cohorts/{cohort_id}'>{cohort_id}</a></td>"
            f"<td>{escape(str(item.get('accuracy', '')))}</td>"
            f"<td>{escape(str(item.get('time_to_decision_sec', '')))}</td>"
            f"<td>{escape(str(item.get('training_level', '')))}</td>"
            "</tr>"
        )

    comparison_rows = []
    for item in comparisons if isinstance(comparisons, list) else []:
        if not isinstance(item, dict):
            continue
        keys = sorted(item)
        cells = "".join(
            f"<td>{escape(str(item.get(key, '')))}</td>" for key in keys[:4]
        )
        comparison_rows.append(f"<tr>{cells}</tr>")

    audit_rows = []
    for item in audit_conditions if isinstance(audit_conditions, list) else []:
        if not isinstance(item, dict):
            continue
        audit_rows.append(
            "<tr>"
            f"<td>{escape(str(item.get('condition', '')))}</td>"
            f"<td>{escape(str(item.get('ok', '')))}</td>"
            f"<td>{escape(str(item.get('detail', '')))}</td>"
            "</tr>"
        )

    banner_class = "banner warn" if run.get("readiness") != "ready" else "banner"
    run_id = escape(str(run.get("run_id", "")))
    scope_line = (
        f"<p>Scope: {escape(str(benchmark_scope))}</p>"
        if benchmark_scope is not None
        else ""
    )
    body = (
        f"<p><a href='/'>All runs</a> | <a href='/api/runs/{run_id}'>JSON</a></p>"
        f"<h1>Run {run_id}</h1>"
        f"<div class='{banner_class}'>Readiness: "
        f"{escape(str(run.get('readiness', '')))}"
        f" | Warnings: {escape(warning_text)}</div>"
        f"<p>Package type: {escape(str(package_type or 'readiness'))}</p>"
        f"{scope_line}"
        "<h2>Summary</h2>"
        f"<pre>{escape(json.dumps(summary, indent=2, sort_keys=True))}</pre>"
        "<h2>Verification</h2>"
        "<table><thead><tr><th>Check</th><th>OK</th><th>Detail</th></tr></thead>"
        f"<tbody>{''.join(verification_rows)}</tbody></table>"
        "<h2>Tools</h2>"
        "<table><thead><tr><th>Tool</th><th>Available</th><th>Detail</th></tr></thead>"
        f"<tbody>{''.join(tool_rows)}</tbody></table>"
        "<h2>Cases</h2>"
        "<table><thead><tr><th>Case</th><th>Type</th><th>Evidence</th>"
        "<th>Quality</th></tr></thead>"
        f"<tbody>{''.join(case_rows)}</tbody></table>"
        "<h2>Objects</h2>"
        "<table><thead><tr><th>Object</th><th>Tier</th><th>Evidence</th>"
        "<th>Quality</th><th>Primary Metric</th></tr></thead>"
        f"<tbody>{''.join(object_rows)}</tbody></table>"
        "<h2>Tasks</h2>"
        "<table><thead><tr><th>Task</th><th>Mode</th><th>Type</th></tr></thead>"
        f"<tbody>{''.join(task_rows)}</tbody></table>"
        "<h2>Cohorts</h2>"
        "<table><thead><tr><th>Cohort</th><th>Accuracy</th>"
        "<th>Time To Decision</th><th>Training Level</th></tr></thead>"
        f"<tbody>{''.join(cohort_rows)}</tbody></table>"
        "<h2>Comparisons</h2>"
        f"<table><tbody>{''.join(comparison_rows)}</tbody></table>"
        "<h2>Claims Audit</h2>"
        "<table><thead><tr><th>Condition</th><th>OK</th><th>Detail</th></tr></thead>"
        f"<tbody>{''.join(audit_rows)}</tbody></table>"
        f"<p><a href='/files/{run_id}/summary.md'>Run summary file</a></p>"
        f"<p><a href='/files/{run_id}/dossier.md'>Benchmark dossier</a></p>"
    )
    return _html_page(f"Run {run.get('run_id', '')}", body)


def render_case_detail_html(run_id: str, case: dict[str, object]) -> str:
    """Render one case-detail page."""
    case_id = str(case.get("case_id", ""))
    artifact_paths = case.get("artifact_paths", {})
    file_links = []
    artifact_items = (
        artifact_paths.items() if isinstance(artifact_paths, dict) else []
    )
    for label, path in artifact_items:
        file_links.append(
            f"<li><a href='/files/{escape(str(path))}'>{escape(str(label))}</a></li>"
        )
    body = (
        f"<p><a href='/runs/{escape(run_id)}'>Back to run</a> | "
        f"<a href='/api/runs/{escape(run_id)}/cases/{escape(case_id)}'>JSON</a></p>"
        f"<h1>Case {escape(case_id)}</h1>"
        f"<ul>{''.join(file_links)}</ul>"
        f"<pre>{escape(json.dumps(case, indent=2, sort_keys=True))}</pre>"
    )
    return _html_page(f"Case {case_id}", body)


def render_group_detail_html(
    *,
    run_id: str,
    group: str,
    payload: dict[str, object],
    item_id_key: str,
) -> str:
    """Render one grouped detail page."""
    item_id = str(payload.get(item_id_key, ""))
    artifact_paths = payload.get("artifact_paths", {})
    file_links = []
    artifact_items = (
        artifact_paths.items() if isinstance(artifact_paths, dict) else []
    )
    for label, path in artifact_items:
        file_links.append(
            f"<li><a href='/files/{escape(str(path))}'>{escape(str(label))}</a></li>"
        )
    body = (
        f"<p><a href='/runs/{escape(run_id)}'>Back to run</a> | "
        f"<a href='/api/runs/{escape(run_id)}/{escape(group)}/"
        f"{escape(item_id)}'>JSON</a></p>"
        f"<h1>{escape(group[:-1].capitalize())} {escape(item_id)}</h1>"
        f"<ul>{''.join(file_links)}</ul>"
        f"<pre>{escape(json.dumps(payload, indent=2, sort_keys=True))}</pre>"
    )
    return _html_page(f"{group[:-1].capitalize()} {item_id}", body)


def _safe_file_path(artifact_root: Path, relative_path: str) -> Path:
    candidate = (artifact_root / relative_path).resolve()
    root = artifact_root.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("requested file path escapes artifact root")
    return candidate


def build_review_handler(artifact_root: Path) -> type[BaseHTTPRequestHandler]:
    """Build a handler class bound to one artifact root."""

    class ReviewHandler(BaseHTTPRequestHandler):
        def _send_text(
            self,
            *,
            body: str,
            content_type: str,
            status: HTTPStatus = HTTPStatus.OK,
        ) -> None:
            encoded = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def _send_json(self, payload: dict[str, object]) -> None:
            self._send_text(
                body=json.dumps(payload, indent=2, sort_keys=True),
                content_type="application/json; charset=utf-8",
            )

        def _send_file(self, relative_path: str) -> None:
            try:
                file_path = _safe_file_path(artifact_root, relative_path)
            except ValueError:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            if not file_path.exists() or not file_path.is_file():
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            content_type = "text/plain; charset=utf-8"
            if file_path.suffix == ".json":
                content_type = "application/json; charset=utf-8"
            elif file_path.suffix == ".md":
                content_type = "text/markdown; charset=utf-8"
            self._send_text(
                body=file_path.read_text(encoding="utf-8"),
                content_type=content_type,
            )

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = unquote(parsed.path)
            if path == "/":
                self._send_text(
                    body=render_root_index_html(load_root_index(artifact_root)),
                    content_type="text/html; charset=utf-8",
                )
                return
            if path == "/api/runs":
                self._send_json(load_root_index(artifact_root))
                return
            if path.startswith("/api/runs/"):
                segments = [segment for segment in path.split("/") if segment]
                if len(segments) == 3:
                    _, _, run_id = segments
                    self._send_json(load_run_detail(artifact_root, run_id))
                    return
                if len(segments) == 5 and segments[3] == "cases":
                    _, _, run_id, _, case_id = segments
                    self._send_json(load_case_detail(artifact_root, run_id, case_id))
                    return
                if len(segments) == 5 and segments[3] in {
                    "objects",
                    "tasks",
                    "cohorts",
                }:
                    _, _, run_id, group, item_id = segments
                    self._send_json(
                        load_group_detail(artifact_root, run_id, group, item_id)
                    )
                    return
            if path.startswith("/runs/"):
                segments = [segment for segment in path.split("/") if segment]
                if len(segments) == 2:
                    _, run_id = segments
                    run_detail = load_run_detail(artifact_root, run_id)
                    self._send_text(
                        body=render_run_detail_html(run_detail),
                        content_type="text/html; charset=utf-8",
                    )
                    return
                if len(segments) == 4 and segments[2] == "cases":
                    _, run_id, _, case_id = segments
                    self._send_text(
                        body=render_case_detail_html(
                            run_id,
                            load_case_detail(artifact_root, run_id, case_id),
                        ),
                        content_type="text/html; charset=utf-8",
                    )
                    return
                if len(segments) == 4 and segments[2] in {
                    "objects",
                    "tasks",
                    "cohorts",
                }:
                    _, run_id, group, item_id = segments
                    item = load_group_detail(artifact_root, run_id, group, item_id)
                    item_id_key = {
                        "objects": "object_uid",
                        "tasks": "task_id",
                        "cohorts": "cohort_id",
                    }[group]
                    self._send_text(
                        body=render_group_detail_html(
                            run_id=run_id,
                            group=group,
                            payload=item,
                            item_id_key=item_id_key,
                        ),
                        content_type="text/html; charset=utf-8",
                    )
                    return
            if path.startswith("/files/"):
                self._send_file(path.removeprefix("/files/"))
                return
            self.send_error(HTTPStatus.NOT_FOUND)

        def log_message(self, format: str, *args: object) -> None:
            return

    return ReviewHandler


def create_review_server(
    *,
    artifact_root: Path,
    host: str,
    port: int,
) -> ThreadingHTTPServer:
    """Create a thread-capable read-only review server."""
    handler = build_review_handler(artifact_root)
    return ThreadingHTTPServer((host, port), handler)
