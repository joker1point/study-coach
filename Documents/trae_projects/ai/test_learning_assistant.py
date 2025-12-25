# Test script for Learning Assistant Agent
# This script sends a message to the learning assistant agent and checks if it responds

import asyncio
from openagents.agents.worker_agent import WorkerAgent
from openagents.models.agent_config import AgentConfig

async def test_learning_assistant():
    # Create a temporary agent to test the learning assistant
    agent_config = AgentConfig(
        instruction="Test agent to test the learning assistant",
        model_name="qwen:0.5b-chat",
        provider="openai",
        api_base="http://localhost:11434/v1",
        api_key="dummy"
    )
    
    test_agent = WorkerAgent(agent_id="test-assistant-agent", agent_config=agent_config)
    
    try:
        # Connect to the network
        await test_agent._async_start(network_host="localhost", network_port=8700)
        print("Connected to network")
        
        # Get the workspace
        ws = test_agent.workspace()
        
        # Post a message to the general channel that the learning assistant will respond to
        message = "你好，学习助手！"
        print(f"Sending message to general channel: {message}")
        await ws.channel("general").post(message)
        print("Message posted to general channel")
        
        # Wait a few seconds to see the response
        print("Waiting for response...")
        await asyncio.sleep(15)
        
        print("Test completed. Check the OpenAgents Studio for the learning assistant's response.")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
    finally:
        # Stop the agent
        await test_agent.stop()
        print("Test agent stopped")

if __name__ == "__main__":
    asyncio.run(test_learning_assistant())