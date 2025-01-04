import streamlit as st
from main import generate_ats_score, generate_cold_mail
from chains import Chain
from portfolio import Portfolio
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
def main():
    st.title("📃 ResumeXpert")
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Choose an Option:", ["Generate ATS Score", "Cold Mail Generator"])

    # User input for resume skills
    resume_skills = st.sidebar.text_area(
        "Enter Your Skills (comma-separated):",
        value="Python, C++, SQL, Machine Learning, Deep Learning, Power BI"
    )
    resume_skills = [skill.strip() for skill in resume_skills.split(",")]

    job_url = st.text_input("Enter a Job Posting URL:", value="")

    # Initialize Chain and Portfolio
    llm = Chain()
    portfolio = Portfolio()

    if options == "Generate ATS Score":
        if st.button("Generate ATS Score"):
            try:
                scores = generate_ats_score(llm, resume_skills, job_url)
                for score in scores:
                    st.write(f"**Role:** {score['role']}")
                    st.write(f"**ATS Score:** {score['ats_score']:.2f}%")
                    st.write(f"**Required Skills:** {', '.join(score['skills'])}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif options == "Cold Mail Generator":
        if st.button("Generate Cold Mail"):
            try:
                emails = generate_cold_mail(llm, portfolio, job_url)
                for email in emails:
                    st.subheader(f"Cold Email for Role: {email['role']}")
                    st.code(email["email"], language="markdown")
            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="ResumeXpert", page_icon="📃")
    main()
