"""
Base Agent Class for Deep Research System

Provides common functionality and interface for all specialized agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    INITIALIZING = "initializing"

@dataclass
class AgentResult:
    """Standard result format for all agents."""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseAgent(ABC):
    """Base class for all research agents."""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = AgentStatus.OFFLINE
        self.logger = logging.getLogger(f"{__name__}.{agent_type}")
    
    @abstractmethod
    async def process_request(self, request_data: Dict[str, Any]) -> AgentResult:
        """Process a request and return standardized result."""
        pass
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent."""
        pass
    
    async def shutdown(self) -> bool:
        """Shutdown the agent gracefully."""
        self.status = AgentStatus.OFFLINE
        self.logger.info(f"Agent {self.agent_id} shutdown")
        return True
    
    def get_status(self) -> AgentStatus:
        """Get current agent status."""
        return self.status
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status.value
        }