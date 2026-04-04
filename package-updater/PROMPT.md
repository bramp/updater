# Package Update Prompt

To update a project using the `package-updater` skill, copy and paste the following prompt into your Gemini CLI session:

---
Update the project in `[PROJECT_DIRECTORY]` using the `package-updater` skill.

Strictly follow the incremental workflow and engineering standards defined in `package-updater/SKILL.md`:
1. **Checkout & Baseline**: Establish a baseline with tests and analysis.
2. **Migrate Infrastructure**: Migrate to modern project structures (e.g., Go modules, Dart workspaces) and create a `Makefile` following the standards in `SKILL.md`.
3. **Adopt Standard Workflows**: Adopt standard GitHub workflows (e.g., `test.yml`, `publish.yml`, `deploy.yml`).
4. **Dependency Update**: Update SDK/Language constraints and all dependencies to their latest major versions.
5. **Analysis Improvements**: Improve analysis (e.g., `staticcheck` for Go, `very_good_analysis` for Dart) and apply fixes.
6. **Verify & Commit**: Verify and commit after each logical and stable step. Follow the `AGENTS.md` rules: stage specific changes (`git add`), run `pre-commit run --all-files`, and re-stage any modified files before committing.
7. **Dry-Run & Publish**: Perform dry-runs for publication if applicable. If successful, present results and **ask for my permission** before any actual publication or tagging.

Ask me if you have any questions before starting.
---
