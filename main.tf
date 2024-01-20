terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  project     = "data-engineering-409902"
  region      = "us-west1"
}

resource "google_storage_bucket" "terraform_bucket" {
  name          = "data-engineering-409902-terraform-bucket-01"
  location      = "US"
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