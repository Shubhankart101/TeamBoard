variable "server_name" {
  description = "The name which should be used for this PostgreSQL Flexible Server."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the Resource Group in which the PostgreSQL Flexible Server should exist."
  type        = string
}

variable "location" {
  description = "The Azure Region where the PostgreSQL Flexible Server should exist."
  type        = string
}

variable "administrator_login" {
  description = "The Administrator login for the PostgreSQL Flexible Server."
  type        = string
  default     = "tbadmin"
}

variable "administrator_password" {
  description = "The Password associated with the administrator_login for the PostgreSQL Flexible Server."
  type        = string
  sensitive   = true
}

variable "postgres_version" {
  description = "The version of PostgreSQL Flexible Server to use."
  type        = string
  default     = "15"
}

variable "sku_name" {
  description = "The SKU Name for the PostgreSQL Flexible Server."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "storage_mb" {
  description = "The max storage allowed for the PostgreSQL Flexible Server in MB."
  type        = number
  default     = 32768
}

variable "db_name" {
  description = "The name of the PostgreSQL Database."
  type        = string
  default     = "teamboard_db"
}
