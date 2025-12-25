# 任务规划Agent (PlanningAgent)
# 扮演"规划师"角色，接收学情Agent的分析结果，生成个性化学习任务

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, ReplyMessageContext
from openagents.models.agent_config import AgentConfig
import datetime


class PlanningAgent(WorkerAgent):

    default_agent_id = "planning-agent"
    
    def __init__(self, agent_config=None):
        if agent_config is None:
            agent_config = AgentConfig(
                instruction="你是一名专业的学习规划师，能够根据学生的知识盲点生成个性化的学习任务和计划。",
                model_name="qwen:0.5b-chat",  # 使用本地Ollama模型
                provider="openai",  # 使用openai提供商（Ollama提供OpenAI兼容API）
                api_base="http://localhost:11434/v1",  # Ollama默认API地址
                api_key="dummy"  # Ollama不需要API密钥，使用dummy即可
            )
        super().__init__(agent_config=agent_config)
        self.student_plans = {}

    async def on_startup(self):
        ws = self.workspace()
        await ws.channel("tech-talk").post("任务规划Agent已启动！我可以根据学情分析结果为学生制定个性化学习任务。")

    async def on_direct(self, context: EventContext):
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 解析消息内容
        if isinstance(message, dict):
            action = message.get("action", "")
            text_content = message.get("text", "")
        else:
            text_content = message
            action = ""
        
        # 处理复盘总结Agent发送的薄弱点信息，调整学习计划
        if action == "adjust_plan_based_on_weakness":
            student_id = message.get("student_id", context.source_id)
            weak_points = message.get("weak_points", [])
            subject = message.get("subject", "general")
            
            # 如果学生已有学习计划，基于薄弱点调整计划
            if student_id in self.student_plans:
                current_plan = self.student_plans[student_id]["plan"]
                # 基于薄弱点生成新的学习任务
                additional_tasks = []
                for gap in weak_points:
                    additional_tasks.append({
                        "id": f"task_reinforce_{len(current_plan['daily_tasks']) + len(additional_tasks) + 1}",
                        "topic": gap,
                        "type": "薄弱点强化",
                        "duration": "25分钟",
                        "description": f"针对{gap}知识点进行强化练习，完成8道相关题目",
                        "resources": [f"{gap}知识点深度讲解", f"{gap}易错题目集"]
                    })
                
                # 更新学习计划
                updated_plan = current_plan.copy()
                updated_plan["daily_tasks"].extend(additional_tasks)
                updated_plan["date"] = datetime.date.today().isoformat()
                
                # 标记新发现的薄弱点
                if "additional_weak_points" not in updated_plan:
                    updated_plan["additional_weak_points"] = []
                updated_plan["additional_weak_points"].extend(weak_points)
                
                # 更新学生计划
                self.student_plans[student_id]["plan"] = updated_plan
                self.student_plans[student_id]["last_updated"] = datetime.datetime.now().isoformat()
                
                # 向学生发送更新后的学习计划
                await ws.agent(student_id).send({
                    "action": "personalized_plan_updated",
                    "plan": updated_plan,
                    "message": "根据你的学习情况，我们调整了你的学习计划，增加了薄弱点的强化练习！\n" + 
                               self.format_plan_message(updated_plan)
                })
                
                # 向答疑辅导Agent发送更新后的计划
                await ws.agent("tutoring-agent").send({
                    "action": "update_student_plan",
                    "student_id": student_id,
                    "plan": updated_plan
                })
        # 处理学情分析Agent发送的知识盲点信息
        elif action == "knowledge_gaps_identified":
            student_id = message.get("student_id", context.source_id)
            knowledge_gaps = message.get("knowledge_gaps", [])
            knowledge_map = message.get("knowledge_map", {})
            
            # 生成个性化学习计划
            personalized_plan = self.generate_personalized_plan(knowledge_gaps, knowledge_map)
            self.student_plans[student_id] = {
                "plan": personalized_plan,
                "created_at": datetime.datetime.now().isoformat(),
                "knowledge_gaps": knowledge_gaps
            }
            
            # 向学生发送学习计划
            await ws.agent(student_id).send({
                "action": "personalized_plan_generated",
                "plan": personalized_plan,
                "message": self.format_plan_message(personalized_plan)
            })
            
            # 向答疑辅导Agent发送相关信息
            await ws.agent("tutoring-agent").send({
                "action": "update_student_plan",
                "student_id": student_id,
                "plan": personalized_plan
            })
        
        # 处理学生的直接请求
        elif "查看计划" in text_content or "view plan" in text_content.lower():
            student_id = context.source_id
            if student_id in self.student_plans:
                plan = self.student_plans[student_id]["plan"]
                await ws.agent(context.source_id).send(self.format_plan_message(plan))
            else:
                await ws.agent(context.source_id).send("尚未为你生成学习计划，请先提交作业或测试结果进行学情分析。")
        
        elif "调整计划" in text_content or "adjust plan" in text_content.lower():
            student_id = context.source_id
            if student_id in self.student_plans:
                # 简单的计划调整逻辑
                current_plan = self.student_plans[student_id]["plan"]
                adjusted_plan = self.adjust_plan(current_plan, text_content)
                self.student_plans[student_id]["plan"] = adjusted_plan
                self.student_plans[student_id]["last_adjusted"] = datetime.datetime.now().isoformat()
                
                await ws.agent(context.source_id).send(
                    "已根据你的需求调整学习计划！\n" + 
                    self.format_plan_message(adjusted_plan)
                )
            else:
                await ws.agent(context.source_id).send("你尚未有学习计划，请先进行学情分析。")
        
        else:
            await ws.agent(context.source_id).send(
                "你好！我是任务规划Agent，我可以：\n"
                "1. 根据你的知识盲点生成个性化学习任务\n"
                "2. 调整你的学习计划\n"
                "3. 跟踪你的学习进度\n"
                "请先完成学情分析，我将为你制定专属学习计划。"
            )

    async def on_channel_post(self, context: ChannelMessageContext):
        ws = self.workspace()
        message = context.incoming_event.content
        
        # 解析消息内容
        text_content = message.get("text", "") if isinstance(message, dict) else message
        
        if "学习计划" in text_content or "learning plan" in text_content.lower():
            await ws.channel(context.channel).reply(
                context.incoming_event.id, 
                f"你好 {context.source_id}！我是任务规划Agent，我可以根据学情分析结果为你制定个性化学习任务。"
            )

    def generate_personalized_plan(self, knowledge_gaps, knowledge_map):
        """根据知识盲点生成个性化学习计划"""
        plan = {
            "date": datetime.date.today().isoformat(),
            "knowledge_gaps": knowledge_gaps,
            "daily_tasks": [],
            "priority_levels": {
                "high": [],
                "medium": [],
                "low": []
            }
        }
        
        # 基于优先级分配任务
        if knowledge_map.get("priority_gaps"):
            # 为高优先级盲点生成专项练习
            for gap in knowledge_map["priority_gaps"]:
                plan["priority_levels"]["high"].append(gap)
                plan["daily_tasks"].append({
                    "id": f"task_high_{len(plan['daily_tasks']) + 1}",
                    "topic": gap,
                    "type": "专项练习",
                    "duration": "30分钟",
                    "description": f"针对{gap}进行集中练习，完成10道相关题目",
                    "resources": [f"{gap}知识点讲解视频", f"{gap}专项练习册"]
                })
        
        # 为其他盲点生成学习任务
        other_gaps = [g for g in knowledge_gaps if g not in knowledge_map.get("priority_gaps", [])]
        for i, gap in enumerate(other_gaps):
            if i < len(other_gaps) // 2:
                priority = "medium"
            else:
                priority = "low"
            
            plan["priority_levels"][priority].append(gap)
            plan["daily_tasks"].append({
                "id": f"task_{priority}_{len(plan['daily_tasks']) + 1}",
                "topic": gap,
                "type": "知识点回顾",
                "duration": "20分钟",
                "description": f"复习{gap}的核心概念，完成5道相关题目",
                "resources": [f"{gap}知识点总结", f"{gap}基础练习"]
            })
        
        # 添加综合练习任务
        plan["daily_tasks"].append({
            "id": f"task_comprehensive_{len(plan['daily_tasks']) + 1}",
            "topic": "综合练习",
            "type": "综合测试",
            "duration": "40分钟",
            "description": "完成一套综合测试题，检验今日学习成果",
            "resources": ["今日所学知识点汇总"]
        })
        
        return plan

    def format_plan_message(self, plan):
        """格式化学习计划为易读的消息"""
        message = f"📅 个性化学习计划 ({plan['date']})\n\n"
        
        # 添加优先级信息
        if plan['priority_levels']['high']:
            message += f"🔴 高优先级知识点：{', '.join(plan['priority_levels']['high'])}\n"
        if plan['priority_levels']['medium']:
            message += f"🟡 中优先级知识点：{', '.join(plan['priority_levels']['medium'])}\n"
        if plan['priority_levels']['low']:
            message += f"🟢 低优先级知识点：{', '.join(plan['priority_levels']['low'])}\n\n"
        
        # 添加每日任务
        message += "📋 今日学习任务：\n"
        for task in plan['daily_tasks']:
            message += f"\n{task['id']}. {task['topic']} - {task['type']}\n"
            message += f"   ⏱️  时长：{task['duration']}\n"
            message += f"   📝  内容：{task['description']}\n"
            if task['resources']:
                message += f"   📚  推荐资源：{', '.join(task['resources'])}\n"
        
        message += "\n💡 完成任务后可以随时查看学习进度或请求调整计划！"
        return message

    def adjust_plan(self, current_plan, adjustment_request):
        """简单的计划调整逻辑"""
        # 在实际应用中，这里应该实现更复杂的自然语言处理逻辑
        # 这里只是一个简单的示例
        adjusted_plan = current_plan.copy()
        
        # 简单地增加任务时长
        for task in adjusted_plan['daily_tasks']:
            if '30分钟' in task['duration']:
                task['duration'] = '45分钟'
            elif '20分钟' in task['duration']:
                task['duration'] = '30分钟'
        
        return adjusted_plan


if __name__ == "__main__":
    agent = PlanningAgent()
    agent.start(network_host="localhost", network_port=8700, network_id="production-network-1")
    agent.wait_for_stop()