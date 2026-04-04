---
name: go-updater
description: Specialized skill for updating Go projects, following the standard project-updater philosophy.
---

# Go Package Updater

This skill specializes in updating Go projects, adhering to the standards defined in `project-updater/SKILL.md`.

## Language Standards

1.  **Modules**: Every project must use Go modules (`go.mod`).
2.  **Version**: Target the latest stable Go version (currently `1.26` in this environment).
3.  **Linting**: Use `staticcheck` and `go vet` as the primary analysis tools.
4.  **Formatting**: Use `go fmt` and `goimports`.
5.  **Complexity**: Monitor cyclomatic complexity using `gocyclo`. Aim for scores below 25.

## Standard Makefile (Go)

A `Makefile` for a Go project should implement the standard targets as follows:
- `all`: `format analyze test`
- `format`: `go fmt ./... && goimports -w .`
- `analyze`: `go vet ./... && staticcheck ./...`
- `test`: `go test ./...`
- `test-ci`: `go test -v ./...`
- `fix`: `go fmt ./... && go fix ./...`
- `upgrade`: `go mod tidy && go get -u ./... && go mod tidy`

## GitHub Actions (Go)

The `test.yml` for Go should:
- Use `actions/setup-go@v5`.
- Install `staticcheck` and `goimports` if they are not pre-installed.
- Cache Go modules.
- Run `make test-ci`.

Also ensure `.github/dependabot.yml` is present to keep dependencies updated.

## Dependency Management

- **Upgrade Process**:
    - Update `go.mod`'s `go` directive to the latest supported version.
    - Run `go mod tidy` to prune unused dependencies.
    - Run `go get -u ./...` to update all dependencies to latest minor/patch versions.
    - Run `go mod tidy` again to clean up.
- Prefer standard library over external dependencies where possible.
