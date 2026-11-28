---
name: go-updater
description: Modernize Go modules, libraries, and CLI applications using Go 1.24+ tool directives, staticcheck/golangci-lint, govulncheck, and race-enabled testing. Use this skill when updating or scaffolding Go repositories containing go.mod, Gopkg.toml, or .go source files.
license: BSD-3-Clause
---

# Go Package Updater

This skill specializes in modernizing Go projects, building on the core workflow and supply-chain standards in `project-updater`.

## Bundled Templates

- [assets/Makefile](./assets/Makefile): Standard Go `Makefile` using pinned `go tool` executables, `govulncheck`, and `-race` tests.
- [assets/workflows/test.yml](./assets/workflows/test.yml): SHA-pinned CI workflow running on the latest patched `stable` Go toolchain (`check-latest: true`).
- [assets/workflows/release.yml](./assets/workflows/release.yml): SHA-pinned tag release workflow.

## Language & Tooling Standards

1. **Modules & Go Version**:
   - Every project must use Go modules (`go.mod` + `go.sum`) targeting the latest stable Go release (`1.27+`).
   - Prefer modern Go standard library packages (`slices`, `maps`, `cmp`, `log/slog`, `errors.Join`, range-over-int/iterators) over third-party helpers—run `go fix ./...` (and `modernize` if using `golangci-lint` v2) to adopt idioms automatically.
2. **Pinned Dev Tools via `go.mod` `tool` Directive (Go 1.24+)**:
   - Never run unpinned `go install ...@latest` in CI workflows, and remove legacy `tools.go` blank-import files.
   - Pin tool dependencies directly in `go.mod`:
     ```bash
     go get -tool golang.org/x/tools/cmd/goimports@latest
     go get -tool honnef.co/go/tools/cmd/staticcheck@latest
     go get -tool golang.org/x/vuln/cmd/govulncheck@latest
     ```
   - Invoke pinned tools via `go tool <name>` (`go tool staticcheck ./...`). For larger repositories, **`golangci-lint` v2** (`golangci/golangci-lint-action`, SHA-pinned) can consolidate `govet`, `staticcheck`, `gocyclo`, `gofumpt`/`goimports`, and `modernize`.
3. **Vulnerability Scanning & Race Detection**:
   - Run **`go tool govulncheck ./...`** in `make analyze` to catch symbol-level vulnerabilities in dependencies and the Go standard library.
   - Always run **`go test -race -shuffle=on -v ./...`** in `make test-ci` to surface data races and order-dependent tests.
4. **Complexity**:
   - Keep cyclomatic complexity reasonable (aim for `< 25` per function).

## Standard Makefile Targets

See [assets/Makefile](./assets/Makefile):
- `all`: `format-check analyze test`
- `format`: `gofmt -w . && go tool goimports -w .`
- `format-check`: verifies `gofmt -l .` and `go tool goimports -l .` produce empty output
- `analyze`: `go vet ./... && go tool staticcheck ./... && go tool govulncheck ./...`
- `test`: `go test ./...`
- `test-ci`: `format-check analyze` + `go test -race -shuffle=on -v ./...`
- `fix`: `gofmt -w . && go tool goimports -w . && go fix ./...`
- `upgrade`: `go mod tidy && go get -u ./... && go mod tidy` (note: `go get -u` upgrades minor/patch; inspect `semver-major` `/v2+` module path upgrades deliberately)

## CI/CD & Dependabot

- **CI (`test.yml`)**: Copy [assets/workflows/test.yml](./assets/workflows/test.yml). Uses `actions/setup-go` with `go-version: "stable"` and `check-latest: true` rather than `go-version-file: "go.mod"`, because `go-version-file` pins CI to the exact patch release in `go.mod` (causing `govulncheck` to fail as soon as newer stdlib security patches ship). When targeting a specific cloud runtime (e.g. App Engine `go127`), use `"1.27.x"` with `check-latest: true`; for libraries supporting multiple Go releases, add a `['oldstable', 'stable']` matrix.
- **Dependabot**: Use `package-ecosystem: "gomod"` alongside `"github-actions"`, with the standard Friday schedule, cooldowns, minor/patch `groups`, and `dependabot-auto-merge.yml` from `project-updater`.
- **Releases**: Copy [assets/workflows/release.yml](./assets/workflows/release.yml) (or add GoReleaser + `actions/attest-build-provenance` when shipping cross-platform CLI binaries).
