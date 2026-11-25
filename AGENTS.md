# Agent Instructions

This repository contains a collection of modular, self-contained AI Agent Skills (`agentskills.io` specification) focused on project modernization, CI/CD hardening, dependency maintenance, and issue triage.

## Structure

Each skill directory is self-contained so it works both inside this repository and when installed standalone (e.g., in `~/.copilot/skills/`, `~/.gemini/skills/`, or via `npx skills`):

- `project-updater/`: Foundational workflow, `Makefile` contract, Dependabot cooldown + auto-merge standards, SHA-pinned GitHub Actions policy, and shared assets (`project-updater/assets/`).
- `python-updater/`: Modern Python standards (`pyproject.toml`, `uv`, `ruff`, type checking, `pytest`, PyPI Trusted Publishing) and templates (`python-updater/assets/`).
- `go-updater/`: Modern Go standards (`go.mod` `tool` directives, `golangci-lint` v2 / `staticcheck`, `govulncheck`, `-race` testing) and templates (`go-updater/assets/`).
- `js-updater/`: Modern JavaScript/TypeScript standards (ESM, strict `tsconfig.json`, ESLint flat config, Prettier, `vitest` / `node --test`, `publint` / `attw`, npm OIDC provenance) and templates (`js-updater/assets/`).
- `java-updater/`: Modern Java Maven standards (JDK 17/21/25 LTS, `./mvnw`, Spotless, Checkstyle, Error Prone + JSpecify/NullAway, Maven Central Portal publishing) and templates (`java-updater/assets/`).
- `flutter-updater/`: Modern Flutter/Dart workspace standards (`very_good_analysis`, `dart format`, Wasm-ready web deploys, pub.dev OIDC publishing) and templates (`flutter-updater/assets/`).
- `gcp-updater/`: Keyless GCP deployments from GitHub Actions via Workload Identity Federation (WIF) and Cloud Run functions (`gcp-updater/assets/`).
- `issue-triage/`: Batch GitHub issue triage, verification, drafting, and closing workflow with human review gates.
- `scripts/validate_skills.py`: Repository validator checking `SKILL.md` frontmatter, internal links, and SHA pinning across all workflow assets.
- `TODO.md`: Tracks progress of modernizing @bramp's open-source repositories.

## Guidelines for Usage

1. **Activate Relevant Skills**: Match the target project's ecosystem (`project-updater` + the matching `<lang>-updater`, plus `gcp-updater` if deploying to Google Cloud).
2. **Workspace Scratchpad Isolation**: Target repositories live *outside* tracked skill folders. Clone external repositories into `work/<repo-name>/` (or an external workspace) rather than modifying skill assets in place.
3. **Supply-Chain & Safety Standards**:
   - Always pin GitHub Actions to full 40-character commit SHAs with a trailing `# vX.Y.Z` version comment.
   - Always set top-level `permissions: contents: read` in workflows, elevating permissions only at the job level.
   - Never run destructive git commands (`git reset --hard`, force-push) or post public GitHub comments without explicit user approval.
4. **Validate Changes to Skills**: After editing any `SKILL.md` or workflow asset in this repository, run `make test` (or `python3 scripts/validate_skills.py`) to verify frontmatter, links, YAML syntax, and SHA pinning.
