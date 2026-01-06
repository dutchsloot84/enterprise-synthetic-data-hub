"""Flask application that exposes the governed generator for demo use."""
from __future__ import annotations

import logging
from http import HTTPStatus
import secrets
from typing import Any, Tuple

from flask import Flask, jsonify, request, render_template_string

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import (
    SnapshotBundle,
    describe_generation_plan,
    generate_snapshot_bundle,
)

DEFAULT_RECORDS = 5
logger = logging.getLogger(__name__)

DEMO_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Enterprise Synthetic Data Hub Demo</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; }
      .panel { border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; }
      label { display: block; margin-top: 0.5rem; }
      pre { background: #f7f7f7; padding: 1rem; overflow: auto; }
    </style>
  </head>
  <body>
    <h1>Enterprise Synthetic Data Hub Demo</h1>
    <div class="panel">
      <p>Use this lightweight UI to hit the live API without writing code.</p>
      <label>Entity
        <select id="entity">
          <option value="person">Persons</option>
          <option value="vehicle">Vehicles</option>
          <option value="profile">Profiles</option>
          <option value="bundle">Full Bundle</option>
        </select>
      </label>
      <label>Records <input id="records" type="number" value="3" min="1"></label>
      <label>Seed <input id="seed" type="text" placeholder="20240601"></label>
      <label><input id="randomize" type="checkbox"> Randomize seed</label>
      <label>API Key (optional) <input id="api_key" type="text" placeholder="X-API-Key"></label>
      <button onclick="callApi()">Generate</button>
      <button onclick="loadHealth()">Health</button>
    </div>
    <div class="panel">
      <h3>Response</h3>
      <pre id="response">(waiting)</pre>
    </div>
    <script>
      async function callApi() {
        const entity = document.getElementById('entity').value;
        const records = parseInt(document.getElementById('records').value, 10);
        const seed = document.getElementById('seed').value;
        const randomize = document.getElementById('randomize').checked;
        const apiKey = document.getElementById('api_key').value;
        const payload = {records: records, seed: seed || undefined, randomize: randomize};
        const headers = {"Content-Type": "application/json"};
        if (apiKey) { headers["X-API-Key"] = apiKey; }
        const resp = await fetch(`/generate/${entity}`, {method: "POST", headers, body: JSON.stringify(payload)});
        const data = await resp.json();
        document.getElementById('response').innerText = JSON.stringify(data, null, 2);
      }
      async function loadHealth() {
        const apiKey = document.getElementById('api_key').value;
        const headers = {};
        if (apiKey) { headers["X-API-Key"] = apiKey; }
        const resp = await fetch("/healthz", {headers});
        const data = await resp.json();
        document.getElementById('response').innerText = JSON.stringify(data, null, 2);
      }
    </script>
  </body>
</html>
"""


def _parse_request_payload() -> Tuple[int, int | None]:
    payload: dict[str, Any] = request.get_json(silent=True) or {}
    records = payload.get("records", DEFAULT_RECORDS)
    if not isinstance(records, int) or records <= 0:
        raise ValueError("'records' must be a positive integer")

    seed = payload.get("seed")
    randomize = payload.get("randomize", False)
    if isinstance(seed, str) and seed.lower() == "random":
        randomize = True
        seed = None
    if randomize:
        logger.warning("API request using randomized seed", extra={"endpoint": request.path})
        return records, secrets.randbelow(1_000_000_000)
    if seed is None:
        return records, None
    if isinstance(seed, int):
        return records, seed
    if isinstance(seed, str) and seed.isdigit():
        return records, int(seed)
    raise ValueError("'seed' must be an integer, 'random', or omitted")


def _bundle_to_response(bundle: SnapshotBundle) -> dict[str, Any]:
    return {
        "metadata": bundle.metadata.model_dump(mode="json"),
        "persons": bundle.persons,
        "vehicles": bundle.vehicles,
        "profiles": bundle.profiles,
    }


def _generate_subset(entity: str, bundle: SnapshotBundle) -> dict[str, Any]:
    payload = {"metadata": bundle.metadata.model_dump(mode="json")}
    payload[entity] = getattr(bundle, entity)
    payload["record_count"] = len(payload[entity])
    return payload


def create_app() -> Flask:
    app = Flask(__name__)

    def _error_response(message: str, *, status: HTTPStatus = HTTPStatus.BAD_REQUEST):
        return (
            jsonify({"error": {"code": "invalid_request", "message": message}}),
            status,
        )

    @app.before_request
    def _check_api_key():
        required_api_key = settings.demo_api_key
        if not required_api_key:
            return None
        provided = request.headers.get("X-API-Key") or request.args.get("api_key")
        if provided == required_api_key:
            return None
        logger.warning("Request rejected due to missing/invalid API key", extra={"path": request.path})
        return _error_response("API key required for this endpoint", status=HTTPStatus.UNAUTHORIZED)

    @app.get("/healthz")
    def healthz():
        return jsonify(
            {
                "status": "ok",
                "dataset_version": settings.dataset_version,
                "default_seed": settings.random_seed,
                "target_records": settings.target_person_records,
                "version": settings.dataset_version,
                "seed": settings.random_seed,
                "plan": {"steps": describe_generation_plan()},
            }
        )

    def _handle_generation(entity: str | None = None):
        try:
            records, seed = _parse_request_payload()
        except ValueError as exc:
            return _error_response(str(exc))
        bundle = generate_snapshot_bundle(num_records=records, seed=seed)
        if entity:
            payload = _generate_subset(entity, bundle)
        else:
            payload = _bundle_to_response(bundle)
        payload["seed"] = seed if seed is not None else settings.random_seed
        payload["records_requested"] = records
        return jsonify(payload)

    @app.post("/generate/person")
    def generate_person():
        return _handle_generation("persons")

    @app.post("/generate/vehicle")
    def generate_vehicle():
        return _handle_generation("vehicles")

    @app.post("/generate/profile")
    def generate_profile():
        return _handle_generation("profiles")

    @app.post("/generate/bundle")
    def generate_bundle():
        return _handle_generation(None)

    @app.get("/demo")
    def demo():
        return render_template_string(DEMO_TEMPLATE)

    return app


app = create_app()


def main() -> None:  # pragma: no cover - convenience entry point
    app.run(debug=True)


if __name__ == "__main__":  # pragma: no cover
    main()
