output "cluster_name" {
  value = google_container_cluster.gke_cluster.name
}

output "location" {
  value = var.region
}
