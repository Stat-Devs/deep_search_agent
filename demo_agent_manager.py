"""
Demo Script for Agent Manager

This script demonstrates how to use the Agent Manager to orchestrate
all agents in the Deep Research System.
"""

import asyncio
import logging
import time
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demo_agent_manager():
    """Demonstrate the Agent Manager functionality."""
    
    print("🚀 Agent Manager Demo - Deep Research System")
    print("=" * 60)
    
    try:
        # Import the agent manager
        from agent_manager import initialize_agent_manager, get_agent_manager
        from agent_adapters import register_all_agents
        
        print("📦 Initializing Agent Manager...")
        
        # Initialize the agent manager
        agent_manager = await initialize_agent_manager()
        
        print("✅ Agent Manager initialized successfully")
        
        # Register all available agents
        print("\n🔧 Registering agents...")
        success = await register_all_agents(agent_manager)
        
        if success:
            print("✅ All agents registered successfully")
        else:
            print("⚠️ Some agents failed to register")
        
        # Display system status
        print("\n📊 System Status:")
        status = agent_manager.get_system_status()
        print(f"   Status: {status['status']}")
        print(f"   Total Agents: {status['total_agents']}")
        print(f"   Active Agents: {status['active_agents']}")
        print(f"   Queue Size: {status['queue_size']}")
        
        # Display agent details
        print("\n🤖 Agent Details:")
        for agent_id, agent_info in status['agents'].items():
            print(f"   {agent_id}:")
            print(f"     Status: {agent_info['status']}")
            print(f"     Load: {agent_info['current_load']}")
            print(f"     Health: {agent_info['health_score']}")
            print(f"     Capabilities: {', '.join(agent_info['capabilities'])}")
        
        # Demo: Submit a comprehensive research request
        print("\n🎯 Demo: Submitting Comprehensive Research Request")
        print("-" * 50)
        
        # Create a research request for Mana Nutrition
        research_payload = {
            "company_name": "Mana Nutrition",
            "person_name": "Mark Moore",
            "website_url": "https://mananutrition.org/",
            "linkedin_url": "https://www.linkedin.com/in/markmoore6/",
            "company_industry": "Health & Nutrition",
            "company_size": "Mid-market",
            "company_location": "United States",
            "person_role": "CEO/Founder"
        }
        
        print(f"📋 Research Request:")
        for key, value in research_payload.items():
            print(f"   {key}: {value}")
        
        # Submit the request
        print("\n📤 Submitting request...")
        from agent_manager import RequestPriority
        request_id = agent_manager.submit_request(
            request_type="comprehensive_research",
            payload=research_payload,
            priority=RequestPriority.HIGH
        )
        
        print(f"✅ Request submitted with ID: {request_id}")
        
        # Wait for processing
        print("\n⏳ Waiting for processing...")
        await asyncio.sleep(2)
        
        # Check status
        status = agent_manager.get_system_status()
        print(f"📊 Current Status:")
        print(f"   Processing Requests: {status['processing_requests']}")
        print(f"   Completed Requests: {status['completed_requests']}")
        
        # Get results
        print("\n📥 Retrieving results...")
        result = await agent_manager.get_request_result(request_id, timeout=30.0)
        
        if result:
            print(f"✅ Request completed successfully!")
            print(f"   Status: {result.status}")
            print(f"   Assigned Agent: {result.assigned_agent}")
            print(f"   Processing Time: {result.processing_time:.2f}s")
            
            if result.result:
                print(f"   Result: {str(result.result)[:200]}...")
            else:
                print("   Result: No result data")
        else:
            print("❌ Request failed or timed out")
        
        # Display final metrics
        print("\n📈 Final Metrics:")
        metrics = agent_manager.get_all_metrics()
        for agent_id, agent_metrics in metrics.items():
            if agent_metrics:
                print(f"   {agent_id}:")
                print(f"     Total Requests: {agent_metrics['total_requests']}")
                print(f"     Success Rate: {agent_metrics['success_rate']:.2%}")
                print(f"     Avg Response Time: {agent_metrics['average_response_time']:.2f}s")
                print(f"     Error Rate: {agent_metrics['error_rate']:.2%}")
        
        # Demo: Submit individual agent requests
        print("\n🎯 Demo: Individual Agent Requests")
        print("-" * 40)
        
        # Website research request
        print("\n🌐 Submitting website research request...")
        website_request_id = agent_manager.submit_request(
            request_type="website_research",
            payload={
                "company_name": "Mana Nutrition",
                "website_url": "https://mananutrition.org/"
            },
            priority=RequestPriority.NORMAL
        )
        
        # Industry problems request
        print("🎯 Submitting industry problems request...")
        problems_request_id = agent_manager.submit_request(
            request_type="industry_problems",
            payload={
                "company_industry": "Health & Nutrition",
                "company_size": "Mid-market",
                "company_location": "United States",
                "person_role": "CEO/Founder"
            },
            priority=RequestPriority.HIGH
        )
        
        # Wait for completion
        print("\n⏳ Waiting for individual requests to complete...")
        await asyncio.sleep(5)
        
        # Get results
        website_result = await agent_manager.get_request_result(website_request_id, timeout=10.0)
        problems_result = await agent_manager.get_request_result(problems_request_id, timeout=10.0)
        
        print(f"\n📊 Individual Request Results:")
        print(f"   Website Research: {'✅' if website_result and website_result.status == 'completed' else '❌'}")
        print(f"   Industry Problems: {'✅' if problems_result and problems_result.status == 'completed' else '❌'}")
        
        # Performance test
        print("\n🚀 Performance Test: Multiple Concurrent Requests")
        print("-" * 50)
        
        # Submit multiple requests
        request_ids = []
        for i in range(5):
            request_id = agent_manager.submit_request(
                request_type="industry_problems",
                payload={
                    "company_industry": f"Test Industry {i}",
                    "company_size": "Small",
                    "company_location": "Test Location",
                    "person_role": "Manager"
                },
                priority=RequestPriority.NORMAL
            )
            request_ids.append(request_id)
            print(f"   Request {i+1} submitted: {request_id}")
        
        # Wait for completion
        print("\n⏳ Waiting for concurrent requests to complete...")
        await asyncio.sleep(10)
        
        # Check results
        completed_count = 0
        for request_id in request_ids:
            result = await agent_manager.get_request_result(request_id, timeout=5.0)
            if result and result.status == 'completed':
                completed_count += 1
        
        print(f"✅ Concurrent requests completed: {completed_count}/{len(request_ids)}")
        
        # Final system status
        print("\n📊 Final System Status:")
        final_status = agent_manager.get_system_status()
        print(f"   Status: {final_status['status']}")
        print(f"   Total Requests Processed: {final_status['completed_requests']}")
        print(f"   Active Agents: {final_status['active_agents']}")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        try:
            from agent_manager import shutdown_agent_manager
            await shutdown_agent_manager()
            print("\n🧹 Agent Manager shutdown complete")
        except Exception as e:
            print(f"⚠️ Shutdown error: {e}")

async def demo_agent_health_monitoring():
    """Demonstrate agent health monitoring."""
    
    print("\n🏥 Agent Health Monitoring Demo")
    print("=" * 40)
    
    try:
        from agent_manager import get_agent_manager
        
        agent_manager = get_agent_manager()
        
        # Monitor health for a few cycles
        for cycle in range(3):
            print(f"\n📊 Health Check Cycle {cycle + 1}:")
            
            status = agent_manager.get_system_status()
            print(f"   System Status: {status['status']}")
            print(f"   Active Agents: {status['active_agents']}")
            
            # Check individual agent health
            for agent_id in agent_manager.agents.keys():
                metrics = agent_manager.get_agent_metrics(agent_id)
                if metrics:
                    health_status = "🟢" if metrics['health_score'] > 80 else "🟡" if metrics['health_score'] > 50 else "🔴"
                    print(f"   {health_status} {agent_id}: Health {metrics['health_score']:.1f}, Load {metrics['current_load']}")
            
            await asyncio.sleep(5)
        
        print("✅ Health monitoring demo completed")
        
    except Exception as e:
        print(f"❌ Health monitoring demo failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Agent Manager Demo...")
    
    # Run the main demo
    asyncio.run(demo_agent_manager())
    
    # Run health monitoring demo
    asyncio.run(demo_agent_health_monitoring())
    
    print("\n🎉 All demos completed!")
    print("\n💡 Next Steps:")
    print("   • Integrate Agent Manager into your app.py")
    print("   • Use the manager for centralized agent orchestration")
    print("   • Monitor agent performance and health")
    print("   • Scale your system with the manager's capabilities")
