from factory.resume import Resume
from factory.job_description import JobDescription
from factory.matcher import MatchFactory

resume = Resume("Resume.pdf")
resume.extract_skills_ai()
resume.extract_education_ai()
resume.extract_experience_ai()
resume.extract_certifications_ai()
resume.extract_projects_ai()

job_text = """
We are looking for a backend developer with:
- Experience in Python, FastAPI, SQL, AWS, Docker
- Bachelor's degree in Computer Science or related field
- Certifications: AWS Solutions Architect
- Projects: E-commerce platform using Python and FastAPI
"""

# Create job description object
job = JobDescription(job_text)
job.extract_skills_ai()
job.extract_education_ai()
job.extract_experience_ai()
job.extract_certifications_ai()
job.extract_projects_ai()

# Match resume vs job
matcher = MatchFactory()
result = matcher.match(resume, job)

# Display results
print("Resume Skills:", resume.skills)
print("Job Skills:", job.skills)
print("Matched Skills:", result['matched_skills'])
print("Skills Score:", result['skills_score'], "%\n")

print("Resume Education:", [e.get('degree') for e in resume.education])
print("Job Education:", job.education_required)
print("Matched Education:", result['matched_education'])
print("Education Score:", result['education_score'], "%\n")

print("Resume Experience:", [e.get('title') for e in resume.experience])
print("Job Experience:", [e.get('title') for e in job.experience_required])
print("Matched Experience:", result['matched_experience'])
print("Experience Score:", result['experience_score'], "%\n")

print("Resume Certifications:", resume.certifications)
print("Job Certifications:", job.certifications_required)
print("Matched Certifications:", result['matched_certifications'])
print("Certifications Score:", result['certifications_score'], "%\n")

print("Resume Projects:", [p.get('title') for p in resume.projects])
print("Job Projects:", [p.get('title') for p in job.projects_required])
print("Matched Projects:", result['matched_projects'])
print("Projects Score:", result['projects_score'], "%\n")

print("Overall Fit Score:", result['fit_score'], "%")

