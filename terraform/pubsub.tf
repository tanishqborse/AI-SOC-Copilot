# Create PubSub Topic for SOC pipeline
resource "google_pubsub_topic" "soc_pipeline_topic" {
  name = "soc-pipeline"
}

# Create Logging Sink to route logs into PubSub
resource "google_logging_project_sink" "soc_logging_sink" {
  name        = "soc-pipeline-sink"
  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${google_pubsub_topic.soc_pipeline_topic.name}"
  filter      = "resource.type=(\"gke_cluster\" OR \"k8s_container\" OR \"k8s_pod\" OR \"gce_instance\" OR \"project\" OR \"global\")"

  unique_writer_identity = true
}

# Grant Pub/Sub Publisher role to Logging Sink service account
resource "google_pubsub_topic_iam_member" "sink_pubsub_writer" {
  topic    = google_pubsub_topic.soc_pipeline_topic.name
  role     = "roles/pubsub.publisher"
  member   = google_logging_project_sink.soc_logging_sink.writer_identity
}
