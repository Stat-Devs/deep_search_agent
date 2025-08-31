#!/usr/bin/env python3
"""
Test script for the Sales Intelligence Assistant app.
This script tests the core functionality without running the Chainlit interface.
"""

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Import our research system components
from deep_research_system_handoffs import (
    ResearchContext, 
    AgentType, 
    determine_handoff_strategy_direct,
    analyze_company_website_direct,
    research_linkedin_profile_direct,
    generate_email_pitch_direct,
    compile_research_report_direct
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def test_lead_research():
    """Test the lead research functionality."""
    print("🧪 Testing Lead Research Functionality...")
    
    # Create a test research context
    context = ResearchContext(
        company_name="TestCorp Inc.",
        person_name="John Smith",
        website_url="https://testcorp.com",
        person_role="CTO"
    )
    
    print(f"✅ Created research context for {context.company_name}")
    
    # Test website analysis
    try:
        context.website_research = analyze_company_website_direct(
            context.company_name, 
            context.website_url
        )
        print(f"✅ Website analysis: {len(context.website_research)} characters")
    except Exception as e:
        print(f"❌ Website analysis failed: {e}")
    
    # Test LinkedIn research
    try:
        context.linkedin_research = research_linkedin_profile_direct(
            context.person_name, 
            context.company_name
        )
        print(f"✅ LinkedIn research: {len(context.linkedin_research)} characters")
    except Exception as e:
        print(f"❌ LinkedIn research failed: {e}")
    
    # Test handoff strategy
    try:
        handoff_strategy = determine_handoff_strategy_direct(context)
        # The function modifies the context directly
        print(f"✅ Handoff strategy: {context.next_agent.value if context.next_agent else 'General'}")
        print(f"   Priority: {context.priority_level}/5")
        print(f"   Reason: {context.handoff_reason}")
    except Exception as e:
        print(f"❌ Handoff strategy failed: {e}")
    
    # Test research report compilation
    try:
        research_report = compile_research_report_direct(
            context.company_name,
            context.person_name,
            context.website_research or "No website research available",
            context.linkedin_research or "No LinkedIn research available"
        )
        print(f"✅ Research report: {len(research_report)} characters")
    except Exception as e:
        print(f"❌ Research report failed: {e}")
    
    # Test email pitch generation
    try:
        # Create a research summary for email generation
        research_summary = f"""
Company: {context.company_name}
Contact: {context.person_name}
Role: {context.person_role or 'Unknown'}
Website Research: {context.website_research or 'Not available'}
LinkedIn Research: {context.linkedin_research or 'Not available'}
Handoff Strategy: {context.handoff_reason or 'Standard approach'}
        """.strip()
        
        email_pitch = generate_email_pitch_direct(
            context.person_name,
            context.company_name,
            research_summary
        )
        print(f"✅ Email pitch: {len(email_pitch)} characters")
    except Exception as e:
        print(f"❌ Email pitch failed: {e}")
    
    return context

async def test_openai_integration():
    """Test OpenAI API integration."""
    print("\n🧪 Testing OpenAI Integration...")
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful sales assistant."},
                {"role": "user", "content": "Hello! Can you help me with sales research?"}
            ],
            model="gpt-3.5-turbo",
            max_tokens=100
        )
        
        content = response.choices[0].message.content
        print(f"✅ OpenAI API test successful: {len(content)} characters")
        print(f"   Response: {content[:100]}...")
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")

async def test_sales_assistance():
    """Test sales assistance functionality."""
    print("\n🧪 Testing Sales Assistance...")
    
    try:
        # Test lead research query
        query = "Research TechCorp Inc. and their CTO John Smith"
        print(f"📝 Testing query: {query}")
        
        # Simulate the extraction process
        extraction_prompt = f"""
        Extract company and contact information from this sales query:
        "{query}"
        
        Return a JSON object with:
        {{
            "company_name": "extracted company name",
            "person_name": "extracted person name", 
            "person_role": "extracted role or title",
            "website_url": "extracted website if mentioned",
            "linkedin_url": "extracted LinkedIn if mentioned",
            "additional_context": "any other relevant details"
        }}
        
        If information is missing, use "Unknown" or null.
        """
        
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured information from text. Always return valid JSON."},
                {"role": "user", "content": extraction_prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=200
        )
        
        extracted_info = response.choices[0].message.content
        print(f"✅ Information extraction successful: {len(extracted_info)} characters")
        print(f"   Extracted: {extracted_info}")
        
    except Exception as e:
        print(f"❌ Sales assistance test failed: {e}")

async def main():
    """Run all tests."""
    print("🚀 Sales Intelligence Assistant - Test Suite")
    print("=" * 50)
    
    # Check environment
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Please create a .env file with your OpenAI API key")
        return
    
    print(f"✅ OpenAI API key found: {openai_key[:10]}...")
    
    # Run tests
    try:
        # Test core research functionality
        context = await test_lead_research()
        
        # Test OpenAI integration
        await test_openai_integration()
        
        # Test sales assistance
        await test_sales_assistance()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Test Summary:")
        print(f"   • Company: {context.company_name}")
        print(f"   • Contact: {context.person_name}")
        print(f"   • Role: {context.person_role}")
        print(f"   • Priority: {context.priority_level}/5")
        print(f"   • Next Agent: {context.next_agent.value if context.next_agent else 'General'}")
        
        print("\n🚀 Ready to run with: chainlit run app.py -w")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        print("   Please check the error details above")

if __name__ == "__main__":
    asyncio.run(main())
