# {{PROJECT_NAME}} Development Commands
# Run with: just <command>

# Default recipe - show available commands
default:
    @just --list

# Setup development environment
setup:
    uv sync --extra dev --extra data
    uv run pre-commit install
    @echo "✅ Development environment ready!"

# Install dependencies only
install:
    uv sync --extra dev

# Install data dependencies
install-data:
    uv sync --extra dev --extra data

# Run tests
test *args="":
    uv run pytest {{args}}

# Run tests with coverage
test-cov:
    uv run pytest --cov={{PROJECT_NAME}} --cov-report=html --cov-report=term-missing

# Run tests for specific Python versions
test-all:
    nox -s tests

# Lint code with ruff
lint:
    uv run ruff check .

# Format code with ruff
format:
    uv run ruff format .
    uv run ruff check --fix .

# Type check with mypy
type-check:
    uv run mypy src tests

# Security check
security:
    uv run safety check
    uv run bandit -r src/

# Run all quality checks
qa: lint type-check security

# Full CI pipeline
ci:
    nox -s ci

# Clean build artifacts
clean:
    nox -s clean

# Build package
build:
    uv build

# Start Jupyter Lab locally
jupyter:
    nox -s jupyter

# Start development environment in Docker
docker-dev:
    nox -s docker_dev

# Start Jupyter in Docker
docker-jupyter:
    nox -s docker_jupyter

# Open shell in Docker development environment
docker-shell:
    docker compose exec dev bash

# Stop Docker services
docker-down:
    docker compose down

# Build Docker images
docker-build:
    nox -s docker_build

# Setup Spark environment
spark-setup:
    nox -s spark_setup

# Check notebook quality
notebook-qa:
    nox -s data_quality

# Run pre-commit hooks
pre-commit:
    uv run pre-commit run --all-files

# Update dependencies
update:
    uv sync --upgrade

# Show project info
info:
    @echo "📦 Project: {{PROJECT_NAME}}"
    @echo "🐍 Python: $(python --version)"
    @echo "📁 Directory: $(pwd)"
    @echo "🔗 Virtual env: $(uv run python -c 'import sys; print(sys.prefix)')"
    @echo ""
    @echo "🚀 Quick start:"
    @echo "  just setup     # Setup development environment"
    @echo "  just test      # Run tests"
    @echo "  just jupyter   # Start Jupyter Lab"
    @echo "  just ci        # Run full CI pipeline"

# Development workflow helpers
fix: format lint
check: qa test
all: setup check build