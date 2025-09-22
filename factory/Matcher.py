class SkillMatcher:
    @staticmethod
    def match(resume, job_description):
        """Compare resume skills with job description skills."""
        resume_skills = set([s.lower() for s in resume.skills])
        job_skills = set([s.lower() for s in job_description.skills])

        matched = resume_skills.intersection(job_skills)
        match_score = len(matched) / len(job_skills) * 100 if job_skills else 0

        return {
            "matched_skills": list(matched),
            "match_score": round(match_score, 2)
        }
