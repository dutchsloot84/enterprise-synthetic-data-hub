#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
if [[ -f "$SCRIPT_PATH" ]]; then
    REPO_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
else
    REPO_ROOT=""
fi

find_repo_root() {
    local candidate="$1"
    while [[ -n "$candidate" && "$candidate" != "/" ]]; do
        if [[ -f "$candidate/pyproject.toml" && -d "$candidate/src" ]]; then
            echo "$candidate"
            return 0
        fi
        candidate="$(cd "$candidate/.." && pwd)"
    done
    return 1
}

if [[ -z "$REPO_ROOT" ]]; then
    if ! REPO_ROOT="$(find_repo_root "$PWD")"; then
        echo "[BOOTSTRAP] ERROR: Unable to locate the repository root. Clone the repo first." >&2
        exit 1
    fi
fi

cd "$REPO_ROOT"

TOTAL_STEPS=8
CURRENT_STEP=0

step() {
    CURRENT_STEP=$((CURRENT_STEP + 1))
    echo "[BOOTSTRAP ${CURRENT_STEP}/${TOTAL_STEPS}] $1"
}

fail() {
    echo "[BOOTSTRAP] ERROR: $1" >&2
    exit 1
}

trap 'echo "[BOOTSTRAP] ERROR: Bootstrap aborted. Please review the logs above." >&2' ERR

if [[ -t 0 && -t 1 ]]; then
    echo "[BOOTSTRAP] Detected interactive execution."
else
    echo "[BOOTSTRAP] Detected non-interactive execution (curl | bash safe mode)."
fi

PYTHON_BIN=""
step "Checking Python version..."
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PYTHON_BIN="$candidate"
        break
    fi
done
[[ -n "$PYTHON_BIN" ]] || fail "Python 3.10+ is required."
if ! "$PYTHON_BIN" - <<'PY'
import sys
min_v = (3, 10)
max_v = (3, 13)
sys.exit(0 if min_v <= tuple(sys.version_info[:3]) < max_v else 1)
PY
then
    fail "Python version $($PYTHON_BIN -V) is not supported (need 3.10 - 3.12)."
fi

step "Validating pip availability..."
if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
    fail "pip is not available for $PYTHON_BIN"
fi

step "Checking git installation..."
command -v git >/dev/null 2>&1 || fail "git is required for the demo."

step "Checking download tools (curl/wget)..."
if command -v curl >/dev/null 2>&1; then
    :
elif command -v wget >/dev/null 2>&1; then
    :
else
    fail "Either curl or wget must be installed to fetch artifacts."
fi

CONFIG_FILE="$REPO_ROOT/config/demo.yaml"
step "Validating config/demo.yaml..."
[[ -f "$CONFIG_FILE" ]] || fail "Missing $CONFIG_FILE (did you clone the full repo?)."

step "Preparing virtual environment (.venv)..."
if [[ ! -d ".venv" ]]; then
    "$PYTHON_BIN" -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

step "Installing project dependencies..."
python -m pip install --upgrade pip >/dev/null
python -m pip install -e .[dev]

step "Running guided demo..."
if command -v make >/dev/null 2>&1; then
    DEMO_PROFILE=${DEMO_PROFILE:-baseline} make demo
else
    python scripts/run_demo_flow.py
fi

echo "[BOOTSTRAP] Bootstrap completed successfully."
