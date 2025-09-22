from .managers import call_gemini

class JobDescription:
    def __init__(self, text, skills_with_weights=None):
        """
        text: job description text
        skills_with_weights: optional list of dicts [{'name': 'Python', 'weight': 3}, ...]
        """
        self.text = text
        self.skills_with_weights = skills_with_weights or []
        self.skills = []

    def extract_skills_ai(self):
        """Use Gemini to extract required skills from job description text."""
        prompt = f"""
        Extract all required skills, programming languages, and tools
        from the following job description. Provide as a comma-separated list:

        {self.text}
        """
        skills_text = call_gemini(prompt)
        self.skills = [s.strip() for s in skills_text.split(",") if s.strip()]

        # If no weights were provided, default weight = 1
        if not self.skills_with_weights:
            self.skills_with_weights = [{"name": s, "weight": 1} for s in self.skills]

        return self.skills

    def extract_education_ai(self):
        """Extract education requirements using Gemini AI."""
        prompt = f"""
        Extract required education details (degree, field of study) 
        from this job description. Return as JSON:
        [
        {{"degree": "BSc", "field": "Computer Science"}}
        ]
        Job Description:
        {self.text}
        """
        education_json = call_gemini(prompt)
        try:
            import json
            self.required_education = json.loads(education_json)
        except:
            self.required_education = []
        return self.required_education


