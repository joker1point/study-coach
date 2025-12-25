#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多智能体系统协作简单测试脚本
"""

import asyncio
import json

async def simple_test():
    """简单测试多Agent协作流程"""
    print("=== 学生个性化伴学多智能体系统测试 ===")
    
    # 导入必要的模块
    from openagents.agents.worker_agent import WorkerAgent
    
    # 创建一个临时的WorkerAgent来测试
    agent = WorkerAgent()
    
    # 1. 测试学情分析流程
    print("\n1. 测试学情分析Agent")
    
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
            }
        ]
    }
    
    print("发送作业数据到学情分析Agent...")
    try:
        await agent.workspace().agent("diagnosis-agent").send({
            "text": "提交作业",
            "data": test_homework_data
        })
        print("✓ 作业提交成功")
    except Exception as e:
        print(f"✗ 作业提交失败: {e}")
    
    await asyncio.sleep(2)
    
    # 2. 测试任务规划Agent
    print("\n2. 测试任务规划Agent")
    print("检查是否能接收学情分析结果...")
    try:
        await agent.workspace().agent("planning-agent").send({
            "action": "knowledge_gaps_identified",
            "student_id": "test_student_001",
            "knowledge_gaps": ["一元二次方程", "导数计算"],
            "knowledge_map": {
                "subject": "数学",
                "total_topics": 10,
                "gaps_count": 2,
                "mastery_rate": 0.8,
                "priority_gaps": ["一元二次方程"]
            }
        })
        print("✓ 学习计划生成指令发送成功")
    except Exception as e:
        print(f"✗ 学习计划生成指令发送失败: {e}")
    
    await asyncio.sleep(2)
    
    # 3. 测试答疑辅导Agent
    print("\n3. 测试答疑辅导Agent")
    print("发送问题到答疑辅导Agent...")
    try:
        await agent.workspace().agent("tutoring-agent").send({
            "text": "什么是一元二次方程？"
        })
        print("✓ 问题发送成功")
    except Exception as e:
        print(f"✗ 问题发送失败: {e}")
    
    await asyncio.sleep(2)
    
    # 4. 测试复盘总结Agent
    print("\n4. 测试复盘总结Agent")
    print("请求生成学习报告...")
    try:
        await agent.workspace().agent("review-agent").send({
            "action": "generate_daily_report",
            "student_id": "test_student_001"
        })
        print("✓ 报告生成请求发送成功")
    except Exception as e:
        print(f"✗ 报告生成请求发送失败: {e}")
    
    await asyncio.sleep(2)
    
    # 5. 测试学习计划调整流程
    print("\n5. 测试学习计划调整流程")
    print("发送学习计划调整请求...")
    try:
        await agent.workspace().agent("planning-agent").send({
            "action": "adjust_plan_based_on_weakness",
            "student_id": "test_student_001",
            "weak_point": "数学导数概念",
            "evidence": "学生在导数计算中出现错误"
        })
        print("✓ 学习计划调整请求发送成功")
    except Exception as e:
        print(f"✗ 学习计划调整请求发送失败: {e}")
    
    await asyncio.sleep(2)
    
    print("\n=== 测试完成 ===")
    print("\n系统状态检查:")
    
    # 列出当前所有Agent
    try:
        agents = await agent.workspace().list_agents()
        print(f"\n当前运行的Agent数量: {len(agents)}")
        for i, agent_name in enumerate(agents, 1):
            print(f"  {i}. {agent_name}")
    except Exception as e:
        print(f"获取Agent列表失败: {e}")
    
    print("\n测试结束")

if __name__ == "__main__":
    # 使用asyncio.run运行测试
    asyncio.run(simple_test())
