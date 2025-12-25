# 练习生成工具

from tool_manager import tool_manager
from typing import List, Dict, Any

@tool_manager.register_function(
    name="generate_exercises",
    title="生成练习",
    description="根据学情报告生成个性化练习题",
    input_schema={
        "student_id": {"type": "string", "description": "学生ID"},
        "subject": {"type": "string", "description": "学科"},
        "knowledge_points": {"type": "array", "items": {"type": "string"}, "description": "知识点列表"},
        "count": {"type": "integer", "description": "题目数量"},
        "difficulty": {"type": "string", "description": "难度级别: easy, medium, hard"}
    },
    output_schema={
        "exercises": {"type": "array", "items": {"type": "object"}, "description": "生成的练习题列表"}
    }
)
def generate_exercises_tool(student_id: str, subject: str, knowledge_points: List[str], count: int = 5, difficulty: str = "medium") -> Dict[str, Any]:
    """根据学情报告生成个性化练习题"""
    # 模拟练习生成
    exercises = []
    for i in range(count):
        exercises.append({
            "id": f"exercise_{i+1}",
            "subject": subject,
            "knowledge_point": knowledge_points[i % len(knowledge_points)] if knowledge_points else subject,
            "question": f"{subject}练习题 {i+1}: 关于{knowledge_points[i % len(knowledge_points)] if knowledge_points else subject}的问题",
            "options": [
                f"选项A - {difficulty}",
                f"选项B - {difficulty}",
                f"选项C - {difficulty}",
                f"选项D - {difficulty}"
            ],
            "correct_answer": "A",
            "difficulty": difficulty,
            "explanation": f"这是第{i+1}题的详细解释"
        })
    
    return {
        "exercises": exercises
    }

@tool_manager.register_function(
    name="grade_exercises",
    title="批改练习",
    description="批改学生的练习答案并生成反馈",
    input_schema={
        "student_id": {"type": "string", "description": "学生ID"},
        "exercises": {"type": "array", "items": {"type": "object"}, "description": "练习和答案列表"}
    },
    output_schema={
        "score": {"type": "number", "description": "得分"},
        "correct_count": {"type": "integer", "description": "正确数量"},
        "total_count": {"type": "integer", "description": "总数量"},
        "feedback": {"type": "object", "description": "详细反馈"}
    }
)
def grade_exercises_tool(student_id: str, exercises: List[Dict[str, Any]]) -> Dict[str, Any]:
    """批改学生的练习答案并生成反馈"""
    correct_count = 0
    total_count = len(exercises)
    
    for exercise in exercises:
        if exercise.get("student_answer") == exercise.get("correct_answer"):
            correct_count += 1
    
    score = (correct_count / total_count) * 100 if total_count > 0 else 0
    
    return {
        "score": score,
        "correct_count": correct_count,
        "total_count": total_count,
        "feedback": {
            "message": f"您的得分是 {score:.1f} 分",
            "strengths": ["答题速度快", "基础知识扎实"],
            "improvements": ["需要加强知识点的理解", "注意答题细节"]
        }
    }
