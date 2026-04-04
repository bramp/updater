---
name: package-updater
description: A skill for updating and re-publishing open source packages (Dart, Go, etc.), adopting modern GitHub workflows and project structures.
---

# Package Updater

This skill helps you update outdated packages, ensuring they follow modern standards, use automated GitHub workflows, and adhere to engineering best practices.

## Incremental Workflow

Updating a package should be done in small, logical, and stable steps. Commit after each step to maintain a clear history and allow for easy reverts.

1. **Checkout & Baseline**:
    - Clone the package and run existing tests/analysis to establish a baseline.
    - Resolve any immediate issues in the current state.

2. **Migrate Infrastructure (if needed)**:
    - **Dart/Flutter**: If migrating from Melos to standard Dart workspaces:
        - Add `workspace` and `resolution: workspace` to `pubspec.yaml` (requires SDK ^3.5.0).
        - Create a `Makefile` that replicates all Melos scripts.
        - Remove `melos.yaml` and `melos` from dependencies.
    - **Go**: Ensure the project uses Go modules (`go.mod`).
    - **Commit**: "chore: migrate infrastructure to modern standards"

3. **Adopt Standard Workflows & Structure**:
    - Add or update GitHub workflows (e.g., `.github/workflows/test.yml`).
    - Add `.github/dependabot.yml` to keep dependencies updated automatically.
    - Add `.pre-commit-config.yaml` to ensure consistent formatting and analysis before commits.
    - Update `Makefile` to match template naming conventions.
    - **Standardize README Header**: Ensure `README.md` uses the standard header template with the correct title, author/link, Buy Me A Coffee link, description, badges, and links.
    - **Commit**: "chore: adopt standard github workflows, makefile structure, and readme header"

4. **Dependency Update**:
    - **Dart/Flutter**:
        - Upgrade SDK constraints.
        - Run `dart pub outdated`.
        - Run `dart pub upgrade --major-versions --tighten`.
    - **Go**:
        - Upgrade Go version in `go.mod`.
        - Run `go mod tidy`.
        - Run `go get -u ./...`.
    - Verify with `make analyze` and `make test`.
    - **Commit**: "chore: update sdk and dependencies"

5. **Analysis Improvements**:
    - **Dart/Flutter**: Switch to `package:very_good_analysis`.
    - **Go**: Use `staticcheck` and `go vet`.
    - Run `make analyze` and identify new issues.
    - Apply `make fix`.
    - **Commit**: "chore: update analysis options and apply auto-fixes"

6. **Manual Code Fixes**:
    - Fix remaining analysis warnings/errors (e.g., deprecated APIs, unused variables).
    - Adhere to `AGENTS.md` guidelines for naming, testing, and structure.
    - **Commit small batches**: "refactor: fix deprecated API usage", "style: format TODO comments"

7. **Publishing/Deployment Preparation**:
    - Prepend changes to `CHANGELOG.md` (keep historical entries!).
    - **Dart**: Run `dart pub publish --dry-run` and ask for permission before actual publish.
    - **Go**: Tag a new version and push.
    - **Commit**: "chore: update changelog for vX.Y.Z"

## Engineering Standards (from AGENTS.md)

- **Mandatory Review**: Always present a summary or diff of changes to the user and wait for explicit approval before performing any `git commit`.
- **Atomic Commits**: Stage specific files (`git add [file]`) rather than everything (`git add .`).
- **Pre-commit Hooks**: Always run `pre-commit run --all-files` before committing and re-stage any modified files.
- **Safety**: Avoid destructive commands like `git reset --hard` or `rm -f` without explicit user permission.

## Makefile Standards

A standard `Makefile` should support:
- `all`: Runs `format`, `analyze`, and `test`.
- `format`: Runs the language-specific formatter.
- `analyze`: Runs static analysis tools.
- `test`: Runs the full test suite.
- `test-ci`: Replicates the test command used in GitHub Actions.
- `fix`: Runs automated fix tools.
- `upgrade`: Upgrades all dependencies to their latest compatible versions.

## GitHub Workflows

- `test.yml`: CI validation (format, analyze, test).
- `publish.yml`: CD for publishing to a registry (e.g., pub.dev).
- `deploy.yml`: CD for deployment (e.g., GitHub Pages, App Engine).
