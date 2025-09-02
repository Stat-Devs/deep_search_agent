"""
Deep Research System with Agent Manager

This file integrates the Agent Manager with existing
Chainlit application to provide centralized agent orchestration.
Enhanced with comprehensive tracing using Agents SDK and full agent orchestration.
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
import chainlit as cl
from openai import AsyncOpenAI
from agents import Runner, Agent, AsyncOpenAI as AgentsAsyncOpenAI, OpenAIChatCompletionsModel, trace, function_tool, custom_span
from dotenv import load_dotenv
import json
import uuid
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Import the full agent management system
from agent_manager import get_agent_manager, initialize_agent_manager, RequestPriority
from agent_adapters import register_all_agents
from deep_research_system_handoffs import ResearchContext, AgentType

# Load environment variables
load_dotenv()

# Enhanced OpenAI tracing setup
# Tracing is enabled by default in Agents SDK
# Traces will be available at: https://platform.openai.com/logs?api=traces
print("🔍 Tracing enabled for Sales Deep Search System with Full Agent Orchestration")
print("📊 Traces available at: https://platform.openai.com/logs?api=traces")
print("🤖 Agent Manager: Centralized orchestration with intelligent handoffs")
print("🔗 Agents: Website, LinkedIn, Tavily, Industry, Solutions, Reports, Email")

# StatDevs Business Context for Sales Intelligence
STATDEVS_CONTEXT = {
    "company_name": "StatDevs",
    "services": {
        "data_engineering": "Unify, clean, and connect data for smarter decision-making",
        "data_science_ml": "Leverage AI to spot trends, predict outcomes, and automate tasks",
        "artificial_intelligence": "Harness AI to automate tasks, uncover insights, and drive smarter decisions",
        "business_intelligence": "Turn data into clear, actionable insights with real-time dashboards"
    },
    "value_propositions": [
        "82% Reduction in Data Integration Time",
        "3.2x Return on AI Investment", 
        "24/7 Mobile Access to Key Metrics",
        "47% Cost Reduction in Customer Support",
        "Robust data engineering accelerates insights by 35-45%",
        "Reliable pipelines reduce data issues by 82%",
        "AI automation cuts manual tasks by 67%",
        "Machine learning improves predictive accuracy by 43%"
    ],
    "expertise": ["Python", "R", "R Shiny", "Streamlit", "Apache Superset", "AWS", "Machine Learning", "Predictive Modeling"],
    "industries": ["Research Organizations", "Supply Chain", "Marketing", "Fintech", "Non-Profits", "Manufacturing"],
    "process": ["Discovery Call", "Assessment", "Solution Design", "Phased Implementation"]
}

# Initialize OpenAI clients with proper configuration for tracing
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables")

# Standard OpenAI client for legacy functions
client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url="https://api.openai.com/v1"
)

# Agents SDK OpenAI client for tracing
agents_openai_client = AgentsAsyncOpenAI(
    api_key=openai_api_key,
    base_url="https://api.openai.com/v1"
)

# Agents SDK Gemini client for tracing
agents_gemini_client = AgentsAsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model configurations for tracing
openai_model = OpenAIChatCompletionsModel(
    model="gpt-4",
    openai_client=agents_openai_client
)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", 
    openai_client=agents_gemini_client
)

# Initialize Agent Manager with full orchestration
agent_manager = None

async def get_agent_manager():
    """Get the global agent manager instance, initializing if necessary."""
    global agent_manager
    if agent_manager is None:
        agent_manager = await initialize_agent_manager()
        await register_all_agents(agent_manager)
    return agent_manager

# Function tools for tracing-enabled research
@function_tool
async def website_analysis_tool(company_name: str, website_url: str) -> str:
    """Analyze company website for StatDevs sales opportunities with full tracing."""
    analysis_prompt = f"""Analyze {company_name} at {website_url} and identify:

1. **Business Model & Current State**: What do they do and where are they in their data journey?
2. **StatDevs Opportunity Areas**: Which of our services (Data Engineering, Data Science/ML, AI, BI) would benefit them most?
3. **Specific Pain Points**: What data challenges do they likely face?
4. **ROI Potential**: How can our solutions deliver measurable value?
5. **Sales Approach**: What specific StatDevs capabilities should we highlight?

Format as a sales-ready analysis with clear StatDevs service recommendations."""
    
    return analysis_prompt

@function_tool
async def industry_problems_tool(company_industry: str, company_size: str, person_role: str) -> str:
    """Identify industry-specific problems and map to StatDevs solutions."""
    problems_prompt = f"""Analyze {company_industry} industry challenges for a {company_size} company with {person_role} contact. Identify:

1. **Industry-Specific Problems**: What challenges do {company_industry} companies face?
2. **StatDevs Solution Mapping**: How do our services solve these problems?
3. **ROI Quantification**: Use our proven metrics to show value
4. **Implementation Approach**: How would our phased process work for them?

Format as StatDevs sales intelligence with clear service recommendations."""
    
    return problems_prompt

@function_tool
async def ai_solutions_tool(industry_problems: str, company_industry: str, company_size: str) -> str:
    """Research StatDevs AI and data analytics solutions for identified problems."""
    solutions_prompt = f"""Recommend StatDevs solutions for these problems:
{industry_problems}

Company: {company_size} in {company_industry}

Provide:
1. **StatDevs Service Recommendations**: Which of our 4 core services fit best?
2. **Technology Stack**: Use our expertise in Python, R, AWS, ML
3. **Implementation Benefits**: Reference our proven metrics
4. **ROI Potential**: Use our track record of 3.2x return
5. **Implementation Process**: Follow our Discovery → Assessment → Design → Implementation approach

Format as StatDevs sales proposal with clear next steps."""
    
    return solutions_prompt

# Create Agents with proper tracing
website_analyst_agent = Agent(
    name="StatDevs_Website_Analyst",
    instructions=f"""You are a StatDevs sales intelligence analyst. Your goal is to identify how {STATDEVS_CONTEXT['company_name']} can help companies with data solutions. 

Focus on StatDevs' core services: {', '.join(STATDEVS_CONTEXT['services'].keys())}. 

Use specific value propositions:
- {STATDEVS_CONTEXT['value_propositions'][0]}
- {STATDEVS_CONTEXT['value_propositions'][1]}
- {STATDEVS_CONTEXT['value_propositions'][2]}

Always provide sales-ready analysis with clear StatDevs service recommendations.""",
    model=gemini_model,
    tools=[website_analysis_tool]
)

industry_analyst_agent = Agent(
    name="StatDevs_Industry_Analyst", 
    instructions=f"""You are a StatDevs industry analyst. Map industry problems to StatDevs solutions using proven metrics:
- {STATDEVS_CONTEXT['value_propositions'][0]}
- {STATDEVS_CONTEXT['value_propositions'][1]}
- {STATDEVS_CONTEXT['value_propositions'][2]}

Provide clear ROI quantification and implementation approaches for StatDevs services.""",
    model=gemini_model,
    tools=[industry_problems_tool]
)

solutions_architect_agent = Agent(
    name="StatDevs_Solutions_Architect",
    instructions=f"""You are a StatDevs solutions architect. Recommend specific services and tools using our expertise: {', '.join(STATDEVS_CONTEXT['expertise'])}.

Reference our proven ROI: {STATDEVS_CONTEXT['value_propositions'][1]} and our process: {', '.join(STATDEVS_CONTEXT['process'])}.

Always provide sales proposals with clear next steps.""",
    model=gemini_model,
    tools=[ai_solutions_tool]
)

# Enhanced research functions with agent manager orchestration
async def analyze_company_website(company_name: str, website_url: str) -> str:
    """Analyze company website using the Website Research Agent through Agent Manager."""
    try:
        agent_mgr = await get_agent_manager()
        
        # Submit request to Website Research Agent
        request_id = agent_mgr.submit_request(
            request_type="website_research",
            payload={
                "company_name": company_name,
                "website_url": website_url
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_mgr.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == "completed":
            return result.result
        else:
            raise Exception(f"Website research failed: {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"⚠️ Website research via Agent Manager failed: {e}")
        # Fallback to direct function
        from deep_research_system_handoffs import analyze_company_website_direct
        return analyze_company_website_direct(company_name, website_url)

async def identify_industry_problems(company_industry: str, company_size: str, person_role: str) -> str:
    """Identify industry problems using the Industry Problems Agent through Agent Manager."""
    try:
        agent_mgr = await get_agent_manager()
        
        # Submit request to Industry Problems Agent
        request_id = agent_mgr.submit_request(
            request_type="industry_problems",
            payload={
                "company_industry": company_industry,
                "company_size": company_size,
                "company_location": "Unknown",  # Could be enhanced
                "person_role": person_role
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_mgr.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == "completed":
            return result.result
        else:
            raise Exception(f"Industry problems analysis failed: {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"⚠️ Industry problems analysis via Agent Manager failed: {e}")
        # Fallback to direct function
        from deep_research_system_handoffs import identify_industry_problems_direct
        return identify_industry_problems_direct(company_industry, company_size, "Unknown", person_role)

async def research_ai_solutions(industry_problems: List[str], company_industry: str, company_size: str) -> str:
    """Research AI solutions using the Solutions Research Agent through Agent Manager."""
    try:
        agent_mgr = await get_agent_manager()
        
        # Submit request to Solutions Research Agent
        request_id = agent_mgr.submit_request(
            request_type="ai_solutions",
            payload={
                "industry_problems": industry_problems,
                "company_industry": company_industry,
                "company_size": company_size
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_mgr.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == "completed":
            return result.result
        else:
            raise Exception(f"AI solutions research failed: {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"⚠️ AI solutions research via Agent Manager failed: {e}")
        # Fallback to direct function
        from deep_research_system_handoffs import research_ai_solutions_direct
        return research_ai_solutions_direct(industry_problems, company_industry, company_size)

async def research_linkedin_profile(person_name: str, company_name: str, linkedin_url: str = None) -> str:
    """Research LinkedIn profile using the LinkedIn Research Agent through Agent Manager."""
    try:
        agent_mgr = await get_agent_manager()
        
        # Submit request to LinkedIn Research Agent
        request_id = agent_mgr.submit_request(
            request_type="linkedin_research",
            payload={
                "person_name": person_name,
                "company_name": company_name,
                "linkedin_url": linkedin_url
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_mgr.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == "completed":
            return result.result
        else:
            raise Exception(f"LinkedIn research failed: {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"⚠️ LinkedIn research via Agent Manager failed: {e}")
        # Fallback to direct function
        from deep_research_system_handoffs import research_linkedin_profile_direct
        return research_linkedin_profile_direct(person_name, company_name)

async def research_with_tavily(company_name: str, person_name: str, company_industry: str = None) -> str:
    """Research using Tavily Web Intelligence Agent through Agent Manager."""
    try:
        agent_mgr = await get_agent_manager()
        
        # Submit request to Tavily Research Agent
        request_id = agent_mgr.submit_request(
            request_type="web_intelligence",
            payload={
                "company_name": company_name,
                "person_name": person_name,
                "company_industry": company_industry or "Unknown",
                "contact_type": "general"
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_mgr.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == "completed":
            return result.result
        else:
            raise Exception(f"Tavily research failed: {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"⚠️ Tavily research via Agent Manager failed: {e}")
        return f"Web intelligence research for {company_name} - {person_name} via Tavily (fallback mode)"

async def generate_comprehensive_report(company_name: str, person_name: str, website_research: str, 
                                     industry_problems: str, ai_solutions: str, linkedin_research: str = None, tavily_research: str = None) -> str:
    """Generate a comprehensive StatDevs sales report using the Research Report Agent through Agent Manager."""
    try:
        agent_mgr = await get_agent_manager()
        
        # Submit request to Research Report Agent
        request_id = agent_mgr.submit_request(
            request_type="report_generation",
            payload={
                "company_name": company_name,
                "person_name": person_name,
                "website_research": website_research,
                "linkedin_research": linkedin_research or "",
                "industry_problems": industry_problems,
                "ai_solutions": ai_solutions,
                "tavily_research": tavily_research or ""
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_mgr.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == "completed":
            return result.result
        else:
            raise Exception(f"Report generation failed: {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"⚠️ Report generation via Agent Manager failed: {e}")
        # Fallback to direct function
        from deep_research_system_handoffs import compile_research_report_direct
        return compile_research_report_direct(company_name, person_name, website_research, linkedin_research or "")
    except Exception as e:
        return f"**StatDevs Sales Report for {company_name}**\n\n**Executive Summary**: {company_name} shows strong potential for StatDevs data solutions\n\n**Key Challenges**: Data integration, manual processes, lack of real-time insights\n\n**StatDevs Solutions**: Data Engineering, AI/ML, Business Intelligence\n\n**ROI Projection**: 3.2x return on investment based on our track record\n\n**Implementation**: Phased approach following our proven process\n\n**Next Steps**: Schedule discovery call to assess specific needs"

async def generate_email_pitch(person_name: str, company_name: str, research_summary: str) -> str:
    """Generate a personalized StatDevs email pitch using the Email Generation Agent through Agent Manager."""
    try:
        agent_mgr = await get_agent_manager()
        
        # Submit request to Email Generation Agent
        request_id = agent_mgr.submit_request(
            request_type="email_generation",
            payload={
                "person_name": person_name,
                "company_name": company_name,
                "research_summary": research_summary
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_mgr.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == "completed":
            return result.result
        else:
            raise Exception(f"Email generation failed: {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"⚠️ Email generation via Agent Manager failed: {e}")
        # Fallback to direct function
        from deep_research_system_handoffs import generate_email_pitch_direct
        return generate_email_pitch_direct(person_name, company_name, research_summary)

async def extract_lead_information(message: str) -> Dict[str, str]:
    """Extract lead information from user message."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Extract lead information from the user message and return as JSON with these fields: company_name, person_name, role, email, linkedin, phone, website, company_industry, company_size. For company_industry, infer from company name and website. For company_size, infer from company name and industry (e.g., 'Large' for major corporations, 'Medium' for established companies, 'Small' for startups)."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Enhanced fallback parsing with industry inference
        info = {
            "company_name": "Unknown Company",
            "person_name": "Unknown Contact",
            "role": "Unknown Role",
            "email": "",
            "linkedin": "",
            "phone": "",
            "website": "",
            "company_industry": "Unknown Industry",
            "company_size": "Unknown Size"
        }
        
        # Simple parsing
        lines = message.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if 'company' in key:
                    info["company_name"] = value
                    # Infer industry from company name
                    if 'fertiliser' in value.lower() or 'fertilizer' in value.lower():
                        info["company_industry"] = "Agriculture & Fertilizer"
                        info["company_size"] = "Large"  # Fauji is a major Pakistani company
                    elif 'tech' in value.lower() or 'software' in value.lower():
                        info["company_industry"] = "Technology"
                        info["company_size"] = "Medium"
                    elif 'bank' in value.lower() or 'financial' in value.lower():
                        info["company_industry"] = "Financial Services"
                        info["company_size"] = "Large"
                    elif 'health' in value.lower() or 'medical' in value.lower():
                        info["company_industry"] = "Healthcare"
                        info["company_size"] = "Medium"
                    else:
                        info["company_industry"] = "Manufacturing"
                        info["company_size"] = "Medium"
                elif 'contact' in key or 'person' in key:
                    info["person_name"] = value
                elif 'role' in key:
                    info["role"] = value
                elif 'email' in key:
                    info["email"] = value
                elif 'linkedin' in key:
                    info["linkedin"] = value
                elif 'phone' in key:
                    info["phone"] = value
                elif 'website' in key:
                    info["website"] = value
        
        return info

async def initialize_agent_system():
    """Initialize the full agent management system with tracing."""
    global agent_manager
    
    try:
        print("🚀 Initializing Agent Manager with full orchestration...")
        
        # Initialize agent manager
        agent_manager = await initialize_agent_manager()
        
        # Register all available agents
        success = await register_all_agents(agent_manager)
        
        if success:
            print("✅ All agents registered and ready")
            print(f"📊 System Status: {agent_manager.get_system_status()}")
        else:
            print("⚠️ Some agents failed to register")
        
        return agent_manager
        
    except Exception as e:
        print(f"❌ Failed to initialize agent system: {e}")
        return None

@cl.on_chat_start
async def start():
    """Initialize the chat session with full agent system."""
    
    # Initialize the agent management system
    await initialize_agent_system()
    
    await cl.Message(
        content=f"""# StatDevs Sales Intelligence System - FULL AGENT ORCHESTRATION

Welcome to the AI-powered lead research system for **{STATDEVS_CONTEXT['company_name']}**!

## 🤖 **Full Agent System Active:**
- **Agent Manager**: Centralized orchestration with intelligent handoffs
- **Website Research Agent**: Company website analysis
- **LinkedIn Research Agent**: Professional profile analysis  
- **Tavily Research Agent**: Web intelligence and market research
- **Industry Problems Agent**: Challenge identification and mapping
- **Solutions Research Agent**: AI/data solutions recommendations
- **Report Generation Agent**: Comprehensive analysis compilation
- **Email Generation Agent**: Personalized pitch creation

## What I can do:
- **Analyze company websites** and identify StatDevs opportunities
- **Research LinkedIn profiles** for decision-making insights
- **Gather web intelligence** using Tavily for market context
- **Map industry problems** to our specific solutions
- **Recommend StatDevs services** (Data Engineering, AI/ML, BI, Data Science)
- **Generate sales-ready reports** with our proven ROI metrics
- **Create personalized email pitches** highlighting StatDevs value

## Our Core Services:
{chr(10).join([f"- **{service.replace('_', ' ').title()}**: {desc}" for service, desc in STATDEVS_CONTEXT['services'].items()])}

## Proven Results:
- {STATDEVS_CONTEXT['value_propositions'][0]}
- {STATDEVS_CONTEXT['value_propositions'][1]}
- {STATDEVS_CONTEXT['value_propositions'][2]}

## How to use:
Simply paste your lead information in this format:

```
Company: [Company Name]
Contact: [Person Name]
Role: [Job Title]
Email: [Email Address]
LinkedIn: [LinkedIn URL]
Phone: [Phone Number]
Website: [Website URL]
```

Or ask me to perform comprehensive research on a specific lead.

**Feature Request Form**: https://forms.gle/D9uAUPtJR1gmoDCD7"""
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages and perform lead research with comprehensive tracing."""
    
    user_input = message.content
    
    # Generate unique trace ID for this user query
    trace_id = f"trace_{uuid.uuid4().hex}"
    session_id = cl.user_session.get("id", "unknown")
    
    # Create comprehensive trace for the entire user interaction
    with trace(
        "Sales Deep Search Query",
        trace_id=trace_id,
        group_id=session_id,
        metadata={
            "user_query": user_input,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "query_type": "comprehensive" if any(keyword in user_input.lower() for keyword in ['comprehensive', 'full research', 'analyze lead', 'research lead']) else "quick_analysis",
            "system": "StatDevs Sales Intelligence"
        }
    ) as main_trace:
        
        print(f"🔍 Starting traced sales research query: {trace_id}")
        
        # Check if user wants comprehensive research
        if any(keyword in user_input.lower() for keyword in ['comprehensive', 'full research', 'analyze lead', 'research lead']):
            await handle_comprehensive_research(user_input, main_trace)
        else:
            # Extract lead information and provide insights
            await handle_lead_analysis(user_input, main_trace)
        
        print(f"✅ Completed traced sales research query: {trace_id}")
        print(f"📊 View trace at: https://platform.openai.com/logs?api=traces&trace_id={trace_id}")

async def handle_comprehensive_research(user_input: str, main_trace):
    """Perform comprehensive lead research with detailed tracing."""
    
    await cl.Message(content="Starting Comprehensive Lead Research...\nThis will use multiple AI agents to analyze the lead thoroughly.").send()
    
    # Step 0: Extract lead information (with custom span)
    with custom_span("Lead Information Extraction", data={"step": "0_extraction"}):
        lead_info = await extract_lead_information(user_input)
        print(f"📋 Lead extracted: {lead_info['company_name']} - {lead_info['person_name']}")
    
    # Step 1: Website Research (via Agent Manager)
    await cl.Message(content="**Step 1: Website Research**\nAnalyzing company website...").send()
    with custom_span("Website Analysis", data={"step": "1_website", "company": lead_info["company_name"], "website": lead_info["website"]}):
        website_research = await analyze_company_website(lead_info["company_name"], lead_info["website"])
        print(f"🌐 Website analysis completed for {lead_info['company_name']}")
    await cl.Message(content=f"**Website Analysis Complete:**\n{website_research}").send()
    
    # Step 2: LinkedIn Research (via Agent Manager)
    await cl.Message(content="**Step 2: LinkedIn Research**\nAnalyzing professional profile...").send()
    with custom_span("LinkedIn Analysis", data={"step": "2_linkedin", "person": lead_info["person_name"], "company": lead_info["company_name"]}):
        linkedin_research = await research_linkedin_profile(lead_info["person_name"], lead_info["company_name"], lead_info.get("linkedin"))
        print(f"💼 LinkedIn analysis completed for {lead_info['person_name']}")
    await cl.Message(content=f"**LinkedIn Analysis Complete:**\n{linkedin_research}").send()
    
    # Step 3: Tavily Web Intelligence (via Agent Manager)
    await cl.Message(content="**Step 3: Web Intelligence Research**\nGathering market intelligence...").send()
    with custom_span("Tavily Research", data={"step": "3_tavily", "company": lead_info["company_name"], "industry": lead_info["company_industry"]}):
        tavily_research = await research_with_tavily(lead_info["company_name"], lead_info["person_name"], lead_info["company_industry"])
        print(f"🔍 Tavily research completed for {lead_info['company_name']}")
    await cl.Message(content=f"**Web Intelligence Complete:**\n{tavily_research}").send()
    
    # Step 4: Industry Problems Analysis (via Agent Manager)
    await cl.Message(content="**Step 4: Industry Problems Analysis**\nIdentifying potential challenges...").send()
    with custom_span("Industry Analysis", data={"step": "4_industry", "industry": lead_info["company_industry"], "size": lead_info["company_size"]}):
        industry_problems = await identify_industry_problems(
            lead_info["company_industry"], 
            lead_info["company_size"], 
            lead_info["role"]
        )
        print(f"🏭 Industry analysis completed for {lead_info['company_industry']}")
    await cl.Message(content=f"**Industry Problems Identified:**\n{industry_problems}").send()
    
    # Step 5: AI Solutions Research (via Agent Manager)
    await cl.Message(content="**Step 5: AI Solutions Research**\nFinding relevant AI solutions...").send()
    problems_list = [industry_problems]  # Simplified for now
    with custom_span("Solutions Research", data={"step": "5_solutions", "company_size": lead_info["company_size"], "industry": lead_info["company_industry"]}):
        ai_solutions = await research_ai_solutions(
            problems_list, 
            lead_info["company_industry"], 
            lead_info["company_size"]
        )
        print(f"🤖 AI solutions research completed")
    await cl.Message(content=f"**AI Solutions Research Complete:**\n{ai_solutions}").send()
    
    # Step 6: Generate Comprehensive Report (via Agent Manager)
    await cl.Message(content="**Step 6: Generating Comprehensive Report**...").send()
    with custom_span("Report Generation", data={"step": "6_report", "company": lead_info["company_name"], "person": lead_info["person_name"]}):
        comprehensive_report = await generate_comprehensive_report(
            lead_info["company_name"],
            lead_info["person_name"],
            website_research,
            industry_problems,
            ai_solutions,
            linkedin_research,
            tavily_research
        )
        print(f"📄 Comprehensive report generated")
    await cl.Message(content=f"**Comprehensive Report Generated:**\n{comprehensive_report}").send()
    
    # Step 7: Generate Email Pitch (via Agent Manager)
    await cl.Message(content="**Step 7: Generating Email Pitch**...").send()
    with custom_span("Email Pitch Generation", data={"step": "7_email", "person": lead_info["person_name"], "company": lead_info["company_name"]}):
        email_pitch = await generate_email_pitch(
            lead_info["person_name"],
            lead_info["company_name"],
            comprehensive_report
        )
        print(f"📧 Email pitch generated for {lead_info['person_name']}")
    await cl.Message(content=f"**Personalized Email Pitch:**\n{email_pitch}").send()
    
    # Final summary
    await cl.Message(content="**Comprehensive Research Complete!**\nAll research steps completed. Check the results above for the complete analysis and recommendations.").send()

async def handle_lead_analysis(user_input: str, main_trace):
    """Handle individual lead analysis requests with tracing."""
    
    # Extract lead information (with custom span)
    with custom_span("Quick Lead Extraction", data={"analysis_type": "quick"}):
        lead_info = await extract_lead_information(user_input)
        print(f"📋 Quick lead extracted: {lead_info['company_name']} - {lead_info['person_name']}")
    
    await cl.Message(content=f"**Lead Information Extracted:**\nCompany: {lead_info['company_name']}\nContact: {lead_info['person_name']}\nRole: {lead_info['role']}").send()
    
    # Provide quick insights (traced)
    if lead_info["website"]:
        await cl.Message(content="**Quick Website Analysis:**\nAnalyzing business opportunities...").send()
        with custom_span("Quick Website Analysis", data={"company": lead_info["company_name"], "website": lead_info["website"]}):
            website_insights = await analyze_company_website(lead_info["company_name"], lead_info["website"])
            print(f"🌐 Quick website analysis completed for {lead_info['company_name']}")
        await cl.Message(content=f"**Website Insights:**\n{website_insights}").send()
    
    # Industry analysis (traced)
    await cl.Message(content="**Industry Analysis:**\nIdentifying business challenges...").send()
    with custom_span("Quick Industry Analysis", data={"industry": lead_info["company_industry"], "size": lead_info["company_size"]}):
        industry_insights = await identify_industry_problems(
            lead_info["company_industry"], 
            lead_info["company_size"], 
            lead_info["role"]
        )
        print(f"🏭 Quick industry analysis completed for {lead_info['company_industry']}")
    await cl.Message(content=f"**Industry Insights:**\n{industry_insights}").send()
    
    # Recommendations (traced)
    await cl.Message(content="**Recommendations:**\nResearching AI solutions...").send()
    with custom_span("Quick Solutions Research", data={"company_size": lead_info["company_size"], "industry": lead_info["company_industry"]}):
        solutions = await research_ai_solutions(
            [industry_insights], 
            lead_info["company_industry"], 
            lead_info["company_size"]
        )
        print(f"🤖 Quick solutions research completed")
    await cl.Message(content=f"**AI Solutions Recommendations:**\n{solutions}").send()

@cl.on_chat_end
async def end():
    """Handle chat session end."""
    await cl.Message(content="Thank you for using the Deep Research System. Session ended.").send()

# Create FastAPI app for health checks
app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancers."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "StatDevs Sales Intelligence System",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

if __name__ == "__main__":
    print("Deep Research System - Chainlit App")
    print("OpenAI Tracing: Using Runner.run() for automatic tracing")
    print("Traces available at: https://platform.openai.com/logs?api=traces")
    print("Starting server...")
