from .managers import get_synonyms, normalize_skill, fuzzy_match

class MatchFactory:
    def __init__(self, resume_skills, job_skills_with_weights):
        # Normalize resume skills
        self.resume_skills = [normalize_skill(s) for s in resume_skills]
        # Job skills: {'skill_name': weight}
        self.job_skills = {normalize_skill(s["name"]): s["weight"] for s in job_skills_with_weights}

    def match(self):
        matched = []
        total_score, max_score = 0, 0

        for job_skill, weight in self.job_skills.items():
            # Expand job skill with synonyms
            expanded_job = get_synonyms(job_skill)
            expanded_job.add(job_skill)

            max_score += weight

            for resume_skill in self.resume_skills:
                expanded_resume = get_synonyms(resume_skill)
                expanded_resume.add(resume_skill)

                # Exact or synonym match
                if resume_skill in expanded_job or job_skill in expanded_resume:
                    matched.append(job_skill)
                    total_score += weight
                    break

                # Fuzzy match
                if fuzzy_match(resume_skill, job_skill):
                    matched.append(job_skill + " (fuzzy)")
                    total_score += weight * 0.8
                    break

        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        return {
            "matched_skills": matched,
            "score": round(percentage, 2)
        }
