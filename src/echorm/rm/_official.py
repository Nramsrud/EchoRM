"""Helpers for invoking official RM backends."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .base import TimeSeries


def repo_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[3]


def runtime_root() -> Path:
    """Return the runtime scratch directory for backend execution."""
    root = repo_root() / "artifacts" / "runtime"
    root.mkdir(parents=True, exist_ok=True)
    return root


def rm_literal_python() -> Path:
    """Return the Python interpreter for the dedicated literal RM toolchain."""
    candidates = (
        Path.home() / ".conda-envs" / "rm-literal" / "bin" / "python",
        repo_root() / ".conda-envs" / "rm-literal" / "bin" / "python",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def series_payload(series: TimeSeries) -> dict[str, object]:
    """Serialize a time series for subprocess-backed adapters."""
    return {
        "channel": series.channel,
        "mjd_obs": list(series.mjd_obs),
        "values": list(series.values),
        "errors": default_errors(series),
    }


def default_errors(series: TimeSeries) -> list[float]:
    """Build a conservative uncertainty vector from sampled values."""
    if not series.values:
        return []
    amplitude = max(series.values) - min(series.values)
    baseline = max(amplitude * 0.05, 1e-6)
    return [baseline for _ in series.values]


def percentile_bounds(samples: list[float]) -> tuple[float, float, float]:
    """Compute median and approximate 16/84 percentile bounds."""
    if not samples:
        return (0.0, 0.0, 0.0)
    ordered = sorted(float(item) for item in samples)
    median = _percentile(ordered, 0.5)
    lower = _percentile(ordered, 0.16)
    upper = _percentile(ordered, 0.84)
    return (median, lower, upper)


def _percentile(values: list[float], q: float) -> float:
    if len(values) == 1:
        return values[0]
    position = q * (len(values) - 1)
    left = int(position)
    right = min(left + 1, len(values) - 1)
    weight = position - left
    return values[left] * (1.0 - weight) + values[right] * weight


def run_json_backend(
    *,
    python_path: Path,
    code: str,
    payload: dict[str, object],
    timeout_sec: int = 300,
) -> dict[str, Any]:
    """Execute a backend helper script and parse its JSON output."""
    runtime = runtime_root()
    with tempfile.TemporaryDirectory(dir=runtime) as tmpdir:
        payload_path = Path(tmpdir) / "payload.json"
        payload_path.write_text(json.dumps(payload), encoding="utf-8")
        command = [str(python_path), "-c", code, str(payload_path)]
        process = subprocess.Popen(
            command,
            cwd=repo_root(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout_sec)
        except subprocess.TimeoutExpired as exc:
            os.killpg(process.pid, signal.SIGTERM)
            stdout, stderr = process.communicate()
            raise RuntimeError(
                f"backend timed out after {timeout_sec}s"
            ) from exc
        result = subprocess.CompletedProcess(
            command,
            process.returncode,
            stdout,
            stderr,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError("backend returned no JSON payload")
        for line in reversed(lines):
            candidates = [line]
            if "{" in line and "}" in line:
                start = line.find("{")
                end = line.rfind("}") + 1
                if start < end:
                    candidates.append(line[start:end])
            for candidate in candidates:
                try:
                    parsed = json.loads(candidate)
                except json.JSONDecodeError:
                    continue
                if not isinstance(parsed, dict):
                    continue
                return parsed
        raise RuntimeError("backend stdout did not contain a JSON mapping")
