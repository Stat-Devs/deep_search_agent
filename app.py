"""
Example Integration: App.py with Agent Manager

This file shows how to integrate the Agent Manager with your existing
Chainlit application to provide centralized agent orchestration.
"""

import chainlit as cl
import asyncio
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the Agent Manager
from agent_manager import initialize_agent_manager, get_agent_manager
from agent_adapters import register_all_agents

# Global variables
agent_manager = None
PROBLEMS_SOLUTIONS_AVAILABLE = False

async def initialize_system():
    """Initialize the Agent Manager and register all agents."""
    global agent_manager, PROBLEMS_SOLUTIONS_AVAILABLE
    
    try:
        # Initialize the Agent Manager
        agent_manager = await initialize_agent_manager()
        
        # Register all available agents
        success = await register_all_agents(agent_manager)
        
        if success:
            print("✅ All agents registered successfully with Agent Manager")
            PROBLEMS_SOLUTIONS_AVAILABLE = True
        else:
            print("⚠️ Some agents failed to register")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize Agent Manager: {e}")
        return False

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    global agent_manager
    
    # Initialize the system if not already done
    if agent_manager is None:
        await initialize_system()
    
    # Display welcome message
    welcome_message = f"""
# 🚀 **Deep Research System - BETA VERSION** 🚀

Welcome to the **AI-Powered Sales Intelligence Platform**!

## 🎯 **Available Capabilities:**
- **Lead Research**: Website analysis, LinkedIn profiling, market intelligence
- **Industry Analysis**: Problem identification and solution mapping
- **AI Solutions**: Data analytics and AI solution recommendations
- **Email Generation**: Personalized outreach emails
- **Comprehensive Reports**: Complete lead analysis and recommendations

## 🔧 **System Status:**
"""
    
    if agent_manager:
        status = agent_manager.get_system_status()
        welcome_message += f"""
- **System**: {status['status'].upper()}
- **Active Agents**: {status['active_agents']}/{status['total_agents']}
- **Queue Status**: {status['queue_size']} pending requests
"""
    else:
        welcome_message += "- **System**: Initializing..."
    
    welcome_message += f"""

## 📝 **How to Use:**

### **Option 1: Comprehensive Lead Research**
```
Company: [Company Name]
Contact: [Person Name]
Role: [Job Title]
Email: [Email Address]
LinkedIn: [LinkedIn URL]
Phone: [Phone Number]
Website: [Website URL]
```

### **Option 2: Industry Problems Analysis**
```
Analyze problems for: [Company Name] in [Industry]
```

### **Option 3: AI Solutions Research**
```
Find AI solutions for: [Company Name] in [Industry]
```

## 🆘 **Need Help?**
- **Feature Requests**: [Submit Here](https://forms.gle/D9uAUPtJR1gmoDCD7)
- **System Status**: Check agent health and performance
- **Support**: Contact the development team

---
*Powered by Advanced AI Agents with Centralized Orchestration* 🧠✨
"""
    
    await cl.Message(content=welcome_message).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages."""
    global agent_manager, PROBLEMS_SOLUTIONS_AVAILABLE
    
    user_input = message.content.strip()
    
    # Check if system is initialized
    if agent_manager is None:
        await cl.Message(content="🔄 System is initializing, please wait...").send()
        return
    
    # Check system status
    status = agent_manager.get_system_status()
    if status['status'] == 'degraded':
        await cl.Message(content="⚠️ System is currently degraded. Some agents may be unavailable.").send()
    
    # Handle different types of requests
    if "company:" in user_input.lower() and "contact:" in user_input.lower():
        # Comprehensive lead research
        await handle_comprehensive_research(user_input)
    elif "analyze problems" in user_input.lower():
        # Industry problems analysis
        await handle_problems_identification(user_input)
    elif "find ai solutions" in user_input.lower():
        # AI solutions research
        await handle_solutions_research(user_input)
    elif "system status" in user_input.lower():
        # Display system status
        await display_system_status()
    elif "agent metrics" in user_input.lower():
        # Display agent metrics
        await display_agent_metrics()
    else:
        # General help
        await cl.Message(content="🤔 I'm not sure what you'd like me to do. Try asking me to research a lead, analyze industry problems, or find AI solutions!").send()

async def handle_comprehensive_research(user_input: str):
    """Handle comprehensive lead research using the Agent Manager."""
    try:
        # Extract lead information
        lead_info = extract_lead_information(user_input)
        
        if not lead_info:
            await cl.Message(content="❌ Could not extract lead information. Please provide company and contact details.").send()
            return
        
        await cl.Message(content="🔍 **Starting Comprehensive Lead Research...**\n\nThis will use multiple AI agents to analyze the lead thoroughly.").send()
        
        # Step 1: Website Research
        if lead_info.get('website_url'):
            await cl.Message(content="🌐 **Step 1: Website Research**\nAnalyzing company website...").send()
            
            # Submit request to Agent Manager
            from agent_manager import RequestPriority
            request_id = agent_manager.submit_request(
                request_type="website_research",
                payload={
                    "company_name": lead_info['company_name'],
                    "website_url": lead_info['website_url']
                },
                priority=RequestPriority.HIGH
            )
            
            # Wait for result
            result = await agent_manager.get_request_result(request_id, timeout=60.0)
            
            if result and result.status == 'completed':
                await cl.Message(content=f"✅ **Website Research Complete**\n\n{result.result}").send()
            else:
                await cl.Message(content="❌ Website research failed or timed out.").send()
        
        # Step 2: Industry Problems Analysis
        if lead_info.get('company_industry'):
            await cl.Message(content="🎯 **Step 2: Industry Problems Analysis**\nIdentifying potential challenges...").send()
            
            request_id = agent_manager.submit_request(
                request_type="industry_problems",
                payload={
                    "company_industry": lead_info['company_industry'],
                    "company_size": lead_info.get('company_size', 'Unknown'),
                    "company_location": lead_info.get('company_location', 'Unknown'),
                    "person_role": lead_info.get('person_role', 'Unknown')
                },
                priority=RequestPriority.HIGH
            )
            
            result = await agent_manager.get_request_result(request_id, timeout=60.0)
            
            if result and result.status == 'completed':
                await cl.Message(content=f"✅ **Industry Problems Analysis Complete**\n\n{result.result}").send()
            else:
                await cl.Message(content="❌ Industry problems analysis failed or timed out.").send()
        
        # Step 3: AI Solutions Research
        if lead_info.get('company_industry'):
            await cl.Message(content="🤖 **Step 3: AI Solutions Research**\nFinding relevant AI solutions...").send()
            
            request_id = agent_manager.submit_request(
                request_type="ai_solutions",
                payload={
                    "company_industry": lead_info['company_industry'],
                    "company_size": lead_info.get('company_size', 'Unknown'),
                    "industry_problems": "General industry challenges"  # Placeholder
                },
                priority=RequestPriority.HIGH
            )
            
            result = await agent_manager.get_request_result(request_id, timeout=60.0)
            
            if result and result.status == 'completed':
                await cl.Message(content=f"✅ **AI Solutions Research Complete**\n\n{result.result}").send()
            else:
                await cl.Message(content="❌ AI solutions research failed or timed out.").send()
        
        # Final summary
        await cl.Message(content="🎉 **Comprehensive Research Complete!**\n\nAll available agents have analyzed the lead. Check the results above for insights and recommendations.").send()
        
    except Exception as e:
        await cl.Message(content=f"❌ **Research Error**: {str(e)}\n\nPlease try again or contact support.").send()

async def handle_problems_identification(user_input: str):
    """Handle industry problems identification."""
    try:
        company_info = extract_company_info_from_message(user_input)
        
        if not company_info:
            await cl.Message(content="❌ Could not extract company information. Please specify the company and industry.").send()
            return
        
        await cl.Message(content=f"🎯 **Analyzing Industry Problems for {company_info['company_name']}**\n\nThis may take a few moments...").send()
        
        # Submit request to Agent Manager
        request_id = agent_manager.submit_request(
            request_type="industry_problems",
            payload={
                "company_industry": company_info['company_industry'],
                "company_size": company_info.get('company_size', 'Unknown'),
                "company_location": company_info.get('company_location', 'Unknown'),
                "person_role": company_info.get('person_role', 'Unknown')
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_manager.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == 'completed':
            await cl.Message(content=f"✅ **Industry Problems Analysis Complete**\n\n{result.result}").send()
        else:
            await cl.Message(content="❌ Industry problems analysis failed or timed out.").send()
            
    except Exception as e:
        await cl.Message(content=f"❌ **Problems Analysis Error**: {str(e)}").send()

async def handle_solutions_research(user_input: str):
    """Handle AI solutions research."""
    try:
        company_info = extract_company_info_from_message(user_input)
        
        if not company_info:
            await cl.Message(content="❌ Could not extract company information. Please specify the company and industry.").send()
            return
        
        await cl.Message(content=f"🤖 **Researching AI Solutions for {company_info['company_name']}**\n\nThis may take a few moments...").send()
        
        # Submit request to Agent Manager
        request_id = agent_manager.submit_request(
            request_type="ai_solutions",
            payload={
                "company_industry": company_info['company_industry'],
                "company_size": company_info.get('company_size', 'Unknown'),
                "industry_problems": "General industry challenges"  # Placeholder
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for result
        result = await agent_manager.get_request_result(request_id, timeout=60.0)
        
        if result and result.status == 'completed':
            await cl.Message(content=f"✅ **AI Solutions Research Complete**\n\n{result.result}").send()
        else:
            await cl.Message(content="❌ AI solutions research failed or timed out.").send()
            
    except Exception as e:
        await cl.Message(content=f"❌ **Solutions Research Error**: {str(e)}").send()

async def display_system_status():
    """Display the current system status."""
    global agent_manager
    
    if not agent_manager:
        await cl.Message(content="❌ Agent Manager not initialized.").send()
        return
    
    status = agent_manager.get_system_status()
    
    status_message = f"""
# 📊 **System Status Report**

## 🟢 **Overall Status**: {status['status'].upper()}

## 🤖 **Agent Status**:
- **Total Agents**: {status['total_agents']}
- **Active Agents**: {status['active_agents']}
- **Queue Size**: {status['queue_size']}
- **Processing**: {status['processing_requests']}
- **Completed**: {status['completed_requests']}

## 📈 **Individual Agent Status**:
"""
    
    for agent_id, agent_info in status['agents'].items():
        health_emoji = "🟢" if agent_info['health_score'] > 80 else "🟡" if agent_info['health_score'] > 50 else "🔴"
        status_message += f"- {health_emoji} **{agent_id}**: {agent_info['status']} (Health: {agent_info['health_score']:.1f}, Load: {agent_info['current_load']})\n"
    
    await cl.Message(content=status_message).send()

async def display_agent_metrics():
    """Display detailed agent metrics."""
    global agent_manager
    
    if not agent_manager:
        await cl.Message(content="❌ Agent Manager not initialized.").send()
        return
    
    metrics = agent_manager.get_all_metrics()
    
    metrics_message = "# 📊 **Agent Performance Metrics**\n\n"
    
    for agent_id, agent_metrics in metrics.items():
        if agent_metrics:
            metrics_message += f"""
## 🤖 **{agent_id}**
- **Total Requests**: {agent_metrics['total_requests']}
- **Success Rate**: {agent_metrics['success_rate']:.2%}
- **Error Rate**: {agent_metrics['error_rate']:.2%}
- **Avg Response Time**: {agent_metrics['average_response_time']:.2f}s
- **Current Load**: {agent_metrics['current_load']}
- **Health Score**: {agent_metrics['health_score']:.1f}
- **Last Request**: {agent_metrics['last_request_time'] or 'Never'}

"""
    
    await cl.Message(content=metrics_message).send()

def extract_lead_information(user_input: str) -> Optional[Dict[str, str]]:
    """Extract lead information from user input."""
    try:
        lines = user_input.split('\n')
        lead_info = {}
        
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'company':
                    lead_info['company_name'] = value
                elif key == 'contact':
                    lead_info['person_name'] = value
                elif key == 'role':
                    lead_info['person_role'] = value
                elif key == 'email':
                    lead_info['email'] = value
                elif key == 'linkedin':
                    lead_info['linkedin_url'] = value
                elif key == 'phone':
                    lead_info['phone'] = value
                elif key == 'website':
                    lead_info['website_url'] = value
        
        # Add default values for missing fields
        if 'company_name' in lead_info:
            lead_info.setdefault('company_industry', 'Unknown')
            lead_info.setdefault('company_size', 'Unknown')
            lead_info.setdefault('company_location', 'Unknown')
            lead_info.setdefault('person_role', 'Unknown')
        
        return lead_info if lead_info else None
        
    except Exception as e:
        print(f"Error extracting lead information: {e}")
        return None

def extract_company_info_from_message(message: str) -> Optional[Dict[str, str]]:
    """Extract company information from a message."""
    try:
        # Simple extraction for now
        if "for:" in message.lower():
            parts = message.split("for:")
            if len(parts) > 1:
                company_part = parts[1].strip()
                if "in" in company_part:
                    company_name, industry_part = company_part.split("in", 1)
                    return {
                        'company_name': company_name.strip(),
                        'company_industry': industry_part.strip()
                    }
        
        return None
        
    except Exception as e:
        print(f"Error extracting company info: {e}")
        return None

@cl.on_chat_end
async def on_chat_end():
    """Clean up when chat ends."""
    global agent_manager
    
    if agent_manager:
        # Note: Don't shutdown the manager here as it's shared across sessions
        print("Chat session ended, Agent Manager remains active for other sessions")

if __name__ == "__main__":
    print("🚀 Starting Deep Research System with Agent Manager...")
    print("✅ Agent Manager integration ready!")
    print("💡 Use 'chainlit run app_with_agent_manager.py -w' to start the app")
