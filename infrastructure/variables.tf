variable "location" {
  description = "The Azure region where all resources will be created."
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "The deployment environment (e.g. dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "app_name" {
  description = "The application name prefix."
  type        = string
  default     = "teamboard"
}

variable "db_admin_user" {
  description = "PostgreSQL Flexible Server administrator login username."
  type        = string
  default     = "tbadmin"
}

variable "db_admin_password" {
  description = "PostgreSQL Flexible Server administrator password."
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Django SECRET_KEY value for production."
  type        = string
  sensitive   = true
}
