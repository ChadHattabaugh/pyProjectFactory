# pyProjectTemplate GitHub Labeling System

This document describes the comprehensive labeling system used in the pyProjectTemplate repository to organize issues, facilitate automation, and enable efficient collaboration between maintainers and Claude AI.

## Label Categories

### 🏷️ Type Labels
Classify the nature of the issue or pull request:

- `type: bug` - Something isn't working correctly
- `type: feature` - New functionality or enhancement request  
- `type: enhancement` - Improvement to existing functionality
- `type: docs` - Documentation improvements or additions
- `type: refactor` - Code restructuring without changing functionality
- `type: test` - Adding or improving tests
- `type: ci/cd` - Continuous integration/deployment changes
- `type: security` - Security-related issues or improvements
- `type: performance` - Performance optimization
- `type: maintenance` - Routine maintenance tasks

### 🚨 Priority Labels
Indicate urgency and importance:

- `priority: critical` - Urgent fixes needed (security, major bugs)
- `priority: high` - Important issues that should be addressed soon
- `priority: medium` - Standard priority issues
- `priority: low` - Nice-to-have improvements or minor issues

### 📊 Status Labels
Track the current state of work:

- `status: needs-review` - Waiting for maintainer review
- `status: in-progress` - Currently being worked on
- `status: blocked` - Cannot proceed due to dependencies
- `status: ready` - Ready for implementation
- `status: on-hold` - Temporarily paused
- `status: duplicate` - Duplicate of another issue
- `status: wontfix` - Will not be implemented

### 🎯 Area Labels
Specify which part of the project is affected:

- `area: template` - Template structure and generation
- `area: ci/cd` - GitHub Actions and automation
- `area: docs` - Documentation and guides
- `area: setup` - Project setup and configuration
- `area: testing` - Test framework and test cases
- `area: dependencies` - Package dependencies and management
- `area: docker` - Docker environments and containers
- `area: github` - GitHub-specific features (workflows, rulesets)

### 🤖 Claude AI Labels
Special labels for AI-assisted development:

- `claude: implementation` - Issues suitable for Claude to implement
- `claude: review` - Requires Claude AI code review
- `claude: research` - Research tasks for Claude to investigate
- `claude: documentation` - Documentation tasks for Claude
- `claude: analysis` - Code analysis or investigation needed

### ⚡ Effort Labels
Estimate the work required:

- `effort: small` - Quick fixes, 1-2 hours of work
- `effort: medium` - Standard issues, half-day to full-day
- `effort: large` - Complex issues, multiple days of work
- `effort: extra-large` - Major features, week+ of work

### 🌟 Special Labels
Additional categorization:

- `good first issue` - Suitable for new contributors
- `help wanted` - Community assistance needed
- `breaking change` - Will break backward compatibility
- `dependencies` - Dependency updates (often used by Dependabot)
- `question` - General questions or discussions

## Usage Guidelines

### For Issue Creators
When creating a new issue:

1. **Always apply a type label** - Choose the most appropriate `type:` label
2. **Set priority** - Use `priority:` labels to indicate urgency
3. **Specify area** - Add relevant `area:` labels for the affected components
4. **Estimate effort** - If known, add an `effort:` label to help with planning

### For Maintainers
When triaging issues:

1. **Validate labels** - Ensure appropriate type and priority labels are set
2. **Add status labels** - Use `status:` labels to track progress
3. **Tag for Claude** - Use `claude:` labels for AI-suitable tasks
4. **Update effort estimates** - Adjust `effort:` labels based on analysis

### For Claude AI
Claude AI should look for issues with:

- `claude: implementation` - Direct implementation tasks
- `claude: review` - Code review requests
- `claude: research` - Investigation and analysis tasks
- `claude: documentation` - Documentation improvements

When working on issues, Claude should:
1. Add `status: in-progress` when starting work
2. Update to `status: needs-review` when requesting human review
3. Add `status: ready` when implementation is complete

## Label Colors

Labels use consistent color coding:
- **Type labels**: Blue shades (`#1f77b4` family)
- **Priority labels**: Red gradient (critical=red, low=light red)
- **Status labels**: Green/yellow spectrum based on progress
- **Area labels**: Purple shades (`#9467bd` family)  
- **Claude labels**: Orange (`#ff7f0e` family)
- **Effort labels**: Gray gradient (`#7f7f7f` family)
- **Special labels**: Unique colors for visibility

## Automation Integration

The labeling system integrates with:

### GitHub Actions
- Issues with `dependencies` label trigger dependency update workflows
- `ci/cd` labeled issues run additional CI validation
- `claude:` labels can trigger AI notification workflows

### Project Management
- `priority:` labels help with sprint planning
- `effort:` labels assist with capacity planning
- `status:` labels track workflow states

### Filtering and Search
Use label combinations for targeted searches:
```
# Find all high-priority bugs
is:issue label:"type: bug" label:"priority: high"

# Find issues ready for Claude AI
is:issue label:"claude: implementation" label:"status: ready"

# Find small documentation tasks
is:issue label:"type: docs" label:"effort: small"
```

## Best Practices

### Label Maintenance
- Review and update labels regularly
- Remove outdated status labels when issues are resolved
- Ensure consistent labeling across similar issues

### Avoiding Label Pollution
- Don't apply conflicting labels (e.g., multiple priority levels)
- Remove irrelevant labels when issue scope changes
- Use specific rather than general labels when possible

### Communication
- Use labels to communicate issue state clearly
- Update labels when requirements or scope change
- Document label changes in issue comments when significant

## Examples

### Bug Report
```
Labels: type: bug, priority: high, area: ci/cd, effort: medium, status: ready
```

### Feature Request
```
Labels: type: feature, priority: medium, area: template, effort: large, claude: implementation
```

### Documentation Task
```
Labels: type: docs, priority: low, area: docs, effort: small, claude: documentation, good first issue
```

### Security Issue
```
Labels: type: security, priority: critical, area: dependencies, effort: medium, status: in-progress
```

This labeling system ensures consistent issue management, improves project organization, and facilitates effective collaboration between human maintainers and Claude AI.