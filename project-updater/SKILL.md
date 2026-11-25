---
name: project-updater
description: Core modernization workflow, Makefile contract, SHA-pinned GitHub Actions security policy, and Dependabot cooldown + auto-merge setup. Use this skill whenever scaffolding, auditing, or modernizing any open-source repository across any language.
license: BSD-3-Clause
---

# Project Updater (Core Standards)

This skill defines the foundational engineering philosophy, supply-chain security rules, and incremental workflow applied to every open-source project. Pair it with the target project's language skill (`python-updater`, `go-updater`, `js-updater`, `java-updater`, `flutter-updater`) and `gcp-updater` when deploying to Google Cloud.

## Core Philosophy

1. **Modernize**: Target current LTS/stable language runtimes and dependencies. Replace deprecated APIs and legacy tooling.
2. **Clean & Maintainable**: Remove dead code, unused configuration, and legacy build wrappers.
3. **Testable**: Every repository must have a meaningful, deterministic test suite—especially before enabling unattended Dependabot auto-merge.
4. **Standardize**: Provide a uniform `Makefile` command interface across every repository, regardless of language.
5. **Harden Supply Chain**: Pin GitHub Actions to full 40-character commit SHAs, enforce least-privilege workflow permissions, apply Dependabot release cooldowns, and publish via keyless OIDC.
6. **Incremental Progress**: Work in small, reviewable steps with atomic commits.

## Workspace Isolation

Never modify skill assets in place when updating an external repository. Clone target repositories into an ignored scratch directory (such as `work/<repo-name>/`) or work directly inside the target repository's own checkout.

## Project Scaffolding (New Projects)

If starting an empty repository:
1. Initialize git (`git init -b main`) and scaffold from the language skill's `assets/` directory plus shared files in [assets/](./assets).
2. Replace placeholders (`{PROJECT_NAME}`, `{DESCRIPTION}`, `{ECOSYSTEM}`, `{YEARS}`) across configuration files and `README.md`.
3. Commit baseline: `chore: initial project scaffolding from template`.

## Standard Incremental Workflow

Perform updates in small, verified commits:

1. **Baseline**:
   - Run the existing build and test suite to establish a green baseline before changing tooling.
2. **Modernize Infrastructure**:
   - Add/update `Makefile` using the language skill's `assets/Makefile`.
   - Add/update `.github/workflows/test.yml` (and `release.yml` / `publish.yml` / `deploy.yml` as appropriate).
   - Add/update `.github/dependabot.yml` from [assets/dependabot.yml](./assets/dependabot.yml) (replacing `{ECOSYSTEM}`) and `.github/workflows/dependabot-auto-merge.yml` from [assets/workflows/dependabot-auto-merge.yml](./assets/workflows/dependabot-auto-merge.yml).
   - Configure repository auto-merge, branch protection ruleset ([assets/ruleset-main.json](./assets/ruleset-main.json)), and **Immutable Releases** on GitHub.
   - Add/update `.pre-commit-config.yaml` from [assets/pre-commit-config.yaml](./assets/pre-commit-config.yaml) (compatible with **`prek`** and `pre-commit`).
   - Standardize the `README.md` header using [assets/readme_header.md](./assets/readme_header.md).
   - Validate workflows with `actionlint` and `zizmor` if installed.
   - **Commit**: `chore: adopt hardened github workflows, dependabot auto-merge, and makefile`
3. **Dependencies & Runtime**:
   - Upgrade runtime constraints and dependencies (`make upgrade`), then verify with `make test-ci`.
   - **Commit**: `chore: update runtime and dependencies`
4. **Static Analysis & Formatting**:
   - Enable strict modern linting/type-checking and apply automated fixes (`make fix`).
   - **Commit**: `chore: enable strict analysis and apply formatting`
5. **Code Modernization & Tests**:
   - Resolve remaining warnings, deprecated APIs, and test coverage gaps in small batches.
   - **Commit**: `refactor: modernize deprecated API usage`
6. **Release Preparation**:
   - Update `CHANGELOG.md` and verify `make test-ci` passes cleanly.

## Standard Requirements for Every Project

### 1. Uniform Command Interface (`Makefile`)
Every project must expose these targets (separating non-mutating CI checks from local write commands):
- `all`: Default target running `format-check`, `analyze`, and `test` (must not mutate lockfiles).
- `install`: Installs locked dependencies reproducibly (e.g., `uv sync --locked`, `npm ci`).
- `format`: Formats source code in place.
- `format-check`: Verifies formatting without modifying files (used in CI).
- `analyze`: Runs linters, static type checkers, and vulnerability scanners.
- `test`: Runs unit/integration tests for local iteration.
- `test-ci`: Exact non-interactive verification suite run in CI (`format-check` + `analyze` + verbose/race tests).
- `fix`: Applies safe auto-fixes and formatting.
- `upgrade`: Upgrades dependencies and refreshes lockfiles.

### 2. Hardened GitHub Actions Policy
- **Full 40-char SHA Pinning**: Every `uses:` reference to an external action **must** be pinned to a full 40-character commit SHA with a version comment (e.g., `uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`). Use `pinact run` when adding new actions; Dependabot updates both the SHA and comment automatically.
- **Least-Privilege Permissions**: Declare `permissions: contents: read` at the top of every workflow. Grant elevated permissions (`id-token: write`, `pages: write`, `pull-requests: write`, `contents: write`) **only** on the specific job that requires them.
- **Timeouts & Concurrency**: Set `timeout-minutes:` on every job (typically `15`–`20`m) and configure `concurrency:` to cancel superseded PR runs while never canceling in-progress deployments.
- **No Untrusted Shell Interpolation**: Never interpolate `${{ github.event.* }}` directly inside `run:` scripts; pass values via `env:` variables.
- **Official Keyless Publishing & Pages**: Use OIDC Trusted Publishing (PyPI, npm, pub.dev, GCP WIF) and official `actions/upload-pages-artifact` + `actions/deploy-pages` for GitHub Pages (never third-party PAT/branch-push actions).

### 3. Dependabot Cooldowns, Grouping, & Unattended Auto-Merge
Every repository must include [assets/dependabot.yml](./assets/dependabot.yml) covering **both** `"github-actions"` and the project's package ecosystem (`"uv"`, `"gomod"`, `"npm"`, `"maven"`, or `"pub"`):
- **Friday Weekly Schedule + Cooldowns**: `default-days: 7`, `semver-major-days: 30`, `semver-minor-days: 14`, `semver-patch-days: 3` (filters out acute supply-chain compromises and yanked releases).
- **Grouped Minor/Patch PRs**: Batch `minor` and `patch` updates into single grouped PRs to avoid rebase churn.
- **Scoped Unattended Auto-Merge** ([assets/workflows/dependabot-auto-merge.yml](./assets/workflows/dependabot-auto-merge.yml)):
  - Automatically approves and enables `gh pr merge --auto --squash` **only** when:
    1. `github.actor == 'dependabot[bot]'`
    2. `update-type` is `semver-patch` or `semver-minor` (`semver-major` stays open for human/agent review)
    3. `maintainer-changes != 'true'` (blocks auto-merge if package ownership changed)
    4. The target branch enforces `required_status_checks` (the workflow verifies this via the GitHub Rules API and fails closed if missing, preventing immediate untested merges).
  - **Repository Setup Commands** (run once when onboarding a repo with real test coverage):
    ```bash
    gh repo edit {OWNER}/{REPO} --enable-auto-merge --delete-branch-on-merge
    # Replace {REQUIRED_CHECK_CONTEXT} in ruleset-main.json with the exact test job name (e.g. "test" or "JDK 25")
    gh api repos/{OWNER}/{REPO}/rulesets --method POST --input ruleset-main.json
    ```
  - **Downstream Workflow Note**: Merges performed with `GITHUB_TOKEN` intentionally do **not** trigger `on: push` workflows. For libraries (released on tag push), this prevents unintended releases. For auto-deployed sites/Cloud Functions (`deploy.yml` on `main`), add a weekly `schedule:` trigger or trigger `workflow_dispatch` when you want dependency-only updates deployed immediately.

### 4. Releases, Provenance, & Documentation
- Enable **Immutable Releases** in GitHub repository settings so published release tags and assets cannot be tampered with.
- Use `softprops/action-gh-release` (SHA-pinned) with `generate_release_notes: true` and attach build provenance (`actions/attest-build-provenance` or native registry OIDC provenance) where applicable.
- Maintain a standard `README.md` header ([assets/readme_header.md](./assets/readme_header.md)) and `CHANGELOG.md`.
