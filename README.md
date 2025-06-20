# 🛡️ AI-SOC Copilot: Autonomous Security Log Analysis with Gemini (Vertex AI) + GCP

---

## 🌐 Project Overview

This project implements a **serverless AI-driven Security Operations Center (SOC) Copilot** that analyzes security logs, maps MITRE ATT&CK TTPs, classifies threat severity, and recommends remediation steps — fully automated.

### ⚙️ Key Technologies:

- **Google Cloud Functions** (serverless ingestion pipeline)
- **Google Pub/Sub** (real-time log ingestion)
- **Google Cloud Storage** (raw log archival)
- **Google BigQuery** (structured threat database)
- **Vertex AI (Gemini 2.5 Flash Preview)** (Generative AI security analysis)

✅ Simulates Tier-1 and Tier-2 SOC analyst workflows  
✅ Fully serverless — no persistent infrastructure  
✅ Easily extendable for real-world production-grade SOC pipelines

### 🛠️ Infrastructure as Code (Terraform)
This project uses Terraform to automate and provision all the GCP resources needed for the SOC Copilot pipeline. This enables reproducibility, faster deployments, and cloud-native DevSecOps practices.

---

## 🏗️ Architecture Diagram

```plaintext
+---------------------+
|  Security Log Source|
+----------+----------+
           |
           v
+-----------------------+
|   Log Publisher (Pub/Sub) |
+-----------------------+
           |
           v
+------------------------+
|  Cloud Function (GCF)  |
| - Decodes logs         |
| - Stores raw logs      |
| - Calls Vertex AI      |
| - Parses output        |
| - Inserts BigQuery row |
+------------------------+
           |
           v
+------------------------+
| Google BigQuery        |
| - Clean structured DB   |
| - Used by Looker Studio |
+------------------------+
           |
           v
+--------------------------+
| Looker Studio Dashboard  |
| - Threat visibility      |
| - Severity & TTP metrics |
+--------------------------+
```

---

### 4️⃣ **Tools & Stack** 
```
| Layer             | Technology            | Purpose                     |
|-------------------|-----------------------|-----------------------------|
| **Cloud Compute** | Google Cloud Function | Serverless Log Processor    |
| **Messaging Bus** | Google Pub/Sub        | Log Ingestion               |
| **Storage**       | Google Cloud Storage  | Raw Log Archival            |
| **AI Model**      | Vertex AI Gemini 2.5  | Generative Security Analysis|
| **Database**      | BigQuery              | Structured Threat Storage   |
| **Visualization** | Looker Studio         | SOC Monitoring Dashboards   |
| **IaC**           | Terraform (optional)  | Infrastructure Provisioning |
| **Language**      | Python 3.11           | Pipeline Implementation     |

```
## 🚩 Key Capabilities

- ✅ Auto-categorizes Threat Type
- ✅ Maps MITRE ATT&CK TTPs
- ✅ Classifies Severity: Low / Medium / High / Critical
- ✅ Generates AI-powered SOC Analyst recommendations
- ✅ Supports raw log archiving for compliance
- ✅ Visual dashboards for SOC teams


## 📂 Project Structure

```bash
SecOps/
├── soc_copilot_function/    # Cloud Function Source Code
│   ├── main.py              # Full function logic
│   ├── analyzer.py          # AI analyzer logic
│   ├── requirements.txt     # Python dependencies
│   ├── send-log.ps1         # Powershell test log sender
│   └── schema.json          # (Optional future schema validation)
├── terraform/               # (Optional) Infra-as-Code
│   ├── main.tf
│   ├── pubsub.tf
│   └── outputs.tf
└── .gitignore

```

---

## 🚀 Deployment Guide

```
gcloud functions deploy soc-copilot-ingest \
  --runtime python311 \
  --trigger-topic soc-pipeline \
  --entry-point pubsub_handler \
  --set-env-vars GCS_BUCKET=gemini-soc-logs \
  --region us-central1 \
  --memory=512MB
```
### BigQuery Table Schema
```
bq mk -t \
--schema "threat_category:STRING,mitre_ttps:STRING,severity:STRING,recommendation:STRING,event_ts:TIMESTAMP,source_ip:STRING,target_ip:STRING" \
gemini-secops-pipeline:soc_copilot.threat_analysis
```

### 3️⃣ Send Test Log
```
.\send-log.ps1 -SourceIP "192.168.10.5" -TargetIP "10.0.0.8" -EventType "ssh_login_attempt" -Result "failed"
```
### 4️⃣ Build Looker Studio Dashboard
✅ Connect to BigQuery

✅ Add charts: Threat Severity, MITRE TTPs, Critical Threat Timeline

✅ Optional: Use REGEXP_SPLIT for exploding multi-TTP fields

## 📡 Data Sources (For Future Real Integration)

| Data Source              | Ingestion Adapter        |
|---------------------------|--------------------------|
| Firewall Logs (Palo Alto, Fortinet, Cisco ASA) | Pub/Sub Ingestion |
| EDR Logs (CrowdStrike, SentinelOne) | Pub/Sub Adapter |
| Cloud Audit Logs (GCP, AWS) | Direct Pub/Sub Export |
| WAF Logs | GCS + Pub/Sub |
| Syslog | Syslog Collector → Pub/Sub |
| Windows Event Logs | WinLogBeat → GCS/PubSub |

## 💡 Why This Project Stands Out

- ✅ Modern GenAI SOC Automation (Gemini-powered LLM log analysis)
- ✅ Production-grade serverless architecture
- ✅ MITRE ATT&CK integration for real SOC operations
- ✅ Visual analytics (Severity/TTP dashboards)
- ✅ Full code & IaC deployment
- ✅ Cloud-native stack (GCP SOC Engineering skills)

🔥 This is directly aligned with modern SecOps, MDR, and XDR pipelines.
🔥 Excellent demonstration of security automation, AI integration, data engineering and SOC analyst augmentation.

## 📊 Sample Logs for Testing

```powershell
# High Severity Test
.\send-log.ps1 -SourceIP "172.16.8.22" -TargetIP "10.0.5.6" -EventType "malware_detected" -Result "success"
```
# Critical Ransomware Test
```
.\send-log.ps1 -SourceIP "10.5.2.100" -TargetIP "10.0.10.50" -EventType "ransomware_activity" -Result "encrypted"
```

## 🔒 Security Considerations

- ✅ GCP IAM permissions on Pub/Sub, Cloud Functions, Vertex AI, and BigQuery
- ✅ Terraform state files excluded via .gitignore (no keys exposed)
- ✅ Environment isolation for staging/prod via separate deployments


## UI
Looker Studio Viual Dashboard link: https://lookerstudio.google.com/s/i_vKnNdNuJE
![dashboard](https://github.com/user-attachments/assets/e3389234-f8d0-43c8-a2c4-b577c748de5a)
![bigquery](https://github.com/user-attachments/assets/8f876310-703e-4022-8dde-6911f7371254)
If we select a particular event:
![threatbased](https://github.com/user-attachments/assets/c6641e2e-e939-4495-9c65-88a32bddd316)
![threatbased2](https://github.com/user-attachments/assets/ba1f338a-6ff9-4d7a-84fe-cb753434a604)
