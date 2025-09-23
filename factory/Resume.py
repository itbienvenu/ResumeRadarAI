from .managers import call_gemini
import pdfplumber

class Resume:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self._extract_text()
        self.skills = []
        self.education = []
        self.experience = []
        self.certifications = []
        self.projects = []

    def _extract_text(self):
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def extract_skills_ai(self):
        prompt = f"""
        Extract all technical skills, programming languages, tools, and certifications
        from the following resume text. Provide as a comma-separated list:

        {self.text}
        """
        skills_text = call_gemini(prompt)
        self.skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        return self.skills

    def extract_education_ai(self):
        prompt = f"""
        Extract all education details (degree, field of study, institution, graduation year if available)
        from the following resume text.
        Return each entry on a separate line in this format:
        Degree: <degree>, Field: <field>, Institution: <institution>, Year: <year>

        Resume:
        {self.text}
        """
        education_text = call_gemini(prompt)
        education = []
        for line in education_text.split("\n"):
            if "Degree:" in line:
                parts = line.split(",")
                edu = {}
                for part in parts:
                    key, _, value = part.partition(":")
                    edu[key.strip().lower()] = value.strip()
                education.append(edu)
        self.education = education
        return self.education

    def extract_experience_ai(self):
        prompt = f"""
        Extract all work experience entries from the following resume text.
        Each entry format:
        Title: <job title>, Company: <company>, Start: <start date>, End: <end date>, Responsibilities: <comma-separated tasks>

        Resume:
        {self.text}
        """
        exp_text = call_gemini(prompt)
        experience = []
        for line in exp_text.split("\n"):
            if "Title:" in line:
                parts = line.split(",")
                job = {}
                for part in parts:
                    key, _, value = part.partition(":")
                    job[key.strip().lower()] = value.strip()
                experience.append(job)
        self.experience = experience
        return self.experience

    def extract_certifications_ai(self):
        prompt = f"""
        Extract all professional certifications from the following resume.
        Provide a comma-separated list:

        {self.text}
        """
        certs_text = call_gemini(prompt)
        self.certifications = [c.strip() for c in certs_text.split(",") if c.strip()]
        return self.certifications

    def extract_projects_ai(self):
        prompt = f"""
        Extract all projects from the following resume text.
        Provide title and tech used in format:
        Title: <project title>, Tech: <comma-separated technologies>

        Resume:
        {self.text}
        """
        proj_text = call_gemini(prompt)
        projects = []
        for line in proj_text.split("\n"):
            if "Title:" in line:
                parts = line.split(",")
                proj = {}
                for part in parts:
                    key, _, value = part.partition(":")
                    proj[key.strip().lower()] = [t.strip() for t in value.split(",")] if key.strip().lower() == "tech" else value.strip()
                projects.append(proj)
        self.projects = projects
        return self.projects
