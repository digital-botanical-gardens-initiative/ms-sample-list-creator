.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@ poetry run pre-commit install
	@poetry shell

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
	@echo "🚀 TODO checking..."
	@find . -type f -name "*.py" ! -path "./venv/*" ! -path "./.venv/*" \
		! -path "./__pycache__/*" ! -path "./.mypy_cache/*" \
		-exec grep -nH --color=always "TODO" {} \;

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest --doctest-modules

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
