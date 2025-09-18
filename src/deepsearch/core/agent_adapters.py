"""
Agent Adapters - Compatibility Layer for Existing Agents

This module provides adapter classes that wrap existing agents to make them
compatible with the Agent Manager's standardized interface.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AgentAdapter(ABC):
    """Base adapter class for all agents."""
    
    def __init__(self, agent_id: str, agent_type: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.status = "idle"
    
    @abstractmethod
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process a request and return the result."""
        pass
    
    async def initialize(self) -> bool:
        """Initialize the agent."""
        try:
            self.status = "idle"
            logger.info(f"Agent {self.agent_id} initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize agent {self.agent_id}: {e}")
            self.status = "error"
            return False
    
    async def cleanup(self) -> bool:
        """Cleanup the agent."""
        try:
            self.status = "offline"
            logger.info(f"Agent {self.agent_id} cleaned up")
            return True
        except Exception as e:
            logger.error(f"Failed to cleanup agent {self.agent_id}: {e}")
            return False
    
    def heartbeat(self) -> bool:
        """Send a heartbeat signal."""
        try:
            # Simple heartbeat - just update status
            return True
        except Exception as e:
            logger.error(f"Heartbeat failed for agent {self.agent_id}: {e}")
            return False

class WebsiteResearchAdapter(AgentAdapter):
    """Adapter for the Website Research Agent."""
    
    def __init__(self, website_agent):
        super().__init__(
            agent_id="website_researcher",
            agent_type="Website Research",
            capabilities=["website_research"]
        )
        self.website_agent = website_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process website research request."""
        try:
            company_name = payload.get("company_name")
            website_url = payload.get("website_url")
            
            if not company_name or not website_url:
                raise ValueError("company_name and website_url are required")
            
            # Import the direct function
            from deep_research_system_handoffs import analyze_company_website_direct
            
            result = analyze_company_website_direct(company_name, website_url)
            
            logger.info(f"Website research completed for {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Website research failed: {e}")
            raise

class LinkedInResearchAdapter(AgentAdapter):
    """Adapter for the LinkedIn Research Agent."""
    
    def __init__(self, linkedin_agent):
        super().__init__(
            agent_id="linkedin_analyzer",
            agent_type="LinkedIn Research",
            capabilities=["linkedin_research"]
        )
        self.linkedin_agent = linkedin_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process LinkedIn research request."""
        try:
            person_name = payload.get("person_name")
            company_name = payload.get("company_name")
            
            if not person_name or not company_name:
                raise ValueError("person_name and company_name are required")
            
            # Import the direct function
            from deep_research_system_handoffs import research_linkedin_profile_direct
            
            result = research_linkedin_profile_direct(person_name, company_name)
            
            logger.info(f"LinkedIn research completed for {person_name} at {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"LinkedIn research failed: {e}")
            raise

class IndustryProblemsAdapter(AgentAdapter):
    """Adapter for the Industry Problems Agent."""
    
    def __init__(self, problems_agent):
        super().__init__(
            agent_id="industry_problems_specialist",
            agent_type="Industry Problems",
            capabilities=["industry_problems"]
        )
        self.problems_agent = problems_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process industry problems request."""
        try:
            company_industry = payload.get("company_industry")
            company_size = payload.get("company_size", "Unknown")
            company_location = payload.get("company_location", "Unknown")
            person_role = payload.get("person_role", "Unknown")
            
            if not company_industry:
                raise ValueError("company_industry is required")
            
            # Import the direct function
            from deep_research_system_handoffs import identify_industry_problems_direct
            
            result = identify_industry_problems_direct(
                company_industry, company_size, company_location, person_role
            )
            
            logger.info(f"Industry problems analysis completed for {company_industry}")
            return result
            
        except Exception as e:
            logger.error(f"Industry problems analysis failed: {e}")
            raise

class SolutionsResearchAdapter(AgentAdapter):
    """Adapter for the Solutions Research Agent."""
    
    def __init__(self, solutions_agent):
        super().__init__(
            agent_id="solutions_researcher",
            agent_type="AI Solutions Research",
            capabilities=["ai_solutions"]
        )
        self.solutions_agent = solutions_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process AI solutions research request."""
        try:
            industry_problems = payload.get("industry_problems")
            company_industry = payload.get("company_industry")
            company_size = payload.get("company_size", "Unknown")
            
            if not industry_problems or not company_industry:
                raise ValueError("industry_problems and company_industry are required")
            
            # Import the direct function
            from deep_research_system_handoffs import research_ai_solutions_direct
            
            result = research_ai_solutions_direct(
                industry_problems, company_industry, company_size
            )
            
            logger.info(f"AI solutions research completed for {company_industry}")
            return result
            
        except Exception as e:
            logger.error(f"AI solutions research failed: {e}")
            raise

class TavilyResearchAdapter(AgentAdapter):
    """Adapter for the Tavily Research Agent."""
    
    def __init__(self, tavily_agent):
        super().__init__(
            agent_id="tavily_researcher",
            agent_type="Tavily Web Intelligence",
            capabilities=["web_intelligence", "market_research"]
        )
        self.tavily_agent = tavily_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process Tavily research request."""
        try:
            company_name = payload.get("company_name")
            person_name = payload.get("person_name")
            person_role = payload.get("person_role", "Unknown")
            contact_type = payload.get("contact_type", "general")
            company_industry = payload.get("company_industry", "Unknown")
            
            if not company_name:
                raise ValueError("company_name is required")
            
            result = self.tavily_agent.research_lead_with_tavily(
                company_name=company_name,
                person_name=person_name,
                person_role=person_role,
                contact_type=contact_type,
                company_industry=company_industry
            )
            
            logger.info(f"Tavily research completed for {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Tavily research failed: {e}")
            raise

class EmailGenerationAdapter(AgentAdapter):
    """Adapter for the Email Generation Agent."""
    
    def __init__(self, email_agent):
        super().__init__(
            agent_id="email_generator",
            agent_type="Email Generation",
            capabilities=["email_generation"]
        )
        self.email_agent = email_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process email generation request."""
        try:
            person_name = payload.get("person_name")
            company_name = payload.get("company_name")
            research_summary = payload.get("research_summary")
            
            if not person_name or not company_name:
                raise ValueError("person_name and company_name are required")
            
            # Import the direct function
            from deep_research_system_handoffs import generate_email_pitch_direct
            
            result = generate_email_pitch_direct(person_name, company_name, research_summary or "")
            
            logger.info(f"Email generation completed for {person_name} at {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Email generation failed: {e}")
            raise

class HandoffStrategyAdapter(AgentAdapter):
    """Adapter for the Handoff Strategy Agent."""
    
    def __init__(self, handoff_agent):
        super().__init__(
            agent_id="handoff_coordinator",
            agent_type="Handoff Strategy",
            capabilities=["handoff_strategy", "priority_assessment"]
        )
        self.handoff_agent = handoff_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process handoff strategy request."""
        try:
            # Create a ResearchContext object
            from deep_research_system_handoffs import ResearchContext
            
            context = ResearchContext(
                company_name=payload.get("company_name", ""),
                person_name=payload.get("person_name", ""),
                website_url=payload.get("website_url"),
                linkedin_url=payload.get("linkedin_url"),
                email=payload.get("email"),
                phone=payload.get("phone"),
                company_industry=payload.get("company_industry"),
                company_size=payload.get("company_size"),
                person_role=payload.get("person_role"),
                experience_level=payload.get("experience_level"),
                technical_skills=payload.get("technical_skills"),
                decision_power=payload.get("decision_power")
            )
            
            # Import the direct function
            from deep_research_system_handoffs import determine_handoff_strategy_direct
            
            result = determine_handoff_strategy_direct(context)
            
            logger.info(f"Handoff strategy determined for {context.company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Handoff strategy failed: {e}")
            raise

class ResearchReportAdapter(AgentAdapter):
    """Adapter for the Research Report Agent."""
    
    def __init__(self, report_agent):
        super().__init__(
            agent_id="research_reporter",
            agent_type="Research Report",
            capabilities=["report_generation", "data_compilation"]
        )
        self.report_agent = report_agent
    
    async def process_request(self, payload: Dict[str, Any]) -> Any:
        """Process research report generation request."""
        try:
            company_name = payload.get("company_name")
            person_name = payload.get("person_name")
            website_research = payload.get("website_research", "")
            linkedin_research = payload.get("linkedin_research", "")
            
            if not company_name or not person_name:
                raise ValueError("company_name and person_name are required")
            
            # Import the direct function
            from deep_research_system_handoffs import compile_research_report_direct
            
            result = compile_research_report_direct(
                company_name, person_name, website_research, linkedin_research
            )
            
            logger.info(f"Research report generated for {person_name} at {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Research report generation failed: {e}")
            raise

def create_agent_adapters() -> Dict[str, AgentAdapter]:
    """Create all agent adapters."""
    adapters = {}
    
    try:
        # Website Research Adapter
        from research_agent_website import WebsiteResearchAgent
        website_agent = WebsiteResearchAgent()
        adapters["website_researcher"] = WebsiteResearchAdapter(website_agent)
        logger.info("Website Research Adapter created")
    except ImportError as e:
        logger.warning(f"Website Research Agent not available: {e}")
    
    try:
        # LinkedIn Research Adapter
        from research_agent_linkedin import LinkedInResearchAgent
        linkedin_agent = LinkedInResearchAgent()
        adapters["linkedin_analyzer"] = LinkedInResearchAdapter(linkedin_agent)
        logger.info("LinkedIn Research Adapter created")
    except ImportError as e:
        logger.warning(f"LinkedIn Research Agent not available: {e}")
    
    try:
        # Industry Problems Adapter
        from research_agent_industry_problems import IndustryProblemsAgent
        problems_agent = IndustryProblemsAgent()
        adapters["industry_problems_specialist"] = IndustryProblemsAdapter(problems_agent)
        logger.info("Industry Problems Adapter created")
    except ImportError as e:
        logger.warning(f"Industry Problems Agent not available: {e}")
    
    try:
        # Solutions Research Adapter
        from research_agent_solutions import SolutionsAgent
        solutions_agent = SolutionsAgent()
        adapters["solutions_researcher"] = SolutionsResearchAdapter(solutions_agent)
        logger.info("Solutions Research Adapter created")
    except ImportError as e:
        logger.warning(f"Solutions Research Agent not available: {e}")
    
    try:
        # Tavily Research Adapter
        from research_agent_tavily import TavilyResearchAgent
        tavily_agent = TavilyResearchAgent()
        adapters["tavily_researcher"] = TavilyResearchAdapter(tavily_agent)
        logger.info("Tavily Research Adapter created")
    except ImportError as e:
        logger.warning(f"Tavily Research Agent not available: {e}")
    
    try:
        # Email Generation Adapter
        from research_agent_email import EmailGenerationAgent
        email_agent = EmailGenerationAgent()
        adapters["email_generator"] = EmailGenerationAdapter(email_agent)
        logger.info("Email Generation Adapter created")
    except ImportError as e:
        logger.warning(f"Email Generation Agent not available: {e}")
    
    try:
        # Handoff Strategy Adapter
        from deep_research_system_handoffs import handoff_coordinator
        adapters["handoff_coordinator"] = HandoffStrategyAdapter(handoff_coordinator)
        logger.info("Handoff Strategy Adapter created")
    except ImportError as e:
        logger.warning(f"Handoff Strategy Agent not available: {e}")
    
    try:
        # Research Report Adapter
        from deep_research_system_handoffs import compile_research_report_direct
        adapters["research_reporter"] = ResearchReportAdapter(None)  # No actual agent needed
        logger.info("Research Report Adapter created")
    except ImportError as e:
        logger.warning(f"Research Report Agent not available: {e}")
    
    logger.info(f"Created {len(adapters)} agent adapters")
    return adapters

async def register_all_agents(agent_manager) -> bool:
    """Register all available agents with the agent manager."""
    try:
        adapters = create_agent_adapters()
        
        for agent_id, adapter in adapters.items():
            success = agent_manager.register_agent(
                agent_id=agent_id,
                agent=adapter,
                agent_type=adapter.agent_type,
                capabilities=adapter.capabilities,
                max_concurrent=5
            )
            
            if success:
                # Start the agent
                await agent_manager.start_agent(agent_id)
                logger.info(f"Agent {agent_id} registered and started successfully")
            else:
                logger.error(f"Failed to register agent {agent_id}")
        
        logger.info(f"Successfully registered {len(adapters)} agents")
        return True
        
    except Exception as e:
        logger.error(f"Failed to register agents: {e}")
        return False
