# Go Update Prompt

To update a Go project using the specialized `go-updater` and the base `project-updater` philosophy, copy and paste the following prompt into your Gemini CLI session:

---
Update the project in `[PROJECT_DIRECTORY]` following the `project-updater` philosophy and the `go-updater` language standards.

Follow the incremental workflow in `project-updater/SKILL.md`:
1. **Baseline**: Establish a baseline with tests and analysis.
2. **Standardize Infrastructure**: Update `Makefile`, GitHub Actions, and `pre-commit` configs using the standards in `go-updater/SKILL.md`.
3. **Dependency Update**: Upgrade Go version in `go.mod` and all dependencies to their latest major versions with `make upgrade`.
4. **Analysis & Clean-up**: Use `staticcheck` and `go vet` and resolve all lint issues.
5. **Final Validation**: Ensure `make all` passes locally and in CI.

Ensure you use `go fmt` and `goimports` for code formatting.
---
