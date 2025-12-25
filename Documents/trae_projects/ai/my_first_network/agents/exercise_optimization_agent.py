# 练习优化Agent - 根据学习进度生成分层练习题

from openagents.agents.worker_agent import WorkerAgent, EventContext, ChannelMessageContext, on_event
from openagents.models.agent_config import AgentConfig

# 导入知识图谱Mod
import sys
import os
# 添加mods目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mods/openagents.mods.education.knowledge_graph')))
from __init__ import get_related_knowledge_points


class ExerciseOptimizationAgent(WorkerAgent):
    default_agent_id = "exercise-optimization-agent"
    ignore_own_messages = True

    def __init__(self, agent_config=None):
        super().__init__(agent_config=agent_config)
        # 配置模型提供器为OpenAI兼容API（用于Ollama）
        if self.agent_config and not self.agent_config.api_key:
            self.agent_config.api_key = "dummy"  # Ollama不需要真实API密钥
        # 模拟题库
        self.question_bank = self._init_question_bank()
    
    def _init_question_bank(self):
        """初始化模拟题库"""
        return {
            "math_algebra_eq_linear": [
                {
                    "id": "q_math_001",
                    "content": "解方程：2x + 3 = 7",
                    "knowledge_points": ["math_algebra_eq_linear"],
                    "difficulty": "简单",
                    "correct_answer": "x = 2",
                    "options": ["x = 2", "x = 3", "x = 4", "x = 5"]
                },
                {
                    "id": "q_math_002",
                    "content": "解方程：3(x - 1) + 5 = 14",
                    "knowledge_points": ["math_algebra_eq_linear"],
                    "difficulty": "中等",
                    "correct_answer": "x = 4",
                    "options": ["x = 3", "x = 4", "x = 5", "x = 6"]
                }
            ],
            "math_algebra_eq_quadratic": [
                {
                    "id": "q_math_003",
                    "content": "解方程：x² + 2x - 3 = 0",
                    "knowledge_points": ["math_algebra_eq_quadratic"],
                    "difficulty": "中等",
                    "correct_answer": "x = 1 或 x = -3",
                    "options": ["x = 1", "x = -3", "x = 1 或 x = -3", "x = 2 或 x = -1"]
                },
                {
                    "id": "q_math_004",
                    "content": "用配方法解方程：x² + 6x + 5 = 0",
                    "knowledge_points": ["math_algebra_eq_quadratic"],
                    "difficulty": "困难",
                    "correct_answer": "x = -1 或 x = -5",
                    "options": ["x = -1", "x = -5", "x = -1 或 x = -5", "x = 1 或 x = 5"]
                }
            ],
            "math_geometry_triangle_area": [
                {
                    "id": "q_math_005",
                    "content": "已知三角形底边长为6cm，高为4cm，求面积",
                    "knowledge_points": ["math_geometry_triangle_area"],
                    "difficulty": "简单",
                    "correct_answer": "12cm²",
                    "options": ["12cm²", "24cm²", "10cm²", "8cm²"]
                }
            ],
            "math_geometry_circle": [
                {
                    "id": "q_math_006",
                    "content": "已知圆的半径为5cm，求圆的面积（π取3.14）",
                    "knowledge_points": ["math_geometry_circle"],
                    "difficulty": "中等",
                    "correct_answer": "78.5cm²",
                    "options": ["31.4cm²", "78.5cm²", "15.7cm²", "10cm²"]
                }
            ],
            "physics_mechanics_newton": [
                {
                    "id": "q_physics_001",
                    "content": "根据牛顿第一定律，下列说法正确的是（）",
                    "knowledge_points": ["physics_mechanics_newton"],
                    "difficulty": "简单",
                    "correct_answer": "B",
                    "options": [
                        "A. 物体的运动需要力来维持",
                        "B. 物体不受力时会保持静止或匀速直线运动",
                        "C. 物体受力越大，速度越大",
                        "D. 物体不受力时会立即停止运动"
                    ]
                }
            ],
            "english_grammar_tenses": [
                {
                    "id": "q_english_001",
                    "content": "She ___ to the park every Sunday.（用go的正确形式填空）",
                    "knowledge_points": ["english_grammar_tenses"],
                    "difficulty": "简单",
                    "correct_answer": "goes",
                    "options": ["go", "goes", "went", "going"]
                }
            ]
        }
    
    async def generate_exercises(self, learning_report: dict, count: int = 5) -> list:
        """
        根据学情报告生成分层练习题
        
        Args:
            learning_report: 学情报告
            count: 练习题数量
        
        Returns:
            list: 生成的练习题列表
        """
        generated_exercises = []
        
        # 提取知识盲点和掌握程度
        knowledge_gaps = learning_report.get('knowledge_gaps', [])
        subject = learning_report.get('subject', '')
        
        if knowledge_gaps:
            # 按优先级排序知识盲点
            sorted_gaps = sorted(knowledge_gaps, key=lambda x: x['priority'], reverse=True)
            
            # 为每个知识盲点生成对应难度的练习题
            for gap in sorted_gaps:
                kp_id = gap.get('knowledge_point_id', '')
                priority = gap.get('priority', 1)
                
                # 根据优先级确定习题难度
                difficulty_map = {
                    1: ['简单'],
                    2: ['简单', '中等'],
                    3: ['中等'],
                    4: ['中等', '困难'],
                    5: ['困难']
                }
                difficulties = difficulty_map.get(priority, ['中等'])
                
                # 获取相关知识点
                related_kps = get_related_knowledge_points(kp_id, depth=1)
                related_kp_ids = [kp['id'] for kp in related_kps]
                
                # 生成练习题
                exercises = self._generate_exercises_for_kps(related_kp_ids, difficulties, count=2)
                generated_exercises.extend(exercises)
                
                if len(generated_exercises) >= count:
                    break
        else:
            # 没有知识盲点，生成基础练习题
            # 获取该学科的所有知识点
            subject_kps = self._get_subject_knowledge_points(subject)
            if subject_kps:
                generated_exercises = self._generate_exercises_for_kps(subject_kps, ['简单', '中等'], count=count)
        
        # 确保练习题数量
        if len(generated_exercises) < count:
            # 补充一些随机练习题
            additional_exercises = self._generate_random_exercises(subject, count - len(generated_exercises))
            generated_exercises.extend(additional_exercises)
        
        return generated_exercises[:count]
    
    def _generate_exercises_for_kps(self, kp_ids: list, difficulties: list, count: int = 3) -> list:
        """
        为指定知识点生成练习题
        
        Args:
            kp_ids: 知识点ID列表
            difficulties: 难度列表
            count: 练习题数量
        
        Returns:
            list: 生成的练习题列表
        """
        exercises = []
        
        for kp_id in kp_ids:
            if kp_id in self.question_bank:
                kp_questions = self.question_bank[kp_id]
                # 过滤指定难度的题目
                filtered_questions = [q for q in kp_questions if q['difficulty'] in difficulties]
                # 随机选择题目
                import random
                selected_questions = random.sample(filtered_questions, min(count, len(filtered_questions)))
                exercises.extend(selected_questions)
        
        return exercises
    
    def _generate_random_exercises(self, subject: str, count: int = 3) -> list:
        """
        生成随机练习题
        
        Args:
            subject: 学科
            count: 练习题数量
        
        Returns:
            list: 生成的练习题列表
        """
        all_exercises = []
        
        # 收集该学科的所有练习题
        for kp_id, questions in self.question_bank.items():
            for question in questions:
                if subject in kp_id or not subject:  # 简单的学科匹配
                    all_exercises.append(question)
        
        # 随机选择题目
        import random
        return random.sample(all_exercises, min(count, len(all_exercises)))
    
    def _get_subject_knowledge_points(self, subject: str) -> list:
        """
        获取指定学科的知识点ID列表
        
        Args:
            subject: 学科
        
        Returns:
            list: 知识点ID列表
        """
        # 简单的学科到知识点映射
        subject_kp_map = {
            '数学': ['math_algebra_eq_linear', 'math_algebra_eq_quadratic', 'math_geometry_triangle_area', 'math_geometry_circle'],
            '物理': ['physics_mechanics_newton'],
            '英语': ['english_grammar_tenses']
        }
        
        return subject_kp_map.get(subject, [])
    
    async def _publish_exercise_updated_event(self, learning_data: dict):
        """发布练习数据更新事件"""
        try:
            ws = self.workspace()
            await ws.event_system.publish(
                event_type="learning.exercise.updated",
                content=learning_data
            )
            print(f"📤 发布了learning.exercise.updated事件")
        except Exception as e:
            print(f"❌ 发布learning.exercise.updated事件时出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def on_startup(self):
        """Agent启动时执行"""
        ws = self.workspace()
        await ws.channel("general").post("练习优化Agent已上线，随时准备生成个性化练习题！")

    async def on_direct(self, context: EventContext):
        """处理直接发送给Agent的消息"""
        try:
            # 获取消息内容
            message = context.incoming_event.content
            if isinstance(message, dict):
                message_text = message.get("text", str(message))
                
                # 检查是否包含生成练习题请求
                if "generate_exercises" in message:
                    learning_report = message["generate_exercises"]
                    count = message.get("count", 5)
                    
                    # 生成练习题
                    exercises = await self.generate_exercises(learning_report, count)
                    
                    # 发送响应
                    ws = self.workspace()
                    await ws.agent(context.source_id).send({
                        "message": "练习题生成完成",
                        "exercises": exercises
                    })
                # 检查是否包含答题结果
                elif "submit_answers" in message:
                    submit_data = message["submit_answers"]
                    student_id = submit_data.get("student_id", "unknown")
                    subject = submit_data.get("subject", "")
                    answers = submit_data.get("answers", [])
                    
                    # 处理答题结果
                    learning_data = self._process_answers(student_id, subject, answers)
                    
                    # 发布练习数据更新事件
                    await self._publish_exercise_updated_event(learning_data)
                    
                    # 发送响应
                    ws = self.workspace()
                    await ws.agent(context.source_id).send({
                        "message": "答题结果已收到，正在更新学情报告",
                        "learning_data": learning_data
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
    
    def _process_answers(self, student_id: str, subject: str, answers: list) -> dict:
        """
        处理答题结果
        
        Args:
            student_id: 学生ID
            subject: 学科
            answers: 答题结果列表
        
        Returns:
            dict: 学习数据
        """
        processed_questions = []
        
        for answer in answers:
            question_id = answer.get("question_id", "")
            user_answer = answer.get("user_answer", "")
            
            # 查找对应的题目
            question = self._find_question_by_id(question_id)
            if question:
                # 判断答案是否正确
                is_correct = user_answer == question["correct_answer"]
                
                # 确定错误类型
                error_type = None
                if not is_correct:
                    error_type = "concept_error" if user_answer in question["options"] else "misinterpretation"
                
                processed_questions.append({
                    "id": question_id,
                    "content": question["content"],
                    "knowledge_points": question["knowledge_points"],
                    "user_answer": user_answer,
                    "correct_answer": question["correct_answer"],
                    "is_correct": is_correct,
                    "error_type": error_type,
                    "difficulty": question["difficulty"]
                })
        
        # 构建学习数据
        learning_data = {
            "student_id": student_id,
            "subject": subject,
            "learning_duration": 0,  # 可以根据实际情况记录学习时长
            "questions": processed_questions
        }
        
        return learning_data
    
    def _find_question_by_id(self, question_id: str) -> dict:
        """
        根据ID查找题目
        
        Args:
            question_id: 题目ID
        
        Returns:
            dict: 题目信息，不存在返回None
        """
        for kp_questions in self.question_bank.values():
            for question in kp_questions:
                if question["id"] == question_id:
                    return question
        return None
    
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
            # 格式化指令
            formatted_instruction = f"""
            你是一个专业的练习优化助手，能够根据学习进度生成分层练习题。
            
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
        instruction="你是一个专业的练习优化助手，能够根据学习进度生成分层练习题，帮助学生巩固知识。",
        model_name=DEFAULT_LLM_CONFIG["model_name"],
        provider=DEFAULT_LLM_CONFIG["provider"],
        api_base=DEFAULT_LLM_CONFIG["api_base"],
        api_key=DEFAULT_LLM_CONFIG["api_key"]
    )
    agent = ExerciseOptimizationAgent(agent_config=agent_config)
    agent.start(network_host="localhost", network_port=8700)
    agent.wait_for_stop()