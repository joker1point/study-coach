from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, ReplyMessageContext
from openagents.models.agent_config import AgentConfig
import json
from datetime import datetime

class ReviewAgent(WorkerAgent):
    default_agent_id = "review-agent"

    def __init__(self, agent_config=None):
        if agent_config is None:
            agent_config = AgentConfig(
                instruction="你是一名专业的学习复盘员，能够每日汇总学习数据并生成详细的进度报告。",
                model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
                provider="openai",  # 使用openai提供商（Ollama提供OpenAI兼容API）
                api_base="http://localhost:11434/v1",  # Ollama默认API地址
                api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
            )
        super().__init__(agent_config=agent_config)
        self.learning_data = {}
        self.knowledge_mastery = {}
        self.qa_history = []
    
    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("tech-talk").post("复盘总结Agent已启动！我会每日汇总你的学习数据并生成进度报告。")
    
    async def handle_learning_data_update(self, message):
        """处理学习数据更新"""
        if isinstance(message, dict):
            student_id = message.get("student_id", "default")
            subject = message.get("subject", "general")
            
            # 初始化学生数据结构
            if student_id not in self.learning_data:
                self.learning_data[student_id] = {}
            if subject not in self.learning_data[student_id]:
                self.learning_data[student_id][subject] = {
                    "exercises_completed": 0,
                    "questions_answered": 0,
                    "correct_rate": 0.0,
                    "time_spent": 0,  # 分钟
                    "weak_points": set(),
                    "mastered_points": set()
                }
            
            # 更新学习数据
            student_subject_data = self.learning_data[student_id][subject]
            student_subject_data["exercises_completed"] += message.get("exercises_completed", 0)
            student_subject_data["questions_answered"] += message.get("questions_answered", 0)
            
            # 更新正确率
            if message.get("questions_answered", 0) > 0:
                new_correct = message.get("correct_answers", 0)
                total_answered = student_subject_data["questions_answered"]
                total_correct = int(student_subject_data["correct_rate"] * (total_answered - message.get("questions_answered", 0))) + new_correct
                student_subject_data["correct_rate"] = total_correct / total_answered
            
            student_subject_data["time_spent"] += message.get("time_spent", 0)
            
            # 更新知识点掌握情况
            if "weak_points" in message:
                student_subject_data["weak_points"].update(message["weak_points"])
            if "mastered_points" in message:
                student_subject_data["mastered_points"].update(message["mastered_points"])
                # 如果一个知识点已经被掌握，从薄弱点中移除
                student_subject_data["weak_points"] = student_subject_data["weak_points"] - message["mastered_points"]
    
    async def generate_daily_report(self):
        """生成每日学习进度报告"""
        today = datetime.now().strftime("%Y-%m-%d")
        report = f"📅 **{today} 学习进度报告**\n\n"
        ws = self.workspace()
        
        if not self.learning_data:
            report += "今日暂无学习数据\n"
            await ws.channel("general").post(report)
            return
        
        for student_id, subjects in self.learning_data.items():
            report += f"👤 **学生：{student_id}**\n\n"
            
            for subject, data in subjects.items():
                report += f"📚 **{subject}**\n"
                report += f"   ✅ 完成练习：{data['exercises_completed']} 个\n"
                report += f"   💬 回答问题：{data['questions_answered']} 道\n"
                report += f"   🎯 正确率：{data['correct_rate']:.2%}\n"
                report += f"   ⏰ 学习时长：{data['time_spent']} 分钟\n\n"
                
                # 知识点掌握情况
                if data['mastered_points']:
                    report += f"   🌟 今日掌握知识点：\n"
                    for point in data['mastered_points']:
                        report += f"      - {point}\n"
                    report += "\n"
                
                if data['weak_points']:
                    report += f"   ⚠️  需要巩固知识点：\n"
                    for point in data['weak_points']:
                        report += f"      - {point}\n"
                    report += "\n"
                    
                    # 自动触发任务规划Agent调整任务
                    await ws.agent("planning-agent").send({
                        "action": "adjust_plan_based_on_weakness",
                        "student_id": student_id,
                        "subject": subject,
                        "weak_points": list(data['weak_points'])
                    })
            
            report += "---\n\n"
        
        # 发送报告到general频道
        await ws.channel("general").post(report)
        
        # 重置每日数据（保留知识点掌握情况）
        for student_id, subjects in self.learning_data.items():
            for subject, data in subjects.items():
                # 保留知识点掌握情况
                weak_points = data['weak_points']
                mastered_points = data['mastered_points']
                
                # 重置其他每日数据
                self.learning_data[student_id][subject] = {
                    "exercises_completed": 0,
                    "questions_answered": 0,
                    "correct_rate": 0.0,
                    "time_spent": 0,
                    "weak_points": weak_points,
                    "mastered_points": mastered_points
                }
    
    async def on_direct(self, context: EventContext):
        """处理直接消息"""
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
        
        # 处理学习数据更新
        if action == "update_learning_data":
            await self.handle_learning_data_update(message)
        elif action == "record_qa":
            # 记录问答历史
            self.qa_history.append({
                "student_id": message.get("student_id", student_id),
                "question": message.get("question", ""),
                "answer": message.get("answer", ""),
                "timestamp": datetime.now().isoformat()
            })
            
            # 更新学习数据
            await self.handle_learning_data_update({
                "student_id": message.get("student_id", student_id),
                "subject": "general",
                "questions_answered": 1,
                "time_spent": 5  # 假设平均回答问题花费5分钟
            })
        
        # 处理学生的直接请求
        elif "生成今日报告" in text_content or "今日学习报告" in text_content:
            await self.generate_daily_report()
        elif text_content.startswith("查询") and ("学习情况" in text_content or "学习数据" in text_content):
            await self.query_learning_status(context)
        else:
            await self.handle_general_query(context)
    
    async def on_channel_post(self, context: ChannelMessageContext):
        """处理频道消息"""
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 解析消息内容
        text_content = message.get("text", "") if isinstance(message, dict) else message
        
        if "生成今日报告" in text_content or "今日学习报告" in text_content:
            await self.generate_daily_report()
    
    async def query_learning_status(self, context):
        """查询学习状态"""
        ws = self.workspace()
        student_id = context.source_id
        
        if not self.learning_data:
            await ws.agent(context.source_id).send("目前暂无学习数据")
            return
        
        reply = "📊 **当前学习状态**\n\n"
        for student_id, subjects in self.learning_data.items():
            reply += f"👤 学生：{student_id}\n"
            for subject, data in subjects.items():
                reply += f"   📚 {subject}：完成{data['exercises_completed']}个练习，回答{data['questions_answered']}道问题\n"
        
        await ws.agent(student_id).send(reply)
    
    async def handle_general_query(self, context):
        """处理一般查询"""
        ws = self.workspace()
        student_id = context.source_id
        
        await ws.agent(student_id).send(
            "你好！我是复盘总结Agent，我可以：\n" +
            "1. 生成每日学习报告（发送'生成今日报告'）\n" +
            "2. 查询当前学习状态（发送'查询学习情况'）\n" +
            "3. 持续追踪你的学习进度"
        )

if __name__ == "__main__":
    agent = ReviewAgent()
    agent.start(network_host="localhost", network_port=8700)
    agent.wait_for_stop()