# Flutter Makefile Template

.PHONY: all format analyze test test-ci fix upgrade

all: format analyze test

format:
	dart format .

analyze:
	dart analyze --fatal-infos

test:
	dart test

test-ci:
	dart test --reporter=compact

fix:
	dart fix --apply

upgrade:
	dart pub upgrade --major-versions --tighten
