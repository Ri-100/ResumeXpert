import os
import sys
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=st.secrets["GROQ_API_KEY"],
            model_name="llama-3.2-11b-vision-preview"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
                        """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        try:
            res = chain_extract.invoke(input={"page_data": cleaned_text})
            json_parser = JsonOutputParser()
            return json_parser.parse(res.content)
        except OutputParserException as e:
            raise Exception(f"Error extracting jobs: {str(e)}")

    def calculate_match_score(self, job_skills, resume_skills):
        job_skills_set = set(skill.lower() for skill in job_skills)
        resume_skills_set = set(skill.lower() for skill in resume_skills)
        common_skills = job_skills_set.intersection(resume_skills_set)
        total_skills = job_skills_set.union(resume_skills_set)
        return (len(common_skills) / len(total_skills)) * 100 if total_skills else 0

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### INSTRUCTION:
            You are Rishav Shukla, a final-year Computer Science student specializing in Data Science and seeking job opportunities.
            Write a cold email tailored to the job requirements.
            Highlight relevant skills, projects, and experiences aligning with the job, and present yourself as an eager candidate ready to contribute and grow.
            Use the most relevant resume link   provided that macthes with the job role: {link_list}.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        return chain_email.invoke({"job_description": str(job), "link_list": links}).content
