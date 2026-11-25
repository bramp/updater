---
name: js-updater
description: Modernize JavaScript and TypeScript packages, Node.js tools, and web apps using ESM, strict TypeScript, ESLint flat config, Prettier, Vitest or node --test, publint, and npm OIDC Trusted Publishing. Use this skill when updating or scaffolding repositories with package.json, tsconfig.json, or .js/.ts files.
license: BSD-3-Clause
---

# JavaScript & TypeScript Package Updater

This skill specializes in modernizing JavaScript and TypeScript projects, building on the core workflow and supply-chain standards in `project-updater`.

## Bundled Templates

- [assets/Makefile](./assets/Makefile): Uniform `Makefile` separating non-mutating `npm ci` / `format-check` / `analyze` from local write commands.
- [assets/tsconfig.json](./assets/tsconfig.json): Strict modern ESM TypeScript configuration (`NodeNext`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`).
- [assets/workflows/test.yml](./assets/workflows/test.yml): SHA-pinned CI matrix across Node LTS versions (`20`, `22`, `24`).
- [assets/workflows/publish.yml](./assets/workflows/publish.yml): Keyless npm Trusted Publishing (`--provenance`) with `publint` validation.
- [assets/workflows/deploy.yml](./assets/workflows/deploy.yml): Keyless GitHub Pages static site deployment via `upload-pages-artifact` + `deploy-pages`.

## Language & Tooling Standards

1. **Package Manager & Lockfiles**:
   - Default to `npm` and always commit `package-lock.json` (use `npm ci` in CI and `make install`—never run `npm install` in `make all` or CI).
   - Remove deprecated legacy managers/task runners (`bower`, `grunt`, `gulp`, `jshint`).
   - Rename `master` to `main` if still using `master`.
2. **Node.js LTS Support**:
   - Target **Active and Maintenance LTS** releases (currently Node `20`, `22`, `24`—avoid pinning odd-numbered non-LTS releases once superseded). Keep `package.json` `"engines"` aligned with the CI matrix.
3. **ESM & Package Exports**:
   - Prefer native ESM (`"type": "module"` in `package.json`) with an explicit `"exports"` map (including `"types"` conditions when shipping TypeScript declarations).
   - Validate published package metadata and export maps with **`npx publint`** (and **`npx @arethetypeswrong/cli --pack`** for TypeScript libraries).
4. **TypeScript**:
   - For TypeScript projects (or JS libraries benefiting from types), adopt strict compiler flags from [assets/tsconfig.json](./assets/tsconfig.json) (`strict: true`, `noUncheckedIndexedAccess: true`, `verbatimModuleSyntax: true`) and wire `"typecheck": "tsc --noEmit"` into `package.json` so `make analyze` runs it automatically.
5. **Linting & Formatting**:
   - **ESLint (v9/v10+ flat config)**: Use `eslint.config.js` (`@eslint/js` + `typescript-eslint`).
   - **Prettier**: Enforce formatting via `prettier --check .` in CI (`make format-check`) and `prettier --write .` locally (`make format`). Exclude `node_modules/`, `dist/`, `build/`, and `coverage/`.
6. **Testing & Bundling**:
   - For small zero-dependency Node libraries, prefer Node's built-in **`node --test`** runner to avoid heavy devDependency trees.
   - For larger apps, browser code, or TypeScript projects, prefer **`vitest`** (or latest `qunit` when preserving existing browser QUnit suites).
   - Prefer `tsdown` / `tsup` / `esbuild` for bundling TypeScript libraries, and `terser` over legacy `uglify-js` when standalone minification is needed.

## Standard Makefile Targets

See [assets/Makefile](./assets/Makefile):
- `all`: `format-check analyze test`
- `install`: `npm ci`
- `format` / `format-check`: `npx prettier --write .` / `npx prettier --check .`
- `analyze`: `npm run lint && npm run typecheck --if-present`
- `test` / `test-ci`: `npm test` / `format-check analyze` + `npm test`
- `fix`: `npx eslint --fix . && npx prettier --write .`
- `upgrade` / `check-upgrade`: `npm update` / `npm outdated || true`

## Documentation, CI/CD, & Dependabot

- **Documentation**: Keep `README.md` focused on installation, usage, and API; move contributor/release runbooks into `DEVELOPMENT.md`.
- **Dependabot**: Configure `package-ecosystem: "npm"` alongside `"github-actions"`, using the standard Friday schedule, cooldowns, minor/patch `groups`, and `dependabot-auto-merge.yml` from `project-updater`.
- **npm Trusted Publishing (`publish.yml`)**: Copy [assets/workflows/publish.yml](./assets/workflows/publish.yml). Configure Trusted Publishing on npmjs.com for the `npm` GitHub Environment (`id-token: write` + `npm publish --provenance --access public`, zero `NPM_TOKEN` secrets).
- **GCP Deployments**: Pair with `gcp-updater` for Workload Identity Federation Cloud Run function deployments.
