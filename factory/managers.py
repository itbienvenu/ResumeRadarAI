import os
import requests
from dotenv import load_dotenv
from rapidfuzz import fuzz


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


def normalize_skill(skill: str) -> str:
    return skill.strip().lower()


# Some skills synonyms

def expand_with_synonyms(skill):
    synonyms = get_synonyms(skill)
    return set([skill.lower()]) | synonyms


def fuzzy_match(skill1, skill2, threshold=85):
    return fuzz.ratio(skill1, skill2) >= threshold



def get_weight(skill, job_skills_dict):
    return job_skills_dict.get(skill, 1)


def get_synonyms(skill_name):
    prompt = f"""
    Provide a list of all synonyms, alternative names, related frameworks, and tools
    for the skill "{skill_name}". Return them as a comma-separated list.
    """
    response_text = call_gemini(prompt)
    synonyms = [s.strip().lower() for s in response_text.split(",") if s.strip()]
    return set(synonyms)