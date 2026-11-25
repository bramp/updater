---
name: java-updater
description: Modernize Java Maven projects targeting JDK 17/21/25 LTS with Maven Wrapper, Spotless, Checkstyle, Error Prone + JSpecify/NullAway, and Maven Central Portal publishing. Use this skill when updating or scaffolding Java repositories with pom.xml, Maven plugins, or .java source files.
license: BSD-3-Clause
---

# Java Maven Updater

This skill specializes in modernizing Java Maven projects, building on the core workflow and supply-chain standards in `project-updater`.

## Bundled Templates

- [assets/Makefile](./assets/Makefile): Uniform `Makefile` wrapping `./mvnw` across formatting, static analysis, and tests.
- [assets/workflows/test.yml](./assets/workflows/test.yml): SHA-pinned CI matrix across LTS JDKs (`17`, `21`, `25`).
- [assets/workflows/release.yml](./assets/workflows/release.yml): SHA-pinned Maven Central Portal release + GitHub Release + Javadoc Pages deployment.

## Incremental Modernization Workflow

1. **Baseline & Maven Wrapper (`./mvnw`)**:
   - Ensure the Maven Wrapper (`./mvnw`) is committed and pinned to current Maven `3.9.x` (`mvn wrapper:wrapper`) so local and CI builds run identical Maven versions.
   - Run `./mvnw test` to establish a passing baseline.
2. **Adopt Standard Infrastructure**:
   - Add [assets/Makefile](./assets/Makefile), [assets/workflows/test.yml](./assets/workflows/test.yml), and [assets/workflows/release.yml](./assets/workflows/release.yml) (if published to Maven Central).
   - Add `.github/dependabot.yml` (`package-ecosystem: "maven"` + `"github-actions"`) and `dependabot-auto-merge.yml` from `project-updater`.
   - **Commit**: `chore: adopt hardened github workflows, maven wrapper, and makefile`
3. **Runtime, Dependency, & Plugin Updates**:
   - Default to LTS matrix **`[17, 21, 25]`** (retain JDK `11` in the matrix only for widely consumed libraries explicitly promising Java 11 bytecode compatibility).
   - Check updates with `./mvnw versions:display-dependency-updates versions:display-plugin-updates`, migrate JUnit 4 → **JUnit Jupiter (JUnit 5/6)** where practical, and verify with `./mvnw test`.
   - **Commit**: `chore: update dependencies and maven plugins`
4. **Formatting, Style, & Static Null Safety**:
   - **Formatting (`spotless-maven-plugin`)**: Prefer `com.diffplug.spotless:spotless-maven-plugin` with an explicitly pinned `googleJavaFormat` version over `com.spotify.fmt:fmt-maven-plugin` (which frequently lags new JDK bytecode versions). Enable POM sorting and `forbidModuleImports` on JDK 25+.
   - **Style (`maven-checkstyle-plugin`)**: Enforce `google_checks.xml` for naming/semantic style rules not handled by Spotless.
   - **Compiler & Nullness (`Error Prone` + `JSpecify` + `NullAway`)**:
     - Use **`org.jspecify:jspecify` (`@NullMarked` / `@Nullable`)** instead of dormant `com.google.code.findbugs:jsr305` (which causes JPMS split-package conflicts on `javax.annotation`).
     - Pair with Google **Error Prone** and **NullAway** in `maven-compiler-plugin` to turn nullness and bug patterns into compile-time errors.
   - Commit formatting (`style: format code with Spotless`) separately from semantic/checkstyle fixes (`style: resolve checkstyle and Error Prone warnings`).

## Standard Makefile Targets

See [assets/Makefile](./assets/Makefile):
- `all`: `format-check analyze test`
- `format` / `format-check`: `./mvnw spotless:apply` / `./mvnw spotless:check`
- `analyze`: `./mvnw checkstyle:check test-compile -Dgpg.skip`
- `test`: `./mvnw test -Dgpg.skip`
- `test-ci`: `./mvnw --batch-mode --no-transfer-progress spotless:check checkstyle:check verify -Dgpg.skip`
- `fix`: `./mvnw spotless:apply`
- `upgrade`: `./mvnw versions:display-dependency-updates versions:display-plugin-updates`

## Maven Central Portal Release Workflow

Legacy OSSRH (`oss.sonatype.org`) has been sunset. Publish via **`org.sonatype.central:central-publishing-maven-plugin`** using [assets/workflows/release.yml](./assets/workflows/release.yml):
1. **`test`**: Runs `test.yml` across supported LTS JDKs (`17`, `21`, `25`).
2. **`publish`**: Runs on JDK `25` in the protected `publish` GitHub Environment using Sonatype Central Portal user token secrets (`CENTRAL_TOKEN_USERNAME`, `CENTRAL_TOKEN_PASSWORD`) + GPG signing (`GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`), then creates a GitHub Release (`softprops/action-gh-release`, SHA-pinned).
3. **`javadoc`**: Generates Javadoc (`target/reports/apidocs` on `maven-javadoc-plugin` `3.12.0+`) and deploys to GitHub Pages via OIDC (`upload-pages-artifact` + `deploy-pages`).

## Known Gotchas

- **Gating JDK-specific plugins**: If a library still compiles for JDK 11, gate `spotless-maven-plugin`, `maven-checkstyle-plugin` (`10.x+`), and recent Error Prone versions inside a `<profile>` activated by `<jdk>[17,)</jdk>` (or `<jdk>[21,)</jdk>`), running style checks on the newest JDK leg in CI.
- **`maven-javadoc-plugin` 3.12.0+ output path**: Default output moved from `target/site/apidocs` to `target/reports/apidocs`.
- **C/Native wrapper naming**: For libraries mirroring native C structs (e.g., FFmpeg), scope `MemberName`/`ParameterName` exemptions to specific packages in `checkstyle-suppressions.xml` rather than disabling rules globally.

## Safety & Review Standards

- Present a clear summary/diff and obtain user approval before destructive git actions or public releases.
- Stage specific files rather than `git add .`, and run `prek run --all-files` (or `pre-commit run --all-files`) when `.pre-commit-config.yaml` is present.
