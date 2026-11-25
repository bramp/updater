# Java Maven Project Makefile

MVN ?= ./mvnw

.PHONY: all format format-check analyze test test-ci fix upgrade clean

all: format-check analyze test

format:
	$(MVN) spotless:apply

format-check:
	$(MVN) spotless:check

analyze:
	$(MVN) checkstyle:check test-compile -Dgpg.skip

test:
	$(MVN) test -Dgpg.skip

test-ci:
	$(MVN) --batch-mode --no-transfer-progress spotless:check checkstyle:check verify -Dgpg.skip

fix:
	$(MVN) spotless:apply

upgrade:
	$(MVN) versions:display-dependency-updates versions:display-plugin-updates

clean:
	$(MVN) clean
