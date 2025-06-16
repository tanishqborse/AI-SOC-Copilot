terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 4.0.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

resource "google_project_service" "essential_services" {
  for_each = toset([
    "container.googleapis.com",
    "securitycenter.googleapis.com",
    "cloudfunctions.googleapis.com",
    "pubsub.googleapis.com",
    "logging.googleapis.com",
    "iam.googleapis.com",
    "aiplatform.googleapis.com",
    "secretmanager.googleapis.com"
  ])
  service = each.value
}

resource "google_container_cluster" "gke_cluster" {
  provider = google-beta

  name     = "secops-cluster"
  location = var.region

  enable_autopilot = true
}
