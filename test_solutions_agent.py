"""
Test file for Solutions Research Agent

This file tests the functionality of the SolutionsAgent
to ensure it correctly researches AI and data analytics solutions.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_solutions_agent():
    """Test the Solutions Agent functionality."""
    
    print("🧪 Testing Solutions Research Agent...")
    print("=" * 50)
    
    try:
        # Import the agent
        from research_agent_solutions import SolutionsAgent, research_solutions_for_problems_direct
        
        print("✅ Import successful")
        
        # Test with environmental services problems
        print("\n🎯 Testing Environmental Services Solutions...")
        problems = [
            "Regulatory compliance complexity",
            "Waste management costs",
            "Sustainability pressures"
        ]
        
        solutions = research_solutions_for_problems_direct(
            industry_problems=problems,
            company_industry="Environmental Services",
            company_size="Mid-market"
        )
        
        print("✅ Solutions research successful")
        print(f"📊 Solutions found: {solutions.count('**') // 2}")  # Count solution titles
        
        # Test with technology problems
        print("\n🎯 Testing Technology Solutions...")
        problems = [
            "Cybersecurity threats",
            "Digital transformation"
        ]
        
        solutions = research_solutions_for_problems_direct(
            industry_problems=problems,
            company_industry="Technology",
            company_size="Enterprise"
        )
        
        print("✅ Technology solutions research successful")
        print(f"📊 Solutions found: {solutions.count('**') // 2}")
        
        # Test with manufacturing problems
        print("\n🎯 Testing Manufacturing Solutions...")
        problems = [
            "Supply chain disruption",
            "Labor shortages"
        ]
        
        solutions = research_solutions_for_problems_direct(
            industry_problems=problems,
            company_industry="Manufacturing",
            company_size="Large"
        )
        
        print("✅ Manufacturing solutions research successful")
        print(f"📊 Solutions found: {solutions.count('**') // 2}")
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_function():
    """Test the direct callable function."""
    
    print("\n🔧 Testing Direct Function...")
    print("=" * 30)
    
    try:
        from research_agent_solutions import research_solutions_for_problems_direct
        
        # Test the direct function
        problems = ["Regulatory compliance complexity", "Cost management"]
        result = research_solutions_for_problems_direct(
            industry_problems=problems,
            company_industry="Environmental Services",
            company_size="Mid-market"
        )
        
        if result and "AI & Data Analytics Solutions Analysis" in result:
            print("✅ Direct function test passed")
            return True
        else:
            print("❌ Direct function test failed - unexpected output")
            return False
            
    except Exception as e:
        print(f"❌ Direct function test failed: {e}")
        return False

def test_problem_solution_mapping():
    """Test the problem-to-solution mapping functionality."""
    
    print("\n🔗 Testing Problem-Solution Mapping...")
    print("=" * 40)
    
    try:
        from research_agent_solutions import SolutionsAgent
        
        agent = SolutionsAgent()
        
        # Test different problem types
        test_cases = [
            (["compliance", "regulatory"], "Environmental Services"),
            (["cybersecurity", "security"], "Technology"),
            (["supply chain", "disruption"], "Manufacturing"),
            (["cost", "management"], "General")
        ]
        
        for problems, industry in test_cases:
            solutions = agent.research_solutions_for_problems(problems, industry, "Mid-market")
            print(f"✅ {industry}: {len(solutions)} solutions for {len(problems)} problems")
        
        print("✅ Problem-solution mapping test passed")
        return True
        
    except Exception as e:
        print(f"❌ Problem-solution mapping test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Solutions Research Agent Test Suite")
    print("=" * 50)
    
    # Run tests
    test1_passed = test_solutions_agent()
    test2_passed = test_direct_function()
    test3_passed = test_problem_solution_mapping()
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Solutions Agent: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Direct Function: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Problem-Solution Mapping: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All tests passed! The Solutions Research Agent is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
    
    print("\n💡 Next Steps:")
    print("• Test with the main research system")
    print("• Verify integration in app.py")
    print("• Run comprehensive system tests")
    print("• Test the complete workflow with both agents")
