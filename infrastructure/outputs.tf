output "resource_group_name" {
  description = "The name of the resource group."
  value       = azurerm_resource_group.rg.name
}

output "web_app_url" {
  description = "The URL of the deployed App Service."
  value       = module.app_service.web_app_url
}

output "acr_login_server" {
  description = "The Login Server URL of the Azure Container Registry."
  value       = module.container_registry.login_server
}

output "postgres_fqdn" {
  description = "The FQDN of the PostgreSQL Flexible Server."
  value       = module.postgresql.fqdn
}
