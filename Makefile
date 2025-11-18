.PHONY: demo demo-smoke demo-validate demo-stop

PYTHON ?= python3
PACKAGE := enterprise_synthetic_data_hub
export PYTHONPATH := src
DEMO_PROFILE ?= baseline

## Primary guided demo flow
demo:
@echo "Using demo profile: $(DEMO_PROFILE)"
@DEMO_PROFILE=$(DEMO_PROFILE) $(PYTHON) scripts/run_demo_flow.py

## Lightweight CLI/API smoke tests used in demo contexts
demo-smoke:
$(PYTHON) -m pytest -m demo

## Validate snapshot schemas + synthetic marker guardrails
demo-validate:
@DEMO_PROFILE=$(DEMO_PROFILE) $(PYTHON) scripts/demo_validate.py

## Explicit stop hook if an API process remains
demo-stop:
@bash scripts/demo_stop_api.sh
