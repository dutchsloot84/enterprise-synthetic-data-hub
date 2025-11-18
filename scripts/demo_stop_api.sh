#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT_FILE="${REPO_ROOT}/.demo_api_port"
PID_FILE="${REPO_ROOT}/.demo_api_pid"
QUIET="0"
if [[ "${1:-}" == "--quiet" ]]; then
    QUIET="1"
fi

log() {
    if [[ "$QUIET" == "1" ]]; then
        return
    fi
    echo "[API] $*"
}

validate_pid() {
    local pid="$1"
    if ! kill -0 "$pid" >/dev/null 2>&1; then
        return 1
    fi
    if ! command -v ps >/dev/null 2>&1; then
        return 0
    fi
    local cmd
    cmd=$(ps -p "$pid" -o command= 2>/dev/null || ps -p "$pid" -o args= 2>/dev/null || true)
    if [[ -z "$cmd" ]]; then
        return 1
    fi
    if [[ "$cmd" == *python* && "$cmd" == *enterprise_synthetic_data_hub* ]]; then
        return 0
    fi
    return 2
}

if [[ -f "${PID_FILE}" ]]; then
    PID=$(cat "${PID_FILE}")
    validate_pid "$PID"
    status=$?
    if [[ "$status" -eq 0 ]]; then
        log "Stopping Flask demo API (pid=${PID})"
        kill "$PID" >/dev/null 2>&1 || true
        wait "$PID" >/dev/null 2>&1 || true
    elif [[ "$status" -eq 2 ]]; then
        log "PID ${PID} does not look like an enterprise_synthetic_data_hub Flask server; skipping kill."
    else
        log "PID ${PID} not running."
    fi
    rm -f "${PID_FILE}"
else
    log "No PID file found (nothing to stop)."
fi

if [[ -f "${PORT_FILE}" ]]; then
    rm -f "${PORT_FILE}"
fi
