# 答疑辅导Agent (TutoringAgent)
# 扮演"讲师"角色，响应学生实时问题，结合任务规划Agent的内容提供针对性讲解

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, ReplyMessageContext
from openagents.models.agent_config import AgentConfig


class TutoringAgent(WorkerAgent):

    default_agent_id = "tutoring-agent"
    
    def __init__(self, agent_config=None):
        if agent_config is None:
            agent_config = AgentConfig(
                instruction="你是一名专业的学科辅导讲师，能够针对学生的问题提供详细的解答和讲解，结合学生的学习计划提供针对性指导。",
                model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
                provider="openai",  # 使用openai提供商（Ollama提供OpenAI兼容API）
                api_base="http://localhost:11434/v1",  # Ollama默认API地址
                api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
            )
        super().__init__(agent_config=agent_config)
        self.student_plans = {}
        self.student_questions = {}

    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("tech-talk").post("答疑辅导Agent已启动！我可以为学生提供实时答疑和针对性讲解。")

    async def on_direct(self, context: EventContext):
        ws = self.workspace()
        message = context.incoming_event.content
        student_id = context.source_id
        
        # 解析消息内容
        if isinstance(message, dict):
            action = message.get("action", "")
            text_content = message.get("text", "")
        else:
            text_content = message
            action = ""
        
        # 处理任务规划Agent发送的学生计划信息
        if action == "update_student_plan":
            target_student_id = message.get("student_id", student_id)
            plan = message.get("plan", {})
            self.student_plans[target_student_id] = plan
            
            # 回复确认收到计划
            await ws.agent(context.source_id).send({
                "action": "plan_received",
                "message": f"已收到学生 {target_student_id} 的学习计划"
            })
        
        # 处理学生的问题
        elif text_content.strip():
            # 记录学生的问题
            if student_id not in self.student_questions:
                self.student_questions[student_id] = []
            self.student_questions[student_id].append({
                "question": text_content,
                "timestamp": context.incoming_event.timestamp if hasattr(context.incoming_event, 'timestamp') else ""
            })
            
            # 获取学生的学习计划（如果有）
            student_plan = self.student_plans.get(student_id, {})
            
            # 解答学生的问题
            answer = self.answer_question(text_content, student_plan)
            
            # 回复学生
            await ws.agent(student_id).send(answer)
            
            # 向复盘总结Agent发送问答记录
            await ws.agent("review-agent").send({
                "action": "record_qa",
                "student_id": student_id,
                "question": text_content,
                "answer": answer
            })
        
        else:
            await ws.agent(student_id).send(
                "你好！我是答疑辅导Agent，我可以：\n"
                "1. 解答你的学科问题\n"
                "2. 提供知识点的详细讲解\n"
                "3. 根据你的学习计划提供针对性指导\n"
                "请直接提出你的问题，我会尽快为你解答。"
            )

    async def on_channel_post(self, context: ChannelMessageContext):
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 解析消息内容
        text_content = message.get("text", "") if isinstance(message, dict) else message
        
        if "答疑" in text_content or "辅导" in text_content or "问题" in text_content or "question" in text_content.lower():
            await ws.channel(context.channel).reply(
                context.incoming_event.id, 
                f"你好 {context.source_id}！我是答疑辅导Agent，有什么问题可以直接向我提问。"
            )

    def answer_question(self, question, student_plan):
        """根据问题和学生计划提供解答"""
        # 简单的问题分类和解答逻辑
        # 在实际应用中，这里应该连接到更复杂的知识库或使用更强大的模型
        
        # 检查问题是否与学生的学习计划相关
        related_topic = None
        if student_plan.get("daily_tasks"):
            for task in student_plan["daily_tasks"]:
                if task["topic"] in question:
                    related_topic = task["topic"]
                    break
        
        # 根据问题类型提供不同的解答
        if "什么是" in question or "定义" in question or "概念" in question or "what is" in question.lower():
            # 概念解释
            return self.explain_concept(question, related_topic)
        elif "如何" in question or "怎么做" in question or "how to" in question.lower():
            # 方法步骤讲解
            return self.explain_method(question, related_topic)
        elif "为什么" in question or "原因" in question or "why" in question.lower():
            # 原理讲解
            return self.explain_principle(question, related_topic)
        else:
            # 通用解答
            return self.general_answer(question, related_topic)

    def explain_concept(self, question, related_topic=None):
        """解释概念"""
        base_answer = f"为你解答问题：{question}\n\n"
        base_answer += "这是一个概念解释类问题，我将为你详细解释相关概念：\n\n"
        
        # 在实际应用中，这里应该从知识库中获取准确的概念解释
        # 这里只是一个示例
        base_answer += "📚 核心概念：\n"
        base_answer += "相关概念的详细解释内容...\n\n"
        
        # 如果与学习计划相关，添加针对性提示
        if related_topic:
            base_answer += f"💡 学习提示：\n"
            base_answer += f"这个概念是你今日学习计划中 '{related_topic}' 的核心内容，建议结合计划中的专项练习进行巩固。\n"
        
        base_answer += "\n有任何其他问题，欢迎继续提问！"
        return base_answer

    def explain_method(self, question, related_topic=None):
        """讲解方法步骤"""
        base_answer = f"为你解答问题：{question}\n\n"
        base_answer += "这是一个方法步骤类问题，我将为你详细讲解解题步骤：\n\n"
        
        # 在实际应用中，这里应该从知识库中获取准确的解题方法
        # 这里只是一个示例
        base_answer += "📋 解题步骤：\n"
        base_answer += "1. 第一步：明确问题要求\n"
        base_answer += "2. 第二步：分析已知条件\n"
        base_answer += "3. 第三步：选择合适的方法\n"
        base_answer += "4. 第四步：执行解题过程\n"
        base_answer += "5. 第五步：验证结果\n\n"
        
        # 如果与学习计划相关，添加针对性提示
        if related_topic:
            base_answer += f"💡 学习提示：\n"
            base_answer += f"这个方法是你今日学习计划中 '{related_topic}' 的重点内容，建议完成计划中的相关练习。\n"
        
        base_answer += "\n有任何其他问题，欢迎继续提问！"
        return base_answer

    def explain_principle(self, question, related_topic=None):
        """讲解原理"""
        base_answer = f"为你解答问题：{question}\n\n"
        base_answer += "这是一个原理类问题，我将为你详细讲解相关原理：\n\n"
        
        # 在实际应用中，这里应该从知识库中获取准确的原理讲解
        # 这里只是一个示例
        base_answer += "🔬 原理讲解：\n"
        base_answer += "相关原理的详细内容...\n\n"
        
        # 如果与学习计划相关，添加针对性提示
        if related_topic:
            base_answer += f"💡 学习提示：\n"
            base_answer += f"这个原理是你今日学习计划中 '{related_topic}' 的基础内容，建议先理解原理再进行练习。\n"
        
        base_answer += "\n有任何其他问题，欢迎继续提问！"
        return base_answer

    def general_answer(self, question, related_topic=None):
        """通用解答"""
        base_answer = f"为你解答问题：{question}\n\n"
        base_answer += "以下是相关解答：\n\n"
        
        # 在实际应用中，这里应该连接到更复杂的问答系统
        # 这里只是一个示例
        base_answer += "📝 详细解答：\n"
        base_answer += "相关问题的详细解答内容...\n\n"
        
        # 如果与学习计划相关，添加针对性提示
        if related_topic:
            base_answer += f"💡 学习提示：\n"
            base_answer += f"这个问题与你今日学习计划中 '{related_topic}' 相关，建议结合计划内容进行深入学习。\n"
        
        base_answer += "\n有任何其他问题，欢迎继续提问！"
        return base_answer


if __name__ == "__main__":
    agent = TutoringAgent()
    agent.start(network_host="localhost", network_port=8700, network_id="production-learning-assistant-network")
    agent.wait_for_stop()