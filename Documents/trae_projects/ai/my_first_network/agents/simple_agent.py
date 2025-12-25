# Simple Worker Agent - Default Workspace
# A basic Python-based agent that responds to messages

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, ReplyMessageContext
from openagents.models.agent_config import AgentConfig


class SimpleWorkerAgent(WorkerAgent):

    default_agent_id = "simple-worker"

    def __init__(self, agent_config=None):
        if agent_config is None:
            agent_config = AgentConfig(
                instruction="你是一个简单的智能体，能够友好地回应消息。",
                model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
                provider="openai",  # 使用openai提供商（OpenAI兼容API）
                api_base="http://localhost:11434/v1",  # Ollama默认API地址
                api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
            )
        super().__init__(agent_config=agent_config)

    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("general").post("Hello from Simple Worker Agent!")

    async def on_direct(self, context: EventContext):
        ws = self.workspace()
        await ws.agent(context.source_id).send(f"Hello {context.source_id}!")

    async def on_channel_post(self, context: ChannelMessageContext):
        ws = self.workspace()
        await ws.channel(context.channel).reply(context.incoming_event.id, f"Hello {context.source_id}!")


if __name__ == "__main__":
    agent = SimpleWorkerAgent()
    agent.start(network_host="localhost", network_port=8700)
    agent.wait_for_stop()
