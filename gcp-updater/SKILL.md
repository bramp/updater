---
name: gcp-updater
description: Configure keyless Google Cloud Platform (GCP) deployments from GitHub Actions using Workload Identity Federation (WIF) and Cloud Run functions (Gen 2). Use this skill when adding or modernizing GCP CI/CD workflows, Cloud Functions, or Cloud Run deployments.
license: BSD-3-Clause
---

# GCP Deployment Skill

This skill defines the process for setting up keyless, least-privilege deployments to Google Cloud Platform (GCP) from GitHub Actions using **Workload Identity Federation (WIF)** and **Cloud Run functions** (formerly Cloud Functions Gen 2).

## Bundled Templates

- [assets/workflows/deploy-gcp.yml](./assets/workflows/deploy-gcp.yml): SHA-pinned GitHub Actions deployment workflow gated by `test.yml` and the `production` GitHub Environment.

## Core Philosophy

1. **Keyless OIDC Only**: Never create or store long-lived service account JSON keys. Always authenticate via Workload Identity Federation (`id-token: write`).
2. **Environment-Scoped Least Privilege**: Scope both the GCP IAM binding and the GitHub secrets to a protected `production` GitHub Environment (or `refs/heads/main`) so feature branches and pull requests cannot impersonate the deployment service account.
3. **Standardized Secret Names**: Use identical secret names across every repository.

## GitHub Configuration (`production` Environment Secrets)

Configure a **GitHub Environment** named `production` and add:

| Secret Name | Example Value | Description |
| :--- | :--- | :--- |
| **`GCP_PROJECT_ID`** | `my-cool-project` | Unique GCP project ID. |
| **`GCP_SERVICE_ACCOUNT`** | `github-actions@my-cool-project.iam.gserviceaccount.com` | Deployment service account email. |
| **`WIF_PROVIDER_NAME`** | `projects/123456789012/locations/global/workloadIdentityPools/github-pool/providers/github-provider` | Full resource name of the WIF OIDC provider. |

## Initial GCP Setup (One-time per Project)

### Step 0: Create a Least-Privilege Service Account
- **IAM & Admin → Service Accounts → Create Service Account**
- Grant only required deployment roles (for Cloud Run functions Gen 2: `roles/cloudfunctions.developer`, `roles/run.admin`, `roles/iam.serviceAccountUser` on the runtime service account, and `roles/artifactregistry.writer`).

### Step 1: Create Workload Identity Pool
- **IAM & Admin → Workload Identity Federation → Create Pool** (`github-pool`).

### Step 2: Create OIDC Workload Identity Provider
- **Provider Type**: `OIDC`
- **Issuer URL**: `https://token.actions.githubusercontent.com`
- **Attribute Mapping**:
  - `google.subject` = `assertion.sub`
  - `attribute.repository` = `assertion.repository`
  - `attribute.ref` = `assertion.ref`
  - `attribute.environment` = `assertion.environment`
- **Attribute Condition** (defense-in-depth at pool level):
  `assertion.repository_owner == "bramp"` (or exact `assertion.repository == "OWNER/REPO" && assertion.ref == "refs/heads/main"` for single-repo pools).

### Step 3: Bind `Workload Identity User` Narrowly on the Service Account
Prefer binding to the exact `subject` for the `production` GitHub Environment (prevents unmerged PR branches from impersonating the service account even if the pool is shared across repos):
- **Principal**:
  `principal://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/github-pool/subject/repo:<OWNER>/<REPO>:environment:production`
- **Role**: `roles/iam.workloadIdentityUser`

## Workflow & Dependabot Auto-Merge Note

Copy [assets/workflows/deploy-gcp.yml](./assets/workflows/deploy-gcp.yml) into `.github/workflows/deploy-gcp.yml` and replace `{FUNCTION_NAME}`, `{RUNTIME}`, and `{ENTRY_POINT}`.

Note: When `dependabot-auto-merge.yml` merges minor/patch PRs using `GITHUB_TOKEN`, GitHub suppresses downstream `on: push` workflows by design. If you want weekly dependency updates to redeploy automatically, add a weekly `schedule:` trigger to `deploy-gcp.yml` (e.g., Saturday morning) or trigger `workflow_dispatch`.

## Troubleshooting

### `The given credential is rejected by the attribute condition`
1. **Subject / Environment Mismatch**: Ensure `environment: production` is set on the `deploy` job so GitHub sets `sub` to `repo:OWNER/REPO:environment:production` (without `environment:`, GitHub sets `sub` to `repo:OWNER/REPO:ref:refs/heads/main`).
2. **Case Sensitivity**: `OWNER/REPO` in IAM bindings and CEL conditions is case-sensitive.
3. **Trigger Change**: If switching from branch pushes to tag pushes, update any `assertion.ref` check to `assertion.ref.startsWith('refs/tags/v')`.

### `Function already exists in environment GEN_1, can't change it to GEN_2`
GCP does not support in-place Gen 1 → Gen 2 (Cloud Run functions) upgrades under the same name. Either deploy a new Gen 2 service/function and cut traffic over, delete the Gen 1 function first, or pass `gen: 1` if intentionally maintaining a legacy function.
