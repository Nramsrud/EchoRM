# 0022 Benchmark Review Web Interface

## Summary

Provide a read-only web interface for navigating benchmark runs, inspecting readiness state, and reviewing result quality from structured benchmark bundles.

## Scope

- Serve benchmark-run indexes, run-detail views, benchmark-case views, and tool-readiness summaries from structured artifacts.
- Provide HTML and JSON endpoints for the same underlying review data.
- Default network binding to a detected Tailscale IPv4 address, with localhost binding available only by explicit flag.
- Preserve direct links to artifact files and structured records needed for audit and review.

## Non-Goals

- Authentication, remote write access, or Internet-facing deployment.
- Interactive artifact editing or benchmark execution from the browser.
- Discovery-pool review workflows.

## Global Constraints

- The interface must remain read-only and derive all views from structured benchmark bundles rather than hidden in-memory state.
- Default startup behavior must prefer a detected Tailscale IPv4 address and require explicit operator intent for localhost binding.

## Acceptance Criteria

- A tracked command can launch the review interface against a benchmark artifact root and render run, case, and readiness views.
- The service exposes both HTML and JSON views for benchmark metrics, verification outcomes, artifacts, and warnings.
- Default startup binds to a detected Tailscale address when available, while a localhost flag binds to `127.0.0.1`.

## Dependencies

- `0021`
