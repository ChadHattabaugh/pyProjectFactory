#!/usr/bin/env python3
"""
Simple setup script for {{PROJECT_NAME}}.
For project automation, use: nox -l (to list tasks) or nox -s <task>
"""

import subprocess
import sys


def main():
    """Setup development environment."""
    print("🔧 Setting up development environment...")

    # Install dependencies
    print("\n📦 Installing dependencies...")
    result = subprocess.run(['uv', 'sync', '--extra', 'dev', '--extra', 'data'])
    if result.returncode != 0:
        print("❌ Failed to install dependencies")
        return 1

    # Setup pre-commit hooks
    print("\n🪝 Setting up pre-commit hooks...")
    result = subprocess.run(['uv', 'run', 'pre-commit', 'install'])
    if result.returncode != 0:
        print("⚠️  Pre-commit setup failed (may not be configured)")

    print("\n✅ Development environment ready!")
    print("\n🚀 Next steps:")
    print("  nox -l              # List all available tasks")
    print("  nox -s tests        # Run tests")
    print("  nox -s ci           # Run full CI pipeline")
    print("  uv run pytest       # Run tests directly")
    return 0


if __name__ == '__main__':
    sys.exit(main())
