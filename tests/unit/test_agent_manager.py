"""
Test file for Agent Manager

This file tests the functionality of the Agent Manager to ensure
it correctly orchestrates and manages all agents.
"""

import asyncio
import sys
import os
import time
from typing import Dict, Any

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_agent_manager_imports():
    """Test that all required modules can be imported."""
    
    print("🧪 Testing Agent Manager Imports...")
    print("=" * 40)
    
    try:
        from agent_manager import AgentManager, AgentStatus, RequestPriority, Request, AgentInfo, AgentMetrics
        print("✅ Agent Manager classes imported successfully")
        
        from agent_adapters import AgentAdapter, create_agent_adapters
        print("✅ Agent Adapters imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_agent_manager_initialization():
    """Test Agent Manager initialization."""
    
    print("\n🧪 Testing Agent Manager Initialization...")
    print("=" * 45)
    
    try:
        from agent_manager import AgentManager
        
        # Test with default config
        manager = AgentManager()
        print("✅ Agent Manager created with default config")
        
        # Test with custom config
        custom_config = {
            'health_check_interval': 15,
            'max_retries': 5,
            'agent_timeout': 600
        }
        manager_custom = AgentManager(custom_config)
        print("✅ Agent Manager created with custom config")
        
        # Verify config values
        assert manager_custom.config['health_check_interval'] == 15
        assert manager_custom.config['max_retries'] == 5
        assert manager_custom.config['agent_timeout'] == 600
        print("✅ Custom config values verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization test failed: {e}")
        return False

def test_agent_registration():
    """Test agent registration functionality."""
    
    print("\n🧪 Testing Agent Registration...")
    print("=" * 35)
    
    try:
        from agent_manager import AgentManager, AgentStatus
        
        manager = AgentManager()
        
        # Test agent registration
        success = manager.register_agent(
            agent_id="test_agent",
            agent=object(),  # Mock agent
            agent_type="Test Agent",
            capabilities=["test_capability"],
            max_concurrent=3
        )
        
        if success:
            print("✅ Test agent registered successfully")
        else:
            print("❌ Test agent registration failed")
            return False
        
        # Verify agent info
        agent_info = manager.agent_info.get("test_agent")
        if agent_info:
            print(f"✅ Agent info created: {agent_info.agent_id}")
            print(f"   Status: {agent_info.status}")
            print(f"   Capabilities: {agent_info.capabilities}")
        else:
            print("❌ Agent info not found")
            return False
        
        # Test duplicate registration
        success_duplicate = manager.register_agent(
            agent_id="test_agent",
            agent=object(),
            agent_type="Test Agent Updated",
            capabilities=["test_capability", "updated_capability"],
            max_concurrent=5
        )
        
        if success_duplicate:
            print("✅ Duplicate agent registration handled correctly")
        else:
            print("❌ Duplicate agent registration failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Agent registration test failed: {e}")
        return False

def test_request_submission():
    """Test request submission functionality."""
    
    print("\n🧪 Testing Request Submission...")
    print("=" * 35)
    
    try:
        from agent_manager import AgentManager, RequestPriority
        
        manager = AgentManager()
        
        # Test request submission
        payload = {"test": "data"}
        request_id = manager.submit_request(
            request_type="test_request",
            payload=payload,
            priority=RequestPriority.HIGH
        )
        
        if request_id:
            print(f"✅ Request submitted successfully: {request_id}")
        else:
            print("❌ Request submission failed")
            return False
        
        # Verify request in queue
        queue_size = manager.request_queue.qsize()
        if queue_size > 0:
            print(f"✅ Request added to queue: {queue_size} items")
        else:
            print("❌ Request not added to queue")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Request submission test failed: {e}")
        return False

def test_agent_selection():
    """Test agent selection logic."""
    
    print("\n🧪 Testing Agent Selection...")
    print("=" * 30)
    
    try:
        from agent_manager import AgentManager
        
        manager = AgentManager()
        
        # Register multiple test agents
        manager.register_agent(
            agent_id="agent_1",
            agent=object(),
            agent_type="Test Agent 1",
            capabilities=["capability_1", "capability_2"],
            max_concurrent=2
        )
        
        manager.register_agent(
            agent_id="agent_2",
            agent=object(),
            agent_type="Test Agent 2",
            capabilities=["capability_2", "capability_3"],
            max_concurrent=3
        )
        
        # Test agent selection
        selected_agent = manager._select_agent("capability_2", {"test": "data"})
        
        if selected_agent:
            print(f"✅ Agent selected: {selected_agent}")
        else:
            print("❌ No agent selected")
            return False
        
        # Test with unavailable capability
        selected_agent = manager._select_agent("capability_4", {"test": "data"})
        
        if selected_agent is None:
            print("✅ Correctly no agent selected for unavailable capability")
        else:
            print("❌ Agent selected for unavailable capability")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Agent selection test failed: {e}")
        return False

def test_metrics_calculation():
    """Test agent metrics calculation."""
    
    print("\n🧪 Testing Metrics Calculation...")
    print("=" * 35)
    
    try:
        from agent_manager import AgentManager
        
        manager = AgentManager()
        
        # Register a test agent
        manager.register_agent(
            agent_id="metrics_test_agent",
            agent=object(),
            agent_type="Metrics Test Agent",
            capabilities=["test_capability"],
            max_concurrent=2
        )
        
        # Update metrics
        manager._update_agent_metrics("metrics_test_agent", True, 2.5)
        manager._update_agent_metrics("metrics_test_agent", True, 1.5)
        manager._update_agent_metrics("metrics_test_agent", False, 0.5)
        
        # Get metrics
        metrics = manager.get_agent_metrics("metrics_test_agent")
        
        if metrics:
            print("✅ Agent metrics retrieved successfully")
            print(f"   Total Requests: {metrics['total_requests']}")
            print(f"   Success Rate: {metrics['success_rate']:.2%}")
            print(f"   Error Rate: {metrics['error_rate']:.2%}")
            print(f"   Avg Response Time: {metrics['average_response_time']:.2f}s")
            
            # Verify calculations
            assert metrics['total_requests'] == 3
            assert metrics['success_rate'] == 2/3
            assert metrics['error_rate'] == 1/3
            print("✅ Metrics calculations verified")
            
        else:
            print("❌ Agent metrics not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Metrics calculation test failed: {e}")
        return False

def test_system_status():
    """Test system status functionality."""
    
    print("\n🧪 Testing System Status...")
    print("=" * 30)
    
    try:
        from agent_manager import AgentManager
        
        manager = AgentManager()
        
        # Register some test agents
        manager.register_agent(
            agent_id="status_test_1",
            agent=object(),
            agent_type="Status Test Agent 1",
            capabilities=["test_capability"],
            max_concurrent=2
        )
        
        manager.register_agent(
            agent_id="status_test_2",
            agent=object(),
            agent_type="Status Test Agent 2",
            capabilities=["test_capability"],
            max_concurrent=2
        )
        
        # Get system status
        status = manager.get_system_status()
        
        if status:
            print("✅ System status retrieved successfully")
            print(f"   Status: {status['status']}")
            print(f"   Total Agents: {status['total_agents']}")
            print(f"   Active Agents: {status['active_agents']}")
            print(f"   Queue Size: {status['queue_size']}")
            
            # Verify status values
            assert status['total_agents'] == 2
            assert status['active_agents'] == 2
            assert 'status_test_1' in status['agents']
            assert 'status_test_2' in status['agents']
            print("✅ System status values verified")
            
        else:
            print("❌ System status not retrieved")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ System status test failed: {e}")
        return False

async def test_async_functionality():
    """Test async functionality of the Agent Manager."""
    
    print("\n🧪 Testing Async Functionality...")
    print("=" * 35)
    
    try:
        from agent_manager import initialize_agent_manager, shutdown_agent_manager
        
        # Test initialization
        manager = await initialize_agent_manager()
        print("✅ Agent Manager initialized asynchronously")
        
        # Test shutdown
        await shutdown_agent_manager()
        print("✅ Agent Manager shutdown asynchronously")
        
        return True
        
    except Exception as e:
        print(f"❌ Async functionality test failed: {e}")
        return False

def test_agent_adapters():
    """Test agent adapters creation."""
    
    print("\n🧪 Testing Agent Adapters...")
    print("=" * 30)
    
    try:
        from agent_adapters import create_agent_adapters
        
        # Create adapters
        adapters = create_agent_adapters()
        
        if adapters:
            print(f"✅ Created {len(adapters)} agent adapters")
            
            for agent_id, adapter in adapters.items():
                print(f"   {agent_id}: {adapter.agent_type}")
                print(f"     Capabilities: {', '.join(adapter.capabilities)}")
        else:
            print("❌ No agent adapters created")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Agent adapters test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    
    print("🚀 Agent Manager Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_agent_manager_imports),
        ("Initialization Tests", test_agent_manager_initialization),
        ("Agent Registration Tests", test_agent_registration),
        ("Request Submission Tests", test_request_submission),
        ("Agent Selection Tests", test_agent_selection),
        ("Metrics Calculation Tests", test_metrics_calculation),
        ("System Status Tests", test_system_status),
        ("Agent Adapters Tests", test_agent_adapters),
    ]
    
    results = {}
    
    # Run synchronous tests
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
        except Exception as e:
            results[test_name] = False
            print(f"{test_name}: ❌ FAILED - {e}")
    
    # Run async tests
    try:
        async_result = asyncio.run(test_async_functionality())
        results["Async Functionality Tests"] = async_result
        status = "✅ PASSED" if async_result else "❌ FAILED"
        print(f"Async Functionality Tests: {status}")
    except Exception as e:
        results["Async Functionality Tests"] = False
        print(f"Async Functionality Tests: ❌ FAILED - {e}")
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Agent Manager is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
    
    print("\n💡 Next Steps:")
    print("• Run the demo: python demo_agent_manager.py")
    print("• Integrate with your app.py")
    print("• Test with real agent workloads")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
