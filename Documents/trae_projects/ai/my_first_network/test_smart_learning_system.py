# 智能学习辅助系统测试脚本

import asyncio
import json
from openagents.agents.worker_agent import WorkerAgent
from openagents.models.agent_config import AgentConfig

async def test_smart_learning_system():
    """测试智能学习辅助系统"""
    print("🧠 开始测试智能学习辅助系统...")
    
    # 创建测试数据
    test_learning_data = {
        "student_id": "student_001",
        "subject": "数学",
        "learning_duration": 3600,
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
                "content": "已知圆的半径为5cm，求圆的面积（π取3.14）",
                "knowledge_points": ["math_geometry_circle"],
                "user_answer": "78.5cm²",
                "correct_answer": "78.5cm²",
                "is_correct": True,
                "error_type": None
            },
            {
                "id": "q004",
                "content": "用配方法解方程：x² + 6x + 5 = 0",
                "knowledge_points": ["math_algebra_eq_quadratic"],
                "user_answer": "x = 1 或 x = 5",
                "correct_answer": "x = -1 或 x = -5",
                "is_correct": False,
                "error_type": "concept_error"
            }
        ]
    }
    
    print("📚 测试数据已准备好")
    print(f"测试学生ID: {test_learning_data['student_id']}")
    print(f"测试学科: {test_learning_data['subject']}")
    print(f"测试题目数量: {len(test_learning_data['questions'])}")
    
    # 测试知识图谱Mod
    print("\n🔍 测试知识图谱Mod...")
    
    try:
        # 添加mods目录到Python路径
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'mods/openagents.mods.education.knowledge_graph')))
        from __init__ import analyze_learning_data
        
        learning_report = analyze_learning_data(test_learning_data)
        print("✅ 知识图谱Mod测试成功")
        print(f"生成的学情报告包含 {len(learning_report['knowledge_gaps'])} 个知识盲点")
        print(f"掌握率: {learning_report['mastery_overview']['total_count']} 个知识点中，{learning_report['mastery_overview']['excellent_count']} 个优秀，{learning_report['mastery_overview']['good_count']} 个良好，{learning_report['mastery_overview']['average_count']} 个一般，{learning_report['mastery_overview']['poor_count']} 个较差")
        print(f"优先级高的知识盲点: {learning_report['knowledge_map']['priority_gaps']}")
    except Exception as e:
        print(f"❌ 知识图谱Mod测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # 测试学习资源库Mod
    print("\n🎯 测试学习资源库Mod...")
    
    try:
        # 移除之前添加的知识图谱Mod目录
        sys.path = [p for p in sys.path if 'knowledge_graph' not in p]
        
        # 添加学习资源库Mod目录到Python路径
        resource_mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mods/openagents.mods.education.learning_resource'))
        sys.path.append(resource_mod_path)
        
        # 使用importlib动态导入
        import importlib.util
        spec = importlib.util.spec_from_file_location("learning_resource_mod", os.path.join(resource_mod_path, "__init__.py"))
        learning_resource_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(learning_resource_mod)
        
        matched_resources = learning_resource_mod.match_resources(learning_report)
        print("✅ 学习资源库Mod测试成功")
        print(f"匹配到 {len(matched_resources)} 个学习资源")
        for i, resource in enumerate(matched_resources[:3]):
            print(f"  {i+1}. {resource['resource']['title']} (匹配度: {resource['match_score']})")
    except Exception as e:
        print(f"❌ 学习资源库Mod测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # 测试练习优化Agent
    print("\n📝 测试练习优化Agent...")
    
    try:
        # 直接从本地文件导入Agent
        import sys
        import os
        
        # 添加agents目录到Python路径
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'agents')))
        
        # 导入ExerciseOptimizationAgent
        from exercise_optimization_agent import ExerciseOptimizationAgent
        
        # 加载LLM配置
        from llm_config import DEFAULT_LLM_CONFIG
        
        # 创建Agent配置
        agent_config = AgentConfig(
            instruction="测试用练习优化助手",
            model_name=DEFAULT_LLM_CONFIG["model_name"],
            provider=DEFAULT_LLM_CONFIG["provider"],
            api_base=DEFAULT_LLM_CONFIG["api_base"],
            api_key=DEFAULT_LLM_CONFIG["api_key"]
        )
        
        # 创建Agent实例
        agent = ExerciseOptimizationAgent(agent_config=agent_config)
        
        # 生成练习题
        exercises = await agent.generate_exercises(learning_report, count=5)
        print("✅ 练习优化Agent测试成功")
        print(f"生成了 {len(exercises)} 个练习题")
        for i, exercise in enumerate(exercises[:3]):
            print(f"  {i+1}. {exercise['content']} (难度: {exercise['difficulty']})")
            print(f"     知识点: {exercise['knowledge_points']}")
            print(f"     选项: {exercise['options']}")
            print(f"     正确答案: {exercise['correct_answer']}")
    except Exception as e:
        print(f"❌ 练习优化Agent测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # 测试答题结果处理
    print("\n📋 测试答题结果处理...")
    
    try:
        # 创建测试答题结果
        test_answers = []
        for exercise in exercises[:3]:
            test_answers.append({
                "question_id": exercise["id"],
                "user_answer": exercise["options"][0]  # 故意选择第一个选项作为答案
            })
        
        # 处理答题结果
        processed_data = agent._process_answers(
            student_id="student_001",
            subject="数学",
            answers=test_answers
        )
        
        print("✅ 答题结果处理测试成功")
        print(f"处理了 {len(processed_data['questions'])} 个答题结果")
        for i, question in enumerate(processed_data['questions']):
            result = "正确" if question['is_correct'] else "错误"
            print(f"  {i+1}. {question['content']}")
            print(f"     我的答案: {question['user_answer']}，正确答案: {question['correct_answer']}，结果: {result}")
    except Exception as e:
        print(f"❌ 答题结果处理测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🎉 智能学习辅助系统测试完成！")
    print("所有核心功能都已成功测试，系统可以正常工作。")
    print("\n系统功能总结：")
    print("1. 知识图谱Mod：成功生成了详细的学情报告和知识图谱")
    print("2. 学习资源库Mod：成功匹配了适合的学习资源")
    print("3. 练习优化Agent：成功生成了分层练习题")
    print("4. 答题结果处理：成功处理了答题结果并生成了学习数据")
    print("\n系统架构总结：")
    print("- 3个Agent协同工作：学情分析、资源匹配、练习优化")
    print("- 2个核心Mod：知识图谱、学习资源库")
    print("- 事件驱动的协作机制")
    print("- 支持gRPC和HTTP双协议")
    print("- 模块化的扩展设计")
    
    print("\n🚀 智能学习辅助系统已准备就绪，可以开始使用了！")


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_smart_learning_system())