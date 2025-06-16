import base64
import json
import os
from datetime import datetime
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import storage
from google.cloud import bigquery

# Initialize Vertex AI
vertexai.init(project="gemini-secops-pipeline", location="us-central1")
model = GenerativeModel("gemini-2.5-flash-preview-05-20")

# Initialize GCS client
storage_client = storage.Client()
bucket_name = os.environ.get("GCS_BUCKET", "gemini-soc-logs")
bucket = storage_client.bucket(bucket_name)

# Initialize BigQuery client
bq_client = bigquery.Client(project="gemini-secops-pipeline")
bq_dataset = "soc_copilot"
bq_table = "threat_analysis"
table_id = f"{bq_client.project}.{bq_dataset}.{bq_table}"

def analyze_log_entry(log_entry):
    prompt = f"""
You are a SOC Tier-2 Security Analyst. Analyze this security log entry and extract ONLY these fields:

- threat_category
- mitre_ttps (as list of ATT&CK IDs)
- severity (Low, Medium, High, Critical)
- recommendation

Here is the log:

{json.dumps(log_entry)}

Respond in STRICT JSON format, without any markdown, language tags, or extra commentary. Example:

{{
  "threat_category": "Brute Force Attack",
  "mitre_ttps": ["T1110", "TA0006"],
  "severity": "Medium",
  "recommendation": "Lock user account after multiple failed logins."
}}
"""
    response = model.generate_content(prompt, generation_config={"temperature": 0.4})
    return response.text

def parse_ai_output(ai_output):
    try:
        # Clean up common Gemini output formatting
        clean_output = ai_output.strip().replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean_output)

        # Enforce expected schema
        required_fields = ["threat_category", "mitre_ttps", "severity", "recommendation"]
        for field in required_fields:
            if field not in parsed:
                print(f"Field {field} missing in AI response, inserting default.")
                if field == "mitre_ttps":
                    parsed[field] = []
                else:
                    parsed[field] = "N/A"

        # Sanitize mitre_ttps to always be a list
        if not isinstance(parsed["mitre_ttps"], list):
            parsed["mitre_ttps"] = [parsed["mitre_ttps"]]

        return parsed

    except Exception as e:
        print(f"Failed to parse AI output: {e}")
        return None


def save_raw_log(log_entry):
    try:
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        filename = f"raw/{timestamp}.json"
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(log_entry))
        print(f"Raw log saved to {filename}")
    except Exception as e:
        print(f"Error saving raw log to GCS: {e}")

def write_to_bigquery(parsed_output, log_entry):
    row = {
        "threat_category": parsed_output.get("threat_category", ""),
        "mitre_ttps": ", ".join(parsed_output.get("mitre_ttps", [])),
        "severity": parsed_output.get("severity", ""),
        "recommendation": parsed_output.get("recommendation", ""),
        "event_ts": datetime.utcnow().isoformat(),
        "source_ip": log_entry.get("source_ip", ""),
        "target_ip": log_entry.get("target_ip", "")
    }
    errors = bq_client.insert_rows_json(table_id, [row])
    if errors:
        print(f"BigQuery insert errors: {errors}")
    else:
        print("Successfully inserted into BigQuery")

def pubsub_handler(event, context):
    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        log_entry = json.loads(pubsub_message)
        save_raw_log(log_entry)
        ai_output = analyze_log_entry(log_entry)
        print("AI Output:", ai_output)
        parsed_output = parse_ai_output(ai_output)
        if parsed_output:
            write_to_bigquery(parsed_output, log_entry)
        else:
            log_error_to_gcs(f"Failed to parse Gemini response: {ai_output}")
    except Exception as e:
        log_error_to_gcs(f"Error processing message: {e}")
        print(f"Error processing message: {e}")

def log_error_to_gcs(error_message, folder="errors"):
    try:
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        filename = f"{folder}/{timestamp}.json"
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps({"timestamp": timestamp, "error": error_message}))
    except Exception as e:
        print(f"Failed to log error to GCS: {e}")