---
name: python-updater
description: Specialized skill for updating Python projects, following the standard project-updater philosophy.
---

# Python Package Updater

This skill specializes in updating Python projects, adhering to the standards defined in `project-updater/SKILL.md`.

## Language Standards

1.  **Virtual Environments**: Every project must use a virtual environment, typically `.venv` in the project root.
2.  **Version**: Target the latest stable Python version (currently `3.12` in this environment).
3.  **Dependencies**: Use `requirements.txt` for managing project dependencies.
4.  **Formatting**: Use `black` as the primary formatting tool.
5.  **Linting**: Use `flake8` for static analysis.
    -   **Line Length**: Set `--max-line-length 999` if using `black`, as `black` handles formatting while `flake8` focuses on logical issues.
6.  **Testing**: Use `unittest` or `pytest`. Ensure tests are discoverable and can be run non-interactively.

## Standard Makefile (Python)

A `Makefile` for a Python project should implement the standard targets as follows:
- `all`: `format analyze test`
- `format`: `black *.py` (and other relevant directories)
- `analyze`: `flake8 --max-line-length 999 *.py`
- `test`: `python3 -m unittest discover` or similar
- `test-ci`: `python3 -m unittest discover -v`
- `fix`: `black *.py`
- `upgrade`: `pip install --upgrade -r requirements.txt && pip freeze > requirements.txt` (or similar)

## GitHub Actions (Python)

The `test.yml` for Python should:
- Use `actions/setup-python@v5`.
- Cache `pip` dependencies using `cache: 'pip'`.
- Use `requirements.txt` as the cache key.
- Run `make test-ci`.

Also ensure `.github/dependabot.yml` is present to keep dependencies updated.

## Cloud Functions (GCP)

For Python Cloud Functions:
- Use `google-github-actions/deploy-cloud-functions@v3`.
- Target `gen2` for modern functions.
- Set the `runtime` to the latest supported Python version (e.g., `python312`).
- Use **Workload Identity Federation (WIF)** for secure authentication.
- See `gcp-updater/SKILL.md` for secret configuration requirements (`WIF_PROVIDER_NAME`, `GCP_SERVICE_ACCOUNT`, `GCP_PROJECT_ID`).
