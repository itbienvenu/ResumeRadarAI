from factory.resume import Resume
from factory.job_description import JobDescription
from factory.matcher import SkillMatcher

# Load resume
resume = Resume("Resume.pdf")
resume.extract_skills_ai()

# Load job description
job_text = """
We are looking for a backend developer with experience in Python, FastAPI, SQL, 
AWS, and Docker.
"""
job = JobDescription(job_text)
job.extract_skills_ai()

# Match skills
matcher = SkillMatcher()
result = matcher.match(resume, job)

print("Resume Skills:", resume.skills)
print("Job Skills:", job.skills)
print("Matched Skills:", result['matched_skills'])
print("Match Score:", result['match_score'], "%")
