# Deep Research System - Lead Intelligence Platform

An AI-powered system for deep lead research and personalized outreach in the data analytics services space, featuring intelligent handoffs and real-time web intelligence via Tavily API.

## 🏗️ **New Organized Structure**

This project has been restructured for better maintainability, scalability, and organization:

```
deepsearch_project/
├── src/deepsearch/           # Main package with organized modules
├── tests/                    # Comprehensive test suite
├── examples/                 # Demos and sample usage
├── docs/                     # Documentation
├── deployment/               # Deployment configurations
└── main.py                   # Main entry point
```

**See [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed organization.**

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- Gemini API key  
- Tavily API key

### Installation
```bash
# Install dependencies
pip install uv
uv sync

# Set up environment variables
cp config/.env.example .env  # Create .env file
```

### Configuration
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Run the System

#### Web Interface (Recommended)
```bash
# Run with Chainlit web interface
python main.py --mode web

# Or specify port and host
python main.py --mode web --port 8080 --host 0.0.0.0
```

#### Interactive Mode
```bash
# Run in interactive CLI mode
python main.py --mode interactive
```

#### Legacy Entry Points
```bash
# Run examples and demos
python examples/samples/run_research_system.py
python examples/demos/demo_handoff_system.py
python examples/demos/demo_tavily_handoff.py
```

## 🏗️ System Architecture

The system consists of **two versions** - a standard sequential system and an advanced handoff-enabled system with Tavily integration:

### **Standard System (Sequential Processing)**
- **Lead Research Coordinator** - Main orchestrator
- **Website Research Agent** - Company website analysis
- **LinkedIn Research Agent** - Professional profile analysis  
- **Email Generation Agent** - Personalized pitch creation

### **Handoff-Enabled System (Collaborative AI Team)**
- **Intelligent Coordinator** - Makes handoff decisions
- **Executive Specialist** - Handles C-suite and high-level contacts
- **Technical Specialist** - Manages technical contacts and engineers
- **Tavily Research Agent** - Real-time web intelligence and market research
- **Industry Problems Agent** - Identifies potential business challenges and pain points
- **Solutions Research Agent** - Researches AI and data analytics solutions
- **Context Preservation** - Maintains information between agents
- **Dynamic Routing** - Adapts strategy based on lead characteristics

## 🎯 **Specialized Agents**

### **Industry Problems Agent**
- **Purpose**: Identifies potential industry problems, challenges, and pain points that leads may face
- **Capabilities**: Industry-specific problem frameworks, AI-enhanced problem identification, business impact analysis

### **Solutions Research Agent**
- **Purpose**: Researches and identifies AI and data analytics solutions for identified industry problems
- **Capabilities**: Problem-to-solution mapping, technology stack recommendations, ROI analysis

### **Agent Manager - Centralized Orchestration**
- **Purpose**: Centralized orchestration and management for all agents in the system
- **Key Features**: Centralized agent management, intelligent request routing, load balancing, health monitoring, performance metrics

## 🔄 **High-Level System Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           DEEP RESEARCH SYSTEM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LEAD INPUT    │───▶│  COORDINATOR     │───▶│  RESEARCH       │───▶│  FINAL REPORT   │
│                 │    │     AGENT        │    │    AGENTS       │    │                 │
│ • Company Name  │    │                  │    │                 │    │ • Comprehensive │
│ • Person Name   │    │ • Analyzes Lead  │    │ • Website       │    │   Analysis      │
│ • Website URL   │    │ • Determines     │    │ • LinkedIn      │    │ • Email Pitch   │
│ • LinkedIn URL  │    │   Strategy       │    │ • Tavily        │    │ • Next Steps    │
│ • Email/Phone   │    │ • Routes to      │    │ • Email Gen     │    │ • Handoff       │
└─────────────────┘    │   Specialists    │    └─────────────────┘    │   Decisions     │
                       └──────────────────┘                           └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  HANDOFF LOGIC   │
                       │                  │
                       │ • Contact Level  │
                       │ • Decision Power │
                       │ • Technical      │
                       │   Skills         │
                       │ • Priority       │
                       │   Assessment     │
                       └──────────────────┘
                                │
                                ▼
                ┌─────────────────────────────────────┐
                │         SPECIALIST AGENTS           │
                │                                     │
                │  ┌─────────────────┐                │
                │  │   EXECUTIVE     │                │
                │  │   SPECIALIST    │                │
                │  │                 │                │
                │  │ • CEO/CTO/CFO   │                │
                │  │ • Strategic     │                │
                │  │ • ROI Focus     │                │
                │  │ • High Priority │                │
                │  └─────────────────┘                │
                │                                     │
                │  ┌─────────────────┐                │
                │  │   TECHNICAL     │                │
                │  │   SPECIALIST    │                │
                │  │                 │                │
                │  │ • Engineers     │                │
                │  │ • Analysts      │                │
                │  │ • Integration   │                │
                │  │ • Implementation│                │
                │  └─────────────────┘                │
                │                                     │
                │  ┌─────────────────┐                │
                │  │   TAVILY        │                │
                │  │   RESEARCH      │                │
                │  │                 │                │
                │  │ • Web Intel     │                │
                │  │ • Market Data   │                │
                │  │ • News Updates  │                │
                │  │ • Competitive   │                │
                │  └─────────────────┘                │
                └─────────────────────────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ CONTEXT PRESERVATION │
                       │                  │
                       │ • Shared Context │
                       │ • Research Data  │
                       │ • Handoff Info   │
                       │ • Communication  │
                       │   Strategy       │
                       └──────────────────┘
```

## 🆕 **Tavily Research Agent**

The **Tavily Research Agent** provides real-time web intelligence and market research:

### **Key Features:**
- **Real-time Web Research** - Live company news, updates, and market data
- **Contact-Type Specific Analysis** - Tailored research based on handoff decisions
- **Market Intelligence** - Industry trends, competitive landscape, growth indicators
- **Opportunity Analysis** - Immediate and strategic opportunities with timing recommendations

## 🔄 **How the Handoff System Works**

### **1. Lead Input & Analysis**
- System receives lead information (company, person, website, LinkedIn)
- Creates comprehensive research context
- Analyzes contact characteristics and decision-making power

### **2. Intelligent Routing**
- **Executive Contacts**: CEO, CTO, CFO → Executive Specialist (Priority 5/5)
- **Technical Contacts**: Engineers, Analysts → Technical Specialist (Priority 4/5)
- **General Contacts**: Managers, Coordinators → General Coordinator (Priority 3/5)

### **3. Specialized Processing**
- **Executive Specialist**: Strategic business outcomes, ROI focus, executive tone
- **Technical Specialist**: Technical integration, implementation benefits, technical ROI
- **General Coordinator**: Professional approach, value propositions, standard timeline

### **4. Context Preservation**
- All research findings shared between agents
- Handoff decisions and reasoning documented
- Communication strategy and timeline coordinated

## 📋 **Usage Examples**

### **Basic Handoff Usage**
```python
from deepsearch.core import HandoffSystem

# Research a lead with automatic handoffs
handoff_system = HandoffSystem()
result = await handoff_system.research_lead_with_handoffs(
    company_name="TechCorp Inc.",
    person_name="John Smith",
    website_url="https://techcorp.com",
    email="john@techcorp.com"
)
```

### **Tavily Integration**
```python
from deepsearch.agents import TavilyAgent

# Enhanced research with web intelligence
tavily_agent = TavilyAgent()
research_results = await tavily_agent.research_lead_with_tavily(
    company_name="InnovateTech Solutions",
    person_name="Sarah Chen",
    person_role="CTO",
    contact_type="executive",
    company_industry="Technology"
)
```

## 🧪 **Testing & Validation**

### **Run All Tests:**
```bash
# Test handoff system structure
python tests/unit/test_handoff_structure.py

# Test Tavily integration
python tests/unit/test_handoff_tavily_integration.py

# Test Tavily agent functionality
python tests/unit/test_tavily_agent.py

# Run demo with sample data
python examples/demos/demo_tavily_handoff.py
```

## 🔧 **Key Features**

### **Intelligent Research Coordination**
- **Automated workflow** from lead identification to email generation
- **Context-aware analysis** based on company and person research
- **Comprehensive reporting** with actionable insights
- **Role-based communication** strategies (executive vs. technical)

### **Advanced Handoff System**
- **Intelligent Routing** - Automatically detects contact type and level
- **Agent Collaboration** - Agents work together, building on each other's findings
- **Specialized Processing** - Tailored approach for each contact type
- **Context Preservation** - Shared state management between agent transitions

### **Tavily Web Intelligence**
- **Real-time Research** - Live company news, updates, and market data
- **Contact-Type Specific** - Research focus based on handoff decisions
- **Market Context** - Industry trends, competitive landscape, growth indicators

### **Industry Problems & Solutions Analysis**
- **Problem Identification** - Industry-specific challenges and pain points
- **Solution Mapping** - AI and data analytics solutions for identified problems
- **Business Impact Analysis** - Quantified impact and urgency assessment

## 🎯 **Agent Specializations**

| Contact Type | Specialist | Approach | Priority | Timeline |
|--------------|------------|----------|----------|----------|
| **Executive** | Executive Specialist | Strategic, ROI-focused | ⭐⭐⭐⭐⭐ (5/5) | 2-3 days |
| **Technical** | Technical Specialist | Technical integration + business outcomes | ⭐⭐⭐⭐ (4/5) | 3-5 days |
| **General** | General Coordinator | Professional, value-focused | ⭐⭐⭐ (3/5) | 5-7 days |

## 🚀 **Deployment Instructions**

### **🐳 Deploy with Docker (Recommended)**

1. **Ensure Docker is Running:**
   - Start Docker Desktop on your machine
   - Verify with: `docker --version`

2. **Set Up Environment:**
   ```bash
   # Copy environment file
   cp config/.env.example .env
   
   # Edit with your API keys
   nano .env
   ```

3. **Deploy with Docker Compose:**
   ```bash
   # Make script executable (first time only)
   chmod +x deployment/docker-deploy.sh
   
   # Run deployment
   ./deployment/docker-deploy.sh
   ```

4. **Access Your App:**
   - Open browser to: `http://localhost:8000`
   - Your StatDevs Sales Intelligence System is now running!

### **🔧 Docker Management Commands**

#### **Using Docker Compose (Recommended)**
```bash
# Start the service
docker-compose -f deployment/docker-compose.yml up -d

# View logs
docker-compose -f deployment/docker-compose.yml logs -f

# Stop the service
docker-compose -f deployment/docker-compose.yml down

# Restart the service
docker-compose -f deployment/docker-compose.yml restart

# Update and restart
docker-compose -f deployment/docker-compose.yml up --build -d

# Check status
docker-compose -f deployment/docker-compose.yml ps
```

## 🌐 Deployment to Digital Ocean

### Automated CI/CD Deployment

The system includes a complete GitHub Actions CI/CD pipeline for automated deployment to Digital Ocean.

#### Quick Deployment Setup

1. **Setup Digital Ocean Server** (One-time):
   ```bash
   ./deployment/setup-digitalocean.sh
   ```

2. **Configure GitHub Secrets**:
   ```bash
   ./deployment/setup-github-secrets.sh
   ```

3. **Deploy via GitHub Actions**:
   ```bash
   ./deployment/deploy.sh
   ```

#### Manual Deployment

For manual deployment to Digital Ocean:
```bash
# Set environment variables
export OPENAI_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"
export TAVILY_API_KEY="your_key_here"

# Deploy to Digital Ocean
./deployment/deploy-digitalocean.sh
```

#### Access Your Application

After deployment, your application will be available at:
- **Production URL**: http://143.110.183.47:8000
- **GitHub Actions**: Monitor deployments in your repository's Actions tab

#### Required GitHub Secrets

Configure these secrets in your GitHub repository settings:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `DO_HOST` | `143.110.183.47` | Digital Ocean server IP |
| `DO_USERNAME` | `root` | Server username |
| `DO_SSH_KEY` | `[Your private SSH key]` | Private SSH key for server access |
| `OPENAI_API_KEY` | `[Your OpenAI API key]` | OpenAI API key |
| `GEMINI_API_KEY` | `[Your Gemini API key]` | Google Gemini API key |
| `TAVILY_API_KEY` | `[Your Tavily API key]` | Tavily API key |

For detailed deployment instructions, see [DEPLOYMENT.md](docs/DEPLOYMENT.md).

## 🔍 **Troubleshooting**

### **Common Issues**
- **API Key Errors**: Verify `.env` file contains valid keys
- **Dependency Issues**: Run `uv sync --reinstall`
- **Website Blocking**: System handles gracefully with fallbacks
- **Handoff Errors**: Check test output for system validation

### **Testing & Validation**
```bash
# Test basic functionality
python tests/unit/test_system.py

# Test handoff system
python tests/unit/test_handoff_structure.py

# Test Tavily integration
python tests/unit/test_handoff_tavily_integration.py

# Test new agents
python tests/unit/test_industry_problems_agent.py
python tests/unit/test_solutions_agent.py

# Test Agent Manager
python tests/unit/test_agent_manager.py
python examples/demos/demo_agent_manager.py

# Test Integration
python main.py --mode web

# Test with specific leads
python tests/unit/test_christian_lead.py
```

## 📞 **Support & Contributing**

### **Getting Help**
1. Check the test output for common issues
2. Verify API keys are correctly set
3. Ensure all dependencies are installed
4. Review error messages for specific guidance
5. Check generated reports for insights

### **Contributing**
- Fork the repository
- Create feature branches
- Submit pull requests
- Follow Python coding standards
- Test with real lead data

## 📄 **License**

This project is designed for business use in lead research and outreach. Please ensure compliance with relevant data protection and scraping regulations in your jurisdiction.

---

**Built with ❤️ using OpenAI Agents, Python, and Tavily API** | *Transform manual lead research into intelligent AI-powered insights with real-time web intelligence!*