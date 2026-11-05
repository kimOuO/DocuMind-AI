# DocuMind-AI developer commands. Run `make help` for the list.
SHELL := /bin/bash
.DEFAULT_GOAL := help

BACKEND  := app/backend
FRONTEND := app/frontend
VENV     := .venv

# All development tools (Python, pip, Node, npm) live inside the project venv;
# nothing is installed on the host. Node is added to the venv by nodeenv.
export PATH := $(CURDIR)/$(VENV)/bin:$(PATH)

.PHONY: help setup dev dev-backend dev-frontend db migrate up down logs \
        check check-backend check-frontend test eval package transcript

help: ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk -F':.*?## ' '{printf "  %-16s %s\n", $$1, $$2}'

setup: ## Create the venv (Python + Node) and install all dependencies
	@test -x $(VENV)/bin/python || python3 -m venv $(VENV) 2>/dev/null || { \
	  echo "python3 -m venv needs python3-venv; using --without-pip + get-pip.py instead"; \
	  rm -rf $(VENV) && python3 -m venv --without-pip $(VENV) \
	  && curl -sS https://bootstrap.pypa.io/get-pip.py | $(VENV)/bin/python - -q; }
	$(VENV)/bin/pip install -q -r $(BACKEND)/requirements-dev.txt
	@test -x $(VENV)/bin/node || { . $(VENV)/bin/activate && \
	  nodeenv -p --prebuilt --node=$$(cat $(FRONTEND)/.node-version); }
	cd $(FRONTEND) && npm ci
	$(VENV)/bin/pre-commit install

db: ## Start only the database container
	docker compose up -d --wait db

migrate: db ## Apply database migrations
	cd $(BACKEND) && alembic upgrade head

dev: migrate ## Run backend (venv) and frontend (Vite) with hot reload
	@$(MAKE) -j2 dev-backend dev-frontend

dev-backend:
	cd $(BACKEND) && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd $(FRONTEND) && npm run dev

up: ## Build and run everything in Docker (demo / delivery mode)
	docker compose up --build -d --wait
	@echo "Open http://$${WEB_BIND:-127.0.0.1}:$${WEB_PORT:-3000}"

down: ## Stop the Docker deployment (data volumes are kept)
	docker compose down

logs: ## Follow container logs
	docker compose logs -f

check: check-backend check-frontend ## Lint, type-check and test everything

check-backend:
	cd $(BACKEND) && ruff check . && ruff format --check . && mypy app && pytest -q

check-frontend:
	cd $(FRONTEND) && npm run check

test: ## Run backend tests, including those that need the database
	cd $(BACKEND) && pytest -q -m "not llm"

eval: ## Run the retrieval/answer evaluation (added in P4)
	@echo "evaluation is implemented in phase P4" && exit 1

transcript: ## Export Claude Code session transcripts to docs/05-ai-collaboration/sessions/raw
	python3 scripts/export_transcript.py

package: ## Build the delivery zip from the committed tree
	bash scripts/package.sh
