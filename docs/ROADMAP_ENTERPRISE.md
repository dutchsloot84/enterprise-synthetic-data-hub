# Enterprise Readiness Roadmap

## Current state (POC)
- Demo flows are validated via `make demo-gate` / `python -m pytest -m demo -q` and the scripted runner `scripts/run_demo_flow.py --skip-smoke`.
- Docker builds succeed on open networks using `docker build -t esdh:develop .` followed by containerized demo/test runs.
- Bootstrap scripts (`scripts/bootstrap_and_demo.*`) remain the primary “happy path” for new users on Unix/macOS and Windows PowerShell.

## Known gaps
- Docker builds on CSAA networks cannot reach public PyPI due to TLS inspection; an Internal PyPI mirror is required.
- Windows portability is constrained when `make` is unavailable and when shells block bash-based orchestration.
- CI container builds have not been validated against enterprise network constraints.
- Dependency pinning/lockfiles and image signing are not yet enforced.

## Next steps to Pilot
- Stand up and document an Internal PyPI mirror/proxy; wire builds/tests to it via `PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, and `PIP_TRUSTED_HOST`.
- Enable CI to build and smoke-test the Docker image using the mirror and publish to an internal registry.
- Provide a fully scripted demo flow that avoids bash dependencies on Windows (python-native entrypoints).
- Capture platform portability guidance (Docker Desktop vs. Linux daemon vs. Windows hosts) in operator docs.

## Beyond Pilot
- Publish versioned, signed images with SBOMs and vulnerability scanning in the pipeline.
- Introduce dependency lockfiles and reproducible builds to reduce supply-chain drift.
- Add artifact caching for snapshot generation and internal mirrors for other ecosystems as needed.
- Automate reproducible demo snapshots and make them available as tested artifacts.

## Issues to track
- Add Internal PyPI mirror support in CI (mirror configuration, secrets management, and validation jobs).
- Document approved internal index URL and onboarding steps once the mirror exists.
- Make the demo flow Windows-safe without bash (python-native API start and orchestration).
