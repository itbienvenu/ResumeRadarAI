import pdfplumber
from .managers import get_real_dir, call_gemini

class Resume:
    def __init__(self, file_path):
        self.file_path = get_real_dir(file_path)
        self.text = self._extract_text()
        self.skills = []

    def _extract_text(self):
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    def extract_skills_ai(self):
        """Use Gemini to extract skills from resume text."""
        prompt = f"""
        Extract all technical skills, programming languages, tools, and certifications
        from the following resume text. Provide as a comma-separated list:

        {self.text}
        """
        skills_text = call_gemini(prompt)
        self.skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        return self.skills
