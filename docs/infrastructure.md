# 🏗️ Modular Infrastructure as Code (Terraform on Azure)

This document details the modular Terraform architecture deployed to Azure cloud infrastructure for **TeamBoard**.

---

## 🏛️ Modular Architecture Overview

The infrastructure in [infrastructure/](infrastructure/) is organized using reusable child modules to enforce separation of concerns, DRY principles, and maintainability.

```
infrastructure/
├── modules/
│   ├── app_service/
│   │   ├── main.tf          # Linux Service Plan & Web App for Containers
│   │   ├── outputs.tf       # Web app ID & URL outputs
│   │   └── variables.tf     # Container registry & environment variables
│   ├── container_registry/
│   │   ├── main.tf          # Azure Container Registry (ACR - Basic)
│   │   ├── outputs.tf       # Login server & admin credentials outputs
│   │   └── variables.tf     # Registry SKU & location variables
│   └── postgresql/
│       ├── main.tf          # Azure PostgreSQL Flexible Server v15 & Database
│       ├── outputs.tf       # Server FQDN & DB name outputs
│       └── variables.tf     # Storage, SKU & admin credentials variables
├── main.tf                  # Root module (Child module orchestrator)
├── outputs.tf               # Root level deployment outputs
├── providers.tf             # Provider initialization (azurerm ~> 3.80.0)
├── terraform.tfvars         # Active environment variable values
├── terraform.tfvars.example # Template variable file
└── variables.tf             # Root level variable definitions
```

---

## 🧩 Child Modules Breakdown

### 1. Container Registry Module (`modules/container_registry/`)
- Resource: `azurerm_container_registry`
- Features: Basic SKU, Admin user enabled for container deployment authentication.

### 2. PostgreSQL Module (`modules/postgresql/`)
- Resources: `azurerm_postgresql_flexible_server`, `azurerm_postgresql_flexible_server_database`, `azurerm_postgresql_flexible_server_firewall_rule`
- Features: PostgreSQL 15, `teamboard_db` instance creation, firewall rule allowing internal Azure service communication.

### 3. App Service Module (`modules/app_service/`)
- Resources: `azurerm_service_plan`, `azurerm_linux_web_app`
- Features: Linux Service Plan (B1 Basic SKU), Web App for Containers running `teamboard:latest`, configured with database host, credentials, and Django environment variables.

---

## ⚙️ Configuration Files & Variables

- `infrastructure/providers.tf`: Provider configuration locking `hashicorp/azurerm` version to `~> 3.80.0`.
- `infrastructure/variables.tf`: Input declarations for `location`, `environment`, `app_name`, `db_admin_user`, `db_admin_password`, and `django_secret_key`.
- `infrastructure/terraform.tfvars`: File providing actual input values for local or pipeline Terraform execution.
- `infrastructure/outputs.tf`: Exports `resource_group_name`, `web_app_url`, `acr_login_server`, and `postgres_fqdn`.

---

## 🚀 Execution Guide

```bash
cd infrastructure

# Initialize backend providers and child modules
terraform init

# Plan deployment using terraform.tfvars
terraform plan

# Apply infrastructure changes
terraform apply -auto-approve
```
