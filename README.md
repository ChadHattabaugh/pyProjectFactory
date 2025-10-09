# pyProjectFactory

**Manufacturing enterprise-ready Python projects**

A comprehensive, modern Python project template with enterprise-grade automation, repository protection, and AI-assisted development.

## Features

- **Modern Tooling**: uv, ruff, mypy, pytest, nox
- **Multi-Python Support**: Test against Python 3.9-3.12
- **Quality Assurance**: Pre-commit hooks, security scanning, type checking
- **Automation**: GitHub Actions CI/CD, automated dependency updates, repository protection
- **Development Experience**: VS Code configuration, Docker environments, nox automation
- **GitFlow Workflow**: Automated branch protection, naming conventions, AI-assisted reviews
- **Data Science Ready**: Optional PySpark, Jupyter, Docker data environment
- **Template System**: Interactive setup with project customization

## Quick Start

### 🚀 Using GitHub Template (Recommended)

1. **Click "Use this template"** on the [GitHub repository page](https://github.com/ChadHattabaugh/pyProjectFactory)
2. **Create your new repository** with your desired name
3. **Clone your new repository**:
   ```bash
   git clone https://github.com/yourusername/your-new-project.git
   cd your-new-project
   ```
4. **Run the interactive setup**:
   ```bash
   python setup_project.py
   ```
   The setup script will:
   - Check for required tools (only `uv`) and provide installation links if missing
   - Create your project with all template files
   - Initialize git repository with develop branch
   - Automatically set up the development environment
   - Install dependencies and pre-commit hooks

5. **Repository protection and full CI/CD will be automatically configured** (see [Repository Setup](docs/REPOSITORY_SETUP.md))
6. **Start developing** (environment is already set up):
   ```bash
   cd your-project-name
   nox -s tests     # Run tests to verify setup
   ```

### Alternative Methods

#### Option 1: Direct Clone + Setup
```bash
# Clone template directly
git clone https://github.com/ChadHattabaugh/pyProjectFactory.git my-project
cd my-project

# Run interactive setup (includes dependency checking and environment setup)
python setup_project.py
```

#### Option 2: Using Copier
```bash
# Install copier
pip install copier

# Generate project
copier copy https://github.com/ChadHattabaugh/pyProjectFactory.git my-new-project
```

## What You Get

### Core Tools
- **uv**: Fast dependency management and environment handling
- **ruff**: Lightning-fast linting and formatting (replaces black, isort, flake8)
- **mypy**: Static type checking with strict configuration
- **pytest**: Testing framework with coverage reporting
- **nox**: Automation across multiple Python versions
- **pre-commit**: Git hooks for code quality
- **safety**: Security vulnerability scanning

### Development Environment
- **VS Code**: Complete configuration with extensions and tasks
- **Docker**: Development and data science environments
- **run.py**: Simple setup script
- **GitHub Actions**: CI/CD with matrix testing
- **Dependabot**: Automated dependency updates
- **Repository Protection**: Automated GitFlow setup with branch protection and naming rules

### Project Types Supported

#### Library/Package
- Standard Python package structure
- PyPI publishing workflow
- API documentation

#### Application
- CLI interface with Click/Typer
- Configuration management
- Deployment ready

#### Data Science
- PySpark configuration and utilities
- Jupyter Lab environment
- Docker data science stack
- Data directory structure
- Notebook quality checks

## Available Commands

```bash
# Setup and development
python run.py          # Setup development environment
uv sync         # Install dependencies only
nox -s tests           # Run tests
nox -s tests-cov       # Run tests with coverage
nox -s ci             # Full CI pipeline

# Code quality
nox -s format         # Format code with ruff
nox -s lint           # Lint code
nox -s type_check     # Type checking with mypy
nox -s safety       # Security scans
nox -s ci             # All quality checks

# Docker environments
nox -s docker_dev     # Start development container
nox -s docker_jupyter # Start Jupyter container
docker compose exec dev bash   # Open shell in container
docker compose down    # Stop containers

# Utilities
nox -s clean          # Clean build artifacts
uv build          # Build package
nox -l           # Show project information
```

## Template Structure

```
pyProjectFactory/
├── setup_project.py           # Interactive project setup
├── copier.yml                 # Copier template configuration
├── pyproject.toml            # Modern Python packaging
├── noxfile.py                # Multi-environment automation
├── run.py                    # Setup script
├── .github/workflows/        # CI/CD pipelines & repository setup
├── .vscode/                  # VS Code configuration
├── src/{{PROJECT_NAME}}/     # Source code template
├── tests/                    # Test templates
├── notebooks/                # Jupyter notebooks (data projects)
├── data/                     # Data directories (data projects)
├── docs/                     # Documentation and setup guides
├── Dockerfile.dev            # Development environment
├── Dockerfile.data           # Data science environment
├── docker-compose.yml        # Multi-service setup
└── CLAUDE.md.template        # Claude AI context
```

## Why pyProjectFactory?

### Modern Python Ecosystem
- **uv** is faster than pip/poetry for dependency management
- **ruff** is 100x faster than traditional linters
- **nox** handles multi-version testing better than tox
- **nox** provides better task automation than Make

### Best Practices Built-In
- Src layout for better package structure
- Comprehensive testing setup
- Security scanning by default
- Type checking with strict settings
- Pre-commit hooks for quality gates

### Flexible and Scalable
- Works for any project type (library, app, data)
- Optional features based on needs
- Easy to extend and customize
- Docker for consistent environments

### Developer Experience
- One command setup
- IDE configuration included
- Clear documentation
- Automation for common tasks

## Customization

The template supports extensive customization through:

1. **Interactive Setup**: Prompts for project details and features
2. **Copier Variables**: Declarative configuration in `copier.yml`
3. **Feature Flags**: Enable/disable components based on project type
4. **Template Variables**: Replace placeholders throughout files

## Branch Workflow

This template enforces GitFlow branching strategy:

### Branch Types
- `master` - Production-ready code (protected, no direct pushes)
- `develop` - Integration branch (default, protected, no direct pushes)  
- `feature/*` - New features (from develop)
- `bugfix/*` - Bug fixes (from develop)
- `patch/*` - Small patches/hotfixes (from develop)

**Note**: Main branch is not used - master serves as the production branch.

### Development Process
1. Create feature branch: `git checkout -b feature/my-feature develop`
2. Commit with issue numbers: `git commit -m "feat: add feature (#123)"`
3. Push and create PR to `develop`
4. Requires author + AI reviewer approval
5. Merge to `develop`, deploy to `master` for releases

See [Repository Setup Guide](docs/REPOSITORY_SETUP.md) for detailed workflow.

## Roadmap

See our [Development Roadmap](ROADMAP.md) for planned features and timeline. Key upcoming features:

- **Q4 2025**: YAML Configuration System for automated project setup
- **Q1 2025**: FastAPI template support for web API development  
- **Q2 2025**: Template ecosystem with framework-specific options

Track progress and contribute to planning in our [GitHub Project](../../projects).

## Contributing

1. Fork the repository
2. Create a feature branch from `develop`
3. Make your changes with proper commit messages
4. Test with different project configurations
5. Submit a pull request to `develop`

See our [GitHub Labels Guide](docs/GITHUB_LABELS.md) for issue categorization and our [Roadmap](ROADMAP.md) for strategic direction.

## License

MIT License - feel free to use for any project type.

## Credits

Inspired by modern Python packaging standards and community best practices.