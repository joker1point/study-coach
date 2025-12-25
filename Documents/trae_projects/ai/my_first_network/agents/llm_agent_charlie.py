# LLM Worker Agent - Market Analyst
# A Python-based agent that specializes in market analysis

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext
from openagents.models.agent_config import AgentConfig

class LLMWorkerAgent(WorkerAgent):

    default_agent_id = "charlie"
    
    async def on_startup(self):
        ws = self.workspace()
        
        # 发送欢迎消息
        await ws.channel("economic-discussions").post("Hello! I'm Charlie, a market analysis expert. I specialize in financial markets and investment strategies.")
    
    async def on_direct(self, context: EventContext):
        await self.run_agent(
            context=context,
            instruction=self.agent_config.instruction
        )
    
    async def on_channel_post(self, context: ChannelMessageContext):
        # 避免自己回复自己的消息
        if context.source_id == self.agent_id:
            return
        
        await self.run_agent(
            context=context,
            instruction=self.agent_config.instruction
        )

if __name__ == "__main__":
    agent_config = AgentConfig(
        instruction="你是Charlie，一位专业的市场分析师。你的专长是金融市场分析、投资策略和经济趋势预测。请用专业、清晰的语言回答问题，提供有深度的市场洞察。",
        model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
        provider="openai",  # 使用openai提供商（Ollama提供OpenAI兼容API）
        api_base="http://localhost:11434/v1",  # Ollama默认API地址
        api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
    )
    
    agent = LLMWorkerAgent(agent_config=agent_config)
    agent.start(network_host="localhost", network_port=8700)