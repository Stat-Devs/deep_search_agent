"""
Deep Research System - Agents Package

Contains all specialized AI agents for lead research and analysis.
"""

from .base_agent import BaseAgent
from .website_agent import WebsiteResearchAgent
from .linkedin_agent import LinkedInResearchAgent
from .email_agent import EmailGenerationAgent
from .tavily_agent import TavilyResearchAgent
from .industry_problems_agent import IndustryProblemsAgent
from .solutions_agent import SolutionsResearchAgent

__all__ = [
    "BaseAgent",
    "WebsiteResearchAgent", 
    "LinkedInResearchAgent",
    "EmailGenerationAgent",
    "TavilyResearchAgent",
    "IndustryProblemsAgent",
    "SolutionsResearchAgent"
]