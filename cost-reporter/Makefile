.PHONY: help build-CostReporterLambda init install test

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-CostReporterLambda: ## Build command for SAM
	cp src/*.py $(ARTIFACTS_DIR)
	python3 -m pip install -r requirements.txt -t $(ARTIFACTS_DIR)
	rm -rf $(ARTIFACTS_DIR)/bin

# SAM fails if we create the virtualenv in this directory
init: ## Create a virtual environment
	python3 -m venv ../.venv

install: ## Install all dependencies
	. ../.venv/bin/activate; \
	pip install -r requirements-dev.txt

test: ## Run the tests
	tox -e py
