# Python Project Template

A comprehensive, modern Python project template with best practices, automation, and optional data science capabilities.

## Features

- **Modern Tooling**: uv, ruff, mypy, pytest, nox
- **Multi-Python Support**: Test against Python 3.9-3.12
- **Quality Assurance**: Pre-commit hooks, security scanning, type checking
- **Automation**: GitHub Actions CI/CD, automated dependency updates, repository protection
- **Development Experience**: VS Code configuration, Docker environments, justfile commands
- **GitFlow Workflow**: Automated branch protection, naming conventions, AI-assisted reviews
- **Data Science Ready**: Optional PySpark, Jupyter, Docker data environment
- **Template System**: Interactive setup with project customization

## Quick Start

### 🚀 Using GitHub Template (Recommended)

1. **Click "Use this template"** on the [GitHub repository page](https://github.com/ChadHattabaugh/new-project-template)
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
5. **Repository protection will be automatically configured** (see [Repository Setup](docs/REPOSITORY_SETUP.md))
6. **Start developing**:
   ```bash
   just setup    # Setup development environment
   just test     # Run tests
   ```

### Alternative Methods

#### Option 1: Direct Clone + Setup
```bash
# Clone template directly
git clone https://github.com/ChadHattabaugh/new-project-template.git my-project
cd my-project

# Run interactive setup
python setup_project.py
```

#### Option 2: Using Copier
```bash
# Install copier
pip install copier

# Generate project
copier copy https://github.com/ChadHattabaugh/new-project-template.git my-new-project
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
- **justfile**: Convenient command runner
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
just setup          # Setup development environment
just install         # Install dependencies only
just test           # Run tests
just test-cov       # Run tests with coverage
just ci             # Full CI pipeline

# Code quality
just format         # Format code with ruff
just lint           # Lint code
just type-check     # Type checking with mypy
just security       # Security scans
just qa             # All quality checks

# Docker environments
just docker-dev     # Start development container
just docker-jupyter # Start Jupyter container
just docker-shell   # Open shell in container
just docker-down    # Stop containers

# Utilities
just clean          # Clean build artifacts
just build          # Build package
just info           # Show project information
```

## Template Structure

```
python-project-template/
├── setup_project.py           # Interactive project setup
├── copier.yml                 # Copier template configuration
├── pyproject.toml            # Modern Python packaging
├── noxfile.py                # Multi-environment automation
├── justfile                  # Development commands
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

## Why This Template?

### Modern Python Ecosystem
- **uv** is faster than pip/poetry for dependency management
- **ruff** is 100x faster than traditional linters
- **nox** handles multi-version testing better than tox
- **justfile** provides better ergonomics than Make

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
- `master` - Production-ready code
- `develop` - Integration branch (default)
- `feature/*` - New features (from develop)
- `bugfix/*` - Bug fixes (from develop)
- `patch/*` - Small patches/hotfixes (from develop)

### Development Process
1. Create feature branch: `git checkout -b feature/my-feature develop`
2. Commit with issue numbers: `git commit -m "feat: add feature (#123)"`
3. Push and create PR to `develop`
4. Requires author + AI reviewer approval
5. Merge to `develop`, deploy to `master` for releases

See [Repository Setup Guide](docs/REPOSITORY_SETUP.md) for detailed workflow.

## Contributing

1. Fork the repository
2. Create a feature branch from `develop`
3. Make your changes with proper commit messages
4. Test with different project configurations
5. Submit a pull request to `develop`

## License

MIT License - feel free to use for any project type.

## Credits

Inspired by modern Python packaging standards and community best practices.