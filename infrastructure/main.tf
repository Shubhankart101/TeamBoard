resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.app_name}-${var.environment}"
  location = var.location
}

module "container_registry" {
  source              = "./modules/container_registry"
  registry_name       = "acr${var.app_name}${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

module "postgresql" {
  source                 = "./modules/postgresql"
  server_name            = "psql-${var.app_name}-${var.environment}"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  administrator_login    = var.db_admin_user
  administrator_password = var.db_admin_password
  db_name                = "teamboard_db"
}

module "app_service" {
  source                    = "./modules/app_service"
  plan_name                 = "asp-${var.app_name}-${var.environment}"
  web_app_name              = "app-${var.app_name}-${var.environment}"
  resource_group_name       = azurerm_resource_group.rg.name
  location                  = azurerm_resource_group.rg.location
  sku_name                  = "B1"
  docker_image_name         = "${var.app_name}:latest"
  docker_registry_url       = "https://${module.container_registry.login_server}"
  docker_registry_username  = module.container_registry.admin_username
  docker_registry_password  = module.container_registry.admin_password
  django_secret_key         = var.django_secret_key
  db_host                   = module.postgresql.fqdn
  db_name                   = module.postgresql.db_name
  db_user                   = module.postgresql.administrator_login
  db_password               = var.db_admin_password
}
