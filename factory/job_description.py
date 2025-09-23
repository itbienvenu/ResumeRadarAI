from factory.managers import call_gemini

class JobDescription:
    def __init__(self, text, skills_with_weights=None, education_required=None, experience_required=None,
                 certifications_required=None, projects_required=None):
        self.text = text
        self.skills_with_weights = skills_with_weights or []
        self.skills = []
        self.education_required = education_required or []
        self.experience_required = experience_required or []
        self.certifications_required = certifications_required or []
        self.projects_required = projects_required or []

    def extract_skills_ai(self):
        prompt = f"""
        Extract required skills from the following job description.
        Provide comma-separated list:

        {self.text}
        """
        skills_text = call_gemini(prompt)
        self.skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        if not self.skills_with_weights:
            self.skills_with_weights = [{"name": s, "weight": 1} for s in self.skills]
        return self.skills

    def extract_education_ai(self):
        prompt = f"""
        Extract education requirements from the following job description.
        Return comma-separated degrees:

        {self.text}
        """
        edu_text = call_gemini(prompt)
        self.education_required = list(set([e.strip() for e in edu_text.split(",") if e.strip()] + self.education_required))
        return self.education_required

    def extract_experience_ai(self):
        prompt = f"""
        Extract required work experience from the following job description.
        Each line: Title: <title>, Years: <min years>, Skills: <comma-separated required skills>

        Job Description:
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
        self.experience_required = experience
        return self.experience_required

    def extract_certifications_ai(self):
        prompt = f"""
        Extract required certifications from the following job description.
        Provide a comma-separated list:

        {self.text}
        """
        cert_text = call_gemini(prompt)
        self.certifications_required = [c.strip() for c in cert_text.split(",") if c.strip()]
        return self.certifications_required

    def extract_projects_ai(self):
        prompt = f"""
        Extract project requirements from the following job description.
        Format: Title: <project title>, Tech: <comma-separated technologies>

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
        self.projects_required = projects
        return self.projects_required
