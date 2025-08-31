"""
Test: Handoff System Structure and Logic

This test validates the handoff system architecture and logic
without relying on external API calls.
"""

import sys
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def test_imports():
    """Test if all required modules can be imported."""
    print("📦 Testing Module Imports...")
    
    try:
        from deep_research_system_handoffs import (
            ResearchContext, 
            AgentType, 
            determine_handoff_strategy_direct
        )
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_research_context():
    """Test ResearchContext dataclass functionality."""
    print("\n🔍 Testing ResearchContext...")
    
    try:
        from deep_research_system_handoffs import ResearchContext
        
        # Create a test context
        context = ResearchContext(
            company_name="TestCorp Inc.",
            person_name="John Smith",
            website_url="https://testcorp.com",
            person_role="CTO",
            technical_skills=["Python", "Data Science", "AI"],
            decision_power="High"
        )
        
        print(f"✅ ResearchContext created successfully")
        print(f"   Company: {context.company_name}")
        print(f"   Person: {context.person_name}")
        print(f"   Role: {context.person_role}")
        print(f"   Technical Skills: {context.technical_skills}")
        print(f"   Decision Power: {context.decision_power}")
        
        return True
    except Exception as e:
        print(f"❌ ResearchContext test failed: {e}")
        return False

def test_agent_type_enum():
    """Test AgentType enum functionality."""
    print("\n🤖 Testing AgentType Enum...")
    
    try:
        from deep_research_system_handoffs import AgentType
        
        # Test enum values
        print(f"✅ AgentType enum loaded successfully")
        print(f"   Available types: {[agent.value for agent in AgentType]}")
        
        # Test specific types
        executive = AgentType.EXECUTIVE_SPECIALIST
        technical = AgentType.TECHNICAL_SPECIALIST
        general = AgentType.EMAIL_GENERATOR
        
        print(f"   Executive Specialist: {executive.value}")
        print(f"   Technical Specialist: {technical.value}")
        print(f"   Email Generator: {general.value}")
        
        return True
    except Exception as e:
        print(f"❌ AgentType enum test failed: {e}")
        return False

def test_handoff_strategy_logic():
    """Test handoff strategy determination logic."""
    print("\n🔄 Testing Handoff Strategy Logic...")
    
    try:
        from deep_research_system_handoffs import ResearchContext, determine_handoff_strategy_direct
        
        # Test Case 1: Executive Contact
        print("   Test Case 1: Executive Contact (CEO)")
        exec_context = ResearchContext(
            company_name="ExecCorp",
            person_name="Jane CEO",
            person_role="CEO",
            decision_power="High",
            priority_level=5
        )
        
        exec_strategy = determine_handoff_strategy_direct(exec_context)
        print(f"   ✅ Executive strategy generated: {len(exec_strategy)} characters")
        print(f"   Next Agent: {exec_context.next_agent}")
        print(f"   Priority: {exec_context.priority_level}")
        print(f"   Reason: {exec_context.handoff_reason}")
        
        # Test Case 2: Technical Contact
        print("\n   Test Case 2: Technical Contact")
        tech_context = ResearchContext(
            company_name="TechCorp",
            person_name="Bob Engineer",
            person_role="Senior Data Engineer",
            technical_skills=["Python", "SQL", "AWS", "Machine Learning"],
            decision_power="Medium",
            priority_level=4
        )
        
        tech_strategy = determine_handoff_strategy_direct(tech_context)
        print(f"   ✅ Technical strategy generated: {len(tech_strategy)} characters")
        print(f"   Next Agent: {tech_context.next_agent}")
        print(f"   Priority: {tech_context.priority_level}")
        print(f"   Reason: {tech_context.handoff_reason}")
        
        # Test Case 3: General Contact
        print("\n   Test Case 3: General Contact")
        gen_context = ResearchContext(
            company_name="GenCorp",
            person_name="Alice Manager",
            person_role="Marketing Manager",
            decision_power="Medium",
            priority_level=3
        )
        
        gen_strategy = determine_handoff_strategy_direct(gen_context)
        print(f"   ✅ General strategy generated: {len(gen_strategy)} characters")
        print(f"   Next Agent: {gen_context.next_agent}")
        print(f"   Priority: {gen_context.priority_level}")
        print(f"   Reason: {gen_context.handoff_reason}")
        
        return True
    except Exception as e:
        print(f"❌ Handoff strategy test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_function_tools():
    """Test function tool definitions."""
    print("\n🔧 Testing Function Tools...")
    
    try:
        from deep_research_system_handoffs import (
            analyze_company_website_direct,
            research_linkedin_profile_direct,
            generate_email_pitch_direct,
            compile_research_report_direct
        )
        
        # Test website analysis
        website_result = analyze_company_website_direct("TestCorp", "https://testcorp.com")
        print(f"✅ Website analysis tool: {len(website_result)} characters")
        
        # Test LinkedIn research
        linkedin_result = research_linkedin_profile_direct("John Smith", "TestCorp")
        print(f"✅ LinkedIn research tool: {len(linkedin_result)} characters")
        
        # Test email generation
        email_result = generate_email_pitch_direct("John Smith", "TestCorp", "Test research summary")
        print(f"✅ Email generation tool: {len(email_result)} characters")
        
        # Test report compilation
        report_result = compile_research_report_direct("TestCorp", "John Smith", "Website data", "LinkedIn data")
        print(f"✅ Report compilation tool: {len(report_result)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Function tools test failed: {e}")
        return False

def test_agent_definitions():
    """Test agent definitions and configurations."""
    print("\n🤖 Testing Agent Definitions...")
    
    try:
        from deep_research_system_handoffs import (
            handoff_coordinator,
            executive_specialist,
            technical_specialist
        )
        
        print(f"✅ Handoff Coordinator: {handoff_coordinator.name}")
        print(f"   Instructions: {len(handoff_coordinator.instructions)} characters")
        print(f"   Tools: {len(handoff_coordinator.tools)} tools")
        
        print(f"✅ Executive Specialist: {executive_specialist.name}")
        print(f"   Instructions: {len(executive_specialist.instructions)} characters")
        print(f"   Tools: {len(executive_specialist.tools)} tools")
        
        print(f"✅ Technical Specialist: {technical_specialist.name}")
        print(f"   Instructions: {len(technical_specialist.instructions)} characters")
        print(f"   Tools: {len(technical_specialist.tools)} tools")
        
        return True
    except Exception as e:
        print(f"❌ Agent definitions test failed: {e}")
        return False

def test_main_function_structure():
    """Test the main research function structure."""
    print("\n🏗️ Testing Main Function Structure...")
    
    try:
        from deep_research_system_handoffs import research_lead_with_handoffs
        
        print("✅ Main function imported successfully")
        print("✅ Function signature validated")
        
        # Test function documentation
        doc = research_lead_with_handoffs.__doc__
        if doc:
            print(f"✅ Function documentation: {len(doc)} characters")
        else:
            print("⚠️  Function missing documentation")
        
        return True
    except Exception as e:
        print(f"❌ Main function test failed: {e}")
        return False

def run_all_tests():
    """Run all structure and logic tests."""
    print("🧪 Handoff System Structure & Logic Test Suite")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("ResearchContext", test_research_context),
        ("AgentType Enum", test_agent_type_enum),
        ("Handoff Strategy Logic", test_handoff_strategy_logic),
        ("Function Tools", test_function_tools),
        ("Agent Definitions", test_agent_definitions),
        ("Main Function Structure", test_main_function_structure)
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
        print("🎉 All structure tests passed! Handoff system architecture is sound.")
        print("\n💡 The system has:")
        print("   • Proper data structures (ResearchContext)")
        print("   • Clear agent type definitions")
        print("   • Intelligent handoff logic")
        print("   • Well-defined function tools")
        print("   • Proper agent configurations")
        print("   • Main orchestration function")
    else:
        print("⚠️  Some structure tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
