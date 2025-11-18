#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

log() {
    echo "[BOOTSTRAP] $*"
}

fail() {
    echo "[BOOTSTRAP] ERROR: $*" >&2
    exit 1
}

trap 'echo "[BOOTSTRAP] ERROR: Bootstrap aborted. Please review the logs above." >&2' ERR

log "Detecting Python interpreter..."
PYTHON_BIN=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PYTHON_BIN="$candidate"
        break
    fi
done
[[ -n "$PYTHON_BIN" ]] || fail "Python 3.10+ is required."

log "Checking Python version via $PYTHON_BIN"
if ! "$PYTHON_BIN" - <<'PY'
import sys
min_v = (3, 10)
max_v = (3, 13)
sys.exit(0 if min_v <= tuple(sys.version_info[:3]) < max_v else 1)
PY
then
    fail "Python version $($PYTHON_BIN -V) is not supported (need 3.10 - 3.12)."
fi

log "Creating virtual environment (.venv) if needed"
if [[ ! -d ".venv" ]]; then
    "$PYTHON_BIN" -m venv .venv
fi

log "Activating .venv"
# shellcheck source=/dev/null
source .venv/bin/activate

log "Installing project dependencies"
pip install --upgrade pip >/dev/null
pip install -e .[dev]

log "Sanity-checking package import"
python -c "import enterprise_synthetic_data_hub as pkg; print(getattr(pkg, '__version__', 'dev-build'))"

if command -v make >/dev/null 2>&1; then
    log "Running make demo"
    make demo
else
    log "Running Python fallback demo flow"
    python scripts/run_demo_flow.py
fi

log "Bootstrap completed successfully."
