#!/usr/bin/env bash
set -euo pipefail

# Avoid MSYS path/URL rewriting in Git Bash.
export MSYS2_ARG_CONV_EXCL="*"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT_FILE="${REPO_ROOT}/.demo_api_port"
PID_FILE="${REPO_ROOT}/.demo_api_pid"
CONFIG_FILE="${REPO_ROOT}/config/demo.yaml"
PROFILE_NAME="${DEMO_PROFILE:-baseline}"
export PYTHONPATH="${REPO_ROOT}/src"
export DEMO_CONFIG_FILE="${CONFIG_FILE}"

log() {
    echo "[API] $*"
}

quiet_stop() {
    if [[ -x "${REPO_ROOT}/scripts/demo_stop_api.sh" ]]; then
        DEMO_STOP_QUIET=1 "${REPO_ROOT}/scripts/demo_stop_api.sh" --quiet >/dev/null 2>&1 || true
    fi
}

quiet_stop

if [[ ! -f "${CONFIG_FILE}" ]]; then
    log "Config file ${CONFIG_FILE} is missing. Run from repo root."
    exit 1
fi

HOST=$(python - <<'PY'
import os, pathlib, yaml
config_path = pathlib.Path(os.environ["DEMO_CONFIG_FILE"])
data = yaml.safe_load(config_path.read_text()) or {}
api = data.get("api") or {}
print(api.get("default_host", "127.0.0.1"))
PY
)
DEFAULT_PORT=$(python - <<'PY'
import os, pathlib, yaml
config_path = pathlib.Path(os.environ["DEMO_CONFIG_FILE"])
data = yaml.safe_load(config_path.read_text()) or {}
api = data.get("api") or {}
print(api.get("default_port", 5000))
PY
)
HEALTH_ENDPOINT=$(python - <<'PY'
import os, pathlib, yaml
config_path = pathlib.Path(os.environ["DEMO_CONFIG_FILE"])
data = yaml.safe_load(config_path.read_text()) or {}
api = data.get("api") or {}
print(api.get("health_endpoint", "/healthz"))
PY
)

BASE_PORT="${DEMO_API_PORT:-${DEFAULT_PORT}}"

port_in_use() {
    python - "$HOST" "$1" <<'PY'
import socket, sys
host = sys.argv[1]
port = int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.settimeout(0.25)
    result = sock.connect_ex((host, port))
    sys.exit(0 if result == 0 else 1)
PY
}

select_port() {
    local base="$1"
    for offset in 0 1 2 3 4; do
        local candidate=$((base + offset))
        if port_in_use "$candidate"; then
            log "Port ${candidate} busy. Trying next port."
            continue
        fi
        echo "$candidate"
        return 0
    done
    log "Unable to find open port between ${base} and $((base + 4))."
    exit 1
}

SELECTED_PORT=$(select_port "$BASE_PORT")
BASE_URL="http://${HOST}:${SELECTED_PORT}"

log "Starting Flask demo API on ${BASE_URL} (profile=${PROFILE_NAME})"
export FLASK_APP=enterprise_synthetic_data_hub.api.app:app
export FLASK_ENV=production

flask run --host "$HOST" --port "$SELECTED_PORT" --no-debugger --no-reload >/tmp/demo_api.log 2>&1 &
API_PID=$!
sleep 2

health_check() {
    python - "$BASE_URL" "$HEALTH_ENDPOINT" <<'PY'
import sys, urllib.request
base_url = sys.argv[1]
endpoint = sys.argv[2]
try:
    with urllib.request.urlopen(f"{base_url.rstrip('/')}{endpoint}", timeout=5) as resp:
        print(resp.read().decode())
except Exception as exc:  # pragma: no cover - shell utility
    sys.stderr.write(str(exc))
    sys.exit(1)
PY
}

if ! health_check >/tmp/demo_api_health.json; then
    log "API failed health check. Stopping."
    kill "$API_PID" >/dev/null 2>&1 || true
    exit 1
fi

printf "%s" "$SELECTED_PORT" >"${PORT_FILE}"
printf "%s" "$API_PID" >"${PID_FILE}"
log "PID recorded in ${PID_FILE}"
log "Port recorded in ${PORT_FILE}"
log "Health check response: $(cat /tmp/demo_api_health.json)"
