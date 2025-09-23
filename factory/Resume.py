# factory/resume.py
from .managers import call_gemini
import pdfplumber
import re
from fuzzywuzzy import fuzz

# Education degree synonyms
DEGREE_SYNONYMS = {
    "bsc": ["bachelor of science", "b.sc", "bsc", "bachelor's degree", "bachelor"],
    "msc": ["master of science", "m.sc", "msc", "master's degree", "master"],
    "phd": ["phd", "doctorate", "doctor of philosophy"]
}

class Resume:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self._extract_text()
        self.skills = []
        self.education = []
        self.certifications = []
        self.projects = []
        self.experience = []

    def _extract_text(self):
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def extract_skills_ai(self):
        prompt = f"Extract all technical skills, programming languages, tools, and certifications from this resume text as a comma-separated list:\n{self.text}"
        skills_text = call_gemini(prompt)
        self.skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        return self.skills

    def extract_education_ai(self):
        prompt = f"Extract all degrees from this resume text with format Degree | Institution:\n{self.text}"
        edu_text = call_gemini(prompt)
        for line in edu_text.split("\n"):
            if line.strip():
                parts = line.split("|")
                degree = parts[0].strip().lower()
                institution = parts[1].strip() if len(parts) > 1 else ""
                self.education.append({"degree": degree, "institution": institution})
        return self.education

    def extract_certifications_ai(self):
        prompt = f"Extract all certifications from this resume text as comma-separated list:\n{self.text}"
        cert_text = call_gemini(prompt)
        self.certifications = [c.strip() for c in cert_text.split(",") if c.strip()]
        return self.certifications

    def extract_projects_ai(self):
        prompt = f"Extract all projects from this resume text with title and description:\n{self.text}"
        proj_text = call_gemini(prompt)
        for line in proj_text.split("\n"):
            if line.strip():
                parts = line.split(" - ")
                title = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ""
                self.projects.append({"title": title, "description": description})
        return self.projects

    def extract_experience_ai(self):
        prompt = f"Extract all work experience from this resume text in format Title | StartYear-EndYear | Skills:\n{self.text}"
        exp_text = call_gemini(prompt)
        for line in exp_text.split("\n"):
            if line.strip():
                parts = line.split("|")
                title = parts[0].strip()
                dates = parts[1].strip() if len(parts) > 1 else "0-0"
                skills = parts[2].strip() if len(parts) > 2 else ""
                years = 0
                match = re.findall(r"\d{4}", dates)
                if match:
                    start = int(match[0])
                    end = int(match[1]) if len(match) > 1 else 2025
                    years = end - start
                self.experience.append({"title": title, "years": years, "skills": skills})
        return self.experience
