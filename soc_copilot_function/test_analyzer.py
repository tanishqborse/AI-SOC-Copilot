from analyzer import analyze_log_entry

sample_log = {
  "timestamp": "2024-06-14T12:00:00Z",
  "source_ip": "192.168.1.10",
  "destination_ip": "10.0.0.5",
  "event": "Unauthorized SSH login attempt",
  "username": "root",
  "location": "us-central1"
}

result = analyze_log_entry(sample_log)
print(result)
