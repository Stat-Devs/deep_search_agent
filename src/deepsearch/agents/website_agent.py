import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
import requests
from urllib.parse import urljoin, urlparse
import re
from typing import Dict, List, Any, Optional

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

class WebsiteResearchAgent:
    """Agent for analyzing company websites and extracting business intelligence."""
    
    def __init__(self):
        self.agent = Agent(
            name="Website Research Agent",
            instructions="""You are a specialized agent for analyzing company websites and extracting business intelligence. 
            Your role is to:
            1. Scrape and analyze website content
            2. Identify company services and business focus
            3. Extract key company metrics and indicators
            4. Identify potential data analytics needs
            5. Provide actionable insights for sales opportunities
            
            Always provide structured, professional analysis with specific recommendations.""",
            model=llm_model,
            tools=[scrape_website_content, analyze_company_services, identify_company_needs, extract_company_metrics]
        )
    
    async def analyze_company_website(self, company_name: str, website_url: str) -> str:
        """Analyze a company website and provide comprehensive business intelligence."""
        try:
            prompt = f"""
            Analyze the website for {company_name} at {website_url}.
            
            Please provide a comprehensive analysis including:
            1. Company overview and business focus
            2. Key services and offerings
            3. Company size and scale indicators
            4. Industry positioning
            5. Potential data analytics needs and opportunities
            6. Sales intelligence insights
            
            Focus on identifying how data analytics solutions could benefit this company.
            """
            
            result = await Runner.run(self.agent, prompt)
            return result.final_output
            
        except Exception as e:
            return f"Error analyzing website: {str(e)}"
    
    def analyze_company_website_sync(self, company_name: str, website_url: str) -> str:
        """Synchronous version of website analysis."""
        import asyncio
        return asyncio.run(self.analyze_company_website(company_name, website_url))

@function_tool
def scrape_website_content(url: str) -> str:
    """Scrape and extract content from a company website."""
    try:
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_content = ' '.join(chunk for chunk in chunks if chunk)
        
        return clean_content[:2000]  # Limit content length
        
    except Exception as e:
        return f"Error scraping website: {str(e)}"

@function_tool
def analyze_company_services(content: str) -> str:
    """Analyze website content to identify company services and business focus."""
    # This would use AI to analyze the content
    # For now, returning a structured analysis
    return f"Content Analysis:\n{content[:500]}...\n\nServices identified: Data analytics, business intelligence, consulting services"

@function_tool
def identify_company_needs(content: str) -> str:
    """Identify potential data analytics needs based on company content."""
    # Analyze content for pain points and opportunities
    needs = []
    
    if "growth" in content.lower() or "scale" in content.lower():
        needs.append("Scalable data infrastructure")
    
    if "manual" in content.lower() or "spreadsheet" in content.lower():
        needs.append("Automation of manual processes")
    
    if "insights" in content.lower() or "analytics" in content.lower():
        needs.append("Advanced analytics capabilities")
    
    if "real-time" in content.lower():
        needs.append("Real-time data processing")
    
    return f"Identified Needs:\n" + "\n".join([f"- {need}" for need in needs]) if needs else "No specific needs identified"

@function_tool
def extract_company_metrics(content: str) -> str:
    """Extract key company metrics and indicators from website content."""
    # Look for common business metrics
    metrics = {}
    
    # Company size indicators
    if re.search(r'\d+\+?\s*(employees?|staff|team)', content.lower()):
        metrics['team_size'] = "Company has multiple employees"
    
    # Industry indicators
    if "tech" in content.lower() or "software" in content.lower():
        metrics['industry'] = "Technology/Software"
    elif "finance" in content.lower() or "banking" in content.lower():
        metrics['industry'] = "Finance/Banking"
    elif "healthcare" in content.lower() or "medical" in content.lower():
        metrics['industry'] = "Healthcare"
    
    # Growth indicators
    if "startup" in content.lower() or "founded" in content.lower():
        metrics['stage'] = "Startup/Early stage"
    elif "enterprise" in content.lower() or "global" in content.lower():
        metrics['stage'] = "Enterprise/Established"
    
    return f"Company Metrics:\n" + "\n".join([f"- {k}: {v}" for k, v in metrics.items()])

# Website Research Agent
website_research_agent = Agent(
    name="WebsiteResearchAgent",
    instructions="""You are a specialized agent for researching company websites. 
    Your job is to extract and analyze company information to identify business opportunities.
    
    When researching a website:
    1. Scrape the website content
    2. Analyze the company's services and business focus
    3. Identify potential data analytics needs
    4. Extract key company metrics and indicators
    
    Focus on finding information that suggests the company could benefit from data analytics services.
    Be thorough and provide actionable insights.""",
    model=llm_model,
    tools=[scrape_website_content, analyze_company_services, identify_company_needs, extract_company_metrics]
)

def research_company_website(company_name: str, website_url: str) -> str:
    """Research a company's website comprehensively."""
    
    query = f"""
    Please research the website for {company_name} at {website_url}.
    
    Please:
    1. Scrape and analyze the website content
    2. Identify the company's services and business focus
    3. Identify potential data analytics needs
    4. Extract key company metrics and indicators
    
    Provide a comprehensive analysis that helps understand if this company would be a good prospect for data analytics services.
    """
    
    result = Runner.run_sync(website_research_agent, query)
    return result

if __name__ == "__main__":
    # Example usage
    print("=== Website Research Agent ===")
    print("Researching: TechCorp Inc. at https://techcorp.com")
    print("-" * 50)
    
    result = research_company_website("TechCorp Inc.", "https://techcorp.com")
    print(result)
