import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# Setup
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client()

TARGET_FILE = "AI_NOTES.md"

# Prompt AI for a daily tech tip based on your stack
prompt = """
You are a senior full-stack developer. Write a short, single-paragraph technical tip or fact 
about either Laravel, Flutter, or Cybersecurity. 
Format it in Markdown. Do not include introductory text, just the tip.
"""

print("🤖 Fetching daily tech tip...")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
)
new_tip = response.text.strip()

# Append the tip to the notes file
with open(TARGET_FILE, "a", encoding="utf-8") as file:
    date_str = datetime.now().strftime("%Y-%m-%d")
    file.write(f"\n\n### Tip for {date_str}\n{new_tip}")

print("✅ File updated.")

# Automate the Git Commit for the Cloud
try:
    # Set up Git identity for the GitHub Action runner
    subprocess.run(["git", "config", "user.name", "AI Learning Agent"], check=True)
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    
    subprocess.run(["git", "add", TARGET_FILE], check=True)
    commit_message = f"docs(AI): Daily learning note for {date_str}"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    
    print(f"🎉 Committed: '{commit_message}'")
except subprocess.CalledProcessError as e:
    print(f"❌ Git commit failed: {e}")