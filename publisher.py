import os
import requests
from dotenv import load_dotenv
from google import genai

# 1. Securely load API Keys
load_dotenv()
gemini_key = os.environ.get("GEMINI_API_KEY")
dev_to_key = os.environ.get("DEV_TO_API_KEY")

client = genai.Client()

# 2. Read the latest short tip from your file
with open("AI_NOTES.md", "r", encoding="utf-8") as file:
    # Get the last 500 characters to grab the most recent tip
    latest_tip = file.read()[-500:] 

print("🤖 Agent 1: Expanding the daily note into a full draft...")

# 3. Prompt Gemini to act as a Technical Writer
prompt = f"""
You are a senior technical writer. Take the following short technical note and expand it into a 
highly engaging, 500-word blog post formatted in Markdown. 
Focus the tone for developers learning Laravel, Flutter, or Cybersecurity. 
Include an Introduction, a Code Example or deep-dive explanation, and a Conclusion.

The Short Note: {latest_tip}
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
)
article_body = response.text.strip()

print("🚀 Agent 2: Sending draft to Dev.to...")

# 4. Construct the API Payload for Dev.to
headers = {
    "api-key": dev_to_key,
    "Content-Type": "application/json"
}

# published: False is the critical safeguard. It keeps it as a private draft.
data = {
    "article": {
        "title": "Daily Dev Dive: Automatically Generated Note",
        "body_markdown": article_body,
        "published": False, 
        "tags": ["webdev", "learning", "tutorial"]
    }
}

# 5. Push to Dev.to API
url = "https://dev.to/api/articles"
api_response = requests.post(url, json=data, headers=headers)

if api_response.status_code == 201:
    print("✅ Success! Your article draft is waiting in your Dev.to dashboard.")
else:
    print(f"❌ Failed to publish: {api_response.text}")