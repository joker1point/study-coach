#!/usr/bin/env python3
"""
测试代理通信脚本
用于验证网络中的代理是否正常工作并能够互相通信
"""

import asyncio
from openagents.agents.worker_agent import WorkerAgent
from openagents.models.agent_config import AgentConfig

async def test_agents_communication():
    """测试代理之间的通信"""
    print("=== 代理通信测试开始 ===")
    
    # 创建一个测试代理
    test_agent = WorkerAgent(
        AgentConfig(
            instruction="测试代理",
            model_name="qwen:0.5b-chat",
            provider="openai",
            api_base="http://localhost:11434/v1",
            api_key="dummy"
        )
    )
    
    ws = test_agent.workspace()
    
    # 测试的代理列表
    agents_to_test = [
        "simple-worker",
        "alex",
        "diagnosis-agent",
        "planning-agent", 
        "tutoring-agent"
    ]
    
    # 向所有代理发送测试消息
    for agent_id in agents_to_test:
        try:
            print(f"\n向 {agent_id} 发送测试消息...")
            await ws.agent(agent_id).send("你好！这是一条测试消息。")
            print(f"✓ 消息发送成功到 {agent_id}")
        except Exception as e:
            print(f"✗ 发送消息到 {agent_id} 失败: {e}")
    
    # 测试向频道发送消息
    try:
        print(f"\n向 general 频道发送测试消息...")
        await ws.channel("general").post("这是一条来自测试脚本的频道消息。")
        print(f"✓ 频道消息发送成功")
    except Exception as e:
        print(f"✗ 发送频道消息失败: {e}")
    
    print("\n=== 代理通信测试完成 ===")
    print("请在网络控制台或代理日志中查看响应情况。")
    
    # 等待一下，让代理有时间处理消息
    await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(test_agents_communication())
