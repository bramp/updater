---
name: java-updater
description: A skill for updating Java Maven projects. Use this skill when the user wants to update a Java project, bump its Maven dependencies, fix plugins, update CI/CD workflows, or fix typical Java deprecations/ErrorProne warnings.
---

# Java Updater

This skill helps you update outdated Java projects, ensuring they follow modern standards, use automated GitHub workflows, and adhere to engineering best practices.

## Incremental Workflow

Updating a Java project should be done in small, logical, and stable steps. Commit after each step to maintain a clear history.

1. **Checkout & Baseline**:
    - Run `mvn test` to ensure the project builds and tests pass in its current state.
    - Check the Java version supported by the project (`pom.xml` compiler target, `README.md`). If the current JDK is incompatible, find a compatible one or upgrade the project's target version.

2. **Adopt Standard Workflows & Structure**:
    - Add or update GitHub workflows (e.g., `.github/workflows/test.yml`).
    - Add `.github/dependabot.yml` to keep dependencies updated automatically.
    - Add `.pre-commit-config.yaml` if not present.
    - **Commit**: "chore: adopt standard github workflows"

3. **Dependency Update**:
    - Run `mvn versions:display-dependency-updates` to check for dependency updates.
    - Run `mvn versions:display-plugin-updates` to check for plugin updates.
    - Update versions in `pom.xml` (`<properties>`, `<dependencies>`, `<plugins>`).
    - Run `mvn test` to verify changes.
    - Fix any compilation or static analysis issues caused by the updates (e.g., `Error Prone` or `SpotBugs` warnings).
    - **Commit**: "chore: update dependencies and plugins"

4. **Formatting and Linting**:
    - Run the project's formatter plugin, e.g., `mvn formatter:format` or `mvn spotless:apply` if available.
    - Check and fix any new static analysis errors.
    - **Commit**: "style: format code and fix lint issues"

5. **Manual Code Fixes**:
    - Address Java deprecation warnings and API changes from updated dependencies.
    - Follow the user's instructions for any project-specific manual changes.
    - **Commit small batches**: "refactor: fix deprecated API usage"

## Engineering Standards (from AGENTS.md)

- **Mandatory Review**: Always present a summary or diff of changes to the user and wait for explicit approval before performing any `git commit`.
- **Atomic Commits**: Stage specific files (`git add [file]`) rather than everything (`git add .`).
- **Pre-commit Hooks**: Always run `pre-commit run --all-files` before committing and re-stage any modified files.
- **Safety**: Avoid destructive commands like `git reset --hard` or `rm -f` without explicit user permission.

## Common Maven Commands

- `mvn clean`: Cleans the target directory.
- `mvn compile`: Compiles the source code.
- `mvn test`: Runs unit tests.
- `mvn package`: Packages the compiled code.
- `mvn install`: Installs the package into the local repository.
- `mvn versions:display-dependency-updates`: Lists available updates for project dependencies.
- `mvn versions:display-plugin-updates`: Lists available updates for project plugins.
