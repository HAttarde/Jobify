from crewai import Agent
from crewai import LLM
import os

# Initialize the Gemini model using CrewAI's LLM class
llm = LLM(
    model="gemini/gemini-2.5-flash",  # Use gemini/ prefix for Google AI Studio
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

resume_tailoring_agent = Agent(
    role='Resume and Cover Letter Specialist',
    goal='Tailor resumes and generate compelling cover letters based on job descriptions.',
    backstory=(
        "You are an expert career coach with a specialization in resume optimization and"
        " compelling storytelling. You know how to highlight the most relevant skills and"
        " experiences to catch a recruiter's eye and pass through applicant tracking systems."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)