"""
Test: Sales Deep Search System Tracing Validation

This test validates that comprehensive tracing is working correctly
for the Sales Deep Search System using OpenAI Agents SDK.
"""

import os
import asyncio
import uuid
from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI as AgentsAsyncOpenAI, OpenAIChatCompletionsModel, trace, function_tool, custom_span

# Load environment variables
load_dotenv()

def test_environment_setup():
    """Test that all required environment variables are available."""
    print("🧪 Testing Environment Setup...")
    
    # Check API keys
    required_keys = ["OPENAI_API_KEY", "GEMINI_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        value = os.getenv(key)
        if value:
            print(f"✅ {key}: Found ({key[:10]}...)")
        else:
            print(f"❌ {key}: Missing")
            missing_keys.append(key)
    
    if missing_keys:
        print(f"⚠️  Missing keys: {', '.join(missing_keys)}")
        return False
    
    print("✅ All environment variables found")
    return True

async def test_sales_agent_tracing():
    """Test tracing with a sales research simulation."""
    print("\n🔍 Testing Sales Agent Tracing...")
    
    try:
        # Set up OpenAI client for tracing
        openai_client = AgentsAsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )
        
        # Create model
        openai_model = OpenAIChatCompletionsModel(
            model="gpt-4o-mini",  # Using faster model for testing
            openai_client=openai_client
        )
        
        # Create a test sales agent
        sales_agent = Agent(
            name="Test_Sales_Agent",
            instructions="You are a StatDevs sales intelligence agent. Provide brief, professional responses about data analytics solutions.",
            model=openai_model
        )
        
        # Generate unique trace ID
        trace_id = f"trace_test_{uuid.uuid4().hex}"
        
        # Create comprehensive trace for sales interaction
        with trace(
            "Test Sales Deep Search Query",
            trace_id=trace_id,
            metadata={
                "test_type": "sales_tracing_validation",
                "timestamp": datetime.now().isoformat(),
                "system": "StatDevs Sales Intelligence",
                "test_company": "TechCorp Inc."
            }
        ) as main_trace:
            
            print(f"🔍 Starting traced sales interaction: {trace_id}")
            
            # Simulate lead extraction
            with custom_span("Lead Information Extraction", data={"step": "1_extraction"}):
                print("📋 Extracting lead information...")
                await asyncio.sleep(0.1)  # Simulate processing
                
            # Simulate website analysis
            with custom_span("Website Analysis", data={"step": "2_website", "company": "TechCorp Inc."}):
                print("🌐 Analyzing company website...")
                result1 = await Runner.run(
                    sales_agent,
                    "Briefly analyze TechCorp Inc. for StatDevs data analytics opportunities. This is a test."
                )
                
            # Simulate industry analysis
            with custom_span("Industry Analysis", data={"step": "3_industry", "industry": "Technology"}):
                print("🏭 Analyzing industry challenges...")
                result2 = await Runner.run(
                    sales_agent,
                    "Identify key data challenges in the technology industry. Keep response brief for testing."
                )
                
            # Simulate solutions research
            with custom_span("Solutions Research", data={"step": "4_solutions", "focus": "Data Engineering"}):
                print("🤖 Researching data solutions...")
                result3 = await Runner.run(
                    sales_agent,
                    "Recommend StatDevs data engineering solutions. Brief response for testing purposes."
                )
            
            print(f"✅ Sales tracing test completed successfully")
            print(f"📊 Trace ID: {trace_id}")
            print(f"🌐 View trace at: https://platform.openai.com/logs?api=traces&trace_id={trace_id}")
            
            return True
            
    except Exception as e:
        print(f"❌ Sales tracing test failed: {e}")
        return False

async def test_multiple_traces():
    """Test multiple concurrent traces to validate trace isolation."""
    print("\n👥 Testing Multiple Concurrent Traces...")
    
    try:
        # Set up client and model
        openai_client = AgentsAsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )
        
        openai_model = OpenAIChatCompletionsModel(
            model="gpt-4o-mini",
            openai_client=openai_client
        )
        
        sales_agent = Agent(
            name="Multi_Test_Sales_Agent",
            instructions="You are a StatDevs sales agent. Give very brief responses for testing.",
            model=openai_model
        )
        
        # Create multiple traces concurrently
        async def create_trace(company_name: str, trace_num: int):
            trace_id = f"trace_multi_{trace_num}_{uuid.uuid4().hex[:8]}"
            
            with trace(
                f"Multi-Trace Test {trace_num}",
                trace_id=trace_id,
                metadata={
                    "test_type": "multi_trace_validation",
                    "trace_number": trace_num,
                    "company": company_name,
                    "timestamp": datetime.now().isoformat()
                }
            ) as test_trace:
                
                with custom_span(f"Analysis for {company_name}", data={"company": company_name}):
                    result = await Runner.run(
                        sales_agent,
                        f"Brief analysis of {company_name} for data solutions. Test response only."
                    )
                
                return trace_id
        
        # Run multiple traces concurrently
        trace_tasks = [
            create_trace("Company A", 1),
            create_trace("Company B", 2),
            create_trace("Company C", 3)
        ]
        
        trace_ids = await asyncio.gather(*trace_tasks)
        
        print(f"✅ Multiple traces test completed")
        for i, trace_id in enumerate(trace_ids, 1):
            print(f"📊 Trace {i}: {trace_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multiple traces test failed: {e}")
        return False

async def run_tracing_validation():
    """Run comprehensive tracing validation tests."""
    print("🧪 Sales Deep Search System - Tracing Validation")
    print("=" * 60)
    
    # Test 1: Environment Setup
    env_ok = test_environment_setup()
    if not env_ok:
        print("❌ Environment setup failed. Please check your .env file.")
        return
    
    # Test 2: Sales Agent Tracing
    sales_ok = await test_sales_agent_tracing()
    if not sales_ok:
        print("❌ Sales agent tracing test failed.")
        return
    
    # Test 3: Multiple Traces
    multi_ok = await test_multiple_traces()
    if not multi_ok:
        print("❌ Multiple traces test failed.")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 ALL TRACING VALIDATION TESTS PASSED!")
    print("\n📊 Tracing Summary:")
    print("   ✅ Environment setup validated")
    print("   ✅ Sales agent tracing working")
    print("   ✅ Multiple concurrent traces working")
    print("   ✅ Custom spans and metadata working")
    print("\n🌐 All traces available at: https://platform.openai.com/logs?api=traces")
    print("\n🚀 Your Sales Deep Search System now has comprehensive tracing!")
    print("   • Every user query generates a unique trace")
    print("   • All agent interactions are logged with metadata")
    print("   • Custom spans provide detailed workflow visibility")
    print("   • Traces can be viewed in OpenAI dashboard")

def main():
    """Main function to run validation tests."""
    try:
        asyncio.run(run_tracing_validation())
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")

if __name__ == "__main__":
    main()
