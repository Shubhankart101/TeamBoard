resource "azurerm_service_plan" "asp" {
  name                = var.plan_name
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = var.sku_name
}

resource "azurerm_linux_web_app" "webapp" {
  name                = var.web_app_name
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      docker_image_name        = var.docker_image_name
      docker_registry_url      = var.docker_registry_url
      docker_registry_username = var.docker_registry_username
      docker_registry_password = var.docker_registry_password
    }
  }

  app_settings = {
    "SECRET_KEY"                      = var.django_secret_key
    "DEBUG"                           = "False"
    "ALLOWED_HOSTS"                   = "${var.web_app_name}.azurewebsites.net,localhost,127.0.0.1"
    "DB_ENGINE"                       = "django.db.backends.postgresql"
    "DB_NAME"                         = var.db_name
    "DB_USER"                         = var.db_user
    "DB_PASSWORD"                     = var.db_password
    "DB_HOST"                         = var.db_host
    "DB_PORT"                         = "5432"
    "WEBSITES_PORT"                   = "8000"
    "DOCKER_REGISTRY_SERVER_URL"      = var.docker_registry_url
    "DOCKER_REGISTRY_SERVER_USERNAME" = var.docker_registry_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = var.docker_registry_password
  }
}
