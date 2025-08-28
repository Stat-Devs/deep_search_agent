#!/usr/bin/env python3
"""
Demo script for the Handoff-Enabled Deep Research System
Shows how agents collaborate and hand off work intelligently.
"""

import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def demo_single_handoff():
    """Demonstrate the handoff system with a single lead."""
    
    print("🎯 Handoff System Demo - Single Lead")
    print("=" * 60)
    
    # Demo lead
    company_name = "InnovateTech Solutions"
    person_name = "Sarah Chen"
    person_title = "Chief Technology Officer"
    website_url = "https://innovatetech.com"
    email = "sarah.chen@innovatetech.com"
    phone = "1-555-0124"
    
    print(f"Company: {company_name}")
    print(f"Person: {person_name}")
    print(f"Title: {person_title}")
    print(f"Website: {website_url}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    print("-" * 60)
    
    print("\n🤖 Starting Handoff Research Process...")
    print("The system will now:")
    print("1. Research the lead with the coordinator agent")
    print("2. Determine the best specialized agent")
    print("3. Hand off to the appropriate specialist")
    print("4. Generate specialized recommendations")
    
    try:
        # Import and run the handoff system
        from deep_research_system_handoffs import research_lead_with_handoffs
        
        print("\n🚀 Executing handoff research...")
        result = research_lead_with_handoffs(
            company_name=company_name,
            person_name=person_name,
            website_url=website_url,
            email=email,
            phone=phone
        )
        
        if result:
            print("\n🎉 Handoff Research Completed Successfully!")
            print("=" * 60)
            
            print(f"🤖 Handoff Agent: {result['handoff_agent']}")
            print(f"📊 Coordinator Analysis Length: {len(result['coordinator_result'])} characters")
            print(f"🎯 Specialized Analysis Length: {len(result['specialized_result'])} characters")
            print(f"📋 Total Report Length: {len(result['final_report'])} characters")
            
            print("\n📋 Handoff Decision Summary:")
            if "Executive" in result['handoff_agent']:
                print("✅ Lead routed to Executive Specialist")
                print("   - High-level strategic approach")
                print("   - ROI and business impact focus")
                print("   - Executive communication tone")
            elif "Technical" in result['handoff_agent']:
                print("✅ Lead routed to Technical Specialist")
                print("   - Technical integration focus")
                print("   - Implementation details")
                print("   - Technical ROI demonstration")
            else:
                print("✅ Lead handled by General Coordinator")
                print("   - Standard professional approach")
                print("   - General value proposition")
                print("   - Standard follow-up timeline")
            
            print(f"\n💾 Full report saved to: handoff_research_{company_name.replace(' ', '_')}_{person_name.replace(' ', '_')}.md")
            
            return result
        else:
            print("❌ Handoff research failed")
            return None
            
    except Exception as e:
        print(f"❌ Error during handoff demo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def explain_handoff_benefits():
    """Explain the benefits of the handoff system."""
    
    print("\n🔄 Handoff System Benefits")
    print("=" * 60)
    
    print("🎯 **Intelligent Routing**")
    print("   - Automatically detects contact type and level")
    print("   - Routes to the most appropriate specialist agent")
    print("   - Adapts strategy based on lead characteristics")
    
    print("\n🤝 **Agent Collaboration**")
    print("   - Agents work together as a team")
    print("   - Context is preserved between handoffs")
    print("   - Each agent builds on previous findings")
    
    print("\n⚡ **Specialized Processing**")
    print("   - Executive contacts get strategic, ROI-focused approach")
    print("   - Technical contacts get integration and implementation details")
    print("   - General contacts get professional, value-focused approach")
    
    print("\n📈 **Improved Quality**")
    print("   - Higher-quality, more targeted communications")
    print("   - Better lead qualification and prioritization")
    print("   - Increased conversion rates through personalization")
    
    print("\n🔄 **Dynamic Workflows**")
    print("   - System adapts based on research findings")
    print("   - No rigid, one-size-fits-all approach")
    print("   - Intelligent decision-making at each step")

def main():
    """Main demo function."""
    print("🚀 Handoff-Enabled Deep Research System - Demo")
    print("=" * 80)
    
    # Run the demo
    result = demo_single_handoff()
    
    # Explain benefits
    explain_handoff_benefits()
    
    print("\n" + "=" * 80)
    print("🏁 Handoff System Demo Completed!")
    
    if result:
        print(f"\n🎯 Demo Results:")
        print(f"- Successfully demonstrated agent collaboration")
        print(f"- Handoff decision: {result['handoff_agent']}")
        print(f"- Generated comprehensive research report")
        print(f"- Showcased intelligent routing capabilities")
    
    print("\n🚀 Next Steps:")
    print("1. Test with your real leads using the handoff system")
    print("2. Customize handoff logic for your specific needs")
    print("3. Add more specialized agents as needed")
    print("4. Integrate with your existing lead management workflow")

if __name__ == "__main__":
    main()
