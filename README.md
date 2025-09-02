# Deep Research System - Lead Intelligence Platform

An AI-powered system for deep lead research and personalized outreach in the data analytics services space, featuring intelligent handoffs and real-time web intelligence via Tavily API.

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
cp .env.example .env  # Create .env file
```

### Configuration
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Run the System
```bash
# Interactive mode
uv run run_research_system.py

# Test handoff system
uv run demo_handoff_system.py

# Test Tavily integration
uv run demo_tavily_handoff.py

# Run comprehensive tests
uv run test_system.py
```

## 🌐 Deployment to Digital Ocean

### Automated CI/CD Deployment

The system includes a complete GitHub Actions CI/CD pipeline for automated deployment to Digital Ocean.

#### Quick Deployment Setup

1. **Setup Digital Ocean Server** (One-time):
   ```bash
   ./setup-digitalocean.sh
   ```

2. **Configure GitHub Secrets**:
   ```bash
   ./setup-github-secrets.sh
   ```

3. **Deploy via GitHub Actions**:
   ```bash
   ./deploy.sh
   ```

#### Manual Deployment

For manual deployment to Digital Ocean:
```bash
# Set environment variables
export OPENAI_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"
export TAVILY_API_KEY="your_key_here"

# Deploy to Digital Ocean
./deploy-digitalocean.sh
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

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

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

## 🔄 **System Workflow Diagram**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LEAD INPUT    │───▶│  INITIAL         │───▶│  HANDOFF        │───▶│  SPECIALIZED    │
│                 │    │  RESEARCH        │    │  DECISION       │    │  PROCESSING     │
│ • Company Info  │    │                  │    │                  │    │                 │
│ • Contact Info  │    │ • Website        │    │ • Contact Level │    │ • Executive     │
│ • URLs          │    │   Analysis       │    │ • Decision      │    │   Approach      │
│ • Contact       │    │ • LinkedIn       │    │   Power         │    │ • Technical     │
│   Details       │    │   Research       │    │ • Tavily         │    │   Skills        │
└─────────────────┘    │ • Tavily         │    │ • Priority      │    │   Market Data   │
                       │   Web Intel      │    │   Level         │    └─────────────────┘
                       └──────────────────┘    └──────────────────┘              │
                                │                       │                        │
                                ▼                       ▼                        ▼
                       ┌──────────────────┐    ┌──────────────────┐    ┌─────────────────┐
                       │  CONTEXT         │    │  AGENT           │    │  FINAL          │
                       │  PRESERVATION    │    │  SELECTION       │    │  OUTPUT         │
                       │                  │    │                  │    │                 │
                       │ • Research       │    │ • Executive      │    │ • Comprehensive │
                       │   Findings       │    │   Specialist     │    │   Report        │
                       │ • Company        │    │ • Technical      │    │ • Personalized  │
                       │   Intelligence   │    │   Specialist     │    │   Email Pitch   │
                       │ • Market         │    │ • Tavily         │    │ • Handoff       │
                       │   Context        │    │   Research       │    │   Strategy      │
                       │ • Handoff        │    │ • Priority       │    │ • Next Steps    │
                       │   Decisions      │    │   Assignment     │    │ • Timeline      │
                       └──────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🤖 **Agent Interaction Flow**

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    COORDINATOR AGENT                        │
                    │                                                             │
                    │  • Receives Lead Input                                     │
                    │  • Initiates Research                                      │
                    │  • Analyzes Characteristics                                │
                    │  • Makes Handoff Decision                                  │
                    │  • Integrates Tavily Data                                  │
                    └─────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    HANDOFF LOGIC                            │
                    │                                                             │
                    │  IF Contact = CEO/CTO/CFO/Director/VP                      │
                    │     → Route to EXECUTIVE SPECIALIST                        │
                    │     → Priority: ⭐⭐⭐⭐⭐ (5/5)                              │
                    │     → Tone: Strategic, ROI-focused                         │
                    │     → Timeline: 2-3 business days                          │
                    │                                                             │
                    │  IF Contact = Engineer/Analyst/Scientist                   │
                    │     → Route to TECHNICAL SPECIALIST                        │
                    │     → Priority: ⭐⭐⭐⭐ (4/5)                               │
                    │     → Tone: Technical + Business outcomes                  │
                    │     → Timeline: 3-5 business days                          │
                    │                                                             │
                    │  IF Contact = General/Manager/Coordinator                  │
                    │     → Route to GENERAL COORDINATOR                         │
                    │     → Priority: ⭐⭐⭐ (3/5)                                │
                    │     → Tone: Professional, value-focused                    │
                    │     → Timeline: 5-7 business days                          │
                    └─────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                ┌─────────────────────────────────────────────────────────────────┐
                │                    SPECIALIST AGENTS                           │
                │                                                               │
                │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
                │  │   EXECUTIVE     │  │   TECHNICAL     │  │     TAVILY      │ │
                │  │   SPECIALIST    │  │   SPECIALIST    │  │    RESEARCH     │ │
                │  │                 │  │                 │  │                 │ │
                │  │ • Strategic     │  │ • Technical     │  │ • Web Intel     │ │
                │  │   Value Prop    │  │   Integration   │  │ • Market Data   │ │
                │  │ • Business      │  │ • Implementation│  │ • News Updates  │ │
                │  │   Impact        │  │ • ROI Metrics   │  │ • Competitive   │ │
                │  │ • ROI Focus     │  │ • Technical     │  │   Analysis      │ │
                │  │ • High Priority │  │   Benefits      │  │ • Industry      │ │
                │  └─────────────────┘  └─────────────────┘  │   Trends        │ │
                └─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    FINAL OUTPUT                            │
                    │                                                             │
                    │  • Comprehensive Research Report                           │
                    │  • Personalized Email Pitch                               │
                    │  • Handoff Strategy & Reasoning                           │
                    │  • Priority Level & Timeline                              │
                    │  • Communication Strategy                                 │
                    │  • Market Context & Competitive Insights                  │
                    │  • Next Steps & Recommendations                           │
                    └─────────────────────────────────────────────────────────────┘
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
from deep_research_system_handoffs import research_lead_with_handoffs

# Research a lead with automatic handoffs
result = research_lead_with_handoffs(
    company_name="TechCorp Inc.",
    person_name="John Smith",
    website_url="https://techcorp.com",
    email="john@techcorp.com"
)
```

### **Tavily Integration**
```python
from research_agent_tavily import TavilyResearchAgent

# Enhanced research with web intelligence
tavily_agent = TavilyResearchAgent()
research_results = tavily_agent.research_lead_with_tavily(
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
uv run test_handoff_structure.py

# Test Tavily integration
uv run test_handoff_tavily_integration.py

# Test Tavily agent functionality
uv run test_tavily_agent.py

# Run demo with sample data
uv run demo_tavily_handoff.py
```

## 📁 **File Structure**

```
deepsearch_project/
├── deep_research_system.py              # Standard sequential system
├── deep_research_system_handoffs.py     # Advanced handoff-enabled system
├── research_agent_tavily.py            # 🆕 Tavily research agent
├── research_agent_industry_problems.py  # 🆕 Industry problems identification agent
├── research_agent_solutions.py          # 🆕 AI solutions research agent
├── agent_manager.py                     # 🆕 Centralized agent orchestration
├── app.py                               # 🆕 Updated with Agent Manager integration
├── research_agent_website.py           # Website research agent
├── research_agent_linkedin.py          # LinkedIn research agent
├── research_agent_email.py             # Email generation agent
├── demo_handoff_system.py              # Handoff system demo
├── demo_tavily_handoff.py              # 🆕 Tavily integration demo
├── test_handoff_structure.py           # 🆕 Handoff system tests
├── test_handoff_tavily_integration.py  # 🆕 Integration tests
├── test_tavily_agent.py                # 🆕 Tavily agent tests
├── test_system.py                      # System tests
├── pyproject.toml                      # Dependencies (includes tavily-python)
└── README.md                           # This documentation
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
   cp env.example .env
   
   # Edit with your API keys
   nano .env
   ```

3. **Deploy with Docker Compose:**
   ```bash
   # Make script executable (first time only)
   chmod +x docker-deploy.sh
   
   # Run deployment
   ./docker-deploy.sh
   ```

4. **Access Your App:**
   - Open browser to: `http://localhost:8000`
   - Your StatDevs Sales Intelligence System is now running!

### **🔧 Docker Management Commands**

#### **Using Docker Compose (Recommended)**
```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down

# Restart the service
docker-compose restart

# Update and restart
docker-compose up --build -d

# Check status
docker-compose ps
```

#### **Using Docker Directly**
```bash
# Build image
docker build -t statdevs-sales-ai .

# Run container
docker run -d --name statdevs-sales-ai -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  -e OPENAI_TRACE=1 \
  statdevs-sales-ai

# View logs
docker logs -f statdevs-sales-ai

# Stop container
docker stop statdevs-sales-ai

# Remove container
docker rm statdevs-sales-ai
```

## 🚨 **Docker Troubleshooting**

### **Common Issues & Solutions**

#### **Port Already in Use**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
docker run -p 8001:8000 statdevs-sales-ai
```

#### **Container Won't Start**
```bash
# Check container logs
docker logs statdevs-sales-ai

# Check container status
docker ps -a

# Remove and recreate
docker rm statdevs-sales-ai
docker run -d --name statdevs-sales-ai -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  statdevs-sales-ai
```

## 🔍 **Troubleshooting**

### **Common Issues**
- **API Key Errors**: Verify `.env` file contains valid keys
- **Dependency Issues**: Run `uv sync --reinstall`
- **Website Blocking**: System handles gracefully with fallbacks
- **Handoff Errors**: Check test output for system validation

### **Testing & Validation**
```bash
# Test basic functionality
uv run test_system.py

# Test handoff system
uv run test_handoff_structure.py

# Test Tavily integration
uv run test_handoff_tavily_integration.py

# Test new agents
uv run python research_agent_industry_problems.py
uv run python research_agent_solutions.py

# Test Agent Manager
uv run python test_agent_manager.py
uv run python demo_agent_manager.py

# Test Integration
uv run python app.py

# Test with specific leads
uv run test_christian_lead.py
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

