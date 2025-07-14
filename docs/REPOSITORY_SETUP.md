# pyProjectTemplate Repository Protection Setup Guide

pyProjectTemplate includes automated repository protection setup to enforce GitFlow branching strategy and code quality standards.

## Automatic Setup

When you create a new repository from this template, the following will be automatically configured:

### Repository Protection Rules

The automated setup will configure repository protection rules for your branches.

### CI/CD Pipeline

pyProjectTemplate includes two CI configurations:
- **Template CI** (current): Validates the template repository structure
- **Project CI** (deployed): Full CI/CD pipeline for your actual project

When you run `python setup_project.py`, the template CI is replaced with a full-featured CI pipeline that includes:
- Multi-platform testing (Ubuntu, Windows, macOS)
- Python version matrix testing (3.9-3.12)
- Code quality checks (ruff, mypy)
- Security scanning (safety, bandit)
- Package building and testing
- Optional notebook quality checks

### Branch Protection Rules

#### Protected Branches
- `master` - Production-ready code (protected from direct pushes)
- `develop` - Integration branch for features (protected from direct pushes)

#### Protection Requirements
- **2 required reviewers**: Author approval + AI reviewer (Claude)
- **Commit message pattern**: Must include issue number (e.g., `feat: add login (#123)`)
- **No direct pushes**: All changes must come via pull requests
- **No force pushes**: Prevents rewriting history
- **No deletions**: Protects branches from accidental removal
- **Status checks**: All CI/CD checks must pass

### Branch Naming Convention

New branches must follow these naming patterns:
- `feature/description` - New features
- `bugfix/description` - Bug fixes  
- `patch/description` - Small patches or hotfixes

**Examples:**
- `feature/user-authentication`
- `bugfix/login-error-handling`
- `patch/security-update`

## Manual Setup (if automation fails)

### 1. Create Develop Branch
```bash
git checkout -b develop
git push -u origin develop
```

### 2. Configure GitHub Rulesets

Go to your repository Settings → Rules → Rulesets and create:

#### Branch Naming Ruleset
- **Name**: Branch Naming Convention
- **Target**: All branches (`**`)
- **Rules**: Restrict creations
- **Exclude patterns**: `master`, `develop`, `feature/**`, `bugfix/**`, `patch/**`

#### Protected Branch Ruleset
- **Name**: Protected Branches
- **Target**: `master`, `develop` (no main branch)
- **Rules**:
  - Require pull request reviews (2 reviewers)
  - Require status checks
  - Block direct pushes (PR only)
  - Block force pushes
  - Restrict deletions
  - Commit message pattern: `.*#\\d+.*`

### 3. Install Claude AI Integration

1. Install Claude Code GitHub App: https://github.com/apps/claude-code
2. Configure as required reviewer in repository settings
3. Grant necessary permissions for code review

## Workflow Process

### Creating New Features
1. Start from `develop` branch:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-new-feature
   ```

2. Make changes with proper commit messages:
   ```bash
   git commit -m "feat: add user authentication (#123)"
   ```

3. Push and create pull request:
   ```bash
   git push -u origin feature/my-new-feature
   # Create PR targeting develop branch
   ```

### Release Process
1. Create release branch from `develop`:
   ```bash
   git checkout -b release/v1.0.0 develop
   ```

2. Test and finalize release
3. Merge to `master` and tag:
   ```bash
   git checkout master
   git merge release/v1.0.0
   git tag v1.0.0
   ```

4. Merge back to `develop`:
   ```bash
   git checkout develop
   git merge release/v1.0.0
   ```

## Troubleshooting

### Branch Creation Failed
If you can't create a branch, ensure it follows the naming convention:
- Must start with `feature/`, `bugfix/`, or `patch/`
- Use lowercase with hyphens instead of spaces

### Commit Rejected
If your commit is rejected:
- Ensure commit message includes issue number: `#123`
- Check that all required status checks pass

### Pull Request Blocked
If PR can't be merged:
- Verify 2 approvals (author + Claude AI)
- Ensure all conversations are resolved
- Check that target branch is `develop` (not `master`)

## Benefits

- **Consistent workflow**: All repositories follow same branching strategy
- **Quality gates**: Automated checks prevent poor code quality
- **Traceability**: All changes linked to issues
- **AI assistance**: Claude provides intelligent code reviews
- **Protection**: Critical branches safe from accidental changes