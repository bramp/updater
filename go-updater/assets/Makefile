# Go Project Makefile
# Track dev tools in go.mod via:
#   go get -tool golang.org/x/tools/cmd/goimports@latest
#   go get -tool honnef.co/go/tools/cmd/staticcheck@latest
#   go get -tool golang.org/x/vuln/cmd/govulncheck@latest

.PHONY: all format format-check analyze test test-ci fix upgrade

all: format analyze test

format:
	gofmt -w .
	go tool goimports -w .

format-check:
	test -z "$$(gofmt -l .)"
	test -z "$$(go tool goimports -l .)"

analyze:
	go vet ./...
	go tool staticcheck ./...
	go tool govulncheck ./...

test:
	go test ./...

test-ci: format-check analyze
	go test -race -shuffle=on -v ./...

fix:
	gofmt -w .
	go tool goimports -w .
	go fix ./...

upgrade:
	go mod tidy
	go get -u ./...
	go mod tidy
