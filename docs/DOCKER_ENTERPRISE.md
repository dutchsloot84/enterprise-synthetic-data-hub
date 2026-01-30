# Docker-first (Enterprise-ready) Guide

Last Updated: 2026-01-06

This guide captures the current Docker experience, the enterprise TLS limitation on CSAA networks, and the path to a sustainable Internal PyPI mirror. All findings below are observed in this repository and should be treated as facts, not assumptions.

## What works today (non-enterprise networks)
- Build: `docker build -t esdh-demo .`
- Run tests: `docker run --rm esdh-demo python -m pytest -m demo -q`
- Run the demo flow: `docker run --rm -p 5000:5000 esdh-demo ./scripts/docker_run_demo.sh`
- Run the demo gate: `docker run --rm -p 5000:5000 -e DEMO_PROFILE=baseline esdh-demo make demo-gate`
- Demo profile inspection: `docker run --rm esdh-demo make demo-profile-info`
- Pip respects standard environment variables (`PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, `PIP_TRUSTED_HOST`) and an optional pip config copied in via `PIP_CONF_PATH` at build time.

## Observed enterprise limitation on CSAA networks
- Docker Desktop works, but containers cannot TLS-verify public PyPI on CSAA networks.
- Reproduction (clean container):
  ```bash
  docker run --rm -it python:3.11-slim bash
  apt-get update && apt-get install -y ca-certificates curl
  curl -Iv https://pypi.org/simple/pip/
  ```
- Outcome: `SSL certificate problem: self-signed certificate in certificate chain` / TLS alert unknown CA. Docker builds that run `pip install` against public PyPI therefore fail regardless of app code.

## Why CA-in-repo is not a best practice
- Certificates vary per tenant and expire; baking them into git rots quickly and risks distribution of internal trust anchors.
- Copying a PEM into the repo does not guarantee coverage for all enterprise interceptors or networks.
- It complicates supply-chain review and encourages ad-hoc trust management instead of standardized enterprise controls.

## Workarounds until Internal PyPI mirror exists
- **Workaround A: Use personal/home network where public PyPI is accessible (short-term POC).** Keep this to POC evaluation only; avoid moving data or credentials that require corporate governance.
- **Workaround B: Prebuild the image on a network that can access PyPI and distribute it internally (POC-only).** Share the built image through an internal registry or tarball using the same `esdh-demo` tag referenced in README commands. Security note: ensure the image is scanned and avoid embedding secrets.
- **Workaround C: Use an internal index when available (preferred).** Provide `PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, and `PIP_TRUSTED_HOST` at build/run time or mount a pip config (see `config/pip.conf.example`). This keeps TLS trust anchored to enterprise-managed endpoints.
- **Workaround D (last resort): trusted-host flags / disabling verification only with explicit warning and only for POC demos if approved.** This weakens TLS verification and should be avoided outside of time-boxed demos with risk acceptance.

## Ideal solution: Internal PyPI mirror/proxy
- Provide an internal, TLS-terminated PyPI mirror that is reachable from Docker hosts and build nodes.
- Configuration knobs (build or runtime):
  - `PIP_INDEX_URL=https://<internal-pypi>/simple`
  - `PIP_EXTRA_INDEX_URL=https://<optional-secondary>/simple`
  - `PIP_TRUSTED_HOST=<internal-pypi-hostname>`
  - Optional: supply `PIP_CONF_PATH=config/pip.conf` during `docker build` to copy a vetted pip config into `/etc/pip.conf`.
- Mirror expectations: availability from CI and developer laptops, enterprise-issued certificates, audit logging, and caching to reduce external dependency exposure.

### Enterprise build/run example (mirror)
- Bash:
  ```bash
  docker build -t esdh-demo \
    --build-arg PIP_INDEX_URL=https://<internal-pypi>/simple \
    --build-arg PIP_TRUSTED_HOST=<internal-pypi-hostname> .
  docker run --rm esdh-demo python -m pytest -m demo -q
  ```
- PowerShell:
  ```powershell
  docker build -t esdh-demo `
    --build-arg PIP_INDEX_URL=https://<internal-pypi>/simple `
    --build-arg PIP_TRUSTED_HOST=<internal-pypi-hostname> .
  docker run --rm esdh-demo python -m pytest -m demo -q
  ```

## Pilot+ considerations
- **Repeatability:** pinned dependencies, deterministic Docker builds, and versioned images for demos.
- **Security:** avoid shipping certificates in git; rely on enterprise-trusted mirrors and standard TLS validation.
- **CI/CD:** container builds must succeed inside corporate networks using the internal mirror; publish images to an internal registry.
- **Artifact caching:** leverage mirror caching to reduce external calls and speed builds.
- **SBOM and vulnerability scanning:** generate SBOMs and scan images before distribution.
- **Supply chain:** document the provenance of dependencies and ensure mirror whitelisting aligns with governance.

## Troubleshooting checklist
- Confirm Docker context and daemon health: `docker context ls` and `docker info`.
- Verify Docker Engine version (Desktop/Server): `docker version`.
- Re-run the curl reproduction above inside a clean container to differentiate TLS issues from app code.
- On Windows, prefer an elevated PowerShell or WSL shell when Docker commands fail due to permissions.
- Validate build args: if providing `PIP_CONF_PATH`, ensure the file exists in the build context; otherwise rely on environment variables.
- If builds stall, test network egress with a simple alpine curl: `docker run --rm curlimages/curl https://example.com`.
- Verify pip settings when using a mirror: `pip config debug -v | grep -E "index-url|extra-index-url|trusted-host"`.

## Final Sign-off Summary
- Date: 2025-03-17
- Environment tested: Windows + Docker Desktop
- Result: Public PyPI TLS fails on CSAA networks (see curl reproduction).
- Result: Non-enterprise networks path works with `esdh-demo` tag.
- Next step: provide an Internal PyPI mirror/proxy with trusted certificates.
- Workarounds: A (home network), B (prebuilt `esdh-demo` image), C (internal index), D (last-resort trusted-host for POC).

## Status update
- 2026-01-06: Guidance remains current; no Internal PyPI mirror implementation has been captured in-repo yet.
