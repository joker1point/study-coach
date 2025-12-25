import asyncio
from openagents.agents.worker_agent import WorkerAgent
from openagents.models.agent_config import AgentConfig

async def test_diagnosis_agent():
    # 创建一个临时代理用于测试
    agent = WorkerAgent(AgentConfig(instruction='test', model_name='gpt-3.5-turbo'))
    ws = agent.workspace()
    
    # 发送测试消息给诊断代理
    await ws.agent('diagnosis-agent').send('你好')
    print('测试消息已发送："你好"')
    
    # 再发送一个成绩测试消息
    await ws.agent('diagnosis-agent').send('数学46')
    print('测试消息已发送："数学46"')
    
    print('测试完成！请在Studio中查看诊断代理的响应。')

if __name__ == '__main__':
    asyncio.run(test_diagnosis_agent())