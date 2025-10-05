from crewai import Agent
from crewai import LLM
import os
from crewai_tools import SerperDevTool

# Initialize the Gemini model using CrewAI's LLM class
llm = LLM(
    model="gemini/gemini-2.5-flash",  # Use gemini/ prefix for Google AI Studio
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

search_tool = SerperDevTool()

outreach_agent = Agent(
    role='Professional Networking and Outreach Strategist',
    goal=(
        "Write highly personalized LinkedIn connection notes and cold emails for the EXACT contacts provided. "
        "Use the contact information exactly as given - do not modify names, emails, or LinkedIn URLs. "
        "Focus on creating warm, authentic messages that connect the candidate's experience to each contact's role."
    ),
     backstory=(
        "You are a professional outreach specialist who excels at writing personalized, genuine messages. "
        "You understand that the contacts provided to you are REAL people with verified email addresses "
        "from Hunter.io, so you treat their information with respect and use it exactly as provided. "
        "You never create fictional contacts or modify contact details. Your strength is crafting messages "
        "that feel personal and authentic, making recipients want to respond positively."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool]  # Give agent ability to search
)