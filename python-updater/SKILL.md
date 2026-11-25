---
name: python-updater
description: Modernize Python packages, CLI tools, and scripts to current standards using uv, pyproject.toml, ruff, static type checking, pytest, and PyPI OIDC Trusted Publishing. Use this skill when updating or scaffolding Python repositories containing pyproject.toml, setup.py, setup.cfg, Pipfile, or requirements.txt.
license: BSD-3-Clause
---

# Python Package Updater

This skill specializes in modernizing Python projects, building on the core workflow and supply-chain standards in `project-updater`.

## Bundled Templates

- [assets/Makefile](./assets/Makefile): Standard Python `Makefile` powered by `uv`, `ruff`, `mypy`, and `pytest`.
- [assets/pyproject.toml](./assets/pyproject.toml): PEP 621 + PEP 735 `pyproject.toml` using `hatchling` and `src/` layout.
- [assets/workflows/test.yml](./assets/workflows/test.yml): SHA-pinned CI matrix across Python `3.12`, `3.13`, and `3.14` using `astral-sh/setup-uv`.
- [assets/workflows/release.yml](./assets/workflows/release.yml): Isolated `uv build` + keyless PyPI Trusted Publishing (`pypa/gh-action-pypi-publish`) with automatic PEP 740 Sigstore attestations.

## Language & Tooling Standards

1. **Project & Dependency Management (`uv` + `pyproject.toml`)**:
   - Migrate legacy `setup.py`, `setup.cfg`, `Pipfile`, or flat `requirements.txt` (`pip freeze`) to PEP 621 **`pyproject.toml`** + PEP 735 **`[dependency-groups]`** (`dev = [...]`).
   - Commit **`uv.lock`** for reproducible environments and CI caching (`uv sync --locked`).
   - Use **`src/<package_name>/`** layout with `hatchling` (or `uv_build`) for installable packages.
   - For standalone single-file scripts that don't warrant a full package, declare dependencies inline via **PEP 723** (`# /// script`) and run with `uv run script.py`.
2. **Python Versions**:
   - Support active Python releases (**`3.12`–`3.14`** matrix for libraries; latest stable `3.14` for applications, or the latest GCP-supported runtime such as `python313` for Cloud Run functions).
   - Set `requires-python = ">=3.12"` unless legacy callers require older support.
3. **Formatting & Linting (`ruff`)**:
   - Replace `black`, `flake8`, `isort`, and `pyupgrade` with **`ruff`**:
     - Format: `uv run ruff format .` (`--check` in CI).
     - Lint: `uv run ruff check .` with rule sets `["E", "F", "I", "B", "UP", "SIM", "RUF"]`.
4. **Static Type Checking**:
   - Require **`mypy --strict`** (or `basedpyright` / Astral's `ty`) in `make analyze`.
   - Include an empty `py.typed` marker file inside published library packages (PEP 561).
5. **Testing (`pytest`)**:
   - Prefer **`pytest`** under `tests/` over legacy `unittest discover` runners (`pytest` runs existing `unittest.TestCase` classes seamlessly during migration).

## Standard Makefile Targets

See [assets/Makefile](./assets/Makefile):
- `all`: `format-check analyze test`
- `install`: `uv sync --locked`
- `format` / `format-check`: `uv run ruff format .` / `uv run ruff format --check .`
- `analyze`: `uv run ruff check . && uv run mypy src tests`
- `test`: `uv run pytest`
- `test-ci`: `format-check analyze` + `uv run pytest -v`
- `fix`: `uv run ruff check --fix . && uv run ruff format .`
- `upgrade`: `uv lock --upgrade && uv sync`

## CI/CD, Dependabot, & Publishing

- **CI (`test.yml`)**: Copy [assets/workflows/test.yml](./assets/workflows/test.yml). `astral-sh/setup-uv` caches `uv` automatically on GitHub-hosted runners.
- **Dependabot**: Use `package-ecosystem: "uv"` (or `"pip"` only for legacy Cloud Functions runtime requirements) alongside `"github-actions"`, with the standard cooldown + minor/patch grouping + `dependabot-auto-merge.yml` from `project-updater`.
- **PyPI Trusted Publishing (`release.yml`)**: Copy [assets/workflows/release.yml](./assets/workflows/release.yml). Configure the repository on PyPI as a Trusted Publisher targeting environment `pypi`—never store long-lived `PYPI_API_TOKEN` secrets.
- **Cloud Run Functions (GCP)**: If deploying to Google Cloud, pair with `gcp-updater` (which provides WIF setup and `deploy-gcp.yml`). Note that Cloud Run functions expect either `pyproject.toml` or an exported `requirements.txt` (`uv export --no-dev --no-hashes -o requirements.txt` if required by an older buildpack).
