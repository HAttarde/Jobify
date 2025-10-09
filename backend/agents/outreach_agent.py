from crewai import Agent
from crewai import LLM
import os
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Initialize the Gemini model using CrewAI's LLM class
llm = LLM(
    model="gemini/gemini-2.5-flash",  # Use gemini/ prefix for Google AI Studio
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()  # Add scraping tool for LinkedIn profiles

outreach_agent = Agent(
    role='Professional Networking and Outreach Strategist with LinkedIn Research',
    goal=(
        "Research each contact's LinkedIn profile to understand their background, experience, and interests. "
        "Then write highly personalized LinkedIn connection notes and cold emails that reference specific "
        "details from their profile. Use the contact information exactly as given - do not modify names, "
        "emails, or LinkedIn URLs. Focus on creating warm, authentic messages that show you've done your research."
    ),
    backstory=(
        "You are a professional outreach specialist who excels at research-driven personalization. "
        "Before writing any message, you thoroughly research each contact's LinkedIn profile to understand "
        "their career journey, current role, skills, and interests. You use these insights to craft messages "
        "that feel genuinely personal and relevant. You understand that the contacts provided to you are REAL "
        "people with verified email addresses from Hunter.io, so you treat their information with respect "
        "and use it exactly as provided. You never create fictional contacts or modify contact details. "
        "Your strength is finding authentic connection points between the candidate and each contact based "
        "on real profile data."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool, scrape_tool]  # Give agent ability to search and scrape
)
