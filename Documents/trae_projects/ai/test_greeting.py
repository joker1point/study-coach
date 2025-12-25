import asyncio
from openagents.agents.worker_agent import WorkerAgent

async def test_greeting():
    # 创建一个临时的WorkerAgent用于测试
    agent = WorkerAgent()
    
    print("发送问候语到诊断代理...")
    
    # 使用正确的方式发送问候消息
    try:
        await agent.workspace().agent("diagnosis-agent").send("你好")
        print("✅ 问候消息发送成功！")
        
        # 等待一下，让代理有时间处理消息
        await asyncio.sleep(2)
        
        print("请在OpenAgents Studio中查看诊断代理的响应。")
        
    except Exception as e:
        print(f"❌ 发送消息失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_greeting())