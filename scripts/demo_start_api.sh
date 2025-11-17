#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${DEMO_API_PORT:-5050}"
export FLASK_APP=enterprise_synthetic_data_hub.api.app:app
export PYTHONPATH="${REPO_ROOT}/src"

echo "Starting Flask API on port ${PORT}..."
flask run --port "${PORT}" --no-debugger --no-reload &
API_PID=$!
trap 'kill ${API_PID} >/dev/null 2>&1 || true' EXIT
sleep 2

echo "Health check:"
curl --silent --show-error "http://127.0.0.1:${PORT}/healthz" \
  | PYTHONPATH="${REPO_ROOT}/src" python - <<'PY'
import json,sys
payload=json.load(sys.stdin)
print(payload.get("status"))
PY

echo "Previewing /generate/person payload (first 2 rows)..."
curl --silent --show-error -X POST "http://127.0.0.1:${PORT}/generate/person" \
  -H 'Content-Type: application/json' \
  -d '{"records": 3, "randomize": true}' \
  | PYTHONPATH="${REPO_ROOT}/src" python - <<'PY'
import json,sys
payload=json.load(sys.stdin)
print(json.dumps(payload.get("persons", [])[:2], indent=2))
PY

python "${REPO_ROOT}/scripts/demo_data.py" --use-api --api-url "http://127.0.0.1:${PORT}" --records 3 --preview 1 --endpoint bundle
