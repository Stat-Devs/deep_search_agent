# Deep Research System - Project Structure

This document describes the organized structure of the Deep Research System project.

## Directory Structure

```
deepsearch_project/
├── src/                          # Source code
│   └── deepsearch/              # Main package
│       ├── __init__.py          # Package initialization
│       ├── app.py               # Main Chainlit application
│       ├── agents/              # AI Agents
│       │   ├── __init__.py
│       │   ├── base_agent.py    # Base agent class
│       │   ├── website_agent.py # Website research agent
│       │   ├── linkedin_agent.py # LinkedIn research agent
│       │   ├── email_agent.py   # Email generation agent
│       │   ├── tavily_agent.py  # Tavily web intelligence agent
│       │   ├── industry_problems_agent.py # Industry analysis agent
│       │   └── solutions_agent.py # AI solutions research agent
│       ├── core/                # Core system components
│       │   ├── __init__.py
│       │   ├── agent_manager.py # Centralized agent orchestration
│       │   ├── research_system.py # Standard research system
│       │   ├── handoff_system.py # Advanced handoff-enabled system
│       │   └── agent_adapters.py # Agent adapter implementations
│       ├── services/            # External service integrations
│       │   ├── __init__.py
│       │   ├── openai_service.py # OpenAI API service
│       │   ├── tavily_service.py # Tavily API service
│       │   └── web_scraping_service.py # Web scraping utilities
│       └── utils/               # Utility functions
│           ├── __init__.py
│           ├── config.py        # Configuration management
│           ├── logger.py        # Logging configuration
│           └── validators.py    # Input validation utilities
├── tests/                       # Test suite
│   ├── unit/                   # Unit tests
│   │   ├── test_agent_manager.py
│   │   ├── test_app.py
│   │   ├── test_system.py
│   │   └── ... (other test files)
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── examples/                   # Example usage and demos
│   ├── demos/                  # Demo scripts
│   │   ├── demo_agent_manager.py
│   │   ├── demo_handoff_system.py
│   │   └── demo_tavily_handoff.py
│   └── samples/                # Sample usage
│       └── run_research_system.py
├── config/                     # Configuration files
│   └── .env.example           # Environment variables template
├── docs/                       # Documentation
│   ├── PROJECT_STRUCTURE.md   # This file
│   ├── API_REFERENCE.md       # API documentation
│   └── DEPLOYMENT.md          # Deployment guide
├── scripts/                    # Utility scripts
├── deployment/                 # Deployment configurations
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── deploy-digitalocean.sh
│   ├── deploy.sh
│   └── ... (other deployment files)
├── logs/                       # Log files (created at runtime)
├── uploads/                    # File uploads (created at runtime)
├── main.py                     # Main entry point
├── pyproject.toml             # Project dependencies
├── requirements.txt           # Python dependencies
├── uv.lock                    # UV lock file
└── README.md                  # Project documentation
```

## Package Organization

### Core Components (`src/deepsearch/core/`)

- **AgentManager**: Centralized orchestration and management of all agents
- **ResearchSystem**: Standard sequential research workflow
- **HandoffSystem**: Advanced collaborative AI team with intelligent handoffs
- **AgentAdapters**: Adapter implementations for different agent types

### Agents (`src/deepsearch/agents/`)

Each agent is a specialized AI component with specific responsibilities:

- **WebsiteAgent**: Company website analysis and opportunity identification
- **LinkedInAgent**: Professional profile research and decision-maker analysis
- **EmailAgent**: Personalized email pitch generation
- **TavilyAgent**: Real-time web intelligence and market research
- **IndustryProblemsAgent**: Industry-specific challenge identification
- **SolutionsAgent**: AI and data analytics solution recommendations

### Services (`src/deepsearch/services/`)

External service integrations:

- **OpenAIService**: OpenAI API integration and management
- **TavilyService**: Tavily web intelligence API integration
- **WebScrapingService**: Web scraping utilities and tools

### Utilities (`src/deepsearch/utils/`)

Common utilities and helpers:

- **Config**: Centralized configuration management
- **Logger**: Logging setup and configuration
- **Validators**: Input validation and sanitization

## Key Benefits of This Structure

1. **Separation of Concerns**: Each component has a clear, single responsibility
2. **Scalability**: Easy to add new agents, services, or utilities
3. **Maintainability**: Clear organization makes code easier to understand and modify
4. **Testability**: Tests are organized by type and scope
5. **Deployment**: Deployment configurations are centralized
6. **Documentation**: Comprehensive documentation structure

## Import Structure

With this organization, imports follow a clear pattern:

```python
# Core components
from deepsearch.core import AgentManager, ResearchSystem, HandoffSystem

# Specific agents
from deepsearch.agents import WebsiteAgent, LinkedInAgent, EmailAgent

# Services
from deepsearch.services import OpenAIService, TavilyService

# Utilities
from deepsearch.utils import Config, setup_logging, validate_lead_data
```

## Development Workflow

1. **Adding New Agents**: Create new agent files in `src/deepsearch/agents/`
2. **Adding Services**: Add service integrations in `src/deepsearch/services/`
3. **Testing**: Add tests in appropriate `tests/` subdirectories
4. **Documentation**: Update relevant docs in `docs/`
5. **Deployment**: Update deployment configs in `deployment/`

This structure provides a solid foundation for scaling the Deep Research System while maintaining code quality and organization.