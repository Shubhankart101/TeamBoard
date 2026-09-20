# 🚀 TeamBoard — B2B Knowledge Base API Platform

<div align="center">

[![GitHub Repository](https://img.shields.io/badge/GitHub-View_Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shubhankart101/TeamBoard)

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.3-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.15.1-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Swagger / OpenAPI](https://img.shields.io/badge/OpenAPI-3.0%20(drf--spectacular)-green?logo=swagger&logoColor=white)](http://127.0.0.1:8000/api/docs/)
[![Terraform Modules](https://img.shields.io/badge/IaC-Terraform%20Modules-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Azure](https://img.shields.io/badge/Cloud-Azure%20App%20Service%20%26%20PostgreSQL-0089D6?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![Coverage](https://img.shields.io/badge/Coverage-97%25-brightgreen?logo=pytest&logoColor=white)](#-automated-testing-framework)

</div>

---

TeamBoard is an enterprise-grade **B2B Knowledge Base API Platform** built with **Django REST Framework (DRF)**, **PostgreSQL**, **Docker**, **Modular Terraform**, **Azure Cloud Services**, and **Templatized CI/CD Pipelines**.

The platform powers customer product helpdesks, onboarding widgets, and AI chat assistants by serving curated technical Q&A entries, tracking usage per client company atomically, and providing real-time platform analytics to system administrators.

---

## 📋 Table of Contents

- [🎯 Scenario \& System Architecture](#-scenario--system-architecture)
- [✨ Key Features](#-key-features)
- [📁 Project Directory Structure](#-project-directory-structure)
- [📖 Swagger / OpenAPI Documentation](#-swagger--openapi-documentation)
- [📡 API Endpoints Reference](#-api-endpoints-reference)
- [⚙️ Environment Variables Configuration](#-environment-variables-configuration)
- [🛠️ Local Setup \& Quick Start](#-local-setup--quick-start)
- [🐳 Docker Containerization](#-docker-containerization)
- [🏗️ Modular Infrastructure as Code (Terraform on Azure)](#-modular-infrastructure-as-code-terraform-on-azure)
- [🔄 Templatized CI/CD Pipelines \& PR Quality Gates](#-templatized-cicd-pipelines--pr-quality-gates)
- [🧪 Automated Testing Framework](#-automated-testing-framework)
- [📮 Postman Collection Scenarios](#-postman-collection-scenarios)

---

## 🎯 Scenario & Architecture Overview

TeamBoard hosts backend technical Knowledge Base entries (spanning APIs, Databases, Cloud Infrastructure, Frameworks, and General Software Architecture). B2B customers register their product with TeamBoard and integrate the API into their customer-facing products.

### Security & Usage Logging Architecture
- **Credential Validation vs. Client-Provided IDs:** Companies authenticate securely using SimpleJWT tokens issued upon login. Company identity is derived directly from `request.user.company`, preventing identity spoofing or tampering.
- **Atomic Usage Logging:** Every query executed against `/api/kb/query/` is logged to `QueryLog` inside a `django.db.transaction.atomic()` block alongside the query result count. Searches returning 0 results are still logged to accurately track platform resource consumption for usage-based billing.
- **Role-Based Access Control (RBAC):** Custom `IsAdminUser` permission class ensures admin dashboard endpoints are strictly reserved for companies with `role == 'admin'`, returning `403 Forbidden` for standard `client` roles (without relying on Django internal `is_staff` / `is_superuser` flags).

---

## ✨ Key Features

- **JWT Authentication & Global Protection:** Configured with `DEFAULT_AUTHENTICATION_CLASSES` and `DEFAULT_PERMISSION_CLASSES` (`IsAuthenticated`), protecting endpoints globally while explicitly exempting public auth routes (`Register` and `Login`).
- **Automated Profile & API Key Creation:** Uses Django `post_save` signals on the `User` model to automatically instantiate a `Company` record and generate a 32-character URL-safe API key (`secrets.token_urlsafe(32)`).
- **Interactive Swagger UI & ReDoc:** Built-in OpenAPI 3.0 schema generation using `drf-spectacular` with typed request/response schemas and interactive API testing.
- **Modular Terraform Architecture:** Structured with reusable child modules (`modules/container_registry`, `modules/postgresql`, `modules/app_service`) and separated root declarations (`providers.tf`, `variables.tf`, `outputs.tf`, `main.tf`).
- **Templatized Pipelines & Separation of Duties:** Independent CI/CD pipelines for **Code Testing**, **Infrastructure Provisioning**, and **Code Deployment**, built using reusable steps templates in both GitHub Actions and Azure DevOps.
- **Automated Testing Suite:** Pytest-driven test suite with `pytest-django` and `pytest-cov`, maintaining 97%+ code coverage.

---

## 📁 Project Directory Structure

```
TeamBoard/
├── .github/
│   └── workflows/
│       ├── pipeline-pr-validation.yml# PR Pre-Merge Quality Gate Workflow (GitHub Actions)
│       ├── pipeline-code-testing.yml # Automated Testing Workflow (GitHub Actions)
│       ├── pipeline-infra.yml        # Infrastructure Provisioning Workflow (GitHub Actions)
│       └── pipeline-code.yml         # Container Build & Deploy Workflow (GitHub Actions)
├── api/
│   ├── management/
│   │   └── commands/
│   │       └── seed_kb.py            # Management command to seed Knowledge Base entries
│   ├── admin.py                      # Django Admin site model registrations
│   ├── apps.py                       # App configuration & signal receiver connection
│   ├── models.py                     # Data models: Company, KBEntry, QueryLog
│   ├── permissions.py                # Custom IsAdminUser RBAC permission class
│   ├── serializers.py                # DRF & drf-spectacular serializers
│   ├── signals.py                    # User post_save signal for Company auto-creation
│   ├── tests.py                      # Comprehensive API test suite (Pytest & DRF TestCase)
│   ├── urls.py                       # API & Swagger route definitions
│   └── views.py                      # Register, Login, Query KB, and Usage Summary views
├── infrastructure/
│   ├── modules/                      # Reusable Terraform Child Modules
│   │   ├── app_service/              # Module: App Service Plan & Linux Web App
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── container_registry/       # Module: Azure Container Registry (ACR)
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   └── postgresql/               # Module: Azure PostgreSQL Flexible Server & DB
│   │       ├── main.tf
│   │       ├── outputs.tf
│   │       └── variables.tf
│   ├── main.tf                       # Terraform Root Module (Module orchestrator)
│   ├── outputs.tf                    # Root Output Variables
│   ├── providers.tf                  # Provider configuration (azurerm & version lock)
│   ├── terraform.tfvars              # Configured Terraform Variable Values file
│   ├── terraform.tfvars.example      # Example Terraform Variable template file
│   └── variables.tf                  # Root Input Variable definitions
├── pipelines/
│   ├── templates/                    # Reusable Pipeline Step Templates (Azure DevOps)
│   │   ├── docker-deploy-steps-template.yml # Template: Container build & Web App deploy
│   │   ├── terraform-steps-template.yml     # Template: Terraform init & apply
│   │   └── test-steps-template.yml          # Template: Python setup, Pytest & coverage
│   ├── pipeline-pr-validation.yml    # Separate Pipeline: PR Validation Gate
│   ├── pipeline-code-testing.yml     # Separate Pipeline: Automated Code Testing
│   ├── pipeline-infra.yml            # Separate Pipeline: Infrastructure Provisioning
│   └── pipeline-code.yml             # Separate Pipeline: Code Deployment
├── teamboard/
│   ├── asgi.py                       # ASGI configuration
│   ├── settings.py                   # Django settings, SimpleJWT & drf-spectacular config
│   ├── urls.py                       # Root URL router
│   └── wsgi.py                       # WSGI entry point
├── .dockerignore                     # Files excluded from Docker builds
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore patterns
├── azure-pipelines.yml               # Master Orchestrator Pipeline (Azure DevOps)
├── azure-pipelines-test.yml          # Test Runner Pipeline (Azure DevOps)
├── docker-compose.yml                # Multi-container orchestration (Django + PostgreSQL)
├── Dockerfile                        # Production-ready Python Docker container image
├── manage.py                         # Django administrative CLI
├── pytest.ini                        # Pytest configuration file
├── README.md                         # Comprehensive documentation
├── requirements.txt                  # Pinned Python dependencies
└── TeamBoard.postman_collection.json # 11-scenario Postman collection
```

---

## 📖 Swagger / OpenAPI Documentation

Interactive Swagger documentation and schema endpoints are built into the platform using `drf-spectacular`:

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **ReDoc UI:** `http://127.0.0.1:8000/api/redoc/`
- **OpenAPI 3.0 Schema (JSON):** `http://127.0.0.1:8000/api/schema/`

---

## 📡 API Endpoints Reference

### 1. Register a New Company
`POST /api/auth/register/` (Public)

**Request Body:**
```json
{
  "username": "acmecorp",
  "password": "securepass123",
  "company_name": "Acme Corp",
  "email": "dev@acmecorp.com"
}
```

**Response (201 Created):**
```json
{
  "username": "acmecorp",
  "company_name": "Acme Corp",
  "api_key": "gTk8...auto-generated...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

---

### 2. Company Login
`POST /api/auth/login/` (Public)

**Request Body:**
```json
{
  "username": "acmecorp",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "company_name": "Acme Corp",
  "api_key": "gTk8..."
}
```

---

### 3. Query Knowledge Base
`POST /api/kb/query/` (Protected — Requires `Authorization: Bearer <access_token>`)

**Request Body:**
```json
{
  "search": "select_related"
}
```

**Response (200 OK):**
```json
{
  "search": "select_related",
  "count": 2,
  "results": [
    {
      "id": 1,
      "question": "What is select_related in Django ORM?",
      "answer": "select_related performs a SQL JOIN and fetches...",
      "category": "database"
    }
  ]
}
```

---

### 4. Admin Usage Summary Dashboard
`GET /api/admin/usage-summary/` (Protected — Requires `Authorization: Bearer <admin_access_token>`)

**Response (200 OK):**
```json
{
  "total_queries": 254,
  "active_companies": 7,
  "top_search_terms": [
    { "search_term": "select_related", "count": 42 },
    { "search_term": "transaction atomic", "count": 31 },
    { "search_term": "JWT authentication", "count": 28 },
    { "search_term": "Q objects", "count": 19 },
    { "search_term": "signals django", "count": 14 }
  ]
}
```

---

## ⚙️ Environment Variables Configuration

The application uses `python-dotenv` to manage secrets. Copy `.env.example` to `.env`:

| Variable Name | Default Value | Description |
|---|---|---|
| `SECRET_KEY` | `django-insecure-...` | Django secret key for session signing and cryptography |
| `DEBUG` | `True` | Debug flag (`True` for local development, `False` for production) |
| `ALLOWED_HOSTS` | `*` | Comma-separated list of allowed hostnames |
| `USE_SQLITE` | `False` | Set to `True` for fast in-memory SQLite (used during testing) |
| `DB_ENGINE` | `django.db.backends.postgresql` | Database backend engine |
| `DB_NAME` | `teamboard_db` | PostgreSQL database name |
| `DB_USER` | `teamboard_user` | PostgreSQL user |
| `DB_PASSWORD` | `teamboard_pass` | PostgreSQL password |
| `DB_HOST` | `localhost` | Database host server |
| `DB_PORT` | `5432` | Database host port |

---

## 🛠️ Local Setup & Quick Start

### Prerequisites
- **Python 3.11+** installed
- **Docker & Docker Compose** installed
- **Git** installed

### Step-by-step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shubhankart101/TeamBoard.git
   cd TeamBoard
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   $env:USE_SQLITE="True" # Optional for quick local testing without PostgreSQL
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed Knowledge Base entries:**
   ```bash
   python manage.py seed_kb
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```
   Access Swagger UI at `http://127.0.0.1:8000/api/docs/`.

---

## 🐳 Docker Containerization

Run the full stack (Django API + PostgreSQL 15) using Docker Compose:

```bash
# Start container services in detached mode
docker compose up -d

# Execute migrations inside container
docker compose exec web python manage.py migrate

# Seed KB entries inside container
docker compose exec web python manage.py seed_kb
```

---

## 🏗️ Modular Infrastructure as Code (Terraform on Azure)

The infrastructure is built using modular Terraform components under `infrastructure/`:

### Module Architecture
- **Root Module (`infrastructure/main.tf`)**: Instantiates child modules, managing dependencies and passing configuration variables.
- **Container Registry Module (`infrastructure/modules/container_registry/`)**: Provisions Azure Container Registry (`ACR`) with admin credentials enabled.
- **PostgreSQL Module (`infrastructure/modules/postgresql/`)**: Provisions Azure PostgreSQL Flexible Server v15, database instance (`teamboard_db`), and firewall rules for Azure internal routing.
- **App Service Module (`infrastructure/modules/app_service/`)**: Provisions Linux App Service Plan (`asp-teamboard-dev`) and Azure Web App for Containers (`app-teamboard-dev`), configuring container registries and application environment variables.

### Provision Infrastructure via Terraform

```bash
cd infrastructure

# Initialize providers and child modules
terraform init

# Validate execution plan
terraform plan -var="db_admin_password=<YOUR_PASSWORD>" -var="django_secret_key=<YOUR_SECRET_KEY>"

# Apply infrastructure changes
terraform apply -auto-approve -var="db_admin_password=<YOUR_PASSWORD>" -var="django_secret_key=<YOUR_SECRET_KEY>"
```

---

## 🧪 Templatized CI/CD Pipelines & Automated Testing

### 1. Separate Pipeline Architecture
To ensure separation of concerns and independent execution lifecycle, the pipelines are decoupled into three distinct workflows:

| Pipeline Name | Purpose | Trigger / Scope |
|---|---|---|
| **Code Testing Pipeline** | Runs Django migration checks, Pytest suite, and code coverage reporting | Triggers on pull requests & pushes across all branches |
| **Infrastructure Pipeline** | Initializes and applies Terraform modules to provision/update Azure resources | Triggers on changes inside `infrastructure/` directory |
| **Code Deployment Pipeline** | Builds Docker container image, pushes to ACR, and updates Azure Web App | Triggers on push to `main`/`master` branches |

---

### 2. Pipeline Templatisation (Azure DevOps)
Azure DevOps pipelines leverage step templates defined in `pipelines/templates/`:

- **`test-steps-template.yml`**: Configures Python, installs dependencies, checks migrations, runs Pytest with JUnit output, and publishes coverage reports.
- **`terraform-steps-template.yml`**: Executes `terraform init` and `terraform apply` using Azure CLI credentials.
- **`docker-deploy-steps-template.yml`**: Performs Docker container builds, pushes tagged images to ACR, and updates the Azure Web App.

---

### 3. Separate Pipelines (GitHub Actions & Azure DevOps)

- **GitHub Actions Workflows (`.github/workflows/`)**:
  - `pipeline-code-testing.yml`: Independent workflow for automated tests.
  - `pipeline-infra.yml`: Independent workflow for Terraform infrastructure deployment.
  - `pipeline-code.yml`: Independent workflow for building & deploying container images.
- **Azure DevOps Pipelines (`pipelines/` & root)**:
  - `pipelines/pipeline-code-testing.yml`: Independent test pipeline.
  - `pipelines/pipeline-infra.yml`: Independent infra pipeline.
  - `pipelines/pipeline-code.yml`: Independent code deployment pipeline.
  - `azure-pipelines.yml`: Master CI/CD orchestrator pipeline combining all stages.

---

### 4. Running Tests & Coverage Locally

```bash
# Run pytest test suite with coverage report
$env:USE_SQLITE="True"
pytest
```

### Coverage Summary (97% Total)
```
Name                                Stmts   Miss  Cover
-------------------------------------------------------
api/admin.py                           17      0   100%
api/apps.py                             6      0   100%
api/models.py                          33      0   100%
api/permissions.py                      5      0   100%
api/serializers.py                     36      0   100%
api/signals.py                          9      0   100%
api/tests.py                          150      0   100%
api/urls.py                             4      0   100%
api/views.py                           78      0   100%
-------------------------------------------------------
TOTAL                                 357     12    97%
```

---

## 📮 Postman Collection

Import `TeamBoard.postman_collection.json` into Postman to execute all 11 automated request scenarios:

1. `POST /api/auth/register/` — Register a new company (`201 Created`)
2. `POST /api/auth/register/` — Duplicate username validation (`400 Bad Request`)
3. `POST /api/auth/login/` — Valid credentials (`200 OK`)
4. `POST /api/auth/login/` — Invalid password (`401 Unauthorized`)
5. `POST /api/kb/query/` — Query without token (`401 Unauthorized`)
6. `POST /api/kb/query/` — Query with valid token & matching results (`200 OK`)
7. `POST /api/kb/query/` — Query with valid token & 0 matching results (`200 OK`)
8. `POST /api/kb/query/` — Query with missing search field (`400 Bad Request`)
9. `GET /api/admin/usage-summary/` — Access with CLIENT token (`403 Forbidden`)
10. `GET /api/admin/usage-summary/` — Access with ADMIN token (`200 OK`)
11. `QueryLog Verification` — Validates QueryLog records created in database



