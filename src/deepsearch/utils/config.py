"""
Configuration Management for Deep Research System

Centralized configuration handling with environment variable support.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """Configuration class for the Deep Research System."""
    
    # API Keys
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    
    # Model Configuration
    openai_model: str = "gpt-4"
    gemini_model: str = "gemini-2.5-flash"
    
    # System Configuration
    max_retries: int = 3
    timeout_seconds: int = 60
    log_level: str = "INFO"
    
    # Business Context
    company_name: str = "StatDevs"
    services: Dict[str, str] = None
    value_propositions: list = None
    
    def __post_init__(self):
        """Initialize configuration from environment variables."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        
        # Override with environment variables if present
        self.openai_model = os.getenv("OPENAI_MODEL", self.openai_model)
        self.gemini_model = os.getenv("GEMINI_MODEL", self.gemini_model)
        self.max_retries = int(os.getenv("MAX_RETRIES", self.max_retries))
        self.timeout_seconds = int(os.getenv("TIMEOUT_SECONDS", self.timeout_seconds))
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)
        
        # Initialize business context
        if self.services is None:
            self.services = {
                "data_engineering": "Unify, clean, and connect data for smarter decision-making",
                "data_science_ml": "Leverage AI to spot trends, predict outcomes, and automate tasks",
                "artificial_intelligence": "Harness AI to automate tasks, uncover insights, and drive smarter decisions",
                "business_intelligence": "Turn data into clear, actionable insights with real-time dashboards"
            }
        
        if self.value_propositions is None:
            self.value_propositions = [
                "82% Reduction in Data Integration Time",
                "3.2x Return on AI Investment", 
                "24/7 Mobile Access to Key Metrics",
                "47% Cost Reduction in Customer Support",
                "Robust data engineering accelerates insights by 35-45%",
                "Reliable pipelines reduce data issues by 82%",
                "AI automation cuts manual tasks by 67%",
                "Machine learning improves predictive accuracy by 43%"
            ]
    
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
        if not self.gemini_api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables")
        if not self.tavily_api_key:
            print("Warning: TAVILY_API_KEY not found in environment variables")
        
        return True
    
    def get_business_context(self) -> Dict[str, Any]:
        """Get business context for StatDevs."""
        return {
            "company_name": self.company_name,
            "services": self.services,
            "value_propositions": self.value_propositions,
            "expertise": ["Python", "R", "R Shiny", "Streamlit", "Apache Superset", "AWS", "Machine Learning", "Predictive Modeling"],
            "industries": ["Research Organizations", "Supply Chain", "Marketing", "Fintech", "Non-Profits", "Manufacturing"],
            "process": ["Discovery Call", "Assessment", "Solution Design", "Phased Implementation"]
        }

# Global configuration instance
config = Config()