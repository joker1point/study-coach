# Custom Worker Agent V2 - 自定义智能体版本2
# 一个具有个性化功能的Python智能体，能够回应特定问题

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, ReplyMessageContext
from openagents.models.agent_config import AgentConfig


class CustomWorkerAgentV2(WorkerAgent):

    default_agent_id = "custom-agent-v2"
    
    def __init__(self, agent_config=None):
        if agent_config is None:
            agent_config = AgentConfig(
                instruction="你是一个自定义智能体，能够回答关于OpenAgents的基本问题，并且友好地与其他智能体互动。",
                model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
                provider="openai",  # 使用openai提供商（Ollama兼容OpenAI API）
                api_base="http://localhost:11434/v1",  # Ollama默认API地址
                api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
            )
        super().__init__(agent_config=agent_config)

    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("general").post("你好！我是自定义智能体V2，我可以回答关于OpenAgents的问题。")

    async def on_direct(self, context: EventContext):
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 简单的回应逻辑
        if isinstance(message, dict):
            message = message.get("text", str(message))
        
        if "你好" in message or "hello" in message.lower():
            response = f"你好 {context.source_id}！有什么我可以帮助你的吗？"
        elif "什么是OpenAgents" in message or "what is openagents" in message.lower():
            response = "OpenAgents是一个用于构建和运行AI智能体网络的平台，允许智能体之间进行协作和交互。"
        elif "如何创建智能体" in message or "how to create agent" in message.lower():
            response = "你可以通过继承WorkerAgent类来创建自定义智能体，然后实现on_startup、on_direct等方法。"
        elif "网络" in message or "network" in message.lower():
            response = "OpenAgents网络允许智能体之间进行通信和协作，你可以通过openagents network start命令启动网络。"
        else:
            response = f"感谢你的消息！我收到了：{message}"
            
        await ws.agent(context.source_id).send(response)

    async def on_channel_post(self, context: ChannelMessageContext):
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 只有当消息中提到特定关键词时才回应
        text_content = message.get("text", "") if isinstance(message, dict) else message
        if "自定义智能体" in text_content or "custom agent" in text_content.lower() or "你" in text_content:
            await ws.channel(context.channel).reply(context.incoming_event.id, f"你好 {context.source_id}！有什么我可以帮助你的吗？")


if __name__ == "__main__":
    agent = CustomWorkerAgentV2()
    agent.start(network_host="localhost", network_port=8700)
    agent.wait_for_stop()