# Flutter Workspace Makefile

.PHONY: all run format format-check analyze test test-ci fix upgrade clean

# Device to run on: chrome, macos, ios, android (default: chrome)
DEVICE ?= chrome
APP = cd apps/myapp

all: format-check analyze test

run:
	$(APP) && flutter run -d $(DEVICE)

format:
	dart format .

format-check:
	dart format --output=none --set-exit-if-changed .

analyze:
	flutter analyze

test:
	$(APP) && flutter test

test-ci: format-check analyze
	$(APP) && flutter test --reporter=compact

fix:
	dart fix --apply
	dart format .

upgrade:
	dart pub upgrade --major-versions --tighten

clean:
	$(APP) && flutter clean
