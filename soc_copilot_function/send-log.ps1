param(
    [string]$SourceIP = "192.168.1.10",
    [string]$TargetIP = "10.0.0.5",
    [string]$EventType = "ssh_login_attempt",
    [string]$Result = "failed"
)

# Build JSON object
$jsonObj = @{
    source_ip = $SourceIP
    target_ip = $TargetIP
    event_type = $EventType
    result = $Result
}

# Convert to JSON string
$json = $jsonObj | ConvertTo-Json -Compress

# Escape quotes correctly for gcloud pubsub
$jsonEscaped = $json -replace '"','\"'

# Publish to PubSub topic
gcloud pubsub topics publish soc-pipeline --message "`"$jsonEscaped`""
