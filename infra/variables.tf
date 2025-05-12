variable "yc_token" {
  type        = string
  description = "Yandex Cloud OAuth token"
}

variable "yc_cloud_id" {
  type = string
  description = "Yandex Cloud ID"
}

variable "yc_folder_id" {
  type        = string
  description = "Yandex Cloud Folder ID"
}

variable "yc_zone" {
  type        = string
  description = "Zone for Yandex Cloud resources"
}

variable "yc_subnet_name" {
  type        = string
  description = "Name of the custom subnet"
}

variable "yc_network_name" {
  type        = string
  description = "Name of the network"
}

variable "yc_subnet_range" {
  type        = string
  description = "CIDR block for the subnet"  
}

variable "yc_mysql_cluster_name" {
  type        = string
  description = "Name of the MySQL cluster"
}

variable "yc_mysql_version" {
  type        = string
  description = "Version of MySQL"
}

variable "yc_mysql_environment" {
  type        = string
  description = "Environment of MySQL"
}

variable "mysql_database_name" {
  type        = string
  description = "Name of the MySQL database"
}

variable "mysql_user_name" {
  type        = string
  description = "Name of the MySQL user"
}

variable "mysql_user_password" {
  type        = string
  description = "Password of the MySQL user"
}

variable "mysql_resource_preset_id" {
  description = "Resource preset for MySQL cluster"
  type        = string
  default     = "s2.micro"
}

variable "mysql_disk_type_id" {
  description = "Disk type for MySQL cluster"
  type        = string
  default     = "network-ssd"
}

variable "mysql_disk_size" {
  description = "Disk size for MySQL cluster in GB"
  type        = number
  default     = 30
}

variable "mysql_config" {
  description = "MySQL configuration"
  type = object({
    sql_mode                      = string
    max_connections               = number
    default_authentication_plugin = string
    innodb_print_all_deadlocks    = bool
  })
  default = {
    sql_mode                      = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
    max_connections               = 100
    default_authentication_plugin = "MYSQL_NATIVE_PASSWORD"
    innodb_print_all_deadlocks    = true
  }
}

variable "yc_service_account_name" {
  type        = string
  description = "Name of the service account"
}

variable "yc_bucket_name" {
  type        = string
  description = "Name of the bucket"
}