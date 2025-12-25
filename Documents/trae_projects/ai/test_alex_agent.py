import asyncio
from openagents.agents.worker_agent import WorkerAgent

async def test_alex_agent():
    """
    Test script to verify if Alex agent responds correctly to messages
    """
    try:
        # Create a temporary agent to send messages to Alex
        agent = WorkerAgent(
            agent_config=None,  # No specific config needed for sending
            agent_id="test_agent"
        )
        
        # Get workspace
        ws = agent.workspace()
        
        # Send a test message to Alex
        print("Sending test message to Alex...")
        await ws.agent("alex").send("Hello Alex! This is a test message.")
        print("Test message sent successfully!")
        
        # Wait a bit to allow Alex to process and respond
        await asyncio.sleep(2)
        print("Test completed. Please check Alex's response in the logs.")
        
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        # Stop the test agent
        agent.stop()

if __name__ == "__main__":
    asyncio.run(test_alex_agent())
