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

if [[ -f "${PID_FILE}" ]]; then
    PID=$(cat "${PID_FILE}")
    if kill -0 "$PID" >/dev/null 2>&1; then
        log "Stopping Flask demo API (pid=${PID})"
        kill "$PID" >/dev/null 2>&1 || true
        wait "$PID" >/dev/null 2>&1 || true
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
