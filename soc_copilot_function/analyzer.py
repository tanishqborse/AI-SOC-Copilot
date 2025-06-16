import google.generativeai as genai
import json
import os

# Load your MakerSuite API key from env var for security
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")

# Configure Gemini API (MakerSuite)
genai.configure(api_key=GENAI_API_KEY)

# Load Gemini 1.5 Pro (MakerSuite version automatically handles region)
model = genai.GenerativeModel("gemini-1.5-pro")

# Function to analyze log entry
def analyze_log_entry(log_entry):
    prompt = f"""
You are a SOC Tier-2 Security Analyst. Analyze this security log entry and extract:
- Threat Category
- MITRE ATT&CK TTP mappings (if applicable)
- Severity level (Low, Medium, High, Critical)
- Recommendation for next SOC action

Security Log:
{json.dumps(log_entry)}

Respond ONLY in valid JSON format like:
{{
  "threat_category": "...",
  "mitre_ttps": ["..."],
  "severity": "...",
  "recommendation": "..."
}}
"""
    response = model.generate_content(prompt, generation_config={"temperature": 0.4})
    return response.text
