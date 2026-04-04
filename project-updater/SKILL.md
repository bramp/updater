---
name: project-updater
description: Core philosophy, standards, and workflow for updating open-source projects to modern, clean, and testable states.
---

# Project Updater (Generic)

This skill defines the foundational philosophy and incremental workflow for updating any open-source project. Language-specific skills (e.g., `go-updater`, `flutter-updater`, `java-updater`) inherit these standards and provide implementation details.

## Core Philosophy

1.  **Modernize**: Always bump to the latest stable language versions and dependencies. Use modern language features and idioms.
2.  **Clean & Maintainable**: Remove dead code, unused constants, and deprecated API usage. Follow the principle of "leave it better than you found it."
3.  **Testable**: Ensure the project has a working test suite. If tests are missing or broken, fixing/adding them is a priority. Use Dependency Injection and pure functions to improve testability.
4.  **Standardize**: Use a consistent project structure and command interface (e.g., a standard `Makefile`) across all projects of the same language.
5.  **Automate**: Every project must have GitHub Actions for CI (testing/analysis) and, where appropriate, CD (deployment/publishing).
6.  **Incremental Progress**: Perform updates in small, logical, and stable steps. Commit frequently with clear messages.

## Standard Incremental Workflow

Updating a project should be done in small, stable steps. Commit after each step.

1.  **Checkout & Baseline**:
    - Clone the project and run existing tests/analysis to establish a baseline.
    - Resolve any immediate issues in the current state.

2.  **Modernize Infrastructure**:
    - Add/update `Makefile` to match template naming conventions.
    - Add/update GitHub workflows (e.g., `.github/workflows/test.yml`).
    - Add/update `.github/dependabot.yml` for automated dependency updates.
    - Add/update `.pre-commit-config.yaml` for formatting and basic checks.
    - **Standardize README Header**: Ensure `README.md` uses the standard header format.
    - **Commit**: "chore: adopt standard github workflows, makefile, and readme header"

3.  **Bump Dependencies**:
    - Update language version constraints (e.g., in `go.mod`, `pubspec.yaml`, `pom.xml`).
    - Run language-specific upgrade commands (e.g., `dart pub upgrade`, `go mod tidy`, `mvn versions:display-dependency-updates`).
    - Verify with `make analyze` and `make test`.
    - **Commit**: "chore: update sdk and dependencies"

4.  **Analysis Improvements**:
    - Switch to stricter, modern linting rules (e.g., `very_good_analysis` for Dart, `staticcheck` for Go).
    - Run `make fix` to apply automated changes.
    - **Commit**: "chore: update analysis options and apply auto-fixes"

5.  **Manual Code Clean-up**:
    - Fix remaining warnings/errors (deprecated APIs, architectural issues).
    - **Commit small batches**: "refactor: fix deprecated API usage", "style: format TODO comments"

6.  **Publishing/Deployment Prep**:
    - Update `CHANGELOG.md` with new entries.
    - Perform a dry-run of the publishing process (if applicable).
    - **Commit**: "chore: update changelog for vX.Y.Z"

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
- Optional: `.github/workflows/deploy.yml` (CD for deployment), `.github/workflows/publish.yml` (CD for publishing).
- Use official GitHub-provided actions where possible.

### 3. Documentation
- **Standard README Header**:
  1.  **Project Title**: `# {PROJECT_NAME}`
  2.  **Description**: A brief, one-sentence summary.
  3.  **Author & Copyright**: `by Andrew Brampton ([bramp.net](https://bramp.net)) (c) {YEARS}`
  4.  **Buy Me A Coffee**: `[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/bramp)`
  5.  **Badges**: Relevant badges (CI status, coverage, version, etc.).
  6.  **Links**: Primary links (GitHub, Docs, etc.).
  7.  **Divider**: A horizontal rule `---` before the main content.
- Maintain a clean `CHANGELOG.md`.
