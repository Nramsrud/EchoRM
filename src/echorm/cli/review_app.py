"""Benchmark review web application CLI entry point."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path

from ..reports.review_app import create_review_server

TextCommandRunner = Callable[[tuple[str, ...]], str | None]


def _default_command_runner(command: tuple[str, ...]) -> str | None:
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if process.returncode != 0:
        return None
    text = process.stdout.strip()
    return text or None


def resolve_tailscale_ipv4(
    *,
    run_command: TextCommandRunner | None = None,
) -> str | None:
    """Resolve a Tailscale IPv4 address from local tooling."""
    runner = run_command or _default_command_runner
    tailscale_text = runner(("tailscale", "ip", "-4"))
    if tailscale_text:
        first_line = tailscale_text.splitlines()[0].strip()
        if first_line:
            return first_line
    interface_text = runner(("ip", "-4", "addr", "show", "tailscale0"))
    if not interface_text:
        return None
    match = re.search(r"inet ([0-9.]+)/", interface_text)
    return match.group(1) if match else None


def resolve_bind_host(
    *,
    localhost: bool,
    host: str | None = None,
    run_command: TextCommandRunner | None = None,
) -> str:
    """Resolve the bind host for the review app."""
    if host is not None:
        return host
    if localhost:
        return "127.0.0.1"
    tailscale_host = resolve_tailscale_ipv4(run_command=run_command)
    if tailscale_host is None:
        raise RuntimeError(
            "could not resolve a Tailscale IPv4 address; use --localhost or --host"
        )
    return tailscale_host


def build_parser() -> argparse.ArgumentParser:
    """Build the benchmark review app CLI parser."""
    parser = argparse.ArgumentParser(prog="python -m echorm.cli.review_app")
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=Path("artifacts/benchmark_runs"),
        help="Artifact root containing benchmark readiness bundles.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7301,
        help="TCP port used by the review service.",
    )
    parser.add_argument(
        "--host",
        help="Explicit bind host override.",
    )
    parser.add_argument(
        "--localhost",
        action="store_true",
        help="Bind to 127.0.0.1 instead of resolving a Tailscale address.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the benchmark review app."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    artifact_root = args.artifact_root.resolve()
    host = resolve_bind_host(localhost=args.localhost, host=args.host)
    server = create_review_server(
        artifact_root=artifact_root,
        host=host,
        port=args.port,
    )
    print(f"http://{host}:{server.server_port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
