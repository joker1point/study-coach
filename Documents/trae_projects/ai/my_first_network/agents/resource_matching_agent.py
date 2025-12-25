# 资源匹配Agent - 基于学情报告匹配并推送学习资源

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, on_event
from openagents.models.agent_config import AgentConfig

# 导入学习资源库Mod
import sys
import os
# 添加mods目录到Python路径
mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../mods/openagents.mods.education.learning_resource'))
sys.path.append(mod_path)

# 添加tools目录到Python路径
tools_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tools'))
sys.path.append(tools_path)

from __init__ import match_resources as match_learning_resources
# 导入工具实现，使它们被注册
from tool_manager import tool_manager
import resource_tools
import exercise_tools



class ResourceMatchingAgent(WorkerAgent):
    default_agent_id = "resource-matching-agent"
    ignore_own_messages = True

    def __init__(self, agent_config=None):
        super().__init__(agent_config=agent_config)
        # 配置模型提供器为OpenAI兼容API（用于Ollama）
        if self.agent_config and not self.agent_config.api_key:
            self.agent_config.api_key = "dummy"  # Ollama不需要真实API密钥
    
    @on_event("learning.analysis.completed")
    async def _handle_learning_completed_event(self, context: EventContext):
        """处理学情分析完成事件"""
        try:
            print(f"🔍 收到learning.analysis.completed事件: {context.incoming_event}")
            
            # 获取事件内容（学情报告）
            learning_report = context.incoming_event.content
            if isinstance(learning_report, dict):
                # 使用工具管理器匹配学习资源
                student_id = learning_report.get("student_id", "unknown")
                subject = learning_report.get("subject", "")
                knowledge_points = learning_report.get("knowledge_points", [])
                learning_level = learning_report.get("learning_level", "")
                
                matched_resources_result = tool_manager.call_tool(
                    "match_learning_resources",
                    student_id=student_id,
                    subject=subject,
                    knowledge_points=knowledge_points,
                    learning_level=learning_level
                )
                
                matched_resources = matched_resources_result["resources"]
                print(f"🎯 匹配到的资源: {matched_resources}")
                
                # 推送资源给学生
                await self._push_resources_to_student(learning_report, matched_resources)
            else:
                print(f"❌ 学情报告格式错误: {learning_report}")
        except Exception as e:
            print(f"❌ 处理learning.analysis.completed事件时出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def _push_resources_to_student(self, learning_report: dict, matched_resources: list):
        """推送资源给学生"""
        try:
            student_id = learning_report.get("student_id", "unknown")
            subject = learning_report.get("subject", "")
            
            # 构建资源推送消息
            resource_message = {
                "student_id": student_id,
                "subject": subject,
                "matched_resources": matched_resources,
                "message": f"为您匹配到了{len(matched_resources)}个适合的学习资源，请注意查收！",
                "analysis_time": learning_report.get("analysis_time", "")
            }
            
            # 发送资源推送消息
            ws = self.workspace()
            await ws.channel("learning-resources").post(resource_message)
            print(f"📤 已推送资源到learning-resources频道")
            
            # 也可以直接发送给学生Agent（如果存在）
            await ws.agent(student_id).send(resource_message)
            print(f"📤 已直接发送资源给学生{student_id}")
        except Exception as e:
            print(f"❌ 推送资源时出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def on_startup(self):
        """Agent启动时执行"""
        ws = self.workspace()
        await ws.channel("general").post("资源匹配Agent已上线，随时准备为您匹配学习资源！")

    async def on_direct(self, context: EventContext):
        """处理直接发送给Agent的消息"""
        try:
            # 获取消息内容
            message = context.incoming_event.content
            if isinstance(message, dict):
                message_text = message.get("text", str(message))
                # 检查是否包含资源请求
                if "resource_request" in message:
                    request_data = message["resource_request"]
                    # 匹配资源
                    matched_resources = match_learning_resources(request_data)
                    # 发送响应
                    ws = self.workspace()
                    await ws.agent(context.source_id).send({
                        "message": "资源匹配完成",
                        "matched_resources": matched_resources
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
            # 检查指令是否包含工具调用请求
            # 简单的模式匹配，寻找类似"调用工具[工具名]"的模式
            import re
            tool_call_pattern = r"调用工具\[(\w+)\]\s*(?:参数\[(.*?)\])?"
            match = re.search(tool_call_pattern, instruction)
            
            if match:
                # 提取工具名和参数
                tool_name = match.group(1)
                params_str = match.group(2) or ""
                
                # 解析参数
                params = {}
                if params_str:
                    param_pattern = r"(\w+)=(.*?)(?:,|$)"
                    param_matches = re.finditer(param_pattern, params_str)
                    for param_match in param_matches:
                        key = param_match.group(1)
                        value = param_match.group(2).strip()
                        # 尝试转换为数字
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                pass  # 保持字符串
                        params[key] = value
                
                # 调用工具
                result = tool_manager.call_tool(tool_name, **params)
                
                # 生成工具调用结果响应
                response_text = f"✅ 工具调用成功！\n工具名称：{tool_name}\n参数：{params}\n结果：{result}"
                
                # 返回工具调用结果
                return type('obj', (object,), {
                    'actions': [
                        type('obj', (object,), {
                            'payload': {
                                'response': response_text,
                                'tool_call_result': result
                            }
                        })()
                    ]
                })()
            else:
                # 普通指令，调用LLM生成响应
                # 格式化指令
                formatted_instruction = f"""
                你是一个专业的资源匹配助手，能够根据学情报告为学生匹配最合适的学习资源。
                
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
            error_msg = f"抱歉，我在处理您的请求时遇到了错误：{str(e)}"
            print(f"❌ 处理请求时出错: {str(e)}")
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
        instruction="你是一个专业的资源匹配助手，能够根据学情报告为学生匹配最合适的学习资源，包括课件、微课和习题等。",
        model_name=DEFAULT_LLM_CONFIG["model_name"],
        provider=DEFAULT_LLM_CONFIG["provider"],
        api_base=DEFAULT_LLM_CONFIG["api_base"],
        api_key=DEFAULT_LLM_CONFIG["api_key"]
    )
    agent = ResourceMatchingAgent(agent_config=agent_config)
    agent.start(network_host="localhost", network_port=8700)
    agent.wait_for_stop()