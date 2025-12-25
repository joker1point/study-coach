# 学情分析Agent (DiagnosisAgent)
# 扮演"诊断师"角色，抓取学生作业/测试数据，定位知识盲点

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, ReplyMessageContext
from openagents.models.agent_config import AgentConfig
import sys
import os

# 添加mods目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mods')))

# 导入学情诊断Mod
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mods/openagents.mods.education.learning_diagnosis')))
from __init__ import analyze_homework

import json
from datetime import datetime


class DiagnosisAgent(WorkerAgent):

    default_agent_id = "diagnosis-agent"
    
    def __init__(self, agent_config=None):
        if agent_config is None:
            agent_config = AgentConfig(
                instruction="你是一名专业的学习诊断专家，能够分析学生的学习情况并提供个性化建议。",
                model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
                provider="openai",  # 使用openai提供商（Ollama提供OpenAI兼容API）
                api_base="http://localhost:11434/v1",  # Ollama默认API地址
                api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
            )
        super().__init__(agent_config=agent_config)
        self.student_data = {}

    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("tech-talk").post("学情分析Agent已启动！我可以帮助分析学生的学习数据并识别知识盲点。")

    async def on_direct(self, context: EventContext):
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 解析消息内容
        if isinstance(message, dict):
            text_content = message.get("text", "")
            data_content = message.get("data", {})
        else:
            text_content = message
            data_content = {}
        
        # 处理不同类型的请求
        if "提交作业" in text_content or "submit homework" in text_content.lower():
            # 模拟接收作业数据
            student_id = context.source_id
            self.student_data[student_id] = data_content
            
            # 分析作业数据，识别知识盲点并生成知识图谱
            analysis_result = self.analyze_homework_data(data_content)
            
            # 向任务规划Agent发送分析结果
            await ws.agent("planning-agent").send({
                "action": "knowledge_gaps_identified",
                "student_id": student_id,
                "knowledge_gaps": analysis_result["knowledge_gaps"],
                "knowledge_map": analysis_result["knowledge_map"]
            })
            
            # 回复学生
            knowledge_gaps = [gap["knowledge_point"] for gap in analysis_result["knowledge_gaps"]]
            await ws.agent(context.source_id).send(
                f"已收到你的作业数据并完成分析！已识别出以下知识盲点：\n{', '.join(knowledge_gaps)}\n\n"
                "已将分析结果发送给任务规划Agent，他将为你制定个性化学习任务。"
            )
        elif "查看学情" in text_content or "check status" in text_content.lower():
            student_id = context.source_id
            if student_id in self.student_data:
                await ws.agent(context.source_id).send(
                    f"你的学习数据已记录，上次分析时间：{self.student_data[student_id].get('timestamp', '未知')}\n"
                    f"最近识别的知识盲点：{self.student_data[student_id].get('knowledge_gaps', '暂无')}"
                )
            else:
                await ws.agent(context.source_id).send("尚未收到你的学习数据，请先提交作业或测试结果。")
        elif "数学" in text_content and any(char.isdigit() for char in text_content):
            # 处理类似"数学46"这样的成绩输入
            student_id = context.source_id
            
            # 提取成绩信息
            import re
            score = re.findall(r'\d+', text_content)[0]
            
            # 生成模拟的作业数据
            mock_homework_data = {
                "student_id": student_id,
                "subject": "数学",
                "timestamp": datetime.now().isoformat(),
                "questions": [
                    {
                        "id": "q001",
                        "content": "解方程：2x + 3 = 7",
                        "knowledge_points": ["math_algebra_eq_linear"],
                        "user_answer": "x = 2",
                        "correct_answer": "x = 2",
                        "is_correct": True,
                        "error_type": None
                    },
                    {
                        "id": "q002",
                        "content": "解方程：x² + 2x - 3 = 0",
                        "knowledge_points": ["math_algebra_eq_quadratic"],
                        "user_answer": "x = 1",
                        "correct_answer": "x = 1 或 x = -3",
                        "is_correct": False,
                        "error_type": "incomplete_solution"
                    },
                    {
                        "id": "q003",
                        "content": "计算三角形面积，底为5，高为8",
                        "knowledge_points": ["math_geometry_triangle_area"],
                        "user_answer": "20",
                        "correct_answer": "20",
                        "is_correct": True,
                        "error_type": None
                    },
                    {
                        "id": "q004",
                        "content": "计算圆的面积，半径为3",
                        "knowledge_points": ["math_geometry_circle"],
                        "user_answer": "9π",
                        "correct_answer": "9π",
                        "is_correct": True,
                        "error_type": None
                    }
                ]
            }
            
            # 根据成绩调整错题数量
            if int(score) < 60:
                # 成绩较差，增加错题数量
                mock_homework_data["questions"].extend([
                    {
                        "id": "q005",
                        "content": "求函数f(x) = x²的导数",
                        "knowledge_points": ["math_calculus_derivative"],
                        "user_answer": "x",
                        "correct_answer": "2x",
                        "is_correct": False,
                        "error_type": "concept_error"
                    },
                    {
                        "id": "q006",
                        "content": "解方程组：x + y = 5，2x - y = 1",
                        "knowledge_points": ["math_algebra_eq"],
                        "user_answer": "x = 2",
                        "correct_answer": "x = 2, y = 3",
                        "is_correct": False,
                        "error_type": "incomplete_solution"
                    }
                ])
            elif int(score) < 80:
                # 成绩中等，增加少量错题
                mock_homework_data["questions"].append(
                    {
                        "id": "q005",
                        "content": "求函数f(x) = x²的导数",
                        "knowledge_points": ["math_calculus_derivative"],
                        "user_answer": "x",
                        "correct_answer": "2x",
                        "is_correct": False,
                        "error_type": "concept_error"
                    }
                )
            
            # 保存数据
            self.student_data[student_id] = mock_homework_data
            
            # 分析作业数据
            analysis_result = self.analyze_homework_data(mock_homework_data)
            
            # 向任务规划Agent发送分析结果
            await ws.agent("planning-agent").send({
                "action": "knowledge_gaps_identified",
                "student_id": student_id,
                "knowledge_gaps": analysis_result["knowledge_gaps"],
                "knowledge_map": analysis_result["knowledge_map"]
            })
            
            # 回复学生
            knowledge_gaps = [gap["knowledge_point"] for gap in analysis_result["knowledge_gaps"]]
            await ws.agent(context.source_id).send(
                f"已根据你的数学成绩({score}分)完成分析！\n"
                f"当前掌握度：{round((1 - len(knowledge_gaps)/len(self.analyze_homework_data(mock_homework_data)['knowledge_map']['knowledge_tree']))*100, 2)}%\n"
                f"已识别出以下知识盲点：\n{', '.join(knowledge_gaps)}\n\n"
                "已将分析结果发送给任务规划Agent，他将为你制定个性化学习任务。"
            )
        else:
            # 处理普通问候和对话
            if any(greeting in text_content for greeting in ["你好", "hello", "hi", "嗨", "刚才", "说话", "在吗"]):
                await ws.agent(context.source_id).send(
                    "你好！我是学情分析Agent，很高兴为你服务。\n"
                    "我可以帮助分析你的学习数据，识别知识盲点。\n"
                    "请告诉我你的学科成绩(如：数学46)，我将为你进行详细分析！"
                )
            else:
                await ws.agent(context.source_id).send(
                    "你好！我是学情分析Agent，我可以：\n"
                    "1. 分析你的作业和测试数据\n"
                    "2. 识别你的知识盲点\n"
                    "3. 生成个性化学习建议\n"
                    "请提交你的作业数据、测试结果或成绩(如：数学46)开始分析。"
                )

    async def on_channel_post(self, context: ChannelMessageContext):
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 解析消息内容
        text_content = message.get("text", "") if isinstance(message, dict) else message
        
        if "学情分析" in text_content or "diagnosis" in text_content.lower():
            await ws.channel(context.channel).reply(
                context.incoming_event.id, 
                f"你好 {context.source_id}！我是学情分析Agent，我可以帮助分析学习数据并识别知识盲点。"
            )

    def analyze_homework_data(self, homework_data):
        """分析作业数据 - 使用学情诊断Mod"""
        # 使用学情诊断Mod进行分析
        return analyze_homework(homework_data)

    # 移除内部的generate_knowledge_map方法，因为现在使用学情诊断Mod


if __name__ == "__main__":
    agent = DiagnosisAgent()
    agent.start(network_host="localhost", network_port=8700, network_id="production-learning-assistant-network")
    agent.wait_for_stop()