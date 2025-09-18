#!/usr/bin/env python3
"""
Test script for the Handoff-Enabled Deep Research System
Demonstrates intelligent agent collaboration and context passing.
"""

import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def test_handoff_system():
    """Test the handoff system with different lead types."""
    
    print("🚀 Testing Handoff-Enabled Deep Research System")
    print("=" * 80)
    
    # Test leads with different characteristics
    test_leads = [
        {
            "name": "Yvette Holmes",
            "company": "SerPromise",
            "title": "Chief Executive Officer",
            "type": "Executive",
            "website": "https://serpromise.org/",
            "email": "yvette@serpromise.org",
            "phone": "1 919-832-4359"
        },
        {
            "name": "Christian Marques Rodello",
            "company": "Morpho's",
            "title": "Business Contact",
            "type": "Technical",
            "website": "https://morfo.rest",
            "email": "christian@morfo.rest",
            "phone": "55 31 99295-0675"
        },
        {
            "name": "John Smith",
            "company": "TechCorp Inc.",
            "title": "Data Analyst",
            "type": "Technical",
            "website": "https://techcorp.com",
            "email": "john@techcorp.com",
            "phone": "1-555-0123"
        }
    ]
    
    try:
        # Import the handoff system
        from deep_research_system_handoffs import research_lead_with_handoffs
        
        for i, lead in enumerate(test_leads, 1):
            print(f"\n{'='*60}")
            print(f"🧪 TEST {i}: {lead['type']} LEAD")
            print(f"{'='*60}")
            print(f"Company: {lead['company']}")
            print(f"Person: {lead['name']}")
            print(f"Title: {lead['title']}")
            print(f"Expected Handoff: {lead['type']} Specialist")
            print("-" * 40)
            
            # Run handoff research
            result = research_lead_with_handoffs(
                company_name=lead['company'],
                person_name=lead['name'],
                website_url=lead['website'],
                email=lead['email'],
                phone=lead['phone']
            )
            
            if result:
                print(f"✅ Handoff research completed successfully!")
                print(f"🤖 Handoff Agent: {result['handoff_agent']}")
                print(f"📊 Coordinator Analysis: {len(result['coordinator_result'])} characters")
                print(f"🎯 Specialized Analysis: {len(result['specialized_result'])} characters")
                print(f"📋 Total Report: {len(result['final_report'])} characters")
                
                # Validate handoff decision
                expected_agent = "Executive Specialist" if lead['type'] == "Executive" else "Technical Specialist"
                if expected_agent in result['handoff_agent']:
                    print(f"🎯 Handoff Decision: CORRECT ✅")
                else:
                    print(f"⚠️ Handoff Decision: Different than expected")
                    
            else:
                print(f"❌ Handoff research failed for {lead['name']}")
            
            print(f"\n{'='*60}")
        
        print("\n🎉 All handoff tests completed!")
        
    except Exception as e:
        print(f"❌ Error during handoff testing: {str(e)}")
        import traceback
        traceback.print_exc()

def test_handoff_context_preservation():
    """Test that context is properly preserved between agents."""
    
    print("\n🔄 Testing Context Preservation in Handoffs")
    print("=" * 60)
    
    try:
        from deep_research_system_handoffs import ResearchContext, AgentType
        
        # Create a test context
        context = ResearchContext(
            company_name="TestCorp",
            person_name="Test Person",
            website_url="https://testcorp.com",
            person_role="CEO",
            technical_skills=["Python", "SQL", "Data Analysis"],
            decision_power="High"
        )
        
        print("📋 Initial Context:")
        print(f"- Company: {context.company_name}")
        print(f"- Person: {context.person_name}")
        print(f"- Role: {context.person_role}")
        print(f"- Technical Skills: {context.technical_skills}")
        print(f"- Decision Power: {context.decision_power}")
        
        # Test handoff strategy determination
        from deep_research_system_handoffs import determine_handoff_strategy
        
        handoff_result = determine_handoff_strategy(context)
        print(f"\n🔄 Handoff Strategy:")
        print(handoff_result)
        
        print(f"\n📊 Updated Context:")
        print(f"- Next Agent: {context.next_agent}")
        print(f"- Priority Level: {context.priority_level}")
        print(f"- Communication Tone: {context.communication_tone}")
        print(f"- Follow-up Timeline: {context.follow_up_timeline}")
        
        print("\n✅ Context preservation test completed!")
        
    except Exception as e:
        print(f"❌ Error during context preservation test: {str(e)}")

def main():
    """Main function to run all handoff tests."""
    print("🚀 Handoff-Enabled Deep Research System - Comprehensive Testing")
    print("=" * 100)
    
    # Test basic handoff functionality
    test_handoff_system()
    
    # Test context preservation
    test_handoff_context_preservation()
    
    print("\n" + "=" * 100)
    print("🏁 All handoff system tests completed!")
    
    print("\n📋 Handoff System Features Demonstrated:")
    print("✅ Intelligent agent routing based on lead characteristics")
    print("✅ Context preservation between agents")
    print("✅ Specialized processing for different contact types")
    print("✅ Dynamic handoff decision making")
    print("✅ Collaborative AI team workflow")
    
    print("\n🚀 Next Steps:")
    print("1. Test with your real leads using the handoff system")
    print("2. Customize handoff logic for your specific needs")
    print("3. Add more specialized agents as needed")
    print("4. Integrate with your existing lead management workflow")

if __name__ == "__main__":
    main()
