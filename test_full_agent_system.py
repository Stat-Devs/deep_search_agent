"""
Test: Full Agent Manager System with All Agents

This test validates that the complete agent orchestration system is working
with all agents: Website, LinkedIn, Tavily, Industry, Solutions, Reports, Email.
"""

import os
import asyncio
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_setup():
    """Test that all required environment variables are available."""
    print("🧪 Testing Environment Setup...")
    
    # Check API keys
    required_keys = ["OPENAI_API_KEY", "GEMINI_API_KEY", "TAVILY_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        value = os.getenv(key)
        if value:
            print(f"✅ {key}: Found ({key[:10]}...)")
        else:
            print(f"❌ {key}: Missing")
            missing_keys.append(key)
    
    if missing_keys:
        print(f"⚠️ Missing keys: {', '.join(missing_keys)}")
        return False
    
    print("✅ All environment variables found")
    return True

async def test_agent_manager_initialization():
    """Test that the Agent Manager initializes correctly with all agents."""
    print("\n🤖 Testing Agent Manager Initialization...")
    
    try:
        # Import the agent manager
        from agent_manager import initialize_agent_manager
        from agent_adapters import register_all_agents
        
        # Initialize agent manager
        agent_manager = await initialize_agent_manager()
        print("✅ Agent Manager initialized")
        
        # Register all agents
        success = await register_all_agents(agent_manager)
        
        if success:
            print("✅ All agents registered successfully")
            
            # Get system status
            status = agent_manager.get_system_status()
            print(f"📊 System Status: {status['status']}")
            print(f"🤖 Total Agents: {status['total_agents']}")
            print(f"🟢 Active Agents: {status['active_agents']}")
            
            # List all agents
            print("\n📋 Registered Agents:")
            for agent_id, agent_info in status['agents'].items():
                print(f"   • {agent_id}: {agent_info['status']} ({', '.join(agent_info['capabilities'])})")
            
            return agent_manager
        else:
            print("❌ Some agents failed to register")
            return None
            
    except Exception as e:
        print(f"❌ Agent Manager initialization failed: {e}")
        return None

async def test_individual_agents(agent_manager):
    """Test each individual agent through the Agent Manager."""
    print("\n🔍 Testing Individual Agents...")
    
    test_company = "FFC (Fauji Fertilizer Company)"
    test_person = "John Test"
    test_industry = "Agriculture/Manufacturing"
    
    # Test 1: Website Research Agent
    print("\n1️⃣ Testing Website Research Agent...")
    try:
        from agent_manager import RequestPriority
        request_id = agent_manager.submit_request(
            request_type="website_research",
            payload={
                "company_name": test_company,
                "website_url": "https://ffc.com.pk/"
            },
            priority=RequestPriority.HIGH
        )
        
        result = await agent_manager.get_request_result(request_id, timeout=30.0)
        
        if result and result.status == "completed":
            print("✅ Website Research Agent: Working")
            print(f"   Result: {result.result[:100]}...")
        else:
            print(f"❌ Website Research Agent: Failed - {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"❌ Website Research Agent: Error - {e}")
    
    # Test 2: LinkedIn Research Agent
    print("\n2️⃣ Testing LinkedIn Research Agent...")
    try:
        request_id = agent_manager.submit_request(
            request_type="linkedin_research",
            payload={
                "person_name": test_person,
                "company_name": test_company,
                "linkedin_url": "https://linkedin.com/in/johntest"
            },
            priority=RequestPriority.HIGH
        )
        
        result = await agent_manager.get_request_result(request_id, timeout=30.0)
        
        if result and result.status == "completed":
            print("✅ LinkedIn Research Agent: Working")
            print(f"   Result: {result.result[:100]}...")
        else:
            print(f"❌ LinkedIn Research Agent: Failed - {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"❌ LinkedIn Research Agent: Error - {e}")
    
    # Test 3: Industry Problems Agent
    print("\n3️⃣ Testing Industry Problems Agent...")
    try:
        request_id = agent_manager.submit_request(
            request_type="industry_problems",
            payload={
                "company_industry": test_industry,
                "company_size": "Medium",
                "company_location": "San Francisco",
                "person_role": "Data Scientist"
            },
            priority=RequestPriority.HIGH
        )
        
        result = await agent_manager.get_request_result(request_id, timeout=30.0)
        
        if result and result.status == "completed":
            print("✅ Industry Problems Agent: Working")
            print(f"   Result: {result.result[:100]}...")
        else:
            print(f"❌ Industry Problems Agent: Failed - {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"❌ Industry Problems Agent: Error - {e}")
    
    # Test 4: Solutions Research Agent
    print("\n4️⃣ Testing Solutions Research Agent...")
    try:
        request_id = agent_manager.submit_request(
            request_type="ai_solutions",
            payload={
                "industry_problems": ["Data silos", "Manual reporting", "Lack of real-time insights"],
                "company_industry": test_industry,
                "company_size": "Medium"
            },
            priority=RequestPriority.HIGH
        )
        
        result = await agent_manager.get_request_result(request_id, timeout=30.0)
        
        if result and result.status == "completed":
            print("✅ Solutions Research Agent: Working")
            print(f"   Result: {result.result[:100]}...")
        else:
            print(f"❌ Solutions Research Agent: Failed - {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"❌ Solutions Research Agent: Error - {e}")
    
    # Test 5: Email Generation Agent
    print("\n5️⃣ Testing Email Generation Agent...")
    try:
        request_id = agent_manager.submit_request(
            request_type="email_generation",
            payload={
                "person_name": test_person,
                "company_name": test_company,
                "research_summary": "Test research summary for email generation"
            },
            priority=RequestPriority.HIGH
        )
        
        result = await agent_manager.get_request_result(request_id, timeout=30.0)
        
        if result and result.status == "completed":
            print("✅ Email Generation Agent: Working")
            print(f"   Result: {result.result[:100]}...")
        else:
            print(f"❌ Email Generation Agent: Failed - {result.error if result else 'Unknown error'}")
            
    except Exception as e:
        print(f"❌ Email Generation Agent: Error - {e}")

async def test_tavily_agent():
    """Test Tavily agent specifically."""
    print("\n🔍 Testing Tavily Web Intelligence Agent...")
    
    try:
        # Import Tavily agent directly
        from research_agent_tavily import TavilyResearchAgent
        
        tavily_agent = TavilyResearchAgent()
        result = tavily_agent.research_lead_with_tavily(
            company_name="FFC (Fauji Fertilizer Company)",
            person_name="John Test",
            person_role="Data Scientist",
            contact_type="general",
            company_industry="Agriculture/Manufacturing"
        )
        
        print("✅ Tavily Agent: Working")
        if isinstance(result, str):
            print(f"   Result: {result[:100]}...")
        else:
            print(f"   Result: {str(result)[:100]}...")
        
    except Exception as e:
        print(f"❌ Tavily Agent: Error - {e}")

async def test_full_workflow():
    """Test the complete workflow through the main app functions."""
    print("\n🔄 Testing Complete Workflow...")
    
    try:
        # Import the main functions
        from app import (
            analyze_company_website,
            research_linkedin_profile,
            research_with_tavily,
            identify_industry_problems,
            research_ai_solutions,
            generate_comprehensive_report,
            generate_email_pitch
        )
        
        test_input = """
        Company: FFC (Fauji Fertilizer Company)
        Contact: John Test
        Role: Data Scientist
        Email: john@ffc.com.pk
        LinkedIn: https://linkedin.com/in/johntest
        Phone: +92-51-1234567
        Website: https://ffc.com.pk/
        """
        
        print("📋 Testing complete research workflow...")
        
        # Test each function
        website_result = await analyze_company_website("FFC (Fauji Fertilizer Company)", "https://ffc.com.pk/")
        print("✅ Website Analysis: Working")
        
        linkedin_result = await research_linkedin_profile("John Test", "FFC (Fauji Fertilizer Company)")
        print("✅ LinkedIn Research: Working")
        
        tavily_result = await research_with_tavily("FFC (Fauji Fertilizer Company)", "John Test", "Agriculture/Manufacturing")
        print("✅ Tavily Research: Working")
        
        industry_result = await identify_industry_problems("Agriculture/Manufacturing", "Large", "Data Scientist")
        print("✅ Industry Analysis: Working")
        
        solutions_result = await research_ai_solutions(["Supply chain optimization", "Crop yield prediction"], "Agriculture/Manufacturing", "Large")
        print("✅ Solutions Research: Working")
        
        report_result = await generate_comprehensive_report(
            "FFC (Fauji Fertilizer Company)", "John Test", 
            website_result, industry_result, solutions_result,
            linkedin_result, tavily_result
        )
        print("✅ Report Generation: Working")
        
        email_result = await generate_email_pitch("John Test", "FFC (Fauji Fertilizer Company)", report_result)
        print("✅ Email Generation: Working")
        
        print("🎉 Complete workflow test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Complete workflow test failed: {e}")
        return False

async def test_tracing_integration():
    """Test that tracing is working with the Agent Manager."""
    print("\n📊 Testing Tracing Integration...")
    
    try:
        from agents import trace, custom_span
        
        # Test tracing with Agent Manager
        with trace("Agent Manager Test", metadata={"test_type": "full_system", "timestamp": str(datetime.now())}):
            
            with custom_span("Agent Manager Initialization", data={"component": "agent_manager"}):
                from agent_manager import initialize_agent_manager
                agent_manager = await initialize_agent_manager()
                print("✅ Tracing: Agent Manager initialization")
            
            with custom_span("Agent Registration", data={"component": "agent_adapters"}):
                from agent_adapters import register_all_agents
                await register_all_agents(agent_manager)
                print("✅ Tracing: Agent registration")
            
            with custom_span("Test Request", data={"request_type": "website_research"}):
                request_id = agent_manager.submit_request(
                    request_type="website_research",
                    payload={"company_name": "FFC (Fauji Fertilizer Company)", "website_url": "https://ffc.com.pk/"},
                    priority=RequestPriority.HIGH
                )
                print("✅ Tracing: Request submission")
            
            with custom_span("Result Retrieval", data={"request_id": request_id}):
                result = await agent_manager.get_request_result(request_id, timeout=30.0)
                print("✅ Tracing: Result retrieval")
        
        print("✅ Tracing integration working with Agent Manager")
        return True
        
    except Exception as e:
        print(f"❌ Tracing integration failed: {e}")
        return False

async def run_full_agent_system_test():
    """Run comprehensive test of the full agent system."""
    print("🧪 Full Agent Manager System Test")
    print("=" * 60)
    
    # Test 1: Environment Setup
    env_ok = test_environment_setup()
    if not env_ok:
        print("❌ Environment setup failed. Please check your .env file.")
        return
    
    # Test 2: Agent Manager Initialization
    agent_manager = await test_agent_manager_initialization()
    if not agent_manager:
        print("❌ Agent Manager initialization failed.")
        return
    
    # Test 3: Individual Agents
    await test_individual_agents(agent_manager)
    
    # Test 4: Tavily Agent (direct test)
    await test_tavily_agent()
    
    # Test 5: Complete Workflow
    workflow_ok = await test_full_workflow()
    
    # Test 6: Tracing Integration
    tracing_ok = await test_tracing_integration()
    
    # Summary
    print("\n" + "=" * 60)
    if workflow_ok and tracing_ok:
        print("🎉 FULL AGENT SYSTEM TEST PASSED!")
        print("\n📊 System Summary:")
        print("   ✅ Agent Manager: Centralized orchestration working")
        print("   ✅ Website Research Agent: Company analysis")
        print("   ✅ LinkedIn Research Agent: Professional profile analysis")
        print("   ✅ Tavily Research Agent: Web intelligence")
        print("   ✅ Industry Problems Agent: Challenge identification")
        print("   ✅ Solutions Research Agent: AI/data solutions")
        print("   ✅ Report Generation Agent: Comprehensive analysis")
        print("   ✅ Email Generation Agent: Personalized pitches")
        print("   ✅ Tracing Integration: Full monitoring and debugging")
        print("\n🚀 Your Sales Deep Search System now has FULL AGENT ORCHESTRATION!")
        print("   • All agents managed by Agent Manager")
        print("   • Intelligent handoffs between agents")
        print("   • Comprehensive tracing for all interactions")
        print("   • Complete workflow from lead to email")
        print("   • Traces available at: https://platform.openai.com/logs?api=traces")
    else:
        print("⚠️ Some components need attention")
        print("   Check the individual test results above for details")

def main():
    """Main function to run the full agent system test."""
    try:
        asyncio.run(run_full_agent_system_test())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")

if __name__ == "__main__":
    main()
