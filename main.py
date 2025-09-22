from factory.resume import Resume
from factory.job_description import JobDescription
from factory.matcher import MatchFactory
from factory.file_auth import FileAuth
from factory.managers import get_real_dir

auth = FileAuth(max_size_mb=4, allowed_types=['text/plain', 'application/pdf'])
file_path = get_real_dir("managers.py")

try:
    auth.validate_file(file_path)
    resume = Resume("Resume.pdf")
    resume.extract_skills_ai()  

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
    job.extract_skills_ai()  


    matcher = MatchFactory(resume.skills, job.skills_with_weights)
    result = matcher.match()  # MatchFactory now uses dynamic synonyms


    print("Resume Skills:", resume.skills)
    print("Job Skills:", [s["name"] for s in job.skills_with_weights])
    print("Matched Skills:", result['matched_skills'])
    print("Match Score:", result['score'], "%")

except ValueError as e:
    print("File validation failed:", e)

