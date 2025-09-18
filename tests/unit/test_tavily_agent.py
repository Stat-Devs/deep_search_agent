"""
Test: Tavily Research Agent

This test file validates the Tavily research agent functionality
and ensures proper integration with the handoff system.
"""

import os
import sys
import json
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def test_tavily_api_key():
    """Test if Tavily API key is available."""
    print("🔑 Testing Tavily API Key...")
    
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        print("✅ TAVILY_API_KEY found")
        print(f"   Key: {tavily_key[:10]}...{tavily_key[-4:]}")
        return True
    else:
        print("❌ TAVILY_API_KEY not found")
        print("   Please add TAVILY_API_KEY to your .env file")
        return False

def test_tavily_import():
    """Test if Tavily package can be imported."""
    print("\n📦 Testing Tavily Package Import...")
    
    try:
        from tavily import TavilyClient
        print("✅ Tavily package imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Tavily: {e}")
        print("   Please install tavily-python: pip install tavily-python")
        return False

def test_tavily_agent_import():
    """Test if our Tavily research agent can be imported."""
    print("\n🤖 Testing Tavily Research Agent Import...")
    
    try:
        from research_agent_tavily import TavilyResearchAgent
        print("✅ TavilyResearchAgent imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import TavilyResearchAgent: {e}")
        return False

def test_tavily_client_initialization():
    """Test if Tavily client can be initialized."""
    print("\n🔌 Testing Tavily Client Initialization...")
    
    try:
        from tavily import TavilyClient
        from research_agent_tavily import TavilyResearchAgent
        
        # Test client initialization
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        print("✅ Tavily client initialized successfully")
        
        # Test agent initialization
        agent = TavilyResearchAgent()
        print("✅ TavilyResearchAgent initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Tavily components: {e}")
        return False

def test_basic_search():
    """Test basic search functionality."""
    print("\n🔍 Testing Basic Search Functionality...")
    
    try:
        from research_agent_tavily import TavilyResearchAgent
        
        agent = TavilyResearchAgent()
        
        # Test with a simple search
        print("   Testing simple company search...")
        results = agent.client.search(
            query="OpenAI company overview",
            search_depth="basic",
            max_results=2
        )
        
        if results and results.get("results"):
            print(f"✅ Search successful - {len(results['results'])} results found")
            print(f"   First result title: {results['results'][0].get('title', 'N/A')[:50]}...")
            return True
        else:
            print("❌ Search returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Basic search test failed: {e}")
        return False

def test_quick_research():
    """Test quick research functionality."""
    print("\n⚡ Testing Quick Research Functionality...")
    
    try:
        from research_agent_tavily import TavilyResearchAgent
        
        agent = TavilyResearchAgent()
        
        # Test quick research
        print("   Testing quick research for executive contact...")
        summary = agent.quick_research(
            company_name="Microsoft",
            person_name="Satya Nadella",
            contact_type="executive"
        )
        
        if summary and "Executive Research Summary" in summary:
            print("✅ Quick research successful")
            print(f"   Summary length: {len(summary)} characters")
            return True
        else:
            print("❌ Quick research failed or returned unexpected format")
            return False
            
    except Exception as e:
        print(f"❌ Quick research test failed: {e}")
        return False

def test_comprehensive_research():
    """Test comprehensive research functionality."""
    print("\n📊 Testing Comprehensive Research Functionality...")
    
    try:
        from research_agent_tavily import TavilyResearchAgent
        
        agent = TavilyResearchAgent()
        
        # Test comprehensive research
        print("   Testing comprehensive research for technical contact...")
        results = agent.research_lead_with_tavily(
            company_name="Google",
            person_name="Sundar Pichai",
            person_role="CEO",
            contact_type="executive",
            company_industry="Technology"
        )
        
        if results and isinstance(results, dict):
            print("✅ Comprehensive research successful")
            print(f"   Results keys: {list(results.keys())}")
            
            # Check for expected structure
            expected_keys = [
                "company_name", "person_name", "contact_type", 
                "company_research", "person_research", "market_research",
                "opportunity_analysis", "research_summary"
            ]
            
            missing_keys = [key for key in expected_keys if key not in results]
            if not missing_keys:
                print("✅ All expected result fields present")
                return True
            else:
                print(f"❌ Missing expected fields: {missing_keys}")
                return False
        else:
            print("❌ Comprehensive research failed or returned unexpected format")
            return False
            
    except Exception as e:
        print(f"❌ Comprehensive research test failed: {e}")
        return False

def test_handoff_integration():
    """Test integration with handoff system concepts."""
    print("\n🔄 Testing Handoff System Integration...")
    
    try:
        from research_agent_tavily import TavilyResearchAgent
        
        agent = TavilyResearchAgent()
        
        # Test different contact types
        contact_types = ["executive", "technical", "general"]
        
        for contact_type in contact_types:
            print(f"   Testing {contact_type} contact type...")
            
            results = agent.research_lead_with_tavily(
                company_name="Test Company",
                person_name="Test Person",
                contact_type=contact_type
            )
            
            if results and results.get("contact_type") == contact_type:
                print(f"   ✅ {contact_type} contact research successful")
            else:
                print(f"   ❌ {contact_type} contact research failed")
                return False
        
        print("✅ All contact type tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Handoff integration test failed: {e}")
        return False

def test_example_usage():
    """Test example usage scenarios."""
    print("\n📝 Testing Example Usage Scenarios...")
    
    try:
        from research_agent_tavily import TavilyResearchAgent
        
        agent = TavilyResearchAgent()
        
        # Example 1: Executive contact research
        print("   Example 1: Executive Contact Research")
        executive_results = agent.research_lead_with_tavily(
            company_name="TechCorp Inc.",
            person_name="John Smith",
            person_role="CTO",
            contact_type="executive",
            company_industry="Technology"
        )
        
        if executive_results and executive_results.get("contact_type") == "executive":
            print("   ✅ Executive research successful")
        else:
            print("   ❌ Executive research failed")
            return False
        
        # Example 2: Quick research
        print("   Example 2: Quick Research")
        quick_summary = agent.quick_research(
            company_name="TechCorp Inc.",
            person_name="John Smith",
            contact_type="executive"
        )
        
        if quick_summary and "Executive Research Summary" in quick_summary:
            print("   ✅ Quick research successful")
        else:
            print("   ❌ Quick research failed")
            return False
        
        print("✅ All example usage tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Example usage test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary."""
    print("🧪 Tavily Research Agent Test Suite")
    print("=" * 50)
    
    tests = [
        ("API Key", test_tavily_api_key),
        ("Package Import", test_tavily_import),
        ("Agent Import", test_tavily_agent_import),
        ("Client Initialization", test_tavily_client_initialization),
        ("Basic Search", test_basic_search),
        ("Quick Research", test_quick_research),
        ("Comprehensive Research", test_comprehensive_research),
        ("Handoff Integration", test_handoff_integration),
        ("Example Usage", test_example_usage)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📋 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Tavily Research Agent is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

def run_example_demo():
    """Run a demonstration of the Tavily research agent."""
    print("\n🎯 Tavily Research Agent Example Demo")
    print("=" * 50)
    
    try:
        from research_agent_tavily import TavilyResearchAgent
        
        # Initialize the agent
        agent = TavilyResearchAgent()
        print("✅ TavilyResearchAgent initialized successfully")
        
        # Example 1: Comprehensive research for executive contact
        print("\n📊 Example 1: Executive Contact Research")
        print("Company: TechCorp Inc.")
        print("Contact: John Smith (CTO)")
        print("Contact Type: Executive")
        
        executive_results = agent.research_lead_with_tavily(
            company_name="TechCorp Inc.",
            person_name="John Smith",
            person_role="CTO",
            contact_type="executive",
            company_industry="Technology"
        )
        
        print("✅ Research completed successfully")
        print(f"Research Summary: {executive_results.get('research_summary', 'N/A')}")
        
        # Example 2: Quick research for technical contact
        print("\n⚡ Example 2: Quick Research for Technical Contact")
        print("Company: DataWorks LLC")
        print("Contact: Emily Chen")
        print("Contact Type: Technical")
        
        quick_summary = agent.quick_research(
            company_name="DataWorks LLC",
            person_name="Emily Chen",
            contact_type="technical"
        )
        
        print("✅ Quick research completed successfully")
        print("Summary:")
        for line in quick_summary.split('\n'):
            if line.strip():
                print(f"   {line}")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    # Check if user wants to run demo or tests
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_example_demo()
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
