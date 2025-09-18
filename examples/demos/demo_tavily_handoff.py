"""
Demo: Tavily Research Agent with Handoff System Integration

This demo shows how the Tavily research agent enhances the handoff system
by providing comprehensive web research based on contact type analysis.
"""

import os
from dotenv import load_dotenv, find_dotenv
from research_agent_tavily import TavilyResearchAgent
from deep_research_system_handoffs import ResearchContext, AgentType
import json

# Load environment variables
load_dotenv(find_dotenv())

def demo_tavily_handoff_integration():
    """Demonstrate Tavily research agent integration with handoff system."""
    
    print("🚀 Tavily Research Agent + Handoff System Demo")
    print("=" * 60)
    
    # Initialize Tavily research agent
    try:
        tavily_agent = TavilyResearchAgent()
        print("✅ Tavily Research Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Tavily agent: {e}")
        return
    
    # Sample leads for demonstration
    demo_leads = [
        {
            "company_name": "InnovateTech Solutions",
            "person_name": "Sarah Chen",
            "person_role": "CTO",
            "contact_type": "executive",
            "company_industry": "Technology"
        },
        {
            "company_name": "DataFlow Analytics",
            "person_name": "Mike Rodriguez",
            "person_role": "Senior Data Engineer",
            "contact_type": "technical",
            "company_industry": "Data Analytics"
        },
        {
            "company_name": "GreenGrowth Corp",
            "person_name": "Lisa Thompson",
            "person_role": "Marketing Manager",
            "contact_type": "general",
            "company_industry": "Sustainability"
        }
    ]
    
    for i, lead in enumerate(demo_leads, 1):
        print(f"\n📊 Lead {i}: {lead['person_name']} at {lead['company_name']}")
        print(f"   Role: {lead['person_role']}")
        print(f"   Contact Type: {lead['contact_type']}")
        print(f"   Industry: {lead['company_industry']}")
        print("-" * 50)
        
        # Perform comprehensive research with Tavily
        try:
            research_results = tavily_agent.research_lead_with_tavily(
                company_name=lead['company_name'],
                person_name=lead['person_name'],
                person_role=lead['person_role'],
                company_industry=lead['company_industry'],
                contact_type=lead['contact_type']
            )
            
            # Display key findings
            print("🔍 Research Results:")
            
            # Company research highlights
            if research_results.get('company_research'):
                company = research_results['company_research']
                if company.get('recent_news'):
                    print(f"   📰 Recent News: {len(company['recent_news'])} items found")
                if company.get('challenges'):
                    print(f"   ⚠️  Challenges: {len(company['challenges'])} identified")
                if company.get('growth_indicators'):
                    print(f"   📈 Growth: {len(company['growth_indicators'])} positive signals")
            
            # Person research highlights
            if research_results.get('person_research'):
                person = research_results['person_research']
                if person.get('recent_activity'):
                    print(f"   🎯 Recent Activity: {len(person['recent_activity'])} items found")
                if person.get('thought_leadership'):
                    print(f"   💡 Thought Leadership: {len(person['thought_leadership'])} indicators")
            
            # Market research highlights
            if research_results.get('market_research'):
                market = research_results['market_research']
                if market.get('industry_trends'):
                    print(f"   📊 Market Trends: {len(market['industry_trends'])} insights")
                if market.get('competitive_landscape'):
                    print(f"   🏆 Competitive Analysis: {len(market['competitive_landscape'])} findings")
            
            # Opportunity analysis
            if research_results.get('opportunity_analysis'):
                opportunities = research_results['opportunity_analysis']
                if opportunities.get('immediate_opportunities'):
                    print(f"   🚀 Immediate Opportunities: {len(opportunities['immediate_opportunities'])} high-priority")
                if opportunities.get('strategic_opportunities'):
                    print(f"   🎯 Strategic Opportunities: {len(opportunities['strategic_opportunities'])} long-term")
                
                # Display timing recommendations
                if opportunities.get('timing_recommendations'):
                    print("   ⏰ Timing Recommendations:")
                    for rec in opportunities['timing_recommendations'][:2]:  # Show first 2
                        print(f"      • {rec}")
                
                # Display approach strategy
                if opportunities.get('approach_strategy'):
                    print("   🎯 Approach Strategy:")
                    for strategy in opportunities['approach_strategy'][:2]:  # Show first 2
                        print(f"      • {strategy}")
            
            # Research summary
            if research_results.get('research_summary'):
                print(f"\n📋 Research Summary:")
                print(f"   {research_results['research_summary']}")
            
        except Exception as e:
            print(f"   ❌ Research failed: {e}")
        
        print("\n" + "=" * 60)

def demo_quick_research():
    """Demonstrate quick research functionality."""
    
    print("\n⚡ Quick Research Demo")
    print("=" * 40)
    
    try:
        tavily_agent = TavilyResearchAgent()
        
        # Test quick research for different contact types
        quick_leads = [
            ("TechCorp Inc.", "John Smith", "executive"),
            ("DataWorks LLC", "Emily Chen", "technical"),
            ("GrowthCo", "David Wilson", "general")
        ]
        
        for company, person, contact_type in quick_leads:
            print(f"\n🔍 Quick Research: {person} at {company}")
            print(f"   Contact Type: {contact_type}")
            
            try:
                quick_summary = tavily_agent.quick_research(
                    company_name=company,
                    person_name=person,
                    contact_type=contact_type
                )
                
                print("   Results:")
                for line in quick_summary.split('\n'):
                    if line.strip():
                        print(f"      {line}")
                        
            except Exception as e:
                print(f"   ❌ Quick research failed: {e}")
                
    except Exception as e:
        print(f"❌ Quick research demo failed: {e}")

def demo_handoff_integration():
    """Demonstrate how Tavily research integrates with handoff decisions."""
    
    print("\n🔄 Handoff System Integration Demo")
    print("=" * 50)
    
    try:
        tavily_agent = TavilyResearchAgent()
        
        # Simulate handoff decision process
        print("1. Initial lead analysis...")
        print("2. Handoff decision made...")
        print("3. Tavily research triggered based on contact type...")
        print("4. Enhanced intelligence provided to specialist agent...")
        
        # Example: Executive contact handoff
        print("\n📋 Example: Executive Contact Handoff")
        print("   Lead: CEO of growing startup")
        print("   Handoff: Route to Executive Specialist")
        print("   Tavily Research: Strategic business intelligence + market positioning")
        
        # Example: Technical contact handoff
        print("\n📋 Example: Technical Contact Handoff")
        print("   Lead: Senior Data Engineer")
        print("   Handoff: Route to Technical Specialist")
        print("   Tavily Research: Technical trends + implementation insights")
        
        # Example: General contact handoff
        print("\n📋 Example: General Contact Handoff")
        print("   Lead: Marketing Manager")
        print("   Handoff: Route to General Coordinator")
        print("   Tavily Research: Industry trends + business value focus")
        
    except Exception as e:
        print(f"❌ Handoff integration demo failed: {e}")

def main():
    """Run the complete Tavily handoff integration demo."""
    
    print("🎯 Tavily Research Agent + Handoff System Integration")
    print("=" * 70)
    print("This demo shows how Tavily API enhances lead research")
    print("by providing real-time web intelligence based on handoff decisions.")
    print()
    
    # Check if Tavily API key is available
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ TAVILY_API_KEY not found in environment variables")
        print("Please add your Tavily API key to your .env file:")
        print("TAVILY_API_KEY=your_tavily_api_key_here")
        print()
        print("Get your Tavily API key from: https://tavily.com/")
        return
    
    try:
        # Run demos
        demo_tavily_handoff_integration()
        demo_quick_research()
        demo_handoff_integration()
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Key Benefits of Tavily + Handoff Integration:")
        print("   • Real-time web intelligence for leads")
        print("   • Contact-type specific research focus")
        print("   • Enhanced opportunity identification")
        print("   • Market context and competitive insights")
        print("   • Timing and approach recommendations")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Please check your Tavily API key and internet connection.")

if __name__ == "__main__":
    main()
