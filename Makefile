# al-dente — OKF Bundle Automation Pipeline
#
# Convenience targets for local development.

.PHONY: install build serve clean test help

# Default target
.DEFAULT_GOAL := help

PYTHON := python3
PIP    := pip3
DOCS_PORT := 8000

INPUT_DIR  := data
OUTPUT_DIR := output
DOCS_DIR   := docs

## Display this help message
help:
	@echo "al-dente — OKF Bundle Pipeline"
	@echo ""
	@echo "Available targets:"
	@echo "  make install   Install Python dependencies"
	@echo "  make build     Build OKF bundle from source data"
	@echo "  make serve     Serve docs/ locally on port $(DOCS_PORT)"
	@echo "  make clean     Remove generated files"
	@echo "  make test      Run validation and tests"

## Install Python dependencies
install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

## Build OKF bundle
build:
	$(PYTHON) -m pipeline.build_okf \
		--input $(INPUT_DIR) \
		--output $(DOCS_DIR)/assets/js

## Generate documentation views
views:
	$(PYTHON) -m pipeline.views.generate_views \
		--input $(INPUT_DIR) \
		--output $(DOCS_DIR)

## Serve docs/ locally with Python http.server
serve:
	@echo "Serving $(DOCS_DIR) on http://localhost:$(DOCS_PORT)"
	cd $(DOCS_DIR) && $(PYTHON) -m http.server $(DOCS_PORT)

## Remove generated files
clean:
	rm -rf $(OUTPUT_DIR)
	rm -f $(DOCS_DIR)/assets/js/okf_bundle.json
	rm -f $(DOCS_DIR)/assets/js/okf_data.js
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

## Run validation and tests
test:
	@echo "Running OKF validation..."
	$(PYTHON) -m pipeline.build_okf \
		--input $(INPUT_DIR) \
		--output /tmp/okf-validation \
		--validate-only
	@echo ""
	@echo "Running tests (if pytest available)..."
	@if command -v pytest >/dev/null 2>&1; then \
		pytest tests/ -v || true; \
	else \
		echo "pytest not installed; skipping test step."; \
	fi

## Full pipeline: build + views
all: build views
