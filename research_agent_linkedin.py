import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from typing import Dict, List, Any, Optional
import re

# Load environment variables
load_dotenv(find_dotenv())

# Get API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Configure OpenAI client
openai_client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url="https://api.openai.com/v1"
)

# LLM Model
llm_model = OpenAIChatCompletionsModel(
    model="gpt-4",
    openai_client=openai_client
)

@function_tool
def extract_professional_role(profile_text: str) -> str:
    """Extract the person's current professional role and title from LinkedIn profile."""
    # This would parse actual LinkedIn profile data
    # For now, returning structured information
    if "data" in profile_text.lower() and "analyst" in profile_text.lower():
        role = "Data Analyst"
    elif "data" in profile_text.lower() and "scientist" in profile_text.lower():
        role = "Data Scientist"
    elif "data" in profile_text.lower() and "engineer" in profile_text.lower():
        role = "Data Engineer"
    elif "manager" in profile_text.lower() and "data" in profile_text.lower():
        role = "Data Manager"
    else:
        role = "Professional (role to be determined)"
    
    return f"Current Role: {role}"

@function_tool
def analyze_experience_level(profile_text: str) -> str:
    """Analyze the person's experience level and career progression."""
    # Look for experience indicators
    experience_level = "Mid-level"
    
    if "senior" in profile_text.lower() or "lead" in profile_text.lower():
        experience_level = "Senior/Lead"
    elif "junior" in profile_text.lower() or "entry" in profile_text.lower():
        experience_level = "Junior/Entry"
    elif "director" in profile_text.lower() or "vp" in profile_text.lower():
        experience_level = "Director/VP level"
    elif "ceo" in profile_text.lower() or "founder" in profile_text.lower():
        experience_level = "Executive/Founder"
    
    return f"Experience Level: {experience_level}"

@function_tool
def identify_technical_skills(profile_text: str) -> str:
    """Identify technical skills and tools mentioned in the profile."""
    # Common data analytics skills to look for
    skills = []
    
    # Programming languages
    if "python" in profile_text.lower():
        skills.append("Python")
    if "r" in profile_text.lower():
        skills.append("R")
    if "sql" in profile_text.lower():
        skills.append("SQL")
    if "java" in profile_text.lower():
        skills.append("Java")
    
    # Tools and platforms
    if "tableau" in profile_text.lower():
        skills.append("Tableau")
    if "power bi" in profile_text.lower():
        skills.append("Power BI")
    if "excel" in profile_text.lower():
        skills.append("Excel")
    if "aws" in profile_text.lower():
        skills.append("AWS")
    if "azure" in profile_text.lower():
        skills.append("Azure")
    if "snowflake" in profile_text.lower():
        skills.append("Snowflake")
    
    # Methodologies
    if "machine learning" in profile_text.lower():
        skills.append("Machine Learning")
    if "statistics" in profile_text.lower():
        skills.append("Statistics")
    if "data visualization" in profile_text.lower():
        skills.append("Data Visualization")
    
    return f"Technical Skills:\n" + "\n".join([f"- {skill}" for skill in skills]) if skills else "Skills: General business/analytics background"

@function_tool
def assess_decision_making_power(profile_text: str) -> str:
    """Assess the person's decision-making power and influence in the organization."""
    decision_power = "Medium"
    
    if any(word in profile_text.lower() for word in ["ceo", "founder", "president", "director", "vp"]):
        decision_power = "High - Executive level"
    elif any(word in profile_text.lower() for word in ["manager", "lead", "senior"]):
        decision_power = "Medium-High - Management level"
    elif any(word in profile_text.lower() for word in ["analyst", "specialist", "coordinator"]):
        decision_power = "Medium - Individual contributor"
    elif any(word in profile_text.lower() for word in ["intern", "junior", "associate"]):
        decision_power = "Low - Junior level"
    
    return f"Decision Making Power: {decision_power}"

@function_tool
def extract_contact_preferences(profile_text: str) -> str:
    """Extract contact preferences and communication style indicators."""
    contact_prefs = []
    
    if "open to" in profile_text.lower() and "opportunities" in profile_text.lower():
        contact_prefs.append("Open to new opportunities")
    
    if "networking" in profile_text.lower() or "connect" in profile_text.lower():
        contact_prefs.append("Active networker")
    
    if "speaking" in profile_text.lower() or "conference" in profile_text.lower():
        contact_prefs.append("Public speaker/thought leader")
    
    if "mentor" in profile_text.lower():
        contact_prefs.append("Mentoring mindset")
    
    return f"Contact Preferences:\n" + "\n".join([f"- {pref}" for pref in contact_prefs]) if contact_prefs else "Contact Preferences: Standard professional approach recommended"

# LinkedIn Research Agent
linkedin_research_agent = Agent(
    name="LinkedInResearchAgent",
    instructions="""You are a specialized agent for researching LinkedIn profiles. 
    Your job is to extract professional information that helps understand the person's role, 
    decision-making power, and how to approach them for business opportunities.
    
    When researching a LinkedIn profile:
    1. Extract their current professional role and title
    2. Analyze their experience level and career progression
    3. Identify technical skills and tools they use
    4. Assess their decision-making power in the organization
    5. Extract contact preferences and communication style
    
    Focus on information that helps determine the best approach for pitching data analytics services.
    Be professional and respectful in your analysis.""",
    model=llm_model,
    tools=[extract_professional_role, analyze_experience_level, identify_technical_skills, assess_decision_making_power, extract_contact_preferences]
)

def research_linkedin_profile(person_name: str, company_name: str, profile_data: str = None) -> str:
    """Research a person's LinkedIn profile comprehensively."""
    
    if profile_data is None:
        profile_data = f"Sample profile data for {person_name} at {company_name}"
    
    query = f"""
    Please research the LinkedIn profile for {person_name} at {company_name}.
    
    Profile data: {profile_data}
    
    Please:
    1. Extract their current professional role and title
    2. Analyze their experience level and career progression
    3. Identify technical skills and tools they use
    4. Assess their decision-making power in the organization
    5. Extract contact preferences and communication style
    
    Provide a comprehensive analysis that helps understand how to best approach this person 
    for data analytics services opportunities.
    """
    
    result = Runner.run_sync(linkedin_research_agent, query)
    return result

if __name__ == "__main__":
    # Example usage
    print("=== LinkedIn Research Agent ===")
    print("Researching: John Smith at TechCorp Inc.")
    print("-" * 50)
    
    sample_profile = """
    John Smith
    Senior Data Analyst at TechCorp Inc.
    Experience: 5+ years in data analytics
    Skills: Python, SQL, Tableau, Power BI
    Open to networking opportunities
    """
    
    result = research_linkedin_profile("John Smith", "TechCorp Inc.", sample_profile)
    print(result)
