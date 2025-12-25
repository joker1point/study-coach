# 学情分析Agent - 分析学生学习数据，生成个性化学情报告

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, on_event
from openagents.models.agent_config import AgentConfig

# 导入知识图谱Mod
import sys
import os
# 添加mods目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mods/openagents.mods.education.knowledge_graph')))
from __init__ import analyze_learning_data


class LearningAnalysisAgent(WorkerAgent):
    default_agent_id = "learning-analysis-agent"
    ignore_own_messages = True

    def __init__(self, agent_config=None):
        super().__init__(agent_config=agent_config)
        # 配置模型提供器为OpenAI兼容API（用于Ollama）
        if self.agent_config and not self.agent_config.api_key:
            self.agent_config.api_key = "dummy"  # Ollama不需要真实API密钥
    
    @on_event("learning.exercise.updated")
    async def _handle_exercise_updated_event(self, context: EventContext):
        """处理练习数据更新事件"""
        try:
            print(f"🔍 收到learning.exercise.updated事件: {context.incoming_event}")
            
            # 获取事件内容
            event_content = context.incoming_event.content
            if isinstance(event_content, dict):
                # 分析学习数据
                learning_report = analyze_learning_data(event_content)
                print(f"📊 生成的学情报告: {learning_report}")
                
                # 发布学情就绪事件
                await self._publish_learning_ready_event(learning_report)
            else:
                print(f"❌ 事件内容格式错误: {event_content}")
        except Exception as e:
            print(f"❌ 处理learning.exercise.updated事件时出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def _publish_learning_ready_event(self, learning_report: dict):
        """发布学情就绪事件"""
        try:
            ws = self.workspace()
            await ws.event_system.publish(
                event_type="learning.analysis.completed",
                content=learning_report
            )
            print(f"📤 发布了learning.analysis.completed事件")
        except Exception as e:
            print(f"❌ 发布learning.analysis.completed事件时出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def on_startup(self):
        """Agent启动时执行"""
        ws = self.workspace()
        await ws.channel("general").post("学情分析Agent已上线，随时准备分析学习数据！")

    async def on_direct(self, context: EventContext):
        """处理直接发送给Agent的消息"""
        try:
            # 获取消息内容
            message = context.incoming_event.content
            if isinstance(message, dict):
                message_text = message.get("text", str(message))
                # 检查是否包含学习数据
                if "learning_data" in message:
                    learning_data = message["learning_data"]
                    # 分析学习数据
                    learning_report = analyze_learning_data(learning_data)
                    # 发送响应
                    ws = self.workspace()
                    await ws.agent(context.source_id).send({
                        "message": "学情分析完成",
                        "learning_report": learning_report
                    })
                else:
                    # 普通消息，使用LLM生成响应
                    response = await self.run_agent(context, instruction=message_text, stream=False)
                    ws = self.workspace()
                    await ws.agent(context.source_id).send(response.actions[-1].payload.get("response", ""))
            else:
                message_text = str(message)
                # 普通消息，使用LLM生成响应
                response = await self.run_agent(context, instruction=message_text, stream=False)
                ws = self.workspace()
                await ws.agent(context.source_id).send(response.actions[-1].payload.get("response", ""))
        except Exception as e:
            error_msg = f"处理您的消息时出错: {str(e)}"
            print(error_msg)
            try:
                sender_id = context.source_id if hasattr(context, 'source_id') else getattr(context.incoming_event, 'sender_id', 'unknown')
                ws = self.workspace()
                await ws.agent(sender_id).send(error_msg)
            except:
                pass

    async def on_channel_post(self, context: ChannelMessageContext):
        """处理频道消息"""
        try:
            print(f"🔍 收到频道消息事件: {context.incoming_event}")
            print(f"🔍 消息内容: {context.incoming_event.content}")
            print(f"🔍 频道: {context.channel}")
            print(f"🔍 事件ID: {context.incoming_event.id}")
            
            # 提取消息内容
            message_text = ""
            content = context.incoming_event.content
            
            if isinstance(content, dict):
                # 检查多种可能的用户输入字段路径
                possible_paths = [
                    ['text'],  # 直接text字段
                    ['content', 'text'],  # content.text
                    ['action', 'content', 'text'],  # action.content.text
                    ['message', 'content', 'text'],  # message.content.text
                    ['data', 'content', 'text'],  # data.content.text
                    ['payload', 'content', 'text']  # payload.content.text
                ]
                
                # 尝试所有可能的路径
                for path in possible_paths:
                    current = content
                    found = True
                    for key in path:
                        if isinstance(current, dict) and key in current:
                            current = current[key]
                        else:
                            found = False
                            break
                    if found and isinstance(current, str) and current.strip():
                        message_text = current
                        break
            else:
                message_text = str(content)
            
            # 检查是否包含学习数据请求
            if message_text.strip():
                print(f"📝 解析后的用户输入: {message_text}")
                
                # 使用LLM生成响应
                print(f"🤖 调用LLM生成响应...")
                response = await self.run_agent(context, instruction=message_text, stream=False)
                print(f"🤖 LLM原始响应: {response}")
                
                # 提取响应文本
                response_text = ""
                if hasattr(response, 'actions') and response.actions:
                    last_action = response.actions[-1]
                    if hasattr(last_action, 'payload') and isinstance(last_action.payload, dict):
                        if 'response' in last_action.payload:
                            response_text = last_action.payload['response']
                        else:
                            response_text = str(last_action.payload)
                
                if not response_text or response_text.strip() == "":
                    response_text = "抱歉，我暂时无法生成有效的响应，请稍后再试。"
                
                # 发送响应
                ws = self.workspace()
                await ws.channel(context.channel).reply(context.incoming_event.id, response_text)
        except Exception as e:
            error_msg = f"处理频道消息时出错: {str(e)}"
            print(f"❌ 处理消息时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            try:
                ws = self.workspace()
                await ws.channel(context.channel).post(error_msg)
            except Exception as e2:
                print(f"❌ 发送错误消息时出错: {str(e2)}")

    async def run_agent(self, context: EventContext, instruction: str, stream=False):
        """运行Agent，生成响应"""
        try:
            # 格式化指令
            formatted_instruction = f"""
            你是一个专业的学情分析助手，能够根据学习数据生成详细的学情报告。
            
            注意事项：
            1. 只回答用户的具体问题，不要添加额外的解释或背景信息
            2. 回答要简洁明了，不要包含与问题无关的技术细节
            3. 如果用户的问题不明确，请礼貌地询问更多信息
            4. 如果无法回答问题，请直接说明
            
            用户的问题：{instruction}
            你的回答：
            """
            
            # 调用模型生成响应
            response = await self.run_llm(
                context=context,
                instruction=formatted_instruction,
                stream=stream
            )
            
            return response
        except Exception as e:
            # 处理异常情况
            error_msg = f"抱歉，我在处理您的请求时遇到了错误。"
            print(f"❌ LLM调用出错: {str(e)}")
            import traceback
            traceback.print_exc()
            # 返回友好的错误响应
            return type('obj', (object,), {'actions': [type('obj', (object,), {'payload': {'response': error_msg}})]})()


if __name__ == "__main__":
    # 加载LLM配置
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from llm_config import DEFAULT_LLM_CONFIG
    
    # 配置智能体
    agent_config = AgentConfig(
        instruction="你是一个专业的学情分析助手，能够根据学习数据生成详细的学情报告，包括知识盲点、掌握程度和学习建议。",
        model_name=DEFAULT_LLM_CONFIG["model_name"],
        provider=DEFAULT_LLM_CONFIG["provider"],
        api_base=DEFAULT_LLM_CONFIG["api_base"],
        api_key=DEFAULT_LLM_CONFIG["api_key"]
    )
    agent = LearningAnalysisAgent(agent_config=agent_config)
    agent.start(network_host="localhost", network_port=8700)
    agent.wait_for_stop()