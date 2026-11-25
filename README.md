# Project Updaters

A collection of modular [Agent Skills](https://agentskills.io) designed to automate the modernization, supply-chain hardening, and maintenance of open-source projects across multiple ecosystems.

## Included Skills

- **[project-updater](./project-updater/SKILL.md)**: Core workflow, uniform `Makefile` interface, SHA-pinned GitHub Actions, and Dependabot cooldown + auto-merge standards.
- **[python-updater](./python-updater/SKILL.md)**: Python modernization using `pyproject.toml`, `uv`, `ruff`, static type checking, `pytest`, and PyPI Trusted Publishing (OIDC).
- **[go-updater](./go-updater/SKILL.md)**: Go modernization using `go.mod` `tool` directives, `golangci-lint` v2 / `staticcheck`, `govulncheck`, and `-race` testing.
- **[js-updater](./js-updater/SKILL.md)**: JavaScript & TypeScript modernization using ESM, strict `tsconfig.json`, ESLint flat config, Prettier, `vitest` / `node --test`, `publint`, and npm Trusted Publishing (OIDC).
- **[java-updater](./java-updater/SKILL.md)**: Java Maven modernization targeting JDK 17/21/25 LTS with `./mvnw`, Spotless, Checkstyle, Error Prone + JSpecify/NullAway, and Maven Central Portal publishing.
- **[flutter-updater](./flutter-updater/SKILL.md)**: Flutter & Dart workspace modernization using `very_good_analysis`, Wasm-capable web deployments, and `pub.dev` OIDC publishing.
- **[gcp-updater](./gcp-updater/SKILL.md)**: Keyless Google Cloud deployments from GitHub Actions via Workload Identity Federation (WIF) and Cloud Run functions.
- **[issue-triage](./issue-triage/SKILL.md)**: Batch GitHub issue triage, codebase verification, response drafting, and closure workflow with human review gates.

## Usage

Compatible with GitHub Copilot, Gemini CLI, Claude Code, Codex, Cursor, and any `agentskills.io`-compatible agent.

Each skill folder is self-contained (`SKILL.md` + `assets/`) so you can either:
1. Reference this repository directly (see [AGENTS.md](./AGENTS.md)), or
2. Install/symlink individual skill directories into your agent's skills folder (e.g., `~/.copilot/skills/` or `~/.gemini/skills/`).

## Validation

Run `make test` to validate all `SKILL.md` frontmatter, relative links, YAML templates, and GitHub Action SHA pins.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.
