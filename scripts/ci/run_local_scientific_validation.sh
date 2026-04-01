#!/usr/bin/env bash
set -euo pipefail

HOOK_CONTEXT="${1:-manual}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RM_LITERAL_PREFIX="${RM_LITERAL_PREFIX:-$HOME/.conda-envs/rm-literal}"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[$HOOK_CONTEXT] missing required command: $1" >&2
    exit 1
  fi
}

scientific_runtimes_ready() {
  [[ -x "$RM_LITERAL_PREFIX/bin/python" ]] \
    && [[ -x "$ROOT/.uv-pypetal/bin/python" ]] \
    && [[ -x "$ROOT/.uv-litmus/bin/python" ]]
}

ensure_scientific_runtimes() {
  if scientific_runtimes_ready; then
    return
  fi
  require_command micromamba
  require_command uv
  echo "[$HOOK_CONTEXT] bootstrapping scientific runtimes"
  bash "$ROOT/scripts/ci/setup_scientific_runtimes.sh"
}

run_step() {
  local label="$1"
  shift
  echo "[$HOOK_CONTEXT] $label"
  "$@"
}

cd "$ROOT"

require_command python3
require_command snakemake
ensure_scientific_runtimes

run_step "ruff" python3 -m ruff check .
run_step "mypy" python3 -m mypy src tests
run_step "pytest" python3 -m pytest
run_step "snakemake dry-run" snakemake --snakefile workflows/Snakefile --dry-run
