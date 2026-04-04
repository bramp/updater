# Flutter Update Prompt

To update a Flutter/Dart project using the specialized `flutter-updater` and the base `project-updater` philosophy, copy and paste the following prompt into your Gemini CLI session:

---
Update the project in `[PROJECT_DIRECTORY]` following the `project-updater` philosophy and the `flutter-updater` language standards.

Follow the incremental workflow in `project-updater/SKILL.md`:
1. **Baseline**: Establish a baseline with tests and analysis.
2. **Standardize Infrastructure**: Update `Makefile`, GitHub Actions, and `pre-commit` configs using the templates and standards in `flutter-updater/SKILL.md`.
3. **Dependency Update**: Upgrade SDK constraints and all dependencies to their latest major versions.
4. **Analysis & Clean-up**: Switch to `package:very_good_analysis` and apply fixes with `make fix`. Resolve any remaining lint warnings manually.
5. **Final Validation**: Ensure `make all` passes locally and in CI.

For multi-package projects, ensure you adopt standard Dart/Flutter workspaces.
---
