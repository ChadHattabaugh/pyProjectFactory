#!/usr/bin/env python3
"""Interactive project setup script for the Python template."""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return bool(re.match(pattern, email))


def validate_project_name(name: str) -> bool:
    """Validate project name format."""
    pattern = r'^[a-z][a-z0-9-]*$'
    return bool(re.match(pattern, name))


def get_git_config(key: str) -> Optional[str]:
    """Get a value from git config."""
    try:
        result = subprocess.run(
            ['git', 'config', '--get', key],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip() if result.stdout.strip() else None
    except subprocess.CalledProcessError:
        return None


def get_user_input(
    prompt: str,
    default: Optional[str] = None,
    choices: Optional[List[str]] = None,
    validator: Optional[callable] = None,
    is_bool: bool = False,
) -> Any:
    """Get user input with validation."""
    while True:
        if choices:
            choice_str = " | ".join(f"{i+1}. {choice}" for i, choice in enumerate(choices))
            full_prompt = f"{prompt}\n{choice_str}\nChoice"
        else:
            full_prompt = prompt

        if default:
            full_prompt += f" [{default}]"

        full_prompt += ": "

        user_input = input(full_prompt).strip()

        if not user_input and default:
            user_input = default

        if is_bool:
            if user_input.lower() in ['y', 'yes', 'true', '1']:
                return True
            elif user_input.lower() in ['n', 'no', 'false', '0']:
                return False
            else:
                print("Please enter y/n, yes/no, true/false, or 1/0")
                continue

        if choices:
            try:
                choice_index = int(user_input) - 1
                if 0 <= choice_index < len(choices):
                    return choices[choice_index]
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
                    continue
            except ValueError:
                if user_input in choices:
                    return user_input
                print(f"Please enter a valid choice: {', '.join(choices)}")
                continue

        if validator and not validator(user_input):
            print("Invalid input. Please try again.")
            continue

        return user_input


def collect_project_info() -> Dict[str, Any]:
    """Collect project information from user."""
    print("🚀 Python Project Template Setup")
    print("=" * 40)

    info = {}

    # Basic project info
    info['project_name'] = get_user_input(
        "Project name (lowercase, hyphens allowed)",
        validator=validate_project_name
    )

    info['project_description'] = get_user_input(
        "Project description",
        default="An awesome Python project"
    )

    # Get defaults from git config
    git_name = get_git_config('user.name')
    git_email = get_git_config('user.email')
    
    info['author_name'] = get_user_input(
        "Author name",
        default=git_name or os.environ.get('USER', 'Your Name')
    )

    info['author_email'] = get_user_input(
        "Author email",
        default=git_email,
        validator=validate_email
    )

    info['github_username'] = get_user_input(
        "GitHub username/organization",
        default=info['author_name'].lower().replace(' ', '')
    )

    # Project type
    project_types = ["app", "library", "package", "data"]
    info['project_type'] = get_user_input(
        "Project type",
        choices=project_types,
        default="library"
    )

    # Python version
    python_versions = ["3.9", "3.10", "3.11", "3.12"]
    info['min_python_version'] = get_user_input(
        "Minimum Python version",
        choices=python_versions,
        default="3.9"
    )

    # License
    licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Proprietary"]
    info['license'] = get_user_input(
        "License",
        choices=licenses,
        default="MIT"
    )

    # Optional features
    print("\n📦 Optional Features")
    print("-" * 20)

    info['use_docker'] = get_user_input(
        "Include Docker configuration?",
        default="y",
        is_bool=True
    )

    info['use_pre_commit'] = get_user_input(
        "Include pre-commit hooks?",
        default="y",
        is_bool=True
    )

    info['use_github_actions'] = get_user_input(
        "Include GitHub Actions CI/CD?",
        default="y",
        is_bool=True
    )

    info['use_jupyter'] = get_user_input(
        "Include Jupyter notebook support?",
        default="y" if info['project_type'] == 'data' else "n",
        is_bool=True
    )

    info['use_spark'] = get_user_input(
        "Include PySpark configuration?",
        default="y" if info['project_type'] == 'data' else "n",
        is_bool=True
    )

    info['use_cli'] = get_user_input(
        "Include CLI interface?",
        default="y" if info['project_type'] == 'app' else "n",
        is_bool=True
    )

    if info['project_type'] == 'data':
        info['data_sources'] = get_user_input(
            "Primary data sources (comma-separated)",
            default="CSV files, APIs"
        )

    info['setup_claude_md'] = get_user_input(
        "Create CLAUDE.md with project context?",
        default="y",
        is_bool=True
    )

    # Computed values
    info['python_package_name'] = info['project_name'].replace('-', '_')
    info['project_slug'] = info['project_name'].lower().replace(' ', '-').replace('_', '-')

    return info


def replace_template_vars(file_path: Path, replacements: Dict[str, Any]) -> None:
    """Replace template variables in a file."""
    if file_path.suffix in ['.pyc', '.pyo', '.so', '.dylib', '.dll']:
        return

    try:
        content = file_path.read_text(encoding='utf-8')

        for key, value in replacements.items():
            placeholder = f"{{{{{key.upper()}}}}}"
            content = content.replace(placeholder, str(value))

        file_path.write_text(content, encoding='utf-8')
    except UnicodeDecodeError:
        # Skip binary files
        pass


def process_template_directory(src_dir: Path, dst_dir: Path, info: Dict[str, Any]) -> None:
    """Process template directory and copy to destination."""
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Files to skip based on configuration
    skip_files = set()

    if not info.get('use_docker', True):
        skip_files.update(['Dockerfile.dev', 'Dockerfile.data', 'docker-compose.yml'])

    if not info.get('use_pre_commit', True):
        skip_files.add('.pre-commit-config.yaml')

    if not info.get('use_github_actions', True):
        skip_files.add('.github')

    if not info.get('use_jupyter', False):
        skip_files.update(['notebooks', 'Dockerfile.data'])

    if not info.get('use_spark', False):
        skip_files.update(['src/{{PROJECT_NAME}}/spark_utils.py', 'scripts/setup_spark.py'])

    for item in src_dir.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(src_dir)

            # Skip the destination directory to prevent infinite recursion
            try:
                # Check if this file is within the destination directory
                item.relative_to(dst_dir)
                continue  # Skip files that are in the destination directory
            except ValueError:
                # File is not in destination directory, proceed
                pass

            # Skip files based on configuration
            if any(skip in str(rel_path) for skip in skip_files):
                continue

            # Replace template variables in path
            dst_path_str = str(rel_path)
            for key, value in info.items():
                placeholder = f"{{{{{key.upper()}}}}}"
                dst_path_str = dst_path_str.replace(placeholder, str(value))

            dst_path = dst_dir / dst_path_str
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Handle special template files
            if item.name.endswith('.template'):
                # Remove .template extension for final file
                dst_path = dst_path.with_suffix('')
            
            # Copy file
            shutil.copy2(item, dst_path)

            # Replace template variables in content
            replace_template_vars(dst_path, info)


def create_claude_md(project_dir: Path, info: Dict[str, Any]) -> None:
    """Create CLAUDE.md file with project context."""
    if not info.get('setup_claude_md', True):
        return

    claude_content = f"""# {info['project_name']} - Claude Context

## Project Overview

**Name**: {info['project_name']}
**Description**: {info['project_description']}
**Type**: {info['project_type']}
**Author**: {info['author_name']} ({info['author_email']})
**License**: {info['license']}

## Technical Details

- **Python Version**: {info['min_python_version']}+
- **Package Manager**: uv
- **Testing**: pytest with coverage
- **Linting**: ruff (replaces black, isort, flake8)
- **Type Checking**: mypy
- **Security**: safety, bandit
- **Automation**: nox for multi-environment testing

## Project Structure

```
{info['project_name']}/
├── src/{info['python_package_name']}/     # Source code
├── tests/                                 # Test files
├── pyproject.toml                        # Project configuration
├── noxfile.py                            # Automation tasks
├── justfile                              # Development commands
└── README.md                             # Documentation
```

## Development Workflow

### Setup
```bash
# Install dependencies
uv sync --extra dev

# Setup pre-commit hooks
pre-commit install
```

### Testing
```bash
# Run tests
just test
# or: uv run pytest

# Test with coverage
just test-cov

# Test all Python versions
just test-all
# or: nox -s tests
```

### Code Quality
```bash
# Format code
just format

# Lint code  
just lint

# Type check
just type-check

# All quality checks
just qa
```

### Automation
```bash
# Full CI pipeline
just ci
# or: nox -s ci

# Individual nox sessions
nox -s tests        # Run tests
nox -s lint         # Lint code
nox -s type_check   # Type checking
nox -s safety       # Security check
```

"""

    if info.get('use_docker', True):
        claude_content += """### Docker Development
```bash
# Start development environment
just docker-dev
# or: nox -s docker_dev

# Access development shell
just docker-shell

# Stop services
just docker-down
```

"""

    if info.get('use_jupyter', False):
        claude_content += """### Jupyter Notebooks
```bash
# Start Jupyter Lab locally
just jupyter
# or: nox -s jupyter

# Start Jupyter in Docker
just docker-jupyter

# Check notebook code quality
nox -s data_quality
```

"""

    if info.get('use_spark', False):
        claude_content += """### PySpark
```bash
# Setup Spark environment
nox -s spark_setup

# Example usage in Python:
from {info['python_package_name']}.spark_utils import get_local_spark_session

spark = get_local_spark_session()
# ... your Spark code ...
spark.stop()
```

"""

    claude_content += """## Key Commands

- `just setup` - Setup development environment
- `just test` - Run tests
- `just ci` - Run full CI pipeline
- `just format` - Format and fix code
- `just clean` - Clean build artifacts
- `just info` - Show project information

## Notes for Claude

- This project uses **uv** for dependency management (faster than pip/poetry)
- **ruff** handles all code formatting and linting (replaces black+isort+flake8)
- **nox** provides automation across multiple Python versions
- **justfile** provides convenient development commands
- All tools are configured in `pyproject.toml`

When helping with this project:
1. Use the existing tools and configurations
2. Follow the established patterns in the codebase
3. Add tests for new functionality
4. Update documentation as needed
5. Run `just ci` before committing changes

"""

    if info['project_type'] == 'data':
        claude_content += f"""## Data Project Specifics

**Data Sources**: {info.get('data_sources', 'Not specified')}

- Data files go in `data/` with subdirectories for raw/processed/external
- Notebooks go in `notebooks/` for exploration and analysis
- Use the data utilities in `src/{info['python_package_name']}/data_utils.py`
- Spark utilities available in `src/{info['python_package_name']}/spark_utils.py`

"""

    (project_dir / 'CLAUDE.md').write_text(claude_content)


def initialize_git(project_dir: Path) -> None:
    """Initialize git repository."""
    try:
        subprocess.run(['git', 'init'], cwd=project_dir, check=True, capture_output=True)
        subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_dir, check=True, capture_output=True)
        print("✅ Git repository initialized")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git initialization failed: {e}")


def main() -> None:
    """Main setup function."""
    # Collect project information
    info = collect_project_info()

    print(f"\n🔧 Setting up project '{info['project_name']}'...")

    # Create project directory
    project_dir = Path.cwd() / info['project_name']
    if project_dir.exists():
        overwrite = get_user_input(
            f"Directory '{info['project_name']}' already exists. Overwrite?",
            default="n",
            is_bool=True
        )
        if overwrite:
            shutil.rmtree(project_dir)
        else:
            print("Setup cancelled.")
            return

    # Process template
    template_dir = Path(__file__).parent
    process_template_directory(template_dir, project_dir, info)

    # Create CLAUDE.md
    create_claude_md(project_dir, info)

    # Initialize git
    initialize_git(project_dir)

    print(f"\n🎉 Project '{info['project_name']}' created successfully!")
    print(f"📁 Location: {project_dir}")
    print("\n🚀 Next steps:")
    print(f"1. cd {info['project_name']}")
    print("2. just setup")
    print("3. just test")
    print("4. Start coding!")

    if info.get('use_jupyter', False):
        print("5. just jupyter  # Start Jupyter Lab")


if __name__ == "__main__":
    main()
