output "web_app_id" {
  description = "The ID of the Linux Web App."
  value       = azurerm_linux_web_app.webapp.id
}

output "web_app_url" {
  description = "The default URL of the Web App."
  value       = "https://${azurerm_linux_web_app.webapp.default_hostname}"
}

output "default_hostname" {
  description = "The default hostname of the Web App."
  value       = azurerm_linux_web_app.webapp.default_hostname
}
