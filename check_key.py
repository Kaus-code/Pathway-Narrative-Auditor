from dotenv import load_dotenv
import os
import requests

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print(f"Key loaded: {key[:8]}...{key[-4:] if key else 'None'}")

if not key:
    print("No key found.")
    exit(1)

try:
    resp = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {key}"})
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
