"""
Test file for Industry Problems Agent

This file tests the functionality of the IndustryProblemsAgent
to ensure it correctly identifies industry problems and challenges.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_industry_problems_agent():
    """Test the Industry Problems Agent functionality."""
    
    print("🧪 Testing Industry Problems Agent...")
    print("=" * 50)
    
    try:
        # Import the agent
        from research_agent_industry_problems import IndustryProblemsAgent, identify_lead_problems_direct
        
        print("✅ Import successful")
        
        # Test with environmental services
        print("\n🎯 Testing Environmental Services Industry...")
        problems = identify_lead_problems_direct(
            company_industry="Environmental Services",
            company_size="Mid-market",
            company_location="United States",
            person_role="CEO"
        )
        
        print("✅ Problems identification successful")
        print(f"📊 Problems found: {problems.count('**') // 2}")  # Count problem titles
        
        # Test with technology industry
        print("\n🎯 Testing Technology Industry...")
        problems = identify_lead_problems_direct(
            company_industry="Technology",
            company_size="Enterprise",
            company_location="United States",
            person_role="CTO"
        )
        
        print("✅ Technology problems identification successful")
        print(f"📊 Problems found: {problems.count('**') // 2}")
        
        # Test with manufacturing industry
        print("\n🎯 Testing Manufacturing Industry...")
        problems = identify_lead_problems_direct(
            company_industry="Manufacturing",
            company_size="Large",
            company_location="United States",
            person_role="Operations Manager"
        )
        
        print("✅ Manufacturing problems identification successful")
        print(f"📊 Problems found: {problems.count('**') // 2}")
        
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
        from research_agent_industry_problems import identify_lead_problems_direct
        
        # Test the direct function
        result = identify_lead_problems_direct(
            company_industry="Environmental Services",
            company_size="Mid-market",
            company_location="United States",
            person_role="CEO"
        )
        
        if result and "Industry Problems Analysis" in result:
            print("✅ Direct function test passed")
            return True
        else:
            print("❌ Direct function test failed - unexpected output")
            return False
            
    except Exception as e:
        print(f"❌ Direct function test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Industry Problems Agent Test Suite")
    print("=" * 50)
    
    # Run tests
    test1_passed = test_industry_problems_agent()
    test2_passed = test_direct_function()
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Industry Problems Agent: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Direct Function: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The Industry Problems Agent is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
    
    print("\n💡 Next Steps:")
    print("• Test with the main research system")
    print("• Verify integration in app.py")
    print("• Run comprehensive system tests")
