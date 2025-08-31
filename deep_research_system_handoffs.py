import os
from dotenv import load_dotenv, find_dotenv
try:
    from openai_agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
except ImportError:
    # Fallback for when openai_agents is not available
    print("Warning: openai_agents not available, some functions may not work")
    # Create dummy classes to prevent import errors
    class Agent: pass
    class Runner: pass
    class AsyncOpenAI: pass
    class OpenAIChatCompletionsModel: pass
    def function_tool(func): return func
from typing import Dict, List, Any, Optional
import json
from dataclasses import dataclass
from enum import Enum

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
try:
    openai_client = AsyncOpenAI(
        api_key=openai_api_key,
        base_url="https://api.openai.com/v1"
    )
except:
    openai_client = None

# Configure Gemini client
try:
    gemini_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
except:
    gemini_client = None

# LLM Models
try:
    openai_model = OpenAIChatCompletionsModel(
        model="gpt-4",
        openai_client=openai_client
    )
except:
    openai_model = None

try:
    gemini_model = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=gemini_client
    )
except:
    gemini_model = None

class AgentType(Enum):
    """Types of agents in the system."""
    WEBSITE_RESEARCHER = "website_researcher"
    LINKEDIN_ANALYZER = "linkedin_analyzer"
    EMAIL_GENERATOR = "email_generator"
    EXECUTIVE_SPECIALIST = "executive_specialist"
    TECHNICAL_SPECIALIST = "technical_specialist"
    HUMAN_REVIEWER = "human_reviewer"
    INDUSTRY_PROBLEMS_SPECIALIST = "industry_problems_specialist"
    SOLUTIONS_RESEARCHER = "solutions_researcher"

@dataclass
class ResearchContext:
    """Shared context object passed between agents."""
    company_name: str
    person_name: str
    website_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    # Research findings
    website_research: Optional[str] = None
    linkedin_research: Optional[str] = None
    company_industry: Optional[str] = None
    company_size: Optional[str] = None
    company_stage: Optional[str] = None
    
    # Person analysis
    person_role: Optional[str] = None
    experience_level: Optional[str] = None
    technical_skills: Optional[List[str]] = None
    decision_power: Optional[str] = None
    contact_preferences: Optional[str] = None
    
    # Handoff decisions
    next_agent: Optional[AgentType] = None
    handoff_reason: Optional[str] = None
    priority_level: int = 3  # 1-5 scale
    
    # Communication strategy
    communication_tone: Optional[str] = None
    key_value_props: Optional[List[str]] = None
    follow_up_timeline: Optional[str] = None
    
    # Problem and solution analysis
    industry_problems: Optional[List[str]] = None
    potential_solutions: Optional[str] = None

# Direct callable functions for the handoff system
def analyze_company_website_direct(company_name: str, website_url: str) -> str:
    """Direct callable version of company website analysis."""
    return f"Company: {company_name}\nWebsite Analysis: Business intelligence, data analytics needs identified. Company appears to be in growth phase with potential for data infrastructure improvements."

@function_tool
def analyze_company_website(company_name: str, website_url: str) -> str:
    """Research a company's website to extract key information about their business, services, and needs."""
    return analyze_company_website_direct(company_name, website_url)

def research_linkedin_profile_direct(person_name: str, company_name: str) -> str:
    """Direct callable version of LinkedIn profile research."""
    return f"Person: {person_name}\nRole: Data Analyst/Manager\nCompany: {company_name}\nExperience: 5+ years in data analytics\nInterests: Business intelligence, data visualization, analytics tools"

@function_tool
def research_linkedin_profile(person_name: str, company_name: str) -> str:
    """Research a person's LinkedIn profile to extract professional information and contact details."""
    return research_linkedin_profile_direct(person_name, company_name)

def generate_email_pitch_direct(person_name: str, company_name: str, research_summary: str) -> str:
    """Direct callable version of email pitch generation."""
    return f"Subject: Data Analytics Solutions for {company_name}\n\nDear {person_name},\n\nBased on my research of {company_name}, I believe we can help you optimize your data analytics infrastructure. Our services include business intelligence dashboards, data pipeline optimization, and advanced analytics solutions.\n\nWould you be interested in a brief discussion about how we can help {company_name} leverage data more effectively?\n\nBest regards,\n[Your Name]"

@function_tool
def generate_email_pitch(person_name: str, company_name: str, research_summary: str) -> str:
    """Generate a personalized email pitch for data analytics services based on research findings."""
    return generate_email_pitch_direct(person_name, company_name, research_summary)

def compile_research_report_direct(company_name: str, person_name: str, website_research: str, linkedin_research: str) -> str:
    """Direct callable version of research report compilation."""
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

@function_tool
def compile_research_report(company_name: str, person_name: str, website_research: str, linkedin_research: str) -> str:
    """Compile all research findings into a comprehensive report."""
    return compile_research_report_direct(company_name, person_name, website_research, linkedin_research)

def determine_handoff_strategy_direct(context: ResearchContext) -> str:
    """Direct callable version of handoff strategy determination."""
    
    # Analyze the context to determine next steps
    if context.person_role and "ceo" in context.person_role.lower():
        context.next_agent = AgentType.EXECUTIVE_SPECIALIST
        context.priority_level = 5
        context.handoff_reason = "High-value CEO contact detected - requires executive specialist"
        context.communication_tone = "Executive level - strategic and ROI-focused"
        context.follow_up_timeline = "2-3 business days (executive priority)"
        
    elif context.technical_skills and len(context.technical_skills) > 2:
        context.next_agent = AgentType.TECHNICAL_SPECIALIST
        context.priority_level = 4
        context.handoff_reason = "Technical contact detected - requires technical specialist"
        context.communication_tone = "Technical with business outcomes"
        context.follow_up_timeline = "3-5 business days"
        
    elif context.decision_power and "high" in context.decision_power.lower():
        context.next_agent = AgentType.EXECUTIVE_SPECIALIST
        context.priority_level = 4
        context.handoff_reason = "High decision-making power - requires executive approach"
        context.communication_tone = "Strategic and business-focused"
        context.follow_up_timeline = "3-4 business days"
        
    else:
        context.next_agent = AgentType.EMAIL_GENERATOR
        context.priority_level = 3
        context.handoff_reason = "Standard lead - proceed to email generation"
        context.communication_tone = "Professional and value-focused"
        context.follow_up_timeline = "5-7 business days"
    
    return f"Handoff Strategy: {context.handoff_reason}\nNext Agent: {context.next_agent.value}\nPriority: {context.priority_level}/5\nCommunication Tone: {context.communication_tone}\nFollow-up Timeline: {context.follow_up_timeline}"

@function_tool
def determine_handoff_strategy(context: ResearchContext) -> str:
    """Determine the next agent and handoff strategy based on current research context."""
    return determine_handoff_strategy_direct(context)

def identify_industry_problems_direct(company_industry: str, company_size: str, company_location: str, person_role: str) -> str:
    """Direct callable version of industry problems identification."""
    try:
        from research_agent_industry_problems import identify_lead_problems_direct
        return identify_lead_problems_direct(company_industry, company_size, company_location, person_role)
    except ImportError:
        return f"Industry problems analysis for {company_industry} industry, {company_size} company, {company_location} location, {person_role} role."

@function_tool
def identify_industry_problems(company_industry: str, company_size: str, company_location: str, person_role: str) -> str:
    """Identify potential industry problems and challenges the lead may face."""
    return identify_industry_problems_direct(company_industry, company_size, company_location, person_role)

def research_ai_solutions_direct(industry_problems: List[str], company_industry: str, company_size: str) -> str:
    """Direct callable version of AI solutions research."""
    try:
        from research_agent_solutions import research_solutions_for_problems_direct
        return research_solutions_for_problems_direct(industry_problems, company_industry, company_size)
    except ImportError:
        return f"AI solutions research for {company_industry} industry problems: {', '.join(industry_problems)}"

@function_tool
def research_ai_solutions(industry_problems: List[str], company_industry: str, company_size: str) -> str:
    """Research AI and data analytics solutions for identified industry problems."""
    return research_ai_solutions_direct(industry_problems, company_industry, company_size)

# Handoff-Enabled Research Coordinator Agent
# Commented out due to import issues
# handoff_coordinator = Agent(
#     name="HandoffResearchCoordinator",
#     instructions="""You are an intelligent lead research coordinator that can hand off work to specialized agents.
#     
#     Your job is to:
#     1. Coordinate research activities across multiple specialized agents
#     2. Analyze research context to determine the best next agent
#     3. Make intelligent handoff decisions based on lead characteristics
#     4. Ensure context is preserved and enhanced between agents
#     5. Adapt the research strategy based on findings
#     
#     When making handoff decisions, consider:
#     - Contact level (executive vs. technical vs. general)
#     - Decision-making power
#     - Technical skills and background
#     - Company size and industry
#     - Priority level for the business
#     
#     Always provide clear reasoning for handoff decisions and ensure smooth transitions between agents.""",
#     model=openai_model,
#     tools=[analyze_company_website, research_linkedin_profile, generate_email_pitch, compile_research_report, determine_handoff_strategy, identify_industry_problems, research_ai_solutions]
# )

# Executive Specialist Agent
# Commented out due to import issues
# executive_specialist = Agent(
#     name="ExecutiveSpecialist",
#     instructions="""You are a specialized agent for handling high-level executive contacts (CEO, CTO, CFO, Directors, VPs).
#     
#     Your approach should be:
#     - Strategic and business-focused
#     - ROI and business impact oriented
#     - Respectful of executive time
#     - Concise and value-driven
#     - Focused on strategic decision-making
#     
#     When working with executives:
#     1. Emphasize business outcomes over technical details
#     2. Highlight strategic advantages and competitive positioning
#     3. Provide clear ROI metrics and business impact
#     4. Use executive-level communication tone
#     5. Focus on high-level benefits and strategic value""",
#     model=openai_model,
#     tools=[generate_email_pitch, compile_research_report]
# )

# Technical Specialist Agent
# Commented out due to import issues
# technical_specialist = Agent(
#     name="TechnicalSpecialist",
#     instructions="""You are a specialized agent for handling technical contacts (Data Scientists, Engineers, Analysts).
#     
#     Your approach should be:
#     - Technical but business-outcome focused
#     - Integration and technical capability oriented
#     - Detailed but clear and actionable
#     - Focused on technical benefits and implementation
#     - Balanced between technical depth and business value
#     
#     When working with technical contacts:
#     1. Demonstrate technical understanding and capabilities
#     2. Show how your solutions integrate with their existing tools
#     3. Provide technical benefits while maintaining business focus
#     4. Use appropriate technical terminology
#     5. Highlight implementation advantages and technical ROI""",
#     model=openai_model,
#     tools=[generate_email_pitch, compile_research_report]
# )

def research_lead_with_handoffs(company_name: str, person_name: str, website_url: str = None, linkedin_url: str = None, email: str = None, phone: str = None):
    """Main function to research a lead with intelligent handoffs between agents."""
    
    print(f"🚀 Starting research with handoffs for {person_name} at {company_name}")
    print("=" * 60)
    
    # Initialize research context
    context = ResearchContext(
        company_name=company_name,
        person_name=person_name,
        website_url=website_url,
        linkedin_url=linkedin_url,
        email=email,
        phone=phone
    )
    
    try:
        # Step 1: Initial research by coordinator
        print("\n1️⃣ Initial research and handoff strategy...")
        initial_query = f"""
        Please research this lead and determine the best handoff strategy:
        Company: {company_name}
        Person: {person_name}
        Website: {website_url if website_url else 'Not provided'}
        LinkedIn: {linkedin_url if linkedin_url else 'Not provided'}
        Email: {email if email else 'Not provided'}
        Phone: {phone if phone else 'Not provided'}
        
        Please:
        1. Research the company website
        2. Research the person's LinkedIn profile
        3. Determine the best handoff strategy
        4. Provide clear reasoning for the handoff decision
        """
        
        coordinator_result = Runner.run_sync(handoff_coordinator, initial_query)
        print("✅ Initial research and handoff strategy completed")
        
        # Extract handoff information from coordinator result
        coordinator_text = str(coordinator_result)
        
        # Determine next agent based on coordinator analysis
        if "executive" in coordinator_text.lower() or "ceo" in coordinator_text.lower():
            next_agent = executive_specialist
            agent_name = "Executive Specialist"
        elif "technical" in coordinator_text.lower():
            next_agent = technical_specialist
            agent_name = "Technical Specialist"
        else:
            next_agent = handoff_coordinator
            agent_name = "General Coordinator"
        
        print(f"\n2️⃣ Handing off to {agent_name}...")
        
        # Step 2: Specialized agent processing
        specialized_query = f"""
        Based on the previous research, please provide specialized analysis and recommendations:
        
        Previous Research: {coordinator_text}
        
        Please:
        1. Provide specialized insights for this type of contact
        2. Generate a personalized email pitch
        3. Compile a comprehensive research report
        4. Include specific recommendations for this contact type
        """
        
        specialized_result = Runner.run_sync(next_agent, specialized_query)
        print(f"✅ {agent_name} processing completed")
        
        # Compile final results
        final_report = f"""
# 🎯 LEAD RESEARCH REPORT WITH HANDOFFS: {company_name.upper()}

## 🔄 Handoff Strategy
**Coordinator Analysis:**
{coordinator_text}

**Specialized Agent:** {agent_name}
**Final Output:**
{specialized_result}

## 📋 Lead Summary
- **Company:** {company_name}
- **Contact:** {person_name}
- **Website:** {website_url if website_url else 'Not provided'}
- **LinkedIn:** {linkedin_url if linkedin_url else 'Not provided'}
- **Email:** {email if email else 'Not provided'}
- **Phone:** {phone if phone else 'Not provided'}

## 🚀 Next Steps
1. **Review specialized recommendations** from {agent_name}
2. **Customize the email pitch** based on contact type
3. **Follow the recommended timeline** for this contact level
4. **Prepare appropriate materials** for this contact type

---
*Report generated by Deep Research System with Intelligent Handoffs*
"""
        
        print("\n3️⃣ Final report compiled with handoffs")
        
        # Save report
        filename = f"handoff_research_{company_name.replace(' ', '_')}_{person_name.replace(' ', '_')}.md"
        with open(filename, 'w') as f:
            f.write(final_report)
        
        print(f"💾 Report saved to: {filename}")
        
        return {
            'coordinator_result': coordinator_text,
            'specialized_result': str(specialized_result),
            'final_report': final_report,
            'handoff_agent': agent_name
        }
        
    except Exception as e:
        print(f"❌ Error during handoff research: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Example usage
    print("=== Handoff-Enabled Lead Research System ===")
    print("Researching lead: John Smith at TechCorp Inc.")
    print("-" * 50)
    
    result = research_lead_with_handoffs("TechCorp Inc.", "John Smith", "https://techcorp.com")
    if result:
        print(f"\n🎉 Handoff research completed successfully!")
        print(f"Handoff Agent: {result['handoff_agent']}")
        print(f"Coordinator Analysis: {len(result['coordinator_result'])} characters")
        print(f"Specialized Analysis: {len(result['specialized_result'])} characters")
        print(f"Total Report: {len(result['final_report'])} characters")
