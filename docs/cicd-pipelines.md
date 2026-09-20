# 🔄 Templatized CI/CD Pipelines & PR Quality Gates

This document details the decoupled CI/CD pipelines, pre-merge PR quality gates, step templates, and automated workflows implemented for **TeamBoard**.

---

## 🎯 Decoupled Pipeline Strategy

To maintain separation of duties and prevent unnecessary pipeline runs, TeamBoard separates CI/CD tasks into four distinct pipelines:

| Pipeline Name | Purpose | Trigger Scope |
|---|---|---|
| **PR Validation Pipeline** | Pre-merge quality gate running migration checks, Pytest suite with coverage, and trial container build | Triggers on Pull Requests targeting `main`, `master`, or `develop` |
| **Code Testing Pipeline** | Standalone automated testing and quality checks | Triggers on commits to any branch |
| **Infrastructure Pipeline** | Provisioning and applying Terraform modules on Azure | Triggers on changes inside `infrastructure/` directory |
| **Code Deployment Pipeline** | Building production Docker image, pushing to ACR, and updating Azure App Service | Automated execution post-merge on `main` / `master` |

---

## 🔁 Automated Execution Lifecycle

```mermaid
stateDiagram-v2
    [*] --> PullRequestOpened: Developer opens PR
    PullRequestOpened --> PRValidationPipeline: Trigger PR Validation Gate
    PRValidationPipeline --> ChecksPassed: Migrations, Pytest & Docker Build OK
    PRValidationPipeline --> ChecksFailed: Test failure or migration issue
    ChecksFailed --> PullRequestOpened: Developer fixes code
    ChecksPassed --> PRMerged: Maintainer merges PR to main
    PRMerged --> CodeDeploymentPipeline: Auto-trigger Container Build & Azure Deploy
    CodeDeploymentPipeline --> [*]: App Service Updated Live
```

---

## 🐙 GitHub Actions Templatisation (`.github/workflows/templates/`)

GitHub Actions workflows are built on a modular template architecture using Reusable Workflows (`on: workflow_call:`). Every pipeline workflow in `.github/workflows/` delegates execution to a corresponding template in `.github/workflows/templates/`:

### Reusable Workflow Templates
1. **`template-test.yml`** (`.github/workflows/templates/template-test.yml`):
   - Sets up Python with caching.
   - Installs dependencies from `requirements.txt`.
   - Runs Django migration integrity check (`makemigrations --check --dry-run`).
   - Executes Pytest suite with XML & term-missing coverage reports.
   - Conditionally executes trial Docker container builds (`test-build-docker: true`).
   - Uploads code coverage report artifacts.
2. **`template-infra.yml`** (`.github/workflows/templates/template-infra.yml`):
   - Authenticates to Azure CLI using Azure credentials.
   - Initializes HashiCorp Terraform (`hashicorp/setup-terraform@v3`).
   - Executes `terraform init`, `terraform plan`, and `terraform apply -auto-approve` using environment secrets.
3. **`template-code-deploy.yml`** (`.github/workflows/templates/template-code-deploy.yml`):
   - Authenticates to Azure Container Registry (`az acr login`).
   - Builds and tags production Docker images with `${{ github.sha }}` and `latest`.
   - Pushes image to ACR and deploys container to Azure Web App for Containers (`azure/webapps-deploy@v2`).

### Active GitHub Actions Pipelines (Invoking Templates)
- `.github/workflows/pipeline-pr-validation.yml`: Invokes `template-test.yml` with `test-build-docker: true`.
- `.github/workflows/pipeline-code-testing.yml`: Invokes `template-test.yml` with `test-build-docker: false`.
- `.github/workflows/pipeline-infra.yml`: Invokes `template-infra.yml` passing Azure secrets and workspace settings.
- `.github/workflows/pipeline-code.yml`: Invokes `template-code-deploy.yml` passing ACR & Web App inputs.

---

## 🧱 Azure DevOps Templatisation (`pipelines/`)

Azure DevOps pipelines also utilize reusable step templates defined in `pipelines/templates/`:

### 1. `pipelines/templates/test-steps-template.yml`
Configures Python 3.11, installs dependencies, verifies Django migrations (`makemigrations --check --dry-run`), executes `pytest` with JUnit XML output, and publishes code coverage results.

### 2. `pipelines/templates/terraform-steps-template.yml`
Navigates to `infrastructure/`, runs `terraform init`, and applies Terraform modules using Azure service credentials.

### 3. `pipelines/templates/docker-deploy-steps-template.yml`
Logs into Azure Container Registry, builds Docker container images tagged with `$(Build.BuildId)` and `latest`, pushes to ACR, and updates the target Azure Web App for Containers.

### Azure DevOps Pipeline Files
- [pipelines/pipeline-pr-validation.yml](pipelines/pipeline-pr-validation.yml) (PR Validation Gate)
- [pipelines/pipeline-code-testing.yml](pipelines/pipeline-code-testing.yml) (Automated Code Testing)
- [pipelines/pipeline-infra.yml](pipelines/pipeline-infra.yml) (Infrastructure Provisioning)
- [pipelines/pipeline-code.yml](pipelines/pipeline-code.yml) (Code Deployment)
- [azure-pipelines.yml](azure-pipelines.yml) (Master CI/CD Orchestrator)
