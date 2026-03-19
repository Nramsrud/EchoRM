# 0022 Benchmark Review Web Interface Plan

## Goal

Provide a read-only review interface that makes benchmark readiness and result quality inspectable from a browser without leaving the structured artifact surface.

## Implementation Approach

Build a small Python web service that reads benchmark readiness bundles from disk, exposes matching HTML and JSON views, and binds to a detected Tailscale address by default while allowing explicit localhost startup for local-only review.

## Steps

1. Add benchmark review loaders and route handlers for run indexes, run summaries, benchmark-case detail, and readiness detail.
2. Implement a network-binding helper that resolves a Tailscale IPv4 address by default and falls back to explicit localhost binding only when requested by flag.
3. Add a CLI entry point that launches the review service over a selected artifact root and serves both HTML and JSON views.
4. Add tests that validate route output, artifact navigation, and host-resolution behavior for Tailscale-first and localhost modes.

## Expected File Changes

### New Files

- `src/echorm/reports/review_app.py` - benchmark review loaders and HTML rendering
- `src/echorm/cli/review_app.py` - review server entry point and host selection
- `tests/test_benchmark_review_app.py` - review app and binding tests

### Modified Files

- `src/echorm/cli/__init__.py` - review CLI export if needed
- `tests/test_repository_skeleton.py` - additional CLI import coverage if needed

## Validation

- `python3 -m pytest tests/test_benchmark_review_app.py`
- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`

## Exit Criteria

- The review service renders benchmark runs, readiness state, and case detail from structured artifacts.
- HTML and JSON routes expose the same underlying benchmark information.
- Default host selection prefers Tailscale, with localhost available only by explicit flag.

## Risks

| Risk | Mitigation |
|------|------------|
| The review UI diverges from the artifact structure | Render pages directly from the same loaders that drive JSON output |
| Host-resolution logic becomes environment-fragile | Isolate resolution in a small helper and test both success and fallback paths |

## Dependencies

- `0021`
