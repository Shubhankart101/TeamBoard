# 🏗️ Modular Infrastructure as Code (Terraform on Azure)

This document provides a technical specification for the modular HashiCorp Terraform architecture used to provision cloud infrastructure on **Microsoft Azure** for **TeamBoard**.

---

## 🏛️ Modular Architecture Overview

The infrastructure in `infrastructure/` follows a modular Terraform architecture. It separates resources into encapsulated, reusable child modules, orchestrated by a root module.

```
infrastructure/
├── modules/
│   ├── app_service/
│   │   ├── main.tf          # Linux Service Plan & Web App for Containers
│   │   ├── outputs.tf       # Web App URL and Resource ID outputs
│   │   └── variables.tf     # Registry, DB credentials & app settings variables
│   ├── container_registry/
│   │   ├── main.tf          # Azure Container Registry (ACR - Basic)
│   │   ├── outputs.tf       # Login server & admin credentials outputs
│   │   └── variables.tf     # Registry SKU, name & location variables
│   └── postgresql/
│       ├── main.tf          # Azure PostgreSQL Flexible Server v15 & DB
│       ├── outputs.tf       # Server FQDN & Database name outputs
│       └── variables.tf     # Storage, SKU & admin user/password variables
├── main.tf                  # Root Module (Child module orchestrator)
├── outputs.tf               # Root Output Variables
├── providers.tf             # Provider initialization (azurerm ~> 3.80.0)
├── terraform.tfvars         # Active Environment Variable Values file
├── terraform.tfvars.example # Example Variable Template file
└── variables.tf             # Root Input Variable definitions
```

---

## 🧩 Child Modules Technical Specification

### 1. Container Registry Module (`modules/container_registry/`)
Provisions an Azure Container Registry (`ACR`) instance to host TeamBoard Docker container images.

- **Resource:** `azurerm_container_registry.acr`
- **SKU:** `Basic` (Cost-effective for development/staging workloads).
- **Admin User:** Enabled (`admin_enabled = true`) to provide username and password credentials for App Service deployment pull authentication.
- **Outputs:** `login_server`, `admin_username`, `admin_password` (sensitive), `id`.

### 2. PostgreSQL Module (`modules/postgresql/`)
Provisions a managed Azure Database for PostgreSQL Flexible Server v15 instance.

- **Resources:**
  - `azurerm_postgresql_flexible_server.postgres`: Standard_B1ms SKU (Burstable Tier), 32 GB storage.
  - `azurerm_postgresql_flexible_server_database.db`: Target database `teamboard_db` (`UTF8` charset, `en_US.utf8` collation).
  - `azurerm_postgresql_flexible_server_firewall_rule.allow_azure`: Firewall rule `AllowAzureServices` (`0.0.0.0` to `0.0.0.0`) enabling secure internal network routing from Azure App Service to the database.
- **Outputs:** `server_id`, `fqdn`, `db_name`, `administrator_login`.

### 3. App Service Module (`modules/app_service/`)
Provisions a Linux App Service Plan and Web App for Containers running the application container.

- **Resources:**
  - `azurerm_service_plan.asp`: Linux OS, Basic B1 SKU.
  - `azurerm_linux_web_app.webapp`: Configured with container application stack (`docker_image_name = teamboard:latest`).
- **Environment Injection (`app_settings`):**
  - `SECRET_KEY`: Django cryptographic key.
  - `DEBUG`: Set to `False`.
  - `ALLOWED_HOSTS`: Set to Web App default hostname, `localhost`, `127.0.0.1`.
  - `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: PostgreSQL connection details.
  - `DOCKER_REGISTRY_SERVER_URL`, `DOCKER_REGISTRY_SERVER_USERNAME`, `DOCKER_REGISTRY_SERVER_PASSWORD`: ACR pull credentials.
- **Outputs:** `web_app_id`, `web_app_url`, `default_hostname`.

---

## ⚙️ Root Module Input & Output Mappings

### Root Inputs (`infrastructure/variables.tf` & `infrastructure/terraform.tfvars`)

| Variable Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `location` | String | `"East US"` | No | Target Azure region |
| `environment` | String | `"dev"` | No | Deployment environment prefix |
| `app_name` | String | `"teamboard"` | No | Application name prefix |
| `db_admin_user` | String | `"tbadmin"` | No | PostgreSQL admin username |
| `db_admin_password` | String | — | **Yes** | PostgreSQL admin password |
| `django_secret_key` | String | — | **Yes** | Django SECRET_KEY |

### Root Outputs (`infrastructure/outputs.tf`)

| Output Name | Value Source | Description |
|---|---|---|
| `resource_group_name` | `azurerm_resource_group.rg.name` | Created resource group name |
| `web_app_url` | `module.app_service.web_app_url` | Live HTTPS URL of Web App |
| `acr_login_server` | `module.container_registry.login_server` | ACR registry FQDN |
| `postgres_fqdn` | `module.postgresql.fqdn` | Database server FQDN |

---

## 🚀 Terraform Execution Commands Guide

```bash
cd infrastructure

# 1. Initialize backend providers and download child modules
terraform init

# 2. Validate syntax and structural integrity
terraform validate

# 3. Preview planned infrastructure additions using terraform.tfvars
terraform plan

# 4. Apply infrastructure deployment
terraform apply -auto-approve

# 5. Output resource endpoints
terraform output

# 6. Destroy infrastructure stack (when tearing down environment)
# terraform destroy -auto-approve
```

