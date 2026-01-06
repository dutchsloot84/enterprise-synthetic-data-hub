SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

PYTHON ?=
ifeq ($(OS),Windows_NT)
  ifneq (,$(wildcard .venv/Scripts/python.exe))
    PYTHON := $(CURDIR)/.venv/Scripts/python.exe
  endif
else
  ifneq (,$(wildcard .venv/bin/python))
    PYTHON := $(CURDIR)/.venv/bin/python
  endif
endif
PYTHON ?= python3
ifeq (,$(shell $(SHELL) -lc "command -v '$(PYTHON)' >/dev/null 2>&1 && echo found"))
  PYTHON := python
endif

export PYTHONPATH := src

VERBOSE ?= 0
ifeq ($(VERBOSE),1)
  Q :=
else
  Q := @
endif

PACKAGE := enterprise_synthetic_data_hub
DEMO_PROFILE ?= baseline

.PHONY: demo demo-gate demo-smoke demo-validate demo-stop demo-profile-info demo-clean check-makefile publish-bootstrap doctor critic
.PHONY: doctor

## Primary guided demo flow
demo:
	$(Q)echo "Using demo profile: $(DEMO_PROFILE)"
	$(Q)DEMO_PROFILE=$(DEMO_PROFILE) $(PYTHON) scripts/run_demo_flow.py

## Validate demo artifacts, run smoke tests, and execute the demo flow without its smoke stage
demo-gate:
	$(Q)echo "Running demo-gate: validate → smoke → flow (--skip-smoke)"
	$(Q)[ ! -f .demo_api_pid ] || echo "Warning: .demo_api_pid present; run make demo-stop if needed"
	$(Q)$(MAKE) demo-validate
	$(Q)$(MAKE) demo-smoke
	$(Q)DEMO_PROFILE=$(DEMO_PROFILE) $(PYTHON) scripts/run_demo_flow.py --skip-smoke

## Lightweight CLI/API smoke tests used in demo contexts
demo-smoke:
	$(Q)$(PYTHON) -m pytest -m demo

## Validate snapshot schemas + synthetic marker guardrails
demo-validate:
	$(Q)DEMO_PROFILE=$(DEMO_PROFILE) $(PYTHON) scripts/demo_validate.py

## Explicit stop hook if an API process remains
demo-stop:
	$(Q)bash scripts/demo_stop_api.sh

## Inspect profile metadata + payload structure
demo-profile-info:
	$(Q)$(PYTHON) -m enterprise_synthetic_data_hub.cli.profile_info --profile $(DEMO_PROFILE)

## Remove demo artifacts + background process breadcrumbs
demo-clean:
	$(Q)rm -f .demo_api_pid .demo_api_port
	$(Q)rm -rf data/demo_runs
	$(Q)mkdir -p data/demo_runs
	$(Q)touch data/demo_runs/.gitkeep

## Validate Makefile syntax via local helper script
check-makefile:
	$(Q)bash scripts/check_makefile_syntax.sh

## Upload bootstrap installers to the latest GitHub release
publish-bootstrap:
	$(Q)bash scripts/publish_bootstrap_assets.sh

## Lightweight environment diagnostics for demo day
doctor:
	$(Q)set +e; \
	echo "== Demo doctor =="; \
	if command -v uname >/dev/null 2>&1; then uname -a; else echo "OS: (uname unavailable)"; fi; \
	echo "Make shell: $(SHELL)"; \
	if command -v bash >/dev/null 2>&1; then bash --version | head -n 1; else echo "WARN bash not found in PATH"; fi; \
	if command -v make >/dev/null 2>&1; then make --version | head -n 1; else echo "WARN make not found in PATH"; fi; \
	PY_PATH="$(PYTHON)"; \
	if command -v "$$PY_PATH" >/dev/null 2>&1; then \
	  echo "PASS python resolver: $$PY_PATH"; \
	  "$$PY_PATH" --version 2>/dev/null || echo "WARN could not read python version"; \
	else \
	  echo "FAIL python not found: $$PY_PATH"; \
	  exit 1; \
	fi; \
	if [ -x "$(CURDIR)/.venv/Scripts/python.exe" ]; then echo "PASS venv (Windows): $(CURDIR)/.venv/Scripts/python.exe"; else echo "WARN venv (Windows) missing: .venv/Scripts/python.exe"; fi; \
	if [ -x "$(CURDIR)/.venv/bin/python" ]; then echo "PASS venv (Unix): $(CURDIR)/.venv/bin/python"; else echo "WARN venv (Unix) missing: .venv/bin/python"; fi; \
	if [ -n "$${VIRTUAL_ENV-}" ]; then echo "VIRTUAL_ENV: $$VIRTUAL_ENV"; else echo "VIRTUAL_ENV: (not set)"; fi; \
	for cmd in pytest pip curl; do \
	  if command -v "$$cmd" >/dev/null 2>&1; then echo "PASS $$cmd present at $$(command -v $$cmd)"; else echo "WARN $$cmd not found in PATH"; fi; \
	done; \
	DEMO_PORT="$${DEMO_API_PORT:-5000}"; \
		if command -v "$$PY_PATH" >/dev/null 2>&1; then \
		  "$$PY_PATH" -c "import socket, sys; host='127.0.0.1'; port=int(sys.argv[1]) if len(sys.argv)>1 else 5000; sock=socket.socket(); sock.settimeout(1.0); code=sock.connect_ex((host, port)); sock.close(); \
print(f'WARN port {port} may be in use on {host}' if code == 0 else f'PASS port {port} appears available on {host}')" "$$DEMO_PORT" || true; \
	else \
	  echo "WARN skipped port check (python missing)"; \
	fi

## Static critic to guard demo readiness
critic:
	$(Q)$(PYTHON) scripts/critic_check.py
