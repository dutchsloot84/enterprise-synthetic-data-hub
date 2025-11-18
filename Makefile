.PHONY: demo demo-smoke demo-validate demo-stop demo-profile-info demo-clean

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

## Inspect profile metadata + payload structure
demo-profile-info:
@$(PYTHON) -m enterprise_synthetic_data_hub.cli.profile_info --profile $(DEMO_PROFILE)

## Remove demo artifacts + background process breadcrumbs
demo-clean:
@rm -f .demo_api_pid .demo_api_port
@rm -rf data/demo_runs
@mkdir -p data/demo_runs
@touch data/demo_runs/.gitkeep
