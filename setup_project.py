#!/usr/bin/env python3
"""Interactive project setup script for the Python template."""

import os
import platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email or len(email) < 5 or len(email) > 254:
        return False
    
    # Basic email pattern with more robust validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # Check for valid domain part
    local, domain = email.rsplit('@', 1)
    if len(local) > 64 or len(domain) > 253:
        return False
        
    return True


def validate_project_name(name: str) -> bool:
    """Validate project name format."""
    if not name or len(name) < 2 or len(name) > 214:
        return False
    
    # Must start with letter, can contain letters, numbers, hyphens
    # but not end with hyphen
    pattern = r'^[a-z][a-z0-9-]*[a-z0-9]$'
    if len(name) == 1:
        pattern = r'^[a-z]$'
    
    if not re.match(pattern, name):
        return False
    
    # Check for reserved names
    reserved_names = {'test', 'tests', 'src', 'lib', 'bin', 'tmp', 'temp', 'build', 'dist'}
    if name in reserved_names:
        return False
        
    return True


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
    except (PermissionError, OSError) as e:
        print(f"⚠️  Could not process {file_path}: {e}")
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
├── run.py                                # Setup script
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
nox -s tests
# or: uv run pytest

# Test with coverage
uv run pytest --cov

# Test all Python versions
nox -s tests
```

### Code Quality
```bash
# Format code
nox -s format

# Lint code  
nox -s lint

# Type check
nox -s type_check

# All quality checks
nox -s ci
```

### Automation
```bash
# Full CI pipeline
nox -s ci

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
nox -s docker_dev

# Access development shell
docker compose exec dev bash

# Stop services
docker compose down
```

"""

    if info.get('use_jupyter', False):
        claude_content += """### Jupyter Notebooks
```bash
# Start Jupyter Lab locally
nox -s jupyter
# Start Jupyter in Docker
nox -s docker_jupyter

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

- `python run.py` - Setup development environment
- `nox -s tests` - Run tests
- `nox -s ci` - Run full CI pipeline
- `nox -s format` - Format and fix code
- `nox -s clean` - Clean build artifacts
- `nox -l` - Show project information

## Notes for Claude

- This project uses **uv** for dependency management (faster than pip/poetry)
- **ruff** handles all code formatting and linting (replaces black+isort+flake8)
- **nox** provides automation across multiple Python versions
- **nox** provides convenient development commands
- All tools are configured in `pyproject.toml`

When helping with this project:
1. Use the existing tools and configurations
2. Follow the established patterns in the codebase
3. Add tests for new functionality
4. Update documentation as needed
5. Run `nox -s ci` before committing changes

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


def get_files_to_remove(info: Dict[str, Any]) -> List[str]:
    """Build list of template files to remove based on user configuration.

    Args:
        info: Dictionary containing user configuration choices

    Returns:
        List of file/directory paths (relative to project root) to remove
    """
    files_to_remove = [
        # Always remove template-specific files
        'setup_project.py',
        'ROADMAP.md',
        'copier.yml',
        'CLAUDE.md.template',
        'docs/GITHUB_PROJECT_SETUP.md',
        'docs/REPOSITORY_SETUP.md',
        'docs/GITHUB_LABELS.md',
        '.github/workflows/setup-repository-protection.yml',
        '.github/workflows/ci.yml.template',
    ]

    # Conditional removals based on user selections
    if not info.get('use_jupyter', False):
        files_to_remove.append('notebooks')

    if not info.get('use_spark', False):
        files_to_remove.append('scripts/setup_spark.py')

    if not info.get('use_docker', True):
        files_to_remove.extend([
            'Dockerfile.dev',
            'Dockerfile.data',
            'docker-compose.yml',
            '.dockerignore',
        ])

    if not info.get('use_github_actions', True):
        files_to_remove.extend([
            '.github/workflows/ci.yml',
            '.github/workflows/release.yml',
        ])

    if not info.get('use_pre_commit', True):
        files_to_remove.append('.pre-commit-config.yaml')

    # Remove empty docs directory if it only had template docs
    template_docs = [
        'docs/GITHUB_PROJECT_SETUP.md',
        'docs/REPOSITORY_SETUP.md',
        'docs/GITHUB_LABELS.md'
    ]
    if all(f in files_to_remove for f in template_docs):
        files_to_remove.append('docs')

    return files_to_remove


def cleanup_template_files(project_dir: Path, info: Dict[str, Any]) -> List[str]:
    """Remove template-specific files from the generated project.

    Args:
        project_dir: Path to the generated project directory
        info: Dictionary containing user configuration choices

    Returns:
        List of files/directories that were successfully removed
    """
    files_to_remove = get_files_to_remove(info)
    removed_files = []

    print("\n🧹 Cleaning up template files...")

    for file_path in files_to_remove:
        full_path = project_dir / file_path

        try:
            if full_path.exists():
                if full_path.is_dir():
                    shutil.rmtree(full_path)
                    removed_files.append(f"📁 {file_path}/")
                else:
                    full_path.unlink()
                    removed_files.append(f"📄 {file_path}")
        except (PermissionError, OSError) as e:
            print(f"⚠️  Could not remove {file_path}: {e}")

    return removed_files


def verify_template_placeholders(project_dir: Path, info: Dict[str, Any]) -> List[str]:
    """Verify that no template placeholders remain in project files.

    Args:
        project_dir: Path to the generated project directory
        info: Dictionary containing user configuration choices

    Returns:
        List of files that still contain template placeholders
    """
    placeholder_pattern = re.compile(r'\{\{[A-Z_]+\}\}')
    files_with_placeholders = []

    # Check common text files for placeholders
    extensions_to_check = {'.py', '.md', '.yml', '.yaml', '.toml', '.txt', '.sh', '.json'}

    for file_path in project_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix in extensions_to_check:
            try:
                content = file_path.read_text(encoding='utf-8')
                if placeholder_pattern.search(content):
                    rel_path = file_path.relative_to(project_dir)
                    files_with_placeholders.append(str(rel_path))
            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or files we can't read
                pass

    return files_with_placeholders


def is_template_repo() -> bool:
    """Check if current directory is a cloned template repository.

    Returns:
        True if current directory appears to be a template repo, False otherwise
    """
    cwd = Path.cwd()

    # Check for template markers
    markers = [
        cwd / 'setup_project.py',
        cwd / 'copier.yml',
        cwd / 'src' / '{{PROJECT_NAME}}'
    ]

    return all(marker.exists() for marker in markers)


def is_git_initialized() -> bool:
    """Check if current directory already has git initialized.

    Returns:
        True if .git directory exists, False otherwise
    """
    return (Path.cwd() / '.git').exists()


def check_dependencies() -> None:
    """Check if required tools are installed."""
    # Check uv (required for project setup)
    try:
        subprocess.run(['uv', '--version'], capture_output=True, check=True, timeout=10)
        print("✅ uv is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ Missing required tool: uv")
        print("Please install uv first: https://docs.astral.sh/uv/getting-started/installation/")
        print("uv is required for Python dependency management.")
        exit(1)


def initialize_git(project_dir: Path, info: Dict[str, Any]) -> None:
    """Initialize git repository and create development branch."""
    try:
        subprocess.run(['git', 'init'], cwd=project_dir, check=True, capture_output=True, timeout=30)
        subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True, capture_output=True, timeout=60)
        subprocess.run(['git', 'commit', '-m', 'Initial project setup\n\n🤖 Generated with Claude Code'], cwd=project_dir, check=True, capture_output=True, timeout=30)
        
        # Create and switch to develop branch following GitFlow
        subprocess.run(['git', 'checkout', '-b', 'develop'], cwd=project_dir, check=True, capture_output=True, timeout=30)
        
        print("✅ Git repository initialized with develop branch")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git initialization failed: {e}")


def setup_development_environment(project_dir: Path) -> None:
    """Set up the development environment automatically."""
    try:
        print("🔧 Setting up development environment...")

        # Run uv sync to install dependencies
        subprocess.run(['uv', 'sync', '--extra', 'dev'], cwd=project_dir, check=True, capture_output=True, timeout=300)

        # Install pre-commit hooks if available
        try:
            subprocess.run(['uv', 'run', 'pre-commit', 'install'], cwd=project_dir, check=True, capture_output=True, timeout=60)
            print("✅ Pre-commit hooks installed")
        except subprocess.CalledProcessError:
            print("⚠️  Pre-commit installation skipped (not configured)")

        print("✅ Development environment ready")

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Development environment setup failed: {e}")
        print("You can manually run 'python run.py' or 'uv sync --extra dev' in the project directory")


def setup_in_place(project_dir: Path, info: Dict[str, Any]) -> None:
    """Setup project in place, replacing template files.

    Args:
        project_dir: Path to the current directory (where template exists)
        info: Dictionary containing project configuration
    """
    import tempfile

    print(f"\n🔧 Setting up project '{info['project_name']}' in place...")

    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Process template files into temp directory
        print("📦 Processing template files...")
        process_template_directory(project_dir, temp_path, info)

        # Create CLAUDE.md in temp directory
        create_claude_md(temp_path, info)

        # Remove template-specific files from current directory
        print("🧹 Cleaning up template files...")
        cleanup_template_files(project_dir, info)

        # Copy processed files from temp to current directory
        print("📋 Installing new project files...")
        for item in temp_path.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(temp_path)
                dst_path = project_dir / rel_path
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_path)

    # Initialize git only if not already initialized
    if not is_git_initialized():
        initialize_git(project_dir, info)
    else:
        print("✅ Git already initialized, preserving existing repository")

    # Set up development environment
    setup_development_environment(project_dir)

    # Verify no template placeholders remain
    files_with_placeholders = verify_template_placeholders(project_dir, info)
    if files_with_placeholders:
        print("\n⚠️  Warning: Template placeholders found in the following files:")
        for file in files_with_placeholders[:5]:  # Show first 5
            print(f"   - {file}")
        if len(files_with_placeholders) > 5:
            print(f"   ... and {len(files_with_placeholders) - 5} more")

    print(f"\n✅ Project '{info['project_name']}' created successfully in place!")
    print(f"📁 Location: {project_dir}")
    print("\n✅ Setup complete! Your project is ready for development.")
    print(f"\n🚀 To get started:")
    print("1. nox -l         # List available tasks")
    print("2. nox -s tests   # Run tests to verify setup")
    print("3. Start coding!")

    if info.get('use_jupyter', False):
        print("4. nox -s jupyter # Start Jupyter Lab for data analysis")

    print("\n📚 See CLAUDE.md for detailed development workflow and commands.")


def main() -> None:
    """Main setup function with smart template detection."""
    # Check dependencies first
    check_dependencies()

    # Collect project information
    info = collect_project_info()

    # Smart workflow detection
    is_template = is_template_repo()

    if is_template:
        # Repository was created from GitHub template
        print("\n🔍 Template repository detected!")
        in_place = get_user_input(
            "Replace template with new project in current directory?",
            default="y",
            is_bool=True
        )

        if in_place:
            # In-place setup
            project_dir = Path.cwd()
            setup_in_place(project_dir, info)
            return
        else:
            # User chose to create in new folder instead
            print("\n📁 Creating project in new folder...")

    else:
        # Not a template repository - offer in-place or new folder
        in_place = get_user_input(
            "Setup project in current directory (in-place)?",
            default="n",
            is_bool=True
        )

        if in_place:
            # In-place setup
            project_dir = Path.cwd()
            setup_in_place(project_dir, info)
            return

    # New folder setup (original behavior)
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

    # Initialize git with development branch (always for new folders)
    initialize_git(project_dir, info)

    # Set up development environment automatically
    setup_development_environment(project_dir)

    # Clean up template files
    removed_files = cleanup_template_files(project_dir, info)

    # Verify no template placeholders remain
    files_with_placeholders = verify_template_placeholders(project_dir, info)
    if files_with_placeholders:
        print("\n⚠️  Warning: Template placeholders found in the following files:")
        for file in files_with_placeholders[:5]:  # Show first 5
            print(f"   - {file}")
        if len(files_with_placeholders) > 5:
            print(f"   ... and {len(files_with_placeholders) - 5} more")

    # Print cleanup summary
    if removed_files:
        print(f"\n✨ Removed {len(removed_files)} template-specific files:")
        for file in removed_files[:10]:  # Show first 10
            print(f"   {file}")
        if len(removed_files) > 10:
            print(f"   ... and {len(removed_files) - 10} more")

    print(f"\n�� Project '{info['project_name']}' created successfully!")
    print(f"📁 Location: {project_dir}")
    print("\n✅ Setup complete! Your project is ready for development.")
    print(f"\n🚀 To get started:")
    print(f"1. cd {info['project_name']}")
    print("2. nox -l         # List available tasks")
    print("3. nox -s tests   # Run tests to verify setup")
    print("4. Start coding!")

    if info.get('use_jupyter', False):
        print("5. nox -s jupyter # Start Jupyter Lab for data analysis")

    print("\n📚 See CLAUDE.md for detailed development workflow and commands.")


if __name__ == "__main__":
    main()
