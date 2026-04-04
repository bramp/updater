---
name: project-updater
description: Core philosophy and standards for updating open-source projects to modern, clean, and testable states.
---

# Project Updater (Generic)

This skill defines the foundational philosophy for updating any open-source project. Language-specific skills (e.g., `go-updater`, `flutter-updater`) should be used in conjunction with this one.

## Core Philosophy

1.  **Modernize**: Always bump to the latest stable language versions and dependencies. Use modern language features and idioms.
2.  **Clean & Maintainable**: Remove dead code, unused constants, and deprecated API usage. Follow the principle of "leave it better than you found it."
3.  **Testable**: Ensure the project has a working test suite. If tests are missing or broken, fixing/adding them is a priority. Use Dependency Injection and pure functions to improve testability.
4.  **Standardize**: Use a consistent project structure and command interface (e.g., a standard `Makefile`) across all projects of the same language.
5.  **Automate**: Every project must have GitHub Actions for CI (testing/analysis) and, where appropriate, CD (deployment/publishing).
6.  **Incremental Progress**: Perform updates in small, logical, and stable steps. Commit frequently with clear messages.

## Standard Requirements for Every Project

### 1. Command Interface (Makefile)
Every project must have a `Makefile` that provides a standard entry point for common tasks:
- `make all`: The default target, running format, analyze, and test.
- `make format`: Formats the source code.
- `make analyze`: Performs static analysis/linting.
- `make test`: Runs the full test suite.
- `make test-ci`: The exact command used by CI.
- `make fix`: Applies automated fixes.
- `make upgrade`: Upgrades all dependencies to their latest compatible versions.
- `make check-upgrade`: Checks for available dependency updates without applying them (e.g., `npm outdated`, `go list -u -m all`).

### 2. Continuous Integration (GitHub Actions)
Every project must have a `.github/workflows/test.yml` that runs on every push and PR to `main`. It should:
- Use official GitHub-provided actions where possible (e.g., `actions/checkout`, `actions/setup-node`, `actions/setup-go`) to ensure high trust and security.
- Setup the correct environment (Go, Flutter, etc.).
- Install dependencies.
- Run `make format`, `make analyze`, and `make test-ci`.

Every project must have a `.github/dependabot.yml` to automatically keep dependencies updated.

Where appropriate, add:
- `.github/workflows/deploy.yml`: CD for deployment (e.g., GitHub Pages). For static sites, use official actions (`upload-pages-artifact`, `deploy-pages`).
- `.github/workflows/publish.yml`: CD for publishing to registries (e.g., NPM, pub.dev).

### 3. Pre-commit Hooks
Add a `.pre-commit-config.yaml` to the root to enforce formatting and basic checks before every commit.

### 4. Documentation
- **Standard README Header**: Every project must have a consistent header in its `README.md` following this structure:
  1.  **Project Title**: `# {PROJECT_NAME}`
  2.  **Description**: A brief, one-sentence summary.
  3.  **Author & Copyright**: `by Andrew Brampton ([bramp.net](https://bramp.net)) (c) {YEARS}`
  4.  **Buy Me A Coffee**: `[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/bramp)`
  5.  **Badges**: Relevant badges (CI status, coverage, version, etc.).
  6.  **Links**: Primary links (GitHub, Docs, etc.).
  7.  **Divider**: A horizontal rule `---` before the main content.
- Maintain a clean `CHANGELOG.md`.

## Workflow

1.  **Baseline**: Run existing tests/analysis. If it doesn't pass, fix the "legacy" state first.
2.  **Modernize Infrastructure**: Update `Makefile`, GitHub Actions, and `pre-commit` configs.
3.  **Bump Dependencies**: Update language versions and libraries.
4.  **Surgical Clean-up**: Fix lint warnings, deprecations, and architectural issues.
5.  **Validate**: Ensure `make all` passes locally and in CI.
