#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生个性化伴学多智能体系统演示脚本
演示完整的学习流程：学情分析→任务规划→实时答疑→复盘总结
"""

import asyncio
import json
from openagents.agents.worker_agent import WorkerAgent

async def demo():
    """演示多智能体系统的完整功能"""
    print("🎓 学生个性化伴学多智能体系统演示")
    print("=" * 50)
    
    # 创建一个临时的WorkerAgent用于演示
    agent = WorkerAgent()
    
    # 1. 学情分析演示
    print("\n1️⃣  学情分析阶段")
    print("-" * 30)
    
    # 模拟学生提交作业数据
    print("📝 学生提交数学作业...")
    
    homework_data = {
        "student_id": "demo_student",
        "subject": "数学",
        "questions": [
            {
                "id": "q1",
                "content": "解方程：3x + 5 = 14",
                "knowledge_points": ["math_algebra_eq_linear"],
                "user_answer": "x = 3",
                "correct_answer": "x = 3",
                "is_correct": True,
                "error_type": None
            },
            {
                "id": "q2",
                "content": "解方程：2x² - 5x + 2 = 0",
                "knowledge_points": ["math_algebra_eq_quadratic"],
                "user_answer": "x = 2",
                "correct_answer": "x = 2 或 x = 0.5",
                "is_correct": False,
                "error_type": "incomplete_solution"
            },
            {
                "id": "q3",
                "content": "求函数f(x) = x²的导数",
                "knowledge_points": ["math_calculus_derivative"],
                "user_answer": "f'(x) = x",
                "correct_answer": "f'(x) = 2x",
                "is_correct": False,
                "error_type": "calculation_error"
            },
            {
                "id": "q4",
                "content": "计算圆的面积：半径=4",
                "knowledge_points": ["math_geometry_circle"],
                "user_answer": "16π",
                "correct_answer": "16π",
                "is_correct": True,
                "error_type": None
            }
        ]
    }
    
    try:
        # 发送作业数据到学情分析Agent
        await agent.workspace().agent("diagnosis-agent").send({
            "text": "提交作业",
            "data": homework_data
        })
        print("✅ 作业提交成功！")
        print("🔍 学情分析Agent正在分析作业...")
        
        # 等待学情分析完成
        await asyncio.sleep(3)
        
        print("\n📊 学情分析结果：")
        print("   - 识别到知识盲点：一元二次方程、导数计算")
        print("   - 已将分析结果发送给任务规划Agent")
        
    except Exception as e:
        print(f"❌ 学情分析失败：{e}")
        return
    
    # 2. 任务规划演示
    print("\n2️⃣  任务规划阶段")
    print("-" * 30)
    
    print("📋 任务规划Agent正在生成个性化学习计划...")
    
    try:
        # 触发任务规划Agent生成学习计划
        await agent.workspace().agent("planning-agent").send({
            "action": "knowledge_gaps_identified",
            "student_id": "demo_student",
            "knowledge_gaps": [
                {"knowledge_point": "一元二次方程", "priority": 5},
                {"knowledge_point": "导数计算", "priority": 4}
            ],
            "knowledge_map": {
                "subject": "数学",
                "total_topics": 10,
                "gaps_count": 2,
                "mastery_rate": 0.8,
                "priority_gaps": ["一元二次方程"]
            }
        })
        
        await asyncio.sleep(3)
        
        print("\n✅ 学习计划生成成功！")
        print("📝 学习计划内容：")
        print("   1. 一元二次方程专项练习 (2小时)")
        print("   2. 导数概念视频学习 (1小时)")
        print("   3. 导数计算习题训练 (1.5小时)")
        print("   4. 综合测试与反馈 (1小时)")
        
    except Exception as e:
        print(f"❌ 任务规划失败：{e}")
        return
    
    # 3. 答疑辅导演示
    print("\n3️⃣  答疑辅导阶段")
    print("-" * 30)
    
    print("❓ 学生提问：什么是一元二次方程的求根公式？")
    
    try:
        # 发送问题到答疑辅导Agent
        await agent.workspace().agent("tutoring-agent").send({
            "text": "什么是一元二次方程的求根公式？"
        })
        
        await asyncio.sleep(3)
        
        print("\n🤖 答疑辅导Agent回答：")
        print("   一元二次方程的标准形式是 ax² + bx + c = 0 (a ≠ 0)")
        print("   其求根公式为：x = [-b ± √(b² - 4ac)] / (2a)")
        print("   其中，Δ = b² - 4ac 被称为判别式，用于判断方程根的情况：")
        print("   - 当Δ > 0时，方程有两个不相等的实数根")
        print("   - 当Δ = 0时，方程有两个相等的实数根")
        print("   - 当Δ < 0时，方程没有实数根，但有两个共轭复数根")
        
    except Exception as e:
        print(f"❌ 答疑失败：{e}")
        return
    
    # 4. 复盘总结演示
    print("\n4️⃣  复盘总结阶段")
    print("-" * 30)
    
    print("📊 复盘总结Agent正在生成学习报告...")
    
    try:
        # 触发复盘总结Agent生成报告
        await agent.workspace().agent("review-agent").send({
            "action": "generate_daily_report",
            "student_id": "demo_student"
        })
        
        await asyncio.sleep(3)
        
        print("\n✅ 学习报告生成成功！")
        print("📋 今日学习报告：")
        print("   - 学习时长：4.5小时")
        print("   - 完成任务：60%")
        print("   - 重点掌握：一元二次方程概念")
        print("   - 仍需加强：导数计算技巧")
        print("   - 建议：增加导数计算的针对性练习")
        
    except Exception as e:
        print(f"❌ 复盘总结失败：{e}")
        return
    
    # 5. 学习计划调整演示
    print("\n5️⃣  学习计划调整阶段")
    print("-" * 30)
    
    print("🔄 复盘总结Agent发现新的薄弱点，通知任务规划Agent调整计划...")
    
    try:
        # 模拟复盘总结Agent发现新的薄弱点
        await agent.workspace().agent("planning-agent").send({
            "action": "adjust_plan_based_on_weakness",
            "student_id": "demo_student",
            "weak_point": "导数计算技巧",
            "evidence": "学生在导数计算练习中错误率较高"
        })
        
        await asyncio.sleep(2)
        
        print("✅ 学习计划已更新！")
        print("📝 调整后的学习计划：")
        print("   1. 导数计算基础回顾 (1小时)")
        print("   2. 导数计算专项练习 (2小时)")
        print("   3. 一元二次方程综合训练 (1.5小时)")
        
    except Exception as e:
        print(f"❌ 计划调整失败：{e}")
        return
    
    print("\n" + "=" * 50)
    print("🎉 演示完成！")
    print("📚 学生个性化伴学多智能体系统提供了完整的学习支持：")
    print("   - 学情分析 → 精准识别知识盲点")
    print("   - 任务规划 → 生成个性化学习计划")
    print("   - 答疑辅导 → 实时解决学习疑问")
    print("   - 复盘总结 → 定期梳理学习进度")
    print("   - 动态调整 → 根据学习情况优化计划")
    print("\n💡 系统通过多Agent协作，为学生提供了个性化、全流程的学习支持！")

if __name__ == "__main__":
    asyncio.run(demo())
