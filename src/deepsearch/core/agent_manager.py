"""
Agent Manager - Centralized Orchestration for Sales Intelligence Agents

This module provides centralized management for all agents in the Deep Research System,
including agent lifecycle management, request routing, state management, and monitoring.
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import os
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    INITIALIZING = "initializing"

class RequestPriority(Enum):
    """Request priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

@dataclass
class AgentInfo:
    """Information about an agent."""
    agent_id: str
    agent_type: str
    status: AgentStatus = AgentStatus.OFFLINE
    last_heartbeat: datetime = field(default_factory=datetime.now)
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    current_load: int = 0
    max_concurrent_requests: int = 5
    capabilities: List[str] = field(default_factory=list)
    health_score: float = 100.0

@dataclass
class Request:
    """Request object for agent processing."""
    request_id: str
    request_type: str
    priority: RequestPriority
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    assigned_agent: Optional[str] = None
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None

@dataclass
class AgentMetrics:
    """Performance metrics for agents."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    uptime: timedelta = timedelta(0)
    last_request_time: Optional[datetime] = None
    error_rate: float = 0.0

class AgentManager:
    """Centralized manager for all agents in the system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._load_default_config()
        self.agents: Dict[str, Any] = {}
        self.agent_info: Dict[str, AgentInfo] = {}
        self.request_queue: Queue = Queue()
        self.processing_requests: Dict[str, Request] = {}
        self.completed_requests: Dict[str, Request] = {}
        self.metrics: Dict[str, AgentMetrics] = {}
        
        # Thread pool for concurrent processing
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Event loop for async operations
        self.loop = None
        
        # Health check interval
        self.health_check_interval = self.config.get('health_check_interval', 30)
        
        # Initialize logging
        self._setup_logging()
        
        logger.info("Agent Manager initialized")
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            'health_check_interval': 30,
            'max_retries': 3,
            'retry_delay': 1,
            'agent_timeout': 300,
            'max_queue_size': 1000,
            'enable_monitoring': True,
            'enable_caching': True,
            'cache_ttl': 3600
        }
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = self.config.get('log_level', 'INFO')
        logging.getLogger().setLevel(getattr(logging, log_level))
        
        # Add file handler if specified
        log_file = self.config.get('log_file')
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logging.getLogger().addHandler(file_handler)
    
    async def start(self):
        """Start the agent manager."""
        logger.info("Starting Agent Manager...")
        
        # Start health monitoring
        asyncio.create_task(self._health_monitor())
        
        # Start request processor
        asyncio.create_task(self._request_processor())
        
        logger.info("Agent Manager started successfully")
    
    async def stop(self):
        """Stop the agent manager."""
        logger.info("Stopping Agent Manager...")
        
        # Stop all agents
        for agent_id in list(self.agents.keys()):
            await self.stop_agent(agent_id)
        
        # Shutdown thread pool
        self.executor.shutdown(wait=True)
        
        logger.info("Agent Manager stopped")
    
    def register_agent(self, agent_id: str, agent: Any, agent_type: str, 
                      capabilities: List[str], max_concurrent: int = 5) -> bool:
        """Register a new agent with the manager."""
        try:
            if agent_id in self.agents:
                logger.warning(f"Agent {agent_id} already registered, updating...")
            
            self.agents[agent_id] = agent
            self.agent_info[agent_id] = AgentInfo(
                agent_id=agent_id,
                agent_type=agent_type,
                status=AgentStatus.INITIALIZING,
                capabilities=capabilities,
                max_concurrent_requests=max_concurrent
            )
            self.metrics[agent_id] = AgentMetrics()
            
            # Set agent status to idle
            self.agent_info[agent_id].status = AgentStatus.IDLE
            
            logger.info(f"Agent {agent_id} ({agent_type}) registered successfully")
            logger.info(f"Capabilities: {capabilities}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the manager."""
        try:
            if agent_id not in self.agents:
                logger.warning(f"Agent {agent_id} not found")
                return False
            
            # Stop the agent if it's running
            if self.agent_info[agent_id].status == AgentStatus.BUSY:
                logger.warning(f"Agent {agent_id} is busy, cannot unregister")
                return False
            
            del self.agents[agent_id]
            del self.agent_info[agent_id]
            del self.metrics[agent_id]
            
            logger.info(f"Agent {agent_id} unregistered successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False
    
    async def start_agent(self, agent_id: str) -> bool:
        """Start a specific agent."""
        try:
            if agent_id not in self.agents:
                logger.error(f"Agent {agent_id} not found")
                return False
            
            agent_info = self.agent_info[agent_id]
            if agent_info.status == AgentStatus.BUSY:
                logger.warning(f"Agent {agent_id} is already busy")
                return False
            
            # Initialize agent if it has an init method
            agent = self.agents[agent_id]
            if hasattr(agent, 'initialize') and callable(agent.initialize):
                await agent.initialize()
            
            agent_info.status = AgentStatus.IDLE
            agent_info.last_heartbeat = datetime.now()
            
            logger.info(f"Agent {agent_id} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start agent {agent_id}: {e}")
            self.agent_info[agent_id].status = AgentStatus.ERROR
            return False
    
    async def stop_agent(self, agent_id: str) -> bool:
        """Stop a specific agent."""
        try:
            if agent_id not in self.agents:
                logger.error(f"Agent {agent_id} not found")
                return False
            
            agent_info = self.agent_info[agent_id]
            if agent_info.status == AgentStatus.BUSY:
                logger.warning(f"Agent {agent_id} is busy, cannot stop")
                return False
            
            # Cleanup agent if it has a cleanup method
            agent = self.agents[agent_id]
            if hasattr(agent, 'cleanup') and callable(agent.cleanup):
                await agent.cleanup()
            
            agent_info.status = AgentStatus.OFFLINE
            
            logger.info(f"Agent {agent_id} stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop agent {agent_id}: {e}")
            return False
    
    def submit_request(self, request_type: str, payload: Dict[str, Any], 
                      priority: RequestPriority = RequestPriority.NORMAL) -> str:
        """Submit a new request for processing."""
        try:
            if self.request_queue.qsize() >= self.config['max_queue_size']:
                raise Exception("Request queue is full")
            
            request_id = f"req_{int(time.time() * 1000)}_{id(payload)}"
            request = Request(
                request_id=request_id,
                request_type=request_type,
                priority=priority,
                payload=payload
            )
            
            self.request_queue.put((priority.value, request))
            logger.info(f"Request {request_id} submitted: {request_type}")
            
            return request_id
            
        except Exception as e:
            logger.error(f"Failed to submit request: {e}")
            raise
    
    async def get_request_result(self, request_id: str, timeout: float = 60.0) -> Optional[Request]:
        """Get the result of a completed request."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if request_id in self.completed_requests:
                return self.completed_requests[request_id]
            
            if request_id in self.processing_requests:
                # Request is still processing
                await asyncio.sleep(0.1)
            else:
                # Request not found
                logger.warning(f"Request {request_id} not found")
                return None
        
        logger.warning(f"Timeout waiting for request {request_id}")
        return None
    
    def _select_agent(self, request_type: str, payload: Dict[str, Any]) -> Optional[str]:
        """Select the best agent for a given request."""
        available_agents = []
        
        for agent_id, agent_info in self.agent_info.items():
            if agent_info.status != AgentStatus.IDLE:
                continue
            
            if agent_info.current_load >= agent_info.max_concurrent_requests:
                continue
            
            # Check if agent has the required capabilities
            if self._agent_can_handle_request(agent_id, request_type, payload):
                # Calculate agent score based on health, load, and performance
                score = self._calculate_agent_score(agent_id)
                available_agents.append((agent_id, score))
        
        if not available_agents:
            return None
        
        # Select agent with highest score
        available_agents.sort(key=lambda x: x[1], reverse=True)
        return available_agents[0][0]
    
    def _agent_can_handle_request(self, agent_id: str, request_type: str, 
                                 payload: Dict[str, Any]) -> bool:
        """Check if an agent can handle a specific request."""
        agent_info = self.agent_info[agent_id]
        
        # Check basic capabilities
        if request_type not in agent_info.capabilities:
            return False
        
        # Check specific requirements based on request type
        if request_type == "website_research":
            return "website_url" in payload
        elif request_type == "linkedin_research":
            return "linkedin_url" in payload or "person_name" in payload
        elif request_type == "industry_problems":
            return "company_industry" in payload
        elif request_type == "ai_solutions":
            return "industry_problems" in payload
        
        return True
    
    def _calculate_agent_score(self, agent_id: str) -> float:
        """Calculate a score for agent selection."""
        agent_info = self.agent_info[agent_id]
        metrics = self.metrics[agent_id]
        
        # Health score (0-100)
        health_score = agent_info.health_score
        
        # Load factor (lower is better)
        load_factor = 1.0 - (agent_info.current_load / agent_info.max_concurrent_requests)
        
        # Performance score based on success rate and response time
        success_rate = metrics.successful_requests / max(metrics.total_requests, 1)
        response_score = max(0, 1.0 - (metrics.average_response_time / 60.0))  # Normalize to 1 minute
        
        # Calculate weighted score
        score = (
            health_score * 0.4 +
            load_factor * 100 * 0.3 +
            success_rate * 100 * 0.2 +
            response_score * 100 * 0.1
        )
        
        return score
    
    async def _process_request(self, request: Request) -> bool:
        """Process a single request."""
        try:
            # Select agent
            agent_id = self._select_agent(request.request_type, request.payload)
            if not agent_id:
                logger.error(f"No available agent for request {request.request_id}")
                request.status = "failed"
                request.error = "No available agent"
                return False
            
            # Assign agent and update status
            request.assigned_agent = agent_id
            request.status = "processing"
            self.processing_requests[request.request_id] = request
            
            agent_info = self.agent_info[agent_id]
            agent_info.status = AgentStatus.BUSY
            agent_info.current_load += 1
            
            # Execute request
            start_time = time.time()
            
            if asyncio.iscoroutinefunction(self.agents[agent_id].process_request):
                result = await self.agents[agent_id].process_request(request.payload)
            else:
                # Run in thread pool for synchronous agents
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor, 
                    self.agents[agent_id].process_request, 
                    request.payload
                )
            
            processing_time = time.time() - start_time
            
            # Update request
            request.status = "completed"
            request.result = result
            request.processing_time = processing_time
            
            # Update metrics
            self._update_agent_metrics(agent_id, True, processing_time)
            
            # Move to completed requests
            del self.processing_requests[request.request_id]
            self.completed_requests[request.request_id] = request
            
            logger.info(f"Request {request.request_id} completed successfully in {processing_time:.2f}s")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process request {request.request_id}: {e}")
            logger.error(traceback.format_exc())
            
            # Update request status
            request.status = "failed"
            request.error = str(e)
            
            # Update metrics
            if request.assigned_agent:
                self._update_agent_metrics(request.assigned_agent, False, 0)
            
            # Move to completed requests
            if request.request_id in self.processing_requests:
                del self.processing_requests[request.request_id]
            self.completed_requests[request.request_id] = request
            
            return False
        
        finally:
            # Update agent status
            if request.assigned_agent:
                agent_info = self.agent_info[request.assigned_agent]
                agent_info.current_load = max(0, agent_info.current_load - 1)
                agent_info.status = AgentStatus.IDLE if agent_info.current_load == 0 else AgentStatus.BUSY
    
    def _update_agent_metrics(self, agent_id: str, success: bool, processing_time: float):
        """Update agent performance metrics."""
        metrics = self.metrics[agent_id]
        agent_info = self.agent_info[agent_id]
        
        metrics.total_requests += 1
        if success:
            metrics.successful_requests += 1
            agent_info.successful_requests += 1
        else:
            metrics.failed_requests += 1
            agent_info.failed_requests += 1
        
        # Update average response time
        if metrics.total_requests == 1:
            metrics.average_response_time = processing_time
        else:
            metrics.average_response_time = (
                (metrics.average_response_time * (metrics.total_requests - 1) + processing_time) 
                / metrics.total_requests
            )
        
        # Update agent info
        agent_info.average_response_time = metrics.average_response_time
        
        # Calculate error rate
        metrics.error_rate = metrics.failed_requests / metrics.total_requests
        metrics.last_request_time = datetime.now()
        
        # Update health score
        agent_info.health_score = max(0, 100 - (metrics.error_rate * 100))
    
    async def _request_processor(self):
        """Background task to process requests from the queue."""
        logger.info("Request processor started")
        
        while True:
            try:
                # Get next request from queue
                try:
                    priority, request = self.request_queue.get_nowait()
                except Empty:
                    await asyncio.sleep(0.1)
                    continue
                
                # Process request
                await self._process_request(request)
                
            except Exception as e:
                logger.error(f"Error in request processor: {e}")
                await asyncio.sleep(1)
    
    async def _health_monitor(self):
        """Background task to monitor agent health."""
        logger.info("Health monitor started")
        
        while True:
            try:
                current_time = datetime.now()
                
                for agent_id, agent_info in self.agent_info.items():
                    # Check if agent is responsive
                    if agent_info.status == AgentStatus.BUSY:
                        # Check if agent has been busy too long
                        if current_time - agent_info.last_heartbeat > timedelta(seconds=self.config['agent_timeout']):
                            logger.warning(f"Agent {agent_id} timeout, marking as error")
                            agent_info.status = AgentStatus.ERROR
                            agent_info.current_load = 0
                    
                    # Update uptime
                    if agent_info.status in [AgentStatus.IDLE, AgentStatus.BUSY]:
                        self.metrics[agent_id].uptime = current_time - agent_info.last_heartbeat
                    
                    # Send heartbeat to agent if it has the method
                    if hasattr(self.agents[agent_id], 'heartbeat'):
                        try:
                            if asyncio.iscoroutinefunction(self.agents[agent_id].heartbeat):
                                await self.agents[agent_id].heartbeat()
                            else:
                                self.agents[agent_id].heartbeat()
                            agent_info.last_heartbeat = current_time
                        except Exception as e:
                            logger.warning(f"Agent {agent_id} heartbeat failed: {e}")
                            agent_info.status = AgentStatus.ERROR
                
                await asyncio.sleep(self.health_check_interval)
                
            except Exception as e:
                logger.error(f"Error in health monitor: {e}")
                await asyncio.sleep(5)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        total_agents = len(self.agents)
        active_agents = sum(1 for info in self.agent_info.values() 
                           if info.status in [AgentStatus.IDLE, AgentStatus.BUSY])
        
        queue_size = self.request_queue.qsize()
        processing_count = len(self.processing_requests)
        completed_count = len(self.completed_requests)
        
        return {
            'status': 'healthy' if active_agents > 0 else 'degraded',
            'total_agents': total_agents,
            'active_agents': active_agents,
            'queue_size': queue_size,
            'processing_requests': processing_count,
            'completed_requests': completed_count,
            'uptime': datetime.now().isoformat(),
            'agents': {
                agent_id: {
                    'status': info.status.value,
                    'current_load': info.current_load,
                    'health_score': info.health_score,
                    'capabilities': info.capabilities
                }
                for agent_id, info in self.agent_info.items()
            }
        }
    
    def get_agent_metrics(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed metrics for a specific agent."""
        if agent_id not in self.metrics:
            return None
        
        metrics = self.metrics[agent_id]
        agent_info = self.agent_info[agent_id]
        
        return {
            'agent_id': agent_id,
            'agent_type': agent_info.agent_type,
            'status': agent_info.status.value,
            'total_requests': metrics.total_requests,
            'successful_requests': metrics.successful_requests,
            'failed_requests': metrics.failed_requests,
            'success_rate': metrics.successful_requests / max(metrics.total_requests, 1),
            'average_response_time': metrics.average_response_time,
            'error_rate': metrics.error_rate,
            'uptime': str(metrics.uptime),
            'current_load': agent_info.current_load,
            'max_concurrent_requests': agent_info.max_concurrent_requests,
            'health_score': agent_info.health_score,
            'last_request_time': metrics.last_request_time.isoformat() if metrics.last_request_time else None
        }
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all agents."""
        return {
            agent_id: self.get_agent_metrics(agent_id)
            for agent_id in self.agents.keys()
        }

# Global agent manager instance
_agent_manager: Optional[AgentManager] = None

def get_agent_manager(config: Optional[Dict[str, Any]] = None) -> AgentManager:
    """Get or create the global agent manager instance."""
    global _agent_manager
    
    if _agent_manager is None:
        _agent_manager = AgentManager(config)
    
    return _agent_manager

async def initialize_agent_manager(config: Optional[Dict[str, Any]] = None):
    """Initialize the global agent manager."""
    global _agent_manager
    
    if _agent_manager is None:
        _agent_manager = AgentManager(config)
        await _agent_manager.start()
    
    return _agent_manager

async def shutdown_agent_manager():
    """Shutdown the global agent manager."""
    global _agent_manager
    
    if _agent_manager is not None:
        await _agent_manager.stop()
        _agent_manager = None
