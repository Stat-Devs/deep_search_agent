import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from typing import Dict, List, Any
import json

# Load environment variables
load_dotenv(find_dotenv())

# Get API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure OpenAI client
openai_client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url="https://api.openai.com/v1"
)

# Configure Gemini client
gemini_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# LLM Models
openai_model = OpenAIChatCompletionsModel(
    model="gpt-4",
    openai_client=openai_client
)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=gemini_client
)

@function_tool
def research_company_website(company_name: str, website_url: str = None) -> str:
    """Research a company's website to extract key information about their business, services, and needs."""
    # This would integrate with your web scraping tool (e.g., Trafilatura)
    # For now, returning a placeholder
    return f"Company: {company_name}\nWebsite Analysis: Business intelligence, data analytics needs identified. Company appears to be in growth phase with potential for data infrastructure improvements."

@function_tool
def research_linkedin_profile(person_name: str, company_name: str = None) -> str:
    """Research a person's LinkedIn profile to extract professional information and contact details."""
    # This would integrate with LinkedIn scraping tools
    # For now, returning a placeholder
    return f"Person: {person_name}\nRole: Data Analyst/Manager\nCompany: {company_name}\nExperience: 5+ years in data analytics\nInterests: Business intelligence, data visualization, analytics tools"

@function_tool
def generate_email_pitch(person_name: str, company_name: str, research_summary: str) -> str:
    """Generate a personalized email pitch for data analytics services based on research findings."""
    # This would use the research data to create a compelling pitch
    return f"Subject: Data Analytics Solutions for {company_name}\n\nDear {person_name},\n\nBased on my research of {company_name}, I believe we can help you optimize your data analytics infrastructure. Our services include business intelligence dashboards, data pipeline optimization, and advanced analytics solutions.\n\nWould you be interested in a brief discussion about how we can help {company_name} leverage data more effectively?\n\nBest regards,\n[Your Name]"

@function_tool
def compile_research_report(company_name: str, person_name: str, website_research: str, linkedin_research: str) -> str:
    """Compile all research findings into a comprehensive report."""
    report = f"""
# Lead Research Report: {company_name}

## Company Information
{website_research}

## Contact Person: {person_name}
{linkedin_research}

## Recommended Approach
Based on the research, this lead shows strong potential for data analytics services. 
The company appears to be in a growth phase and could benefit from improved data infrastructure.

## Next Steps
1. Send personalized email pitch
2. Follow up with specific case studies
3. Schedule discovery call
"""
    return report

# Main Lead Research Coordinator Agent
lead_research_coordinator = Agent(
    name="LeadResearchCoordinator",
    instructions="""You are a lead research coordinator for a data analytics services company. 
    Your job is to coordinate research activities and compile comprehensive lead intelligence.
    
    When given a lead, you should:
    1. Research the company website for business intelligence
    2. Research the person's LinkedIn profile for professional context
    3. Generate a personalized email pitch
    4. Compile everything into a comprehensive research report
    
    Always be thorough and professional in your research approach.""",
    model=openai_model,
    tools=[research_company_website, research_linkedin_profile, generate_email_pitch, compile_research_report]
)

# Example usage function
def research_lead(company_name: str, person_name: str, website_url: str = None):
    """Main function to research a lead comprehensively."""
    
    query = f"""
    Please research this lead comprehensively:
    Company: {company_name}
    Person: {person_name}
    Website: {website_url if website_url else 'Not provided'}
    
    Please:
    1. Research the company website
    2. Research the person's LinkedIn profile
    3. Generate a personalized email pitch
    4. Compile a comprehensive research report
    
    Provide all findings in a structured format.
    """
    
    result = Runner.run_sync(lead_research_coordinator, query)
    return result

if __name__ == "__main__":
    # Example usage
    print("=== Lead Research System ===")
    print("Researching lead: John Smith at TechCorp Inc.")
    print("-" * 50)
    
    result = research_lead("TechCorp Inc.", "John Smith", "https://techcorp.com")
    print(result)
