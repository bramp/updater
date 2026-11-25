# JavaScript / TypeScript Project Makefile

.PHONY: all install format format-check analyze test test-ci fix upgrade check-upgrade

all: format-check analyze test

install:
	npm ci

format:
	npx prettier --write .

format-check:
	npx prettier --check .

analyze:
	npm run lint
	npm run typecheck --if-present

test:
	npm test

test-ci: format-check analyze
	npm test

fix:
	npx eslint --fix .
	npx prettier --write .

upgrade:
	npm update

check-upgrade:
	npm outdated || true
