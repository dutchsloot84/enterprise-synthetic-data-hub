"""Flask application that exposes the governed generator for demo use."""
from __future__ import annotations

from http import HTTPStatus
import secrets
from typing import Any, Tuple

from flask import Flask, jsonify, request

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import (
    SnapshotBundle,
    describe_generation_plan,
    generate_snapshot_bundle,
)

DEFAULT_RECORDS = 5


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

    return app


app = create_app()


def main() -> None:  # pragma: no cover - convenience entry point
    app.run(debug=True)


if __name__ == "__main__":  # pragma: no cover
    main()
