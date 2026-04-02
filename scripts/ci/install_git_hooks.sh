#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

chmod +x \
  .githooks/pre-commit \
  .githooks/pre-push \
  scripts/ci/run_local_scientific_validation.sh \
  scripts/ci/install_git_hooks.sh

git config core.hooksPath .githooks

echo "Installed repository git hooks from $ROOT/.githooks"
