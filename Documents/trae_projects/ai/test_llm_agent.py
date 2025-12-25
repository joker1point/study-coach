# Test script for LLM agent
# This script sends a message to the LLM agent and prints the response

import asyncio
from openagents.agents.worker_agent import WorkerAgent
from openagents.models.agent_config import AgentConfig

async def test_llm_agent():
    # Create a temporary agent to send messages to alex
    agent_config = AgentConfig(
        instruction="Test agent to send messages to alex",
        model_name="qwen:0.5b-chat",
        provider="openai",
        api_base="http://localhost:11434/v1",
        api_key="dummy"
    )
    
    agent = WorkerAgent(agent_id="test-agent", agent_config=agent_config)
    
    try:
        # Connect to the network
        await agent._async_start(network_host="localhost", network_port=8700)
        print("Connected to network")
        
        # Get the workspace
        ws = agent.workspace()
        
        # Send a message to alex
        message = "什么是OpenAgents？"
        print(f"Sending message to alex: {message}")
        
        # Create an event context to simulate a direct message
        from openagents.agents.worker_agent import EventContext
        from openagents.models.event import Event
        
        # This is a simplified approach - we'll just observe the channel instead
        # because the direct message API requires proper event handling
        
        # Post a message to the general channel that alex will respond to
        await ws.channel("general").post(message)
        print("Message posted to general channel")
        
        # Wait a few seconds to see the response
        await asyncio.sleep(10)
        
    finally:
        # Stop the agent
        await agent.stop()
        print("Test agent stopped")

if __name__ == "__main__":
    asyncio.run(test_llm_agent())