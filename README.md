# ResumeXpert📃
## Overview🔎

This project is designed to simplify the job application process by matching your pre-saved resumes to job postings and generating cold emails tailored to the job role. Built using LangChain, ChromaDB, and Streamlit, this tool helps identify the best-aligned resume and provides insights into the ATS (Applicant Tracking System) score for your profile.

## Problem Statement📜
Applying for jobs often requires customizing resumes to align with the specific requirements of each job posting. With multiple openings having different skills and experience requirements, using a single, generic resume can reduce the chances of success. Manually tailoring resumes for each application is time-consuming, and understanding how well your profile aligns with the role can be challenging. Additionally, the lack of personalized communication, such as a tailored cold email, can hinder effective outreach to recruiters.

## Features😪

1. Resume Matching: Matches your pre-saved resumes (with different tech stacks) to the job posting.

2. ATS Score Calculation: Calculates the percentage match between your skills and the job requirements.

3. Key Skill Identification: Extracts and highlights the essential skills required for the job.

4. Cold Email Generation: Generates a tailored cold email to introduce yourself and express interest in the role.

5. Streamlit Deployment: Provides an interactive web interface for uploading job descriptions and viewing results.

## Live Demo
https://resume-xpert.streamlit.app/
## Technology Stack🤖

LangChain🦜: For NLP-based document processing and skill extraction.

ChromaDB🧠: As a vector database for efficient resume-job matching.

Streamlit⚡: For building an easy-to-use web interface.

## Installation📩

### Clone the repository:
Using git clone 

### Install the required dependencies:
pip install -r requirements.txt

### Run the application:
streamlit run app.py

## Structure 


![workflow_with_ats](https://github.com/user-attachments/assets/092ba36a-fe35-45e6-970f-69556a4ca0c0)



## Interface

![Screenshot 2025-01-04 211531](https://github.com/user-attachments/assets/b14bf6a9-0f89-48ca-bb0b-1ec5bb85deef)

