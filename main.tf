terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "terraform_bucket" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo" {
  dataset_id                      = var.dataset_name
  default_partition_expiration_ms = var.default_partition_expiration_ms  # 30 days
  default_table_expiration_ms     = var.default_table_expiration_ms # 365 days
  description                     = var.dataset_name
  location                        = var.location
  max_time_travel_hours           = var.max_time_travel_hours # 4 days
}