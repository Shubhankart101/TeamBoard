variable "plan_name" {
  description = "The name of the Service Plan."
  type        = string
}

variable "web_app_name" {
  description = "The name of the Linux Web App."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the App Service."
  type        = string
}

variable "location" {
  description = "The Azure region where the resource exists."
  type        = string
}

variable "sku_name" {
  description = "The SKU for the Service Plan."
  type        = string
  default     = "B1"
}

variable "docker_image_name" {
  description = "Docker image name and tag (e.g. teamboard:latest)."
  type        = string
}

variable "docker_registry_url" {
  description = "The URL of the Docker registry."
  type        = string
}

variable "docker_registry_username" {
  description = "The username for the Docker registry."
  type        = string
}

variable "docker_registry_password" {
  description = "The password for the Docker registry."
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Django application secret key."
  type        = string
  sensitive   = true
}

variable "db_host" {
  description = "PostgreSQL host server FQDN."
  type        = string
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
}

variable "db_user" {
  description = "PostgreSQL admin user."
  type        = string
}

variable "db_password" {
  description = "PostgreSQL admin password."
  type        = string
  sensitive   = true
}
