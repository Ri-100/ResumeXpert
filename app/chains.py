import os
import sys
import uuid
import pandas as pd
import chromadb
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore1')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

class Chain:
    def __init__(self):
        # Initialize ChatGroq with Groq API Key and Model details
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=st.secrets["GROQ_API_KEY"],
            model_name="llama-3.3-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):
        # Template to extract job details
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
            # Get the extracted response in JSON format
            res = chain_extract.invoke(input={"page_data": cleaned_text})
            json_parser = JsonOutputParser()
            return json_parser.parse(res.content)
        except OutputParserException as e:
            raise Exception(f"Error extracting jobs: {str(e)}")

    def calculate_match_score(self, job_skills, resume_skills):
        # Calculate match score based on skill overlap between job and resume
        job_skills_set = set(skill.lower() for skill in job_skills)
        resume_skills_set = set(skill.lower() for skill in resume_skills)
        common_skills = job_skills_set.intersection(resume_skills_set)
        total_skills = job_skills_set.union(resume_skills_set)
        return (len(common_skills) / len(total_skills)) * 100 if total_skills else 0

    def write_mail(self, job, links):
        # Generate personalized cold email for job application
        prompt_email = PromptTemplate.from_template(
            """
            ### INSTRUCTION:
            You are Rishav Shukla, a final-year Computer Science student specializing in Data Science and seeking job opportunities.
            Write a cold email tailored to the job requirements.
            Highlight relevant skills, projects, and experiences aligning with the job, and present yourself as an eager candidate ready to contribute and grow.
            Use the most relevant resume link provided that matches with the job role: {link_list}.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        return chain_email.invoke({"job_description": str(job), "link_list": links}).content


