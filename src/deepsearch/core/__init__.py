"""
Deep Research System - Core Package

Contains core system components including the agent manager,
research system, and handoff logic.
"""

from .agent_manager import AgentManager, RequestPriority, AgentStatus
from .research_system import DeepResearchSystem
from .handoff_system import HandoffSystem, ResearchContext, AgentType

__all__ = [
    "AgentManager",
    "RequestPriority", 
    "AgentStatus",
    "DeepResearchSystem",
    "HandoffSystem",
    "ResearchContext",
    "AgentType"
]