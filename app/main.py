from chains import Chain
from utils import clean_text

def generate_ats_score(llm, resume_skills, job_url):
    from langchain_community.document_loaders import WebBaseLoader

    try:
        loader = WebBaseLoader([job_url])
        data = clean_text(loader.load().pop().page_content)
        jobs = llm.extract_jobs(data)
        scores = [
            {
                "role": job.get("role", "Unknown Role"),
                "ats_score": llm.calculate_match_score(job.get("skills", []), resume_skills),
                "skills": job.get("skills", [])
            }
            for job in jobs
        ]
        return scores
    except Exception as e:
        raise Exception(f"Error generating ATS scores: {str(e)}")

def generate_cold_mail(llm, portfolio, job_url):
    from langchain_community.document_loaders import WebBaseLoader

    try:
        loader = WebBaseLoader([job_url])
        data = clean_text(loader.load().pop().page_content)
        portfolio.load_portfolio()
        jobs = llm.extract_jobs(data)
        emails = []
        for job in jobs:
            skills = job.get("skills", [])
            links = portfolio.query_links(skills)
            email = llm.write_mail(job, links)
            emails.append({"role": job.get("role", "Unknown Role"), "email": email})
        return emails
    except Exception as e:
        raise Exception(f"Error generating cold mail: {str(e)}")
