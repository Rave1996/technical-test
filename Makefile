.DEFAULT_GOAL := help
SHELL := bash
.ONESHELL:

PROJECT_PATH=src
DB_NAME=$(PROJECT_PATH)
ENV_PREFIX=$(shell echo 'poetry run ')


.PHONY: help
help:            	## show the help
	@echo "Usage: make <target>"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'


.PHONY: lint
lint:            	## Run linters
	${ENV_PREFIX}pre-commit run --all-files


virtualenv:     	## Create a virtual environment.
	@echo "creating virtualenv using poetry..."
	@pip install -U pip poetry
	@poetry env use python3.12
	@echo
	@echo "!!! Please run 'poetry shell' to enable the environment !!!"

install: virtualenv  ## Install and setup project dependencies
	python3 -m pip install --upgrade pip wheel
	poetry install --no-root
	${ENV_PREFIX}pre-commit install
.PHONY: install

update_libs:  		## update libs
	poetry update
.PHONY: update-libs

.PHONY: clean
clean:  			## Remove all temporary files like pycache
	find . -name \*.rdb -type f -ls -delete
	find . -name \*.pyc -type f -ls -delete
	find . -name __pycache__ -ls -delete

# == Project Helpers
# ===================================================
start: install  	## Init development server
	@docker compose up -d db
	cd src/ && ${ENV_PREFIX}uvicorn main:app --reload --host 0.0.0.0 --port 9000

.PHONY: test
test: 				## Run all the tests with docker
	@docker compose up --build test && docker compose rm test -f

.PHONY: app
app: 				## Run app with docker
	@docker compose up --build app
