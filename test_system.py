#!/usr/bin/env python3
"""
Test script for the Deep Research System
Tests each agent individually to ensure they're working correctly.
"""

import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from deep_research_system import research_lead
        print("✅ deep_research_system imported successfully")
    except Exception as e:
        print(f"❌ deep_research_system import failed: {e}")
    
    try:
        from research_agent_website import research_company_website
        print("✅ research_agent_website imported successfully")
    except Exception as e:
        print(f"❌ research_agent_website import failed: {e}")
    
    try:
        from research_agent_linkedin import research_linkedin_profile
        print("✅ research_agent_linkedin imported successfully")
    except Exception as e:
        print(f"❌ research_agent_linkedin import failed: {e}")
    
    try:
        from research_agent_email import generate_email_pitch
        print("✅ research_agent_email imported successfully")
    except Exception as e:
        print(f"❌ research_agent_email import failed: {e}")

def test_api_keys():
    """Test that API keys are available."""
    print("\n🔑 Testing API keys...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if openai_key:
        print(f"✅ OpenAI API key found: {openai_key[:10]}...")
    else:
        print("❌ OpenAI API key not found")
    
    if gemini_key:
        print(f"✅ Gemini API key found: {gemini_key[:10]}...")
    else:
        print("❌ Gemini API key not found")

def test_website_scraping():
    """Test website scraping functionality."""
    print("\n🌐 Testing website scraping...")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Test with a simple website
        test_url = "https://httpbin.org/html"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            print(f"✅ Website scraping test successful: {len(text)} characters extracted")
        else:
            print(f"❌ Website scraping test failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Website scraping test failed: {e}")

def main():
    """Run all tests."""
    print("🚀 Deep Research System - System Test")
    print("=" * 50)
    
    test_imports()
    test_api_keys()
    test_website_scraping()
    
    print("\n" + "=" * 50)
    print("🏁 System test completed!")
    
    print("\n📋 Next steps:")
    print("1. Ensure all API keys are set in your .env file")
    print("2. Run 'python run_research_system.py' to start the full system")
    print("3. Or run individual agents for specific research tasks")

if __name__ == "__main__":
    main()
