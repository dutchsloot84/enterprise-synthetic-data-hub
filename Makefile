SHELL := /usr/bin/env bash
.SHELLFLAGS := -eu -o pipefail -c

PYTHON ?= python3
ifeq (, $(shell which $(PYTHON)))
PYTHON = python
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

.PHONY: demo demo-smoke demo-validate demo-stop demo-profile-info demo-clean check-makefile

## Primary guided demo flow
demo:
	$(Q)echo "Using demo profile: $(DEMO_PROFILE)"
	$(Q)DEMO_PROFILE=$(DEMO_PROFILE) $(PYTHON) scripts/run_demo_flow.py

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
