class MatchFactory:
    def __init__(self, weights=None):
        # Default weights for components
        self.weights = weights or {
            "skills": 0.5,
            "education": 0.2,
            "experience": 0.2,
            "certifications": 0.05,
            "projects": 0.05
        }

    def match_skills(self, resume, job):
        matched = []
        total_weight = sum([s['weight'] for s in job.skills_with_weights])
        score = 0
        for r_skill in resume.skills:
            for j_skill in job.skills_with_weights:
                if r_skill.lower() == j_skill['name'].lower():
                    matched.append(r_skill)
                    score += j_skill['weight']
        match_score = (score / total_weight * 100) if total_weight else 0
        return matched, match_score

    def match_list(self, resume_list, job_list, key=None):
        matched = []
        for item in job_list:
            if key:
                # Extract value for comparison from item
                item_val = item.get(key, "") if isinstance(item, dict) else str(item)
                for r in resume_list:
                    r_val = r.get(key, "") if isinstance(r, dict) else str(r)
                    if item_val.lower() in r_val.lower():
                        matched.append(item)
                        break
            else:
                item_val = str(item)
                if any(item_val.lower() in (str(r).lower() if not isinstance(r, dict) else "") for r in resume_list):
                    matched.append(item)
        match_score = (len(matched)/len(job_list)*100) if job_list else 0
        return matched, match_score

    def match_projects(self, resume_projects, job_projects):
        matched = []
        for j_proj in job_projects:
            for r_proj in resume_projects:
                # Match if title matches and at least 1 tech matches
                if j_proj['title'].lower() in r_proj['title'].lower() and \
                   any(tech.lower() in [t.lower() for t in r_proj.get('tech', [])] for tech in j_proj.get('tech', [])):
                    matched.append(j_proj['title'])
        match_score = (len(matched)/len(job_projects)*100) if job_projects else 0
        return matched, match_score

    def match(self, resume, job):
        results = {}
        # Skills
        results['matched_skills'], results['skills_score'] = self.match_skills(resume, job)
        # Education
        results['matched_education'], results['education_score'] = self.match_list(resume.education, job.education_required, key="degree")
        # Experience
        results['matched_experience'], results['experience_score'] = self.match_list(resume.experience, job.experience_required, key="title")
        # Certifications
        results['matched_certifications'], results['certifications_score'] = self.match_list(resume.certifications, job.certifications_required)
        # Projects
        results['matched_projects'], results['projects_score'] = self.match_projects(resume.projects, job.projects_required)

        # Final fit score
        results['fit_score'] = sum(results[f"{k}_score"] * self.weights.get(k,0) for k in ["skills","education","experience","certifications","projects"])
        return results
