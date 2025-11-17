.PHONY: demo demo-data demo-api demo-smoke

PYTHON := python
PACKAGE := enterprise_synthetic_data_hub

export PYTHONPATH := src

demo-data:
	@echo "Generating governed snapshot..."
	$(PYTHON) -m $(PACKAGE).cli.main generate-snapshot --output-dir data/snapshots/v0.1

demo-api:
	@echo "Starting Flask API (Ctrl+C to stop)..."
	FLASK_APP=$(PACKAGE).api.app:app flask run

demo:
	@echo "\n[1/3] Generate governed snapshot"
	$(PYTHON) -m $(PACKAGE).cli.main generate-snapshot --records 25 --randomize --output-dir data/snapshots/v0.1
	@echo "\n[2/3] Run generator preview"
	$(PYTHON) scripts/demo_data.py --records 5 --preview 2
	@echo "\n[3/3] Launch API + CLI preview"
	bash scripts/demo_start_api.sh

demo-smoke:
	pytest -m smoke
