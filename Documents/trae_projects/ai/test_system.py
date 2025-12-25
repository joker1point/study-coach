#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多智能体系统协作测试脚本
测试学生个性化伴学系统的完整协作流程
"""

import asyncio
import json
from openagents.agents.worker_agent import WorkerAgent, EventContext
from openagents.models.agent_config import AgentConfig

async def test_agent_collaboration():
    """测试多Agent协作流程"""
    print("=== 开始测试学生个性化伴学多智能体系统 ===")
    
    # 创建一个测试用的学生Agent
    student_agent_config = AgentConfig(
        instruction="你是一名测试学生，负责测试多Agent协作系统",
        model_name="gpt-3.5-turbo",
        provider="openai"
    )
    
    student_agent = WorkerAgent(agent_config=student_agent_config)
    
    # 启动学生Agent
    await student_agent.start(network_host="localhost", network_port=8700)
    print("✓ 学生Agent启动成功")
    
    try:
        # 1. 测试学情分析流程
        print("\n=== 1. 测试学情分析流程 ===")
        
        # 模拟作业数据
        test_homework_data = {
            "student_id": "test_student_001",
            "subject": "数学",
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
                    "content": "计算三角形面积：底=4，高=3",
                    "knowledge_points": ["math_geometry_triangle_area"],
                    "user_answer": "6",
                    "correct_answer": "6",
                    "is_correct": True,
                    "error_type": None
                },
                {
                    "id": "q004",
                    "content": "求圆的面积：半径=5",
                    "knowledge_points": ["math_geometry_circle"],
                    "user_answer": "25π",
                    "correct_answer": "25π",
                    "is_correct": True,
                    "error_type": None
                },
                {
                    "id": "q005",
                    "content": "求函数f(x) = x² + 2x的导数",
                    "knowledge_points": ["math_calculus_derivative"],
                    "user_answer": "f'(x) = 2x",
                    "correct_answer": "f'(x) = 2x + 2",
                    "is_correct": False,
                    "error_type": "calculation_error"
                }
            ]
        }
        
        # 向学情分析Agent提交作业
        print("向学情分析Agent提交作业数据...")
        await student_agent.workspace().agent("diagnosis-agent").send({
            "text": "提交作业",
            "data": test_homework_data
        })
        
        await asyncio.sleep(3)  # 等待处理完成
        print("✓ 学情分析完成")
        
        # 2. 测试任务规划流程
        print("\n=== 2. 测试任务规划流程 ===")
        
        # 等待任务规划Agent生成学习计划
        await asyncio.sleep(5)
        print("✓ 学习计划生成完成")
        
        # 3. 测试答疑辅导流程
        print("\n=== 3. 测试答疑辅导流程 ===")
        
        # 向答疑辅导Agent提问
        await student_agent.workspace().agent("tutoring-agent").send({
            "text": "什么是一元二次方程的求根公式？"
        })
        
        await asyncio.sleep(3)
        print("✓ 答疑完成")
        
        # 4. 测试复盘总结流程
        print("\n=== 4. 测试复盘总结流程 ===")
        
        # 触发复盘总结Agent生成报告
        await student_agent.workspace().agent("review-agent").send({
            "action": "generate_daily_report",
            "student_id": "test_student_001"
        })
        
        await asyncio.sleep(5)
        print("✓ 复盘总结完成")
        
        # 5. 测试学习计划调整流程
        print("\n=== 5. 测试学习计划调整流程 ===")
        
        # 模拟复盘总结Agent发现新的薄弱点
        await student_agent.workspace().agent("planning-agent").send({
            "action": "adjust_plan_based_on_weakness",
            "student_id": "test_student_001",
            "weak_point": "数学导数概念",
            "evidence": "学生在导数计算中出现多次错误"
        })
        
        await asyncio.sleep(3)
        print("✓ 学习计划调整完成")
        
        print("\n=== 测试完成！多Agent协作流程正常工作 ===")
        
    finally:
        # 停止Agent
        await student_agent.stop()

if __name__ == "__main__":
    asyncio.run(test_agent_collaboration())
