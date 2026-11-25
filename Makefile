# Project Updaters Repository Makefile

.PHONY: all install format format-check analyze test test-ci fix upgrade

all: format-check analyze test

install:
	@true

format:
	@true

format-check:
	@python3 -c "import pathlib, sys; bad=[str(p) for p in pathlib.Path('.').glob('*/*.md') if '\r\n' in p.read_text()]; sys.exit('CRLF line endings in: ' + ', '.join(bad) if bad else 0)"

analyze:
	python3 scripts/validate_skills.py

test:
	python3 scripts/validate_skills.py

test-ci: format-check analyze

fix: format

upgrade:
	@echo "Workflow action SHAs in .github/workflows and */assets/workflows are updated weekly by Dependabot."
