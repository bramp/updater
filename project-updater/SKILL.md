---
name: project-updater
description: Core philosophy, standards, and workflow for updating or creating open-source projects to modern, clean, and testable states.
---

# Project Updater (Generic)

This skill defines the foundational philosophy and incremental workflow for updating or creating any open-source project. Language-specific skills (e.g., `go-updater`, `flutter-updater`, `java-updater`) inherit these standards and provide implementation details.

## Core Philosophy

1.  **Modernize**: Always target the latest stable language versions and dependencies. Use modern language features and idioms.
2.  **Clean & Maintainable**: Remove dead code, unused constants, and deprecated API usage. Follow the principle of "leave it better than you found it."
3.  **Testable**: Ensure every project has a working test suite. If tests are missing or broken, fixing/adding them is a priority.
4.  **Standardize**: Use a consistent project structure and command interface (e.g., a standard `Makefile`) across all projects.
5.  **Automate**: Every project must have GitHub Actions for CI (testing/analysis) and, where appropriate, CD (deployment/publishing).
6.  **Incremental Progress**: Perform work in small, logical, and stable steps. Commit frequently with clear messages.

## Project Scaffolding (New Projects)

If the project directory is empty or just initialized with git, follow these steps before the standard workflow:

1.  **Initialize**: Run `git init` and create a basic directory structure if necessary.
2.  **Scaffold from Templates**: Copy the relevant templates from `templates/{language}/` into the project root.
3.  **Customize**: Rename placeholders (e.g., `{PROJECT_NAME}`) in the `Makefile`, `README.md`, and configuration files to match the new project.
4.  **Baseline Commit**: "chore: initial project scaffolding from template"

## Standard Incremental Workflow

Work should be done in small, stable steps. Commit after each step.

1.  **Checkout & Baseline**:
    - **Existing Projects**: Clone the project and run existing tests/analysis to establish a baseline. Resolve immediate issues.
    - **New Projects**: Follow the **Project Scaffolding** steps above.

2.  **Modernize Infrastructure**:
    - Add/update `Makefile` from `templates/{language}/Makefile`.
    - Add/update GitHub workflows (e.g., `.github/workflows/test.yml`) using `templates/{language}/test.yml` or `templates/common/`.
    - Add/update `.github/dependabot.yml`.
    - Add/update `.pre-commit-config.yaml` for formatting and basic checks.
    - **Standardize README Header**: Ensure `README.md` uses the standard header format (template: `templates/common/readme_header.md`).
    - **Commit**: "chore: adopt standard github workflows, makefile, and readme header"

3.  **Dependencies & SDK**:
    - Update language version constraints (e.g., `go.mod`, `pubspec.yaml`, `pom.xml`).
    - Run language-specific upgrade/init commands (e.g., `dart pub upgrade`, `go mod tidy`, `mvn versions:display-dependency-updates`).
    - Verify with `make analyze` and `make test`.
    - **Commit**: "chore: update sdk and dependencies"

4.  **Analysis & Fixes**:
    - Enable strict, modern linting rules.
    - Run `make fix` to apply automated changes.
    - **Commit**: "chore: update analysis options and apply auto-fixes"

5.  **Implementation / Clean-up**:
    - **Existing**: Fix remaining warnings/errors (deprecated APIs, etc.).
    - **New**: Implement the initial core logic and tests.
    - **Commit small batches**: "refactor: fix deprecated API usage" or "feat: implement core logic"

6.  **Release Preparation**:
    - Ensure `CHANGELOG.md` is present and updated.
    - **Commit**: "chore: prepare for v0.1.0" or "chore: update changelog"

## Standard Requirements for Every Project

### 1. Command Interface (Makefile)
Every project must have a `Makefile` with these standard targets:
- `all`: The default target, running format, analyze, and test.
- `format`: Formats the source code.
- `analyze`: Performs static analysis/linting.
- `test`: Runs the full test suite.
- `test-ci`: The exact command used by CI.
- `fix`: Applies automated fixes.
- `upgrade`: Upgrades all dependencies to their latest compatible versions.

### 2. Continuous Integration (GitHub Actions)
- `.github/workflows/test.yml`: CI validation (format, analyze, test).
- `.github/dependabot.yml`: Automated dependency updates.
- Use official GitHub-provided actions where possible.

### 3. Documentation
- **Standard README Header**: Mandatory use of `templates/common/readme_header.md` structure.
- **CHANGELOG.md**: Mandatory tracking of changes.
