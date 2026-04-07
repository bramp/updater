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
    - Add `.github/workflows/release.yml` if the project publishes releases (see Release Workflow section).
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
    - **Google Java Format**: Use `fmt-maven-plugin` (com.spotify.fmt). Note: requires JDK 17+, so gate the execution in a JDK 17+ Maven profile if the project also supports older JDKs.
    - **Checkstyle**: Use `maven-checkstyle-plugin` with `google_checks.xml` configuration. Also gate in a JDK 17+ profile if needed.
    - Run formatting first (`mvn fmt:format`), then fix any checkstyle violations.
    - Add `fmt:check` and `checkstyle:check` to the CI workflow (run with JDK 21).
    - **Commit formatting and linting in separate steps**: first "style: format code with Google Java Format", then "style: fix checkstyle violations", then "chore: add format and style checking to CI".

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
- `mvn fmt:format` / `mvn fmt:check`: Format / check formatting with Google Java Format.
- `mvn checkstyle:check`: Check style violations against google_checks.xml.

## Release Workflow (GitHub Actions)

For Java projects published to Maven Central, set up `.github/workflows/release.yml` with:

- **Trigger**: Tag push (e.g., `{name}-*`) and optionally `workflow_dispatch` for manual re-runs.
- **Jobs**:
  1. **test**: Matrix across supported JDK versions (e.g., 11, 17, 21).
  2. **publish**: Deploy to Maven Central using `central-publishing-maven-plugin` (or `maven-release-plugin`). Use `actions/setup-java@v5` with `server-id: central` and GPG signing secrets.
  3. **github-release**: Create a GitHub Release with `softprops/action-gh-release@v2` and `generate_release_notes: true`.
  4. **javadoc** (optional): Generate javadoc with `mvn javadoc:javadoc`, then deploy to GitHub Pages with `actions/upload-pages-artifact@v4` + `actions/deploy-pages@v5`.

Example GitHub Release step:
```yaml
- name: Create GitHub Release
  uses: softprops/action-gh-release@v2
  with:
    generate_release_notes: true
```

## Known Gotchas

- **fmt-maven-plugin requires JDK 17+**: If the project supports JDK 11, gate the fmt-maven-plugin execution inside a `<profile>` activated by `<jdk>[17,)</jdk>`. Same applies to checkstyle-plugin with Checkstyle 10.x.
- **maven-javadoc-plugin 3.12.0+**: Default output directory changed from `target/site/apidocs` to `target/reports/apidocs`. Update any CI paths that reference the old location.
- **Checkstyle suppressions for FFmpeg-style naming**: Projects wrapping C/native APIs may have snake_case fields. Use `checkstyle-suppressions.xml` to suppress `MemberName`, `ParameterName`, etc. for specific packages rather than disabling globally.
- **spotbugs-annotations → jsr305**: If removing SpotBugs, replace `spotbugs-annotations` with `com.google.code.findbugs:jsr305:3.0.2` (provides `javax.annotation.Nullable`).
