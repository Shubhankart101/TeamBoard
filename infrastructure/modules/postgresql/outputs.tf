output "server_id" {
  description = "The ID of the PostgreSQL Flexible Server."
  value       = azurerm_postgresql_flexible_server.postgres.id
}

output "fqdn" {
  description = "The FQDN of the PostgreSQL Flexible Server."
  value       = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "db_name" {
  description = "The name of the database created."
  value       = azurerm_postgresql_flexible_server_database.db.name
}

output "administrator_login" {
  description = "The admin login name."
  value       = azurerm_postgresql_flexible_server.postgres.administrator_login
}
