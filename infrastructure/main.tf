terraform {
  required_version = ">= 1.3.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  type    = string
  default = "East US"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "app_name" {
  type    = string
  default = "teamboard"
}

variable "db_admin_user" {
  type    = string
  default = "tbadmin"
}

variable "db_admin_password" {
  type      = string
  sensitive = true
}

variable "django_secret_key" {
  type      = string
  sensitive = true
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.app_name}-${var.environment}"
  location = var.location
}

resource "azurerm_container_registry" "acr" {
  name                = "acr${var.app_name}${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "psql-${var.app_name}-${var.environment}"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "15"
  administrator_login    = var.db_admin_user
  administrator_password = var.db_admin_password
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
}

resource "azurerm_postgresql_flexible_server_database" "db" {
  name      = "teamboard_db"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.postgres.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_service_plan" "asp" {
  name                = "asp-${var.app_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "webapp" {
  name                = "app-${var.app_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      docker_image_name = "${var.app_name}:latest"
      docker_registry_url = "https://${azurerm_container_registry.acr.login_server}"
      docker_registry_username = azurerm_container_registry.acr.admin_username
      docker_registry_password = azurerm_container_registry.acr.admin_password
    }
  }

  app_settings = {
    "SECRET_KEY"                     = var.django_secret_key
    "DEBUG"                          = "False"
    "ALLOWED_HOSTS"                  = "app-${var.app_name}-${var.environment}.azurewebsites.net,localhost,127.0.0.1"
    "DB_ENGINE"                      = "django.db.backends.postgresql"
    "DB_NAME"                        = "teamboard_db"
    "DB_USER"                        = var.db_admin_user
    "DB_PASSWORD"                    = var.db_admin_password
    "DB_HOST"                        = azurerm_postgresql_flexible_server.postgres.fqdn
    "DB_PORT"                        = "5432"
    "WEBSITES_PORT"                  = "8000"
    "DOCKER_REGISTRY_SERVER_URL"     = "https://${azurerm_container_registry.acr.login_server}"
    "DOCKER_REGISTRY_SERVER_USERNAME"= azurerm_container_registry.acr.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD"= azurerm_container_registry.acr.admin_password
  }
}

output "web_app_url" {
  value = "https://${azurerm_linux_web_app.webapp.default_hostname}"
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}
