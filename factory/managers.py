import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def call_gemini(prompt: str) -> str:
    """Send prompt to Gemini API and return the text response."""
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.text}")

    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"].strip()

def get_real_dir(file_name: str):
    # Project root (current working directory)
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(PROJECT_ROOT, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return file_path
