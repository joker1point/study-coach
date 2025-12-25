# Learning Assistant Agent - Default Workspace
# A Python-based agent that uses LLM to generate responses

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext
from openagents.models.agent_config import AgentConfig


class LearningAssistantAgent(WorkerAgent):
    """A learning assistant agent powered by LLM."""

    default_agent_id = "learning-assistant-agent"

    def __init__(self, agent_config=None):
        super().__init__(agent_config=agent_config)
        # 配置模型提供器为OpenAI兼容API（用于Ollama）
        if self.agent_config and not self.agent_config.api_key:
            self.agent_config.api_key = "dummy"  # Ollama不需要真实API密钥
    
    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("general").post("学习助手已上线，随时为您提供帮助！")

    async def on_direct(self, context: EventContext):
        # 获取消息内容，需要处理消息可能是字典的情况
        message = context.incoming_event.content
        if isinstance(message, dict):
            message_text = message.get("text", str(message))
        else:
            message_text = str(message)
        # 获取发送者ID，可能需要使用不同的属性名
        sender_id = context.source_id if hasattr(context, 'source_id') else getattr(context.incoming_event, 'sender_id', 'unknown')
        
        # 使用LLM生成响应（启用流式输出）
        response = await self.run_agent(context, instruction=message_text, stream=True)
        
        # 发送响应
        ws = self.workspace()
        await ws.agent(sender_id).send(response.actions[-1].payload.get("response", ""))

    async def on_channel_post(self, context: ChannelMessageContext):
        # 获取消息内容，需要处理消息可能是字典的情况
        message = context.incoming_event.content
        if isinstance(message, dict):
            message_text = message.get("text", str(message))
        else:
            message_text = str(message)
        
        # 使用LLM生成响应（启用流式输出）
        response = await self.run_agent(context, instruction=message_text, stream=True)
        
        # 发送响应
        ws = self.workspace()
        await ws.channel(context.channel).reply(context.incoming_event.id, response.actions[-1].payload.get("response", ""))

    async def run_agent(self, context: EventContext, instruction: str, stream=False):
        try:
            # 格式化消息，添加学习助手的角色提示
            formatted_instruction = f"你是一个专业的学习助手，能够回答各种学习问题，提供详细的解释和帮助。\n\n用户问题：{instruction}"
            
            # 调用模型生成响应
            response = await self.agent.call_llm(
                instruction=formatted_instruction,
                model_name=self.agent_config.model_name,
                provider=self.agent_config.provider,
                api_base=self.agent_config.api_base,
                api_key=self.agent_config.api_key,
                stream=stream
            )
            
            return response
        except Exception as e:
            # 处理异常情况
            error_msg = f"处理请求时出错: {str(e)}"
            print(error_msg)
            # 返回错误响应
            return type('obj', (object,), {'actions': [type('obj', (object,), {'payload': {'response': error_msg}})]})()


if __name__ == "__main__":
    # 配置本地Ollama的qwen:0.5b-chat模型
    agent_config = AgentConfig(
        instruction="你是一个专业的学习助手，能够回答各种学习问题，提供详细的解释和帮助。",
        model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
        provider="openai",  # 使用openai提供商（Ollama提供OpenAI兼容API）
        api_base="http://localhost:11434/v1",  # Ollama默认API地址
        api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
    )
    agent = LearningAssistantAgent(agent_config=agent_config)
    agent.start(network_host="localhost", network_port=8700, network_transport="grpc")
    agent.wait_for_stop()
