"""Nox configuration for automated testing and quality checks."""

import nox

# Python versions to test against
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]
MAIN_PYTHON_VERSION = "3.11"

nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite with pytest."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev")
    session.run("pytest", *session.posargs)


@nox.session(python=MAIN_PYTHON_VERSION)
def lint(session: nox.Session) -> None:
    """Run linting with ruff."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python=MAIN_PYTHON_VERSION)
def format(session: nox.Session) -> None:
    """Format code with ruff."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev")
    session.run("ruff", "format", ".")
    session.run("ruff", "check", "--fix", ".")


@nox.session(python=MAIN_PYTHON_VERSION)
def type_check(session: nox.Session) -> None:
    """Run type checking with mypy."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev")
    session.run("mypy", "src", "tests")


@nox.session(python=MAIN_PYTHON_VERSION)
def safety(session: nox.Session) -> None:
    """Run security checks with safety."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev")
    session.run("safety", "check", "--json")


@nox.session(python=MAIN_PYTHON_VERSION)
def coverage(session: nox.Session) -> None:
    """Generate coverage report."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev")
    session.run("pytest", "--cov-report=html", "--cov-report=xml")
    session.notify("coverage_report")


@nox.session(python=MAIN_PYTHON_VERSION)
def coverage_report(session: nox.Session) -> None:
    """Show coverage report."""
    session.install("coverage[toml]")
    session.run("coverage", "report", "--show-missing")


@nox.session(python=MAIN_PYTHON_VERSION)
def docs(session: nox.Session) -> None:
    """Build documentation (if using sphinx)."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev")
    # Uncomment if using sphinx
    # session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


@nox.session(python=MAIN_PYTHON_VERSION)
def pre_commit(session: nox.Session) -> None:
    """Run pre-commit hooks."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=PYTHON_VERSIONS)
def install_check(session: nox.Session) -> None:
    """Check that the package installs correctly."""
    session.install("uv")
    session.run("uv", "sync")
    session.run("python", "-c", "import {{PROJECT_NAME}}")


# Convenience sessions
@nox.session(python=MAIN_PYTHON_VERSION)
def dev(session: nox.Session) -> None:
    """Set up development environment."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev", "--extra", "data")
    session.run("pre-commit", "install")


@nox.session(python=MAIN_PYTHON_VERSION)
def ci(session: nox.Session) -> None:
    """Run all CI checks."""
    session.notify("lint")
    session.notify("type_check")
    session.notify("safety")
    session.notify("tests")


@nox.session(python=MAIN_PYTHON_VERSION)
def jupyter(session: nox.Session) -> None:
    """Start Jupyter Lab for data analysis."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev", "--extra", "data")
    session.run("jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root")


@nox.session(python=MAIN_PYTHON_VERSION)
def spark_setup(session: nox.Session) -> None:
    """Set up and test Spark environment."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev", "--extra", "data")
    session.run("python", "scripts/setup_spark.py")


@nox.session(python=MAIN_PYTHON_VERSION)
def data_quality(session: nox.Session) -> None:
    """Run data quality checks on notebooks."""
    session.install("uv")
    session.run("uv", "sync", "--extra", "dev", "--extra", "data")
    # Add nbqa for notebook quality checks
    session.install("nbqa")
    session.run("nbqa", "ruff", "notebooks/")
    session.run("nbqa", "mypy", "notebooks/")


@nox.session(python=MAIN_PYTHON_VERSION)
def docker_build(session: nox.Session) -> None:
    """Build Docker images."""
    session.run("docker", "build", "-f", "Dockerfile.dev", "-t", "{{PROJECT_NAME}}-dev", ".", external=True)
    session.run("docker", "build", "-f", "Dockerfile.data", "-t", "{{PROJECT_NAME}}-data", ".", external=True)


@nox.session(python=MAIN_PYTHON_VERSION)
def docker_dev(session: nox.Session) -> None:
    """Start development environment in Docker."""
    session.run("docker", "compose", "up", "-d", "dev", external=True)
    session.log("Development environment started!")
    session.log("Access shell: docker compose exec dev bash")
    session.log("Jupyter Lab: http://localhost:8888")
    session.log("Spark UI: http://localhost:4040")


@nox.session(python=MAIN_PYTHON_VERSION)
def docker_jupyter(session: nox.Session) -> None:
    """Start Jupyter-only environment in Docker."""
    session.run("docker", "compose", "up", "-d", "jupyter", external=True)
    session.log("Jupyter environment started!")
    session.log("Jupyter Lab: http://localhost:8889")
    session.log("Spark UI: http://localhost:4041")


@nox.session(python=MAIN_PYTHON_VERSION)
def docker_shell(session: nox.Session) -> None:
    """Open shell in development container."""
    session.run("docker", "compose", "exec", "dev", "bash", external=True)


@nox.session(python=MAIN_PYTHON_VERSION)
def docker_down(session: nox.Session) -> None:
    """Stop all Docker Compose services."""
    session.run("docker", "compose", "down", external=True)


@nox.session(python=MAIN_PYTHON_VERSION)
def clean(session: nox.Session) -> None:
    """Clean up build artifacts and cache."""
    import shutil
    from pathlib import Path

    paths_to_clean = [
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".coverage",
        "htmlcov",
        "coverage.xml",
        "dist",
        "build",
        "*.egg-info",
    ]

    for path in paths_to_clean:
        for item in Path().glob(path):
            if item.is_file():
                item.unlink()
                session.log(f"Removed file: {item}")
            elif item.is_dir():
                shutil.rmtree(item)
                session.log(f"Removed directory: {item}")