#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${REPO_ROOT}/src"
cd "${REPO_ROOT}"

if [[ "$#" -eq 0 ]]; then
    set -- python scripts/run_demo_flow.py
else
    set -- python scripts/run_demo_flow.py "$@"
fi

exec "$@"
