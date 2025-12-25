import asyncio
from openagents.agents.worker_agent import WorkerAgent
from openagents.models.agent_config import AgentConfig

async def test_agent_connection():
    # 创建一个临时代理来测试与alex的通信
    test_agent_config = AgentConfig(
        instruction="Test agent to communicate with alex",
        model_name="qwen:0.5b-chat",
        provider="openai",
        api_base="http://localhost:11434/v1",
        api_key="dummy"
    )
    
    test_agent = WorkerAgent(agent_id="test-agent", agent_config=test_agent_config)
    
    try:
        # 连接到网络
        await test_agent._async_start(host="localhost", port=8700)
        print("✅ 测试代理已成功连接到网络")
        
        # 发送消息到alex
        ws = test_agent.workspace()
        message = "你好，alex！你能回答一个问题吗？"
        print(f"发送消息到alex: {message}")
        
        # 使用general频道发送消息，让alex能够看到
        await ws.channel("general").post(message)
        print("✅ 消息已发送到general频道")
        
        # 等待几秒钟，让alex有时间处理消息
        print("等待alex的响应...")
        await asyncio.sleep(10)
        
        print("测试完成！请检查网络日志以查看alex的响应")
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
    finally:
        # 停止测试代理
        await test_agent.stop()
        print("测试代理已停止")

if __name__ == "__main__":
    asyncio.run(test_agent_connection())