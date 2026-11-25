# Python Project Makefile

.PHONY: all install format format-check analyze test test-ci fix upgrade clean

all: format analyze test

install:
	uv sync --locked

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

analyze:
	uv run ruff check .
	uv run mypy src tests

test:
	uv run pytest

test-ci: format-check analyze
	uv run pytest -v

fix:
	uv run ruff check --fix .
	uv run ruff format .

upgrade:
	uv lock --upgrade
	uv sync

clean:
	rm -rf dist build .pytest_cache .mypy_cache .ruff_cache
