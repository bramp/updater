---
name: js-updater
description: Specialized skill for updating JavaScript projects, adhering to the standard project-updater philosophy.
---

# JavaScript Package Updater

This skill specializes in updating JavaScript projects, adhering to the standards defined in `project-updater/SKILL.md`.

## Language Standards

1.  **Package Manager**: Use `npm` (default). **Deprecate and remove `bower`** if found. Always commit `package-lock.json` to ensure reproducible builds and CI caching.
2.  **Branching**: Use `main` as the default branch. Rename `master` to `main` if it exists and update all references.
3.  **Version**: Target all Active LTS and Current versions of Node.js. Update the CI matrix and `package.json` `engines` field accordingly.
4.  **Modules**: Prefer ESM (`type: module` in `package.json`). For hybrid projects, configure ESLint to handle both `commonjs` and `module` source types.
5.  **Linting**: Use `eslint` (v10+) with modern configurations. Use the `json` formatter if the default `stylish` formatter fails on specific Node versions.
6.  **Formatting**: Use `prettier` for consistent code formatting. Add a `.prettierignore` to exclude `node_modules`, `dist`, `coverage`, and `build` directories.
7.  **Testing**: Use modern testing frameworks like `qunit` (latest), `jest`, or `vitest`.
8.  **Bundling/Minification**: Use `terser` instead of `uglify-js`.

## Standard Makefile (JS)

A `Makefile` for a JavaScript project should implement:
- `all`: `install format lint test`
- `install`: `npm install`
- `format`: `npm run format`
- `lint`: `npm run lint`
- `test`: `npm test`
- `test-ci`: `npm test` (ensure it's non-interactive and suitable for CI)
- `fix`: `npx eslint --fix . && npm run format`
- `upgrade`: `npm update && npm install`
- `check-upgrade`: `npm outdated || true`

## Releasing & Documentation

1.  **DEVELOPMENT.md**: Create a `DEVELOPMENT.md` to document the requirements, build, test, and automated release procedures.
2.  **README.md**: Keep the `README.md` focused on usage and API. Move technical release details to `DEVELOPMENT.md`.
3.  **Clean History**: When performing large modernizations, squash multiple incremental fix commits into a single logical "Modernize project" commit before releasing.

## GitHub Actions (JS)

Use high-trust, official GitHub actions where possible.

### `test.yml`
- Trigger on `push` and `pull_request` to `main`.
- Include `workflow_call` to make it reusable.
- Use `actions/checkout@v6` and `actions/setup-node@v6`.
- Matrix test against Active LTS and Current Node versions (e.g., 20, 22, 24, 25).
- Use `cache: 'npm'` (requires `package-lock.json`).
- Run `npm ci` and `make test-ci`.

### `deploy.yml` (Static Sites)
- Use official `actions/upload-pages-artifact@v4` and `actions/deploy-pages@v5`.
- Target the `github-pages` environment.

### `publish.yml` (NPM)
- Use **NPM Trusted Publishing (OIDC)** triggered by tags (e.g., `v*`).
- Require `permissions: id-token: write` and `contents: read`.
- Set `registry-url: 'https://registry.npmjs.org'` in `actions/setup-node`.
- Use `npm publish --provenance --access public`.

Add `.github/dependabot.yml` to the root to keep dependencies and actions updated.
