---
name: flutter-updater
description: Modernize Flutter apps and Dart packages using native Pub workspaces, very_good_analysis, Wasm web builds, and OIDC pub.dev publishing. Use this skill when updating or scaffolding Flutter or Dart repositories containing pubspec.yaml, analysis_options.yaml, or .dart files.
license: BSD-3-Clause
---

# Flutter & Dart Package Updater

This skill specializes in modernizing Flutter applications and Dart packages, building on the core workflow and supply-chain standards in `project-updater`.

## Bundled Templates

- [assets/Makefile](./assets/Makefile): Standard Flutter/Dart workspace `Makefile`.
- [assets/pubspec.yaml](./assets/pubspec.yaml) & [assets/apps/myapp/](./assets/apps/myapp): Native Dart Pub workspace scaffold (`resolution: workspace`).
- [assets/analysis_options.yaml](./assets/analysis_options.yaml): Strict `package:very_good_analysis` analyzer configuration.
- [assets/workflows/test.yml](./assets/workflows/test.yml): SHA-pinned CI workflow using `subosito/flutter-action` with built-in caching.
- [assets/workflows/deploy.yml](./assets/workflows/deploy.yml): Wasm-enabled (`--wasm`) Flutter web build deployed via keyless OIDC GitHub Pages (`upload-pages-artifact` + `deploy-pages`).
- [assets/workflows/publish.yml](./assets/workflows/publish.yml): Keyless OIDC `pub.dev` automated publishing workflow.

## Language & Tooling Standards

1. **Native Pub Workspaces**:
   - Target current stable Dart SDK (`^3.11.0`) and adopt native Pub workspaces (`workspace:` in root `pubspec.yaml`, `resolution: workspace` in member packages) for multi-package or app+package repositories.
   - **Migrating from Melos**: Replace `melos.yaml` scripts with [assets/Makefile](./assets/Makefile) targets, enable native `workspace:` resolution, and remove `melos` from `dev_dependencies`.
2. **Linting & Formatting**:
   - Include `package:very_good_analysis/analysis_options.yaml` ([assets/analysis_options.yaml](./assets/analysis_options.yaml)); document any rule overrides explicitly.
   - Check formatting non-destructively in CI via `dart format --output=none --set-exit-if-changed .` (`make format-check`).
3. **Web Builds (`--wasm`)**:
   - Build Flutter web targets with `--wasm` (`flutter build web --release --wasm`) whenever all transitive packages avoid legacy `dart:html` / `dart:js` APIs (migrate any remaining web interop to `package:web` and `dart:js_interop`).
4. **`pub.dev` Readiness**:
   - Keep `CHANGELOG.md` updated, tighten SDK and dependency constraints (`dart pub upgrade --major-versions --tighten`), and publish via OIDC ([assets/workflows/publish.yml](./assets/workflows/publish.yml) replacing `{PACKAGE_NAME}`).

## Standard Makefile Targets

See [assets/Makefile](./assets/Makefile) (for pure Dart packages without Flutter UI, substitute `dart analyze` and `dart test`):
- `all`: `format-check analyze test`
- `format` / `format-check`: `dart format .` / `dart format --output=none --set-exit-if-changed .`
- `analyze`: `flutter analyze` (or `dart analyze`)
- `test`: `flutter test` (or `dart test`)
- `test-ci`: `format-check analyze` + `flutter test --reporter=compact`
- `fix`: `dart fix --apply && dart format .`
- `upgrade`: `dart pub upgrade --major-versions --tighten`

## CI/CD & Dependabot

- **CI & Pages**: Copy [assets/workflows/test.yml](./assets/workflows/test.yml) and (for web apps) [assets/workflows/deploy.yml](./assets/workflows/deploy.yml). Never manually cache `/opt/hostedtoolcache/flutter/` with `actions/cache`—`subosito/flutter-action` (`cache: true`) handles SDK and `.pub-cache` caching natively, and official `actions/deploy-pages` replaces third-party branch-push actions.
- **Dependabot**: Configure `package-ecosystem: "pub"` alongside `"github-actions"`, with the standard Friday schedule, cooldowns, minor/patch `groups`, and `dependabot-auto-merge.yml` from `project-updater`.
