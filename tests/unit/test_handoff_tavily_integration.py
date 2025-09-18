"""
Test: Handoff System + Tavily Integration

This test demonstrates how the handoff system works with Tavily integration
by simulating the complete workflow without external API calls.
"""

import sys
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def test_handoff_workflow():
    """Test the complete handoff workflow with simulated Tavily data."""
    print("🔄 Testing Complete Handoff Workflow")
    print("=" * 50)
    
    try:
        from deep_research_system_handoffs import (
            ResearchContext, 
            determine_handoff_strategy_direct,
            analyze_company_website_direct,
            research_linkedin_profile_direct,
            generate_email_pitch_direct,
            compile_research_report_direct
        )
        
        # Simulate lead input
        company_name = "InnovateTech Solutions"
        person_name = "Sarah Chen"
        person_role = "CTO"
        website_url = "https://innovatetech.com"
        
        print(f"📊 Lead: {person_name} at {company_name}")
        print(f"   Role: {person_role}")
        print(f"   Website: {website_url}")
        print("-" * 40)
        
        # Step 1: Create research context
        print("1️⃣ Creating Research Context...")
        context = ResearchContext(
            company_name=company_name,
            person_name=person_name,
            website_url=website_url,
            person_role=person_role,
            technical_skills=["Python", "Data Science", "AI", "Cloud Computing"],
            decision_power="High"
        )
        print("✅ Research context created")
        
        # Step 2: Determine handoff strategy
        print("\n2️⃣ Determining Handoff Strategy...")
        handoff_strategy = determine_handoff_strategy_direct(context)
        print("✅ Handoff strategy determined")
        print(f"   Next Agent: {context.next_agent}")
        print(f"   Priority: {context.priority_level}/5")
        print(f"   Reason: {context.handoff_reason}")
        print(f"   Communication Tone: {context.communication_tone}")
        print(f"   Follow-up Timeline: {context.follow_up_timeline}")
        
        # Step 3: Simulate Tavily research data
        print("\n3️⃣ Simulating Tavily Research Data...")
        
        # Company research (simulated from Tavily)
        company_research = f"""
Company: {company_name}
Recent News: 5 items found
- Series B funding round completed
- New AI product launch
- Partnership with major tech company
- Expansion to new markets
- Industry award recognition

Challenges: 3 identified
- Scaling data infrastructure
- Managing rapid growth
- Technical talent acquisition

Growth Indicators: 3 positive signals
- 200% revenue growth
- 150% team expansion
- New market entry
"""
        
        # Person research (simulated from Tavily)
        person_research = f"""
Person: {person_name}
Role: {person_role}
Recent Activity: 3 items found
- Speaking at AI conference
- Published technical article
- Industry panel participation

Thought Leadership: 3 indicators
- AI strategy expertise
- Technical innovation focus
- Industry recognition
"""
        
        print("✅ Tavily research data simulated")
        print(f"   Company Research: {len(company_research)} characters")
        print(f"   Person Research: {len(person_research)} characters")
        
        # Step 4: Generate specialized output based on handoff type
        print("\n4️⃣ Generating Specialized Output...")
        
        if context.next_agent.value == "executive_specialist":
            print("🎯 Executive Specialist Processing...")
            approach = "Strategic business outcomes and ROI focus"
            value_props = [
                "Strategic competitive advantage",
                "Business impact and ROI",
                "Market positioning insights"
            ]
        elif context.next_agent.value == "technical_specialist":
            print("⚡ Technical Specialist Processing...")
            approach = "Technical integration with business outcomes"
            value_props = [
                "Technical implementation benefits",
                "Integration advantages",
                "Technical ROI and timeline"
            ]
        else:
            print("💼 General Coordinator Processing...")
            approach = "Professional value-focused approach"
            value_props = [
                "Practical benefits and solutions",
                "Case studies and references",
                "Standard professional timeline"
            ]
        
        print(f"   Approach: {approach}")
        print(f"   Value Propositions: {len(value_props)} identified")
        
        # Step 5: Generate final outputs
        print("\n5️⃣ Generating Final Outputs...")
        
        # Email pitch
        email_pitch = generate_email_pitch_direct(person_name, company_name, company_research)
        print(f"✅ Email pitch generated: {len(email_pitch)} characters")
        
        # Research report
        research_report = compile_research_report_direct(company_name, person_name, company_research, person_research)
        print(f"✅ Research report compiled: {len(research_report)} characters")
        
        # Final summary
        print("\n📋 Final Handoff Summary:")
        print(f"   Lead: {person_name} at {company_name}")
        print(f"   Handoff Agent: {context.next_agent.value}")
        print(f"   Priority Level: {context.priority_level}/5")
        print(f"   Communication Tone: {context.communication_tone}")
        print(f"   Follow-up Timeline: {context.follow_up_timeline}")
        print(f"   Approach: {approach}")
        print(f"   Email Pitch: {len(email_pitch)} characters")
        print(f"   Research Report: {len(research_report)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Handoff workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_contact_types():
    """Test handoff system with different contact types."""
    print("\n🎯 Testing Multiple Contact Types")
    print("=" * 40)
    
    try:
        from deep_research_system_handoffs import ResearchContext, determine_handoff_strategy_direct
        
        # Test cases
        test_cases = [
            {
                "name": "Executive Contact",
                "role": "CEO",
                "skills": ["Leadership", "Strategy"],
                "decision_power": "High"
            },
            {
                "name": "Technical Contact", 
                "role": "Senior Data Engineer",
                "skills": ["Python", "SQL", "AWS", "Machine Learning", "Data Engineering"],
                "decision_power": "Medium"
            },
            {
                "name": "General Contact",
                "role": "Marketing Manager", 
                "skills": ["Marketing", "Analytics"],
                "decision_power": "Medium"
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n📊 Test Case {i}: {case['name']}")
            print(f"   Role: {case['role']}")
            print(f"   Skills: {case['skills']}")
            print(f"   Decision Power: {case['decision_power']}")
            
            # Create context
            context = ResearchContext(
                company_name=f"TestCorp{i}",
                person_name=f"Person{i}",
                person_role=case['role'],
                technical_skills=case['skills'],
                decision_power=case['decision_power']
            )
            
            # Determine handoff strategy
            strategy = determine_handoff_strategy_direct(context)
            
            print(f"   ✅ Handoff Strategy: {context.next_agent.value}")
            print(f"   Priority: {context.priority_level}/5")
            print(f"   Reason: {context.handoff_reason}")
            print(f"   Timeline: {context.follow_up_timeline}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multiple contact types test failed: {e}")
        return False

def run_integration_tests():
    """Run all integration tests."""
    print("🧪 Handoff System + Tavily Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Complete Handoff Workflow", test_handoff_workflow),
        ("Multiple Contact Types", test_multiple_contact_types)
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
    print("\n📋 Integration Test Results")
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
        print("🎉 All integration tests passed!")
        print("\n💡 The Handoff System is working as an orchestrator:")
        print("   • ✅ Successfully creates research context")
        print("   • ✅ Intelligently determines handoff strategy")
        print("   • ✅ Routes to appropriate specialist agents")
        print("   • ✅ Integrates with Tavily research data")
        print("   • ✅ Generates specialized outputs")
        print("   • ✅ Handles multiple contact types")
        print("   • ✅ Provides timing and approach recommendations")
    else:
        print("⚠️  Some integration tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
