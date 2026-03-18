# 0001 Foundation Baseline Plan

## Goal

Prepare EchoRM for staged implementation by stabilizing the public repository baseline and the Python research scaffold expected by the authority documents.

## Steps

1. Establish the public documentation standard and the public/private repository boundary.
2. Keep the minimal Python package, tests, and CI aligned with the Python 3.12 baseline.
3. Refresh `README.md`, `AGENTS.md`, and `ark/resources/lessons-learned.md` so they reflect the authority documents and the documentation standard.
4. Create the initial numbered work structure and reserve the next work packages.
5. Re-validate the Python quality commands.

## Exit Criteria

- `python3 -m pip install -e .[dev]`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- `python3 -m pytest`
- `README.md` and `AGENTS.md` state the public documentation rules consistently
