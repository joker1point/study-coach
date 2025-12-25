# Learning Assistant Agent - Default Workspace
# A Python-based agent that uses LLM to generate responses

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, on_event
from openagents.models.agent_config import AgentConfig


class LearningAssistantAgent(WorkerAgent):
    default_agent_id = "learning-assistant-agent"
    ignore_own_messages = True

    def __init__(self, agent_config=None):
        super().__init__(agent_config=agent_config)
        # 配置模型提供器为OpenAI兼容API（用于Ollama）
        if self.agent_config and not self.agent_config.api_key:
            self.agent_config.api_key = "dummy"  # Ollama不需要真实API密钥
    
    @on_event("thread.channel_message.post")
    async def _handle_channel_post_event(self, context: EventContext):
        """Handle thread.channel_message.post events and route to on_channel_post."""
        try:
            print(f"🔍 收到thread.channel_message.post事件: {context.incoming_event}")
            
            # 创建ChannelMessageContext对象
            channel_context = ChannelMessageContext(
                incoming_event=context.incoming_event,
                event_threads=context.event_threads,
                incoming_thread_id=context.incoming_thread_id,
                channel=context.incoming_event.content.get("channel", "general") if isinstance(context.incoming_event.content, dict) else "general",
            )
            
            # 调用on_channel_post方法处理消息
            await self.on_channel_post(channel_context)
        except Exception as e:
            print(f"❌ 处理thread.channel_message.post事件时出错: {str(e)}")
            import traceback
            traceback.print_exc()

    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("general").post("学习助手已上线，随时为您提供帮助！")

    async def on_direct(self, context: EventContext):
        try:
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
        try:
            print(f"🔍 收到频道消息事件: {context.incoming_event}")
            print(f"🔍 消息内容: {context.incoming_event.content}")
            print(f"🔍 频道: {context.channel}")
            print(f"🔍 事件ID: {context.incoming_event.id}")
            
            # 更准确地提取用户输入消息内容
            message_text = ""
            content = context.incoming_event.content
            
            # 处理不同的消息格式
            if isinstance(content, dict):
                # 检查是否是我们自己发送的消息（避免无限循环）
                if 'source' in content and content['source'] == self.default_agent_id:
                    print(f"📭 忽略自己发送的消息")
                    return
                    
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
                
                # 如果仍然没有找到，尝试从原始事件中提取
                if not message_text:
                    # 检查incoming_event的其他可能字段
                    if hasattr(context.incoming_event, 'message'):
                        message_obj = context.incoming_event.message
                        if isinstance(message_obj, dict) and 'text' in message_obj:
                            message_text = message_obj['text']
                        elif hasattr(message_obj, 'text'):
                            message_text = message_obj.text
                
                # 如果仍然没有找到，尝试提取最可能的用户输入
                if not message_text:
                    print(f"⚠️  未找到标准text字段，尝试从内容中提取: {content}")
                    # 从整个内容中搜索可能的用户输入模式
                    import re
                    # 尝试匹配中文或英文句子
                    text_patterns = re.findall(r'[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9\s\.,?!]+[\u4e00-\u9fa5a-zA-Z0-9\s\.,?!]', str(content))
                    if text_patterns:
                        # 取最长的匹配作为用户输入
                        message_text = max(text_patterns, key=len)
                    else:
                        message_text = str(content)
            else:
                message_text = str(content)
            
            # 过滤掉可能的系统消息或格式错误的消息
            if not message_text or message_text.strip() == "":
                print(f"📭 忽略空消息或格式错误的消息")
                return
            
            # 过滤掉系统特定的消息内容
            system_messages = [
                "学习助手已上线，随时为您提供帮助！",
                "已上线",
                "channel_message",
                "message_type"
            ]
            
            is_system_message = False
            for sys_msg in system_messages:
                if sys_msg in message_text:
                    is_system_message = True
                    break
            
            if is_system_message:
                print(f"📭 忽略系统消息: {message_text}")
                return
            
            print(f"📝 解析后的用户输入: {message_text}")
            
            # 使用LLM生成响应（禁用流式输出以便更好地控制响应）
            print(f"🤖 调用LLM生成响应...")
            response = await self.run_agent(context, instruction=message_text, stream=False)
            print(f"🤖 LLM原始响应: {response}")
            
            # 更可靠地提取响应文本
            response_text = ""
            if hasattr(response, 'actions') and response.actions:
                last_action = response.actions[-1]
                if hasattr(last_action, 'payload') and isinstance(last_action.payload, dict):
                    if 'response' in last_action.payload:
                        response_text = last_action.payload['response']
                    else:
                        # 尝试从payload中提取其他可能的响应字段
                        print(f"⚠️  未找到标准response字段，尝试从payload中提取: {last_action.payload}")
                        response_text = str(last_action.payload)
            
            # 检查响应是否有效
            if not response_text or response_text.strip() == "":
                response_text = "抱歉，我暂时无法生成有效的响应，请稍后再试。"
            
            # 清理响应文本，移除可能的内部数据结构
            import re
            response_text = re.sub(r'\{[^}]*\}', '', response_text)  # 移除字典格式的内容
            response_text = re.sub(r'\[[^\]]*\]', '', response_text)  # 移除列表格式的内容
            response_text = response_text.strip()
            
            print(f"📤 发送清理后的响应到频道 {context.channel}: {response_text}")
            
            # 发送响应
            ws = self.workspace()
            await ws.channel(context.channel).reply(context.incoming_event.id, response_text)
            print(f"✅ 响应发送成功")
        except Exception as e:
            error_msg = f"处理您的消息时出错: {str(e)}"
            print(f"❌ 处理消息时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            try:
                ws = self.workspace()
                await ws.channel(context.channel).post(error_msg)
                print(f"❌ 错误消息发送成功")
            except Exception as e2:
                print(f"❌ 发送错误消息时出错: {str(e2)}")
                import traceback
                traceback.print_exc()

    async def run_agent(self, context: EventContext, instruction: str, stream=False):
        try:
            # 改进格式化指令，更明确地定义学习助手的角色和任务
            formatted_instruction = f"""
            你是一个专业、友好的学习助手。请严格根据用户的问题提供清晰、准确、有帮助的回答，不要添加任何与问题无关的内容。
            
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
    # 配置本地Ollama的qwen:0.5b-chat模型
    agent_config = AgentConfig(
        instruction="你是一个专业的学习助手，能够回答各种学习问题，提供详细的解释和帮助。",
        model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
        provider="openai",  # 使用openai提供商（Ollama提供OpenAI兼容API）
        api_base="http://localhost:11434/v1",  # Ollama默认API地址
        api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
    )
    agent = LearningAssistantAgent(agent_config=agent_config)
    agent.start(network_host="localhost", network_port=8700)
    agent.wait_for_stop()
