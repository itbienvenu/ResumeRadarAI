# factory/matcher.py
from fuzzywuzzy import fuzz

# Define degree synonyms for matching education degrees
DEGREE_SYNONYMS = {
    "bachelor": ["bachelor", "b.sc", "b.s.", "b.a", "b.a.", "undergraduate"],
    "master": ["master", "m.sc", "m.s.", "m.a", "m.a.", "graduate"],
    "phd": ["phd", "ph.d", "doctorate", "doctoral"],
    "associate": ["associate", "a.a.", "a.s."],
    # Add more synonyms as needed
}

class MatchFactory:
    def match(self, resume, job):
        result = {}

        # Skills
        matched_skills = [s for s in resume.skills if s.lower() in [j.lower() for j in job.skills]]
        skills_score = round(len(matched_skills)/len(job.skills)*100, 2) if job.skills else 0
        result['matched_skills'] = matched_skills
        result['skills_score'] = skills_score

        # Education
        matched_edu = []
        for j_edu in job.education_required:
            for r_edu in resume.education:
                for syn in DEGREE_SYNONYMS.get(j_edu['degree'].lower(), [j_edu['degree'].lower()]):
                    if fuzz.partial_ratio(syn, r_edu['degree'].lower()) > 80:
                        matched_edu.append(r_edu)
        edu_score = round(len(matched_edu)/len(job.education_required)*100, 2) if job.education_required else 0
        result['matched_education'] = matched_edu
        result['education_score'] = edu_score

        # Experience
        matched_exp = []
        total_exp_score = 0
        for j_exp in job.experience_required:
            for r_exp in resume.experience:
                if j_exp['title'].lower() in r_exp['title'].lower():
                    matched_exp.append(r_exp)
                    # Safely cast years to int, default to 1 if missing or invalid
                    try:
                        r_years = int(r_exp.get('years', 1))
                    except (ValueError, TypeError, AttributeError):
                        r_years = 1
                    try:
                        j_years = int(j_exp.get('years', 1))
                    except (ValueError, TypeError, AttributeError):
                        j_years = 1
                    total_exp_score += min(r_years, j_years) / max(1, j_years)
        exp_score = round((total_exp_score / int(max(1, len(job.experience_required)))) * 100, 2) if job.experience_required else 0
        result['matched_experience'] = matched_exp
        result['experience_score'] = exp_score

        # Certifications
        matched_cert = [c for c in resume.certifications if c.lower() in [j.lower() for j in job.certifications_required]]
        cert_score = round(len(matched_cert)/len(job.certifications_required)*100, 2) if job.certifications_required else 0
        result['matched_certifications'] = matched_cert
        result['certifications_score'] = cert_score

        # Projects
        matched_proj = [p for p in resume.projects if any(j.lower() in p['title'].lower() for j in job.projects_required)]
        proj_score = round(len(matched_proj)/len(job.projects_required)*100, 2) if job.projects_required else 0
        result['matched_projects'] = matched_proj
        result['projects_score'] = proj_score

        # Overall fit
        overall = (skills_score + edu_score + exp_score + cert_score + proj_score)/5
        result['fit_score'] = round(overall, 2)

        return result
