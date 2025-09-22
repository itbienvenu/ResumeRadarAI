from factory.resume import Resume
from factory.job_description import JobDescription
from factory.matcher import MatchFactory

# --------------------------
# Step 1: Load Resume
# --------------------------
resume = Resume("Resume.pdf")
resume.extract_skills_ai()  # Gemini extracts skills dynamically

# --------------------------
# Step 2: Load Job Description
# --------------------------
job_text = """
We are looking for a backend developer with experience in Python, FastAPI, SQL, 
AWS, and Docker.
"""
# Include weights for each skill
job_skills_with_weights = [
    {"name": "Python", "weight": 3},
    {"name": "FastAPI", "weight": 3},
    {"name": "SQL", "weight": 2},
    {"name": "AWS", "weight": 2},
    {"name": "Docker", "weight": 2}
]

job = JobDescription(job_text, job_skills_with_weights)
job.extract_skills_ai()  # Gemini extracts skills dynamically from job description

# --------------------------
# Step 3: Match Skills
# --------------------------
matcher = MatchFactory(resume.skills, job.skills_with_weights)
result = matcher.match()  # MatchFactory now uses dynamic synonyms

# --------------------------
# Step 4: Show Results
# --------------------------
print("Resume Skills:", resume.skills)
print("Job Skills:", [s["name"] for s in job.skills_with_weights])
print("Matched Skills:", result['matched_skills'])
print("Match Score:", result['score'], "%")
