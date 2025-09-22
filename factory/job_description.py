from .managers import call_gemini

class JobDescription:
    def __init__(self, text):
        self.text = text
        self.skills = []

    def extract_skills_ai(self):
        """Use Gemini to extract skills from job description text."""
        prompt = f"""
        Extract all required skills, programming languages, and tools
        from the following job description. Provide as a comma-separated list:

        {self.text}
        """
        skills_text = call_gemini(prompt)
        self.skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        return self.skills
