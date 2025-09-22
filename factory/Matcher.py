from factory.Resume import Resume
from factory.JobDescription import JobDescription

class Matcher:
    def __init__(self, resume: Resume, job: JobDescription):
        self.resume = resume
        self.job = job

    def compute_match_score(self):
        resume_skills = set(self.resume.skills)
        job_skills = set(self.job.required_skills)
        if not job_skills:
            return 0
        matched = resume_skills.intersection(job_skills)
        score = len(matched) / len(job_skills) * 100
        return round(score, 2)

    def missing_skills(self):
        return list(set(self.job.required_skills) - set(self.resume.skills))

    def report(self):
        return {
            "match_score": self.compute_match_score(),
            "missing_skills": self.missing_skills()
        }
