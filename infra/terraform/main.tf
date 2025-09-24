terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "data" {
  name                        = var.gcs_bucket
  location                    = var.region
  uniform_bucket_level_access = true
}

resource "google_artifact_registry_repository" "itower" {
  location      = var.region
  repository_id = "itower"
  format        = "DOCKER"
}
