import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from typing import Dict, List, Any, Optional
from datetime import datetime

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
def analyze_company_pain_points(website_research: str) -> str:
    """Analyze company research to identify specific pain points and challenges."""
    pain_points = []
    
    # Look for common business challenges
    if "manual" in website_research.lower() or "spreadsheet" in website_research.lower():
        pain_points.append("Manual data processing and spreadsheet management")
    
    if "growth" in website_research.lower() or "scale" in website_research.lower():
        pain_points.append("Scaling data infrastructure for business growth")
    
    if "insights" in website_research.lower() or "visibility" in website_research.lower():
        pain_points.append("Lack of real-time business insights")
    
    if "efficiency" in website_research.lower() or "productivity" in website_research.lower():
        pain_points.append("Operational inefficiencies in data workflows")
    
    if "cost" in website_research.lower() or "budget" in website_research.lower():
        pain_points.append("High costs of maintaining current data systems")
    
    return f"Identified Pain Points:\n" + "\n".join([f"- {point}" for point in pain_points]) if pain_points else "Pain Points: General business optimization opportunities"

@function_tool
def identify_solution_benefits(company_research: str, person_role: str) -> str:
    """Identify specific benefits of data analytics solutions for this company and person."""
    benefits = []
    
    # Role-specific benefits
    if "analyst" in person_role.lower():
        benefits.append("Automate repetitive data tasks to focus on strategic analysis")
        benefits.append("Advanced visualization tools for better stakeholder communication")
    
    if "manager" in person_role.lower() or "director" in person_role.lower():
        benefits.append("Real-time dashboards for better decision making")
        benefits.append("Streamlined reporting processes for team efficiency")
    
    if "executive" in person_role.lower() or "ceo" in person_role.lower():
        benefits.append("Strategic insights for business growth and competitive advantage")
        benefits.append("Data-driven decision making at the executive level")
    
    # Company-specific benefits
    if "startup" in company_research.lower():
        benefits.append("Scalable data infrastructure that grows with your business")
        benefits.append("Cost-effective solutions for early-stage companies")
    
    if "enterprise" in company_research.lower():
        benefits.append("Enterprise-grade security and compliance")
        benefits.append("Integration with existing enterprise systems")
    
    return f"Solution Benefits:\n" + "\n".join([f"- {benefit}" for benefit in benefits])

@function_tool
def craft_personalized_greeting(person_name: str, person_role: str, company_name: str) -> str:
    """Craft a personalized greeting based on the person's role and company."""
    if "ceo" in person_role.lower() or "founder" in person_role.lower():
        greeting = f"Dear {person_name},"
    elif "director" in person_role.lower() or "vp" in person_role.lower():
        greeting = f"Dear {person_name},"
    elif "manager" in person_role.lower() or "lead" in person_role.lower():
        greeting = f"Dear {person_name},"
    else:
        greeting = f"Hi {person_name},"
    
    return greeting

@function_tool
def generate_value_proposition(company_name: str, pain_points: str, person_role: str) -> str:
    """Generate a compelling value proposition for data analytics services."""
    value_prop = f"""
Based on my research of {company_name}, I believe we can help you address several key challenges:

{pain_points}

Our data analytics solutions are specifically designed to help companies like {company_name}:
• Streamline data workflows and eliminate manual processes
• Gain real-time insights for better decision making
• Scale data infrastructure efficiently as you grow
• Reduce operational costs while improving productivity

Given your role as {person_role}, I think you'd find particular value in our approach to data-driven business intelligence.
"""
    return value_prop

@function_tool
def create_call_to_action(person_name: str, company_name: str) -> str:
    """Create a compelling call to action for the email."""
    cta = f"""
Would you be interested in a brief 15-minute conversation about how we can help {company_name} leverage data more effectively? 

I'd love to share some specific examples of how we've helped similar companies and discuss whether there might be a fit for collaboration.

What would work best for you - a quick call this week, or would you prefer to schedule something for next week?

Best regards,
[Your Name]
[Your Company]
[Your Contact Information]
"""
    return cta

# Email Generation Agent
email_generation_agent = Agent(
    name="EmailGenerationAgent",
    instructions="""You are a specialized agent for generating personalized email pitches for data analytics services. 
    Your job is to create compelling, professional emails that are tailored to the specific company and person.
    
    When generating an email:
    1. Analyze company research to identify pain points
    2. Identify specific benefits relevant to the person's role
    3. Craft a personalized greeting and value proposition
    4. Create a compelling call to action
    5. Ensure the email is professional, concise, and personalized
    
    Focus on creating emails that feel genuine and address real business needs.
    Always be respectful and professional in tone.""",
    model=llm_model,
    tools=[analyze_company_pain_points, identify_solution_benefits, craft_personalized_greeting, generate_value_proposition, create_call_to_action]
)

def generate_email_pitch(person_name: str, company_name: str, person_role: str, website_research: str, linkedin_research: str) -> str:
    """Generate a personalized email pitch based on research findings."""
    
    query = f"""
    Please generate a personalized email pitch for {person_name} at {company_name}.
    
    Person's Role: {person_role}
    Company Research: {website_research}
    LinkedIn Research: {linkedin_research}
    
    Please:
    1. Analyze the company research to identify pain points
    2. Identify specific benefits relevant to the person's role
    3. Craft a personalized greeting and value proposition
    4. Create a compelling call to action
    5. Generate a complete, professional email
    
    The email should be for data analytics services and feel genuinely personalized to this company and person.
    Keep it professional, concise, and focused on business value.
    """
    
    result = Runner.run_sync(email_generation_agent, query)
    return result

if __name__ == "__main__":
    # Example usage
    print("=== Email Generation Agent ===")
    print("Generating email pitch for: John Smith at TechCorp Inc.")
    print("-" * 50)
    
    sample_website_research = """
    TechCorp Inc. is a growing technology company with 50+ employees.
    They currently use manual processes and spreadsheets for data management.
    The company is looking to scale their operations and improve efficiency.
    """
    
    sample_linkedin_research = """
    John Smith is a Senior Data Analyst with 5+ years of experience.
    He uses Python, SQL, and Tableau for data analysis.
    He's open to networking opportunities and professional development.
    """
    
    result = generate_email_pitch(
        "John Smith", 
        "TechCorp Inc.", 
        "Senior Data Analyst",
        sample_website_research,
        sample_linkedin_research
    )
    print(result)
