variable "dataset_name" {
  type = string
  default = "demo_dataset"
  description = "value of the demo dataset"
}

variable "storage_class" {
  type = string
  default = "STANDARD"
  description = "value of the storage class"
}

variable "bucket_name" {
  type = string
  default = "data-engineering-409902-terraform-bucket-01"
  description = "value of the demo bucket"
}

variable "project_id" {
  type = string
  default = "data-engineering-409902"
  description = "value of the project id"
}

variable "region" {
  type = string
  default = "us-west1"
  description = "value of the region"
}

variable "location" {
  type = string
  default = "US"
  description = "value of the location"
}

variable "max_time_travel_hours" {
  type = number
  default = 96
  description = "value of the max time travel hours"
}

variable "default_partition_expiration_ms" {
  type = number
  default = 2592000000
  description = "value of the default partition expiration ms"
}

variable "default_table_expiration_ms" {
  type = number
  default = 31536000000
  description = "value of the default table expiration ms"
}

