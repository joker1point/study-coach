# 测试工具调用功能

import sys
import os

# 添加my_first_network目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# 导入工具管理器
from tools.tool_manager import tool_manager

# 导入工具实现
from tools import resource_tools
from tools import exercise_tools

def test_tool_registration():
    """测试工具注册"""
    print("=== 测试工具注册 ===")
    tools = tool_manager.list_tools()
    print(f"注册的工具: {tools}")
    
    assert len(tools) > 0, "没有工具注册成功"
    print("✅ 工具注册测试通过！")

def test_resource_tools():
    """测试资源工具"""
    print("\n=== 测试资源工具 ===")
    
    # 测试匹配学习资源工具
    print("测试match_learning_resources工具...")
    result = tool_manager.call_tool(
        "match_learning_resources",
        student_id="test_student_123",
        subject="数学",
        knowledge_points=["代数", "几何", "微积分"],
        learning_level="中级"
    )
    print(f"结果: {result}")
    assert "resources" in result, "match_learning_resources工具调用失败"
    print("✅ match_learning_resources工具测试通过！")
    
    # 测试获取资源详情工具
    print("\n测试get_resource_details工具...")
    result = tool_manager.call_tool(
        "get_resource_details",
        resource_id="resource_001"
    )
    print(f"结果: {result}")
    assert "resource" in result, "get_resource_details工具调用失败"
    print("✅ get_resource_details工具测试通过！")

def test_exercise_tools():
    """测试练习工具"""
    print("\n=== 测试练习工具 ===")
    
    # 测试生成练习工具
    print("测试generate_exercises工具...")
    result = tool_manager.call_tool(
        "generate_exercises",
        student_id="test_student_123",
        subject="英语",
        knowledge_points=["语法", "词汇", "阅读"],
        count=3,
        difficulty="medium"
    )
    print(f"结果: {result}")
    assert "exercises" in result, "generate_exercises工具调用失败"
    assert len(result["exercises"]) == 3, "生成的练习数量不正确"
    print("✅ generate_exercises工具测试通过！")
    
    # 测试批改练习工具
    print("\n测试grade_exercises工具...")
    exercises = [
        {"student_answer": "A", "correct_answer": "A"},
        {"student_answer": "B", "correct_answer": "A"},
        {"student_answer": "A", "correct_answer": "A"}
    ]
    result = tool_manager.call_tool(
        "grade_exercises",
        student_id="test_student_123",
        exercises=exercises
    )
    print(f"结果: {result}")
    assert "score" in result, "grade_exercises工具调用失败"
    assert result["correct_count"] == 2, "批改结果不正确"
    assert result["total_count"] == 3, "练习总数不正确"
    print("✅ grade_exercises工具测试通过！")

def test_tool_call_pattern():
    """测试工具调用模式解析"""
    print("\n=== 测试工具调用模式解析 ===")
    
    # 测试模式解析
    import re
    tool_call_pattern = r"调用工具\[(\w+)\]\s*(?:参数\[(.*?)\])?"
    
    # 测试用例1
    test_str1 = "调用工具[generate_exercises]参数[student_id=test_123,subject=数学,count=5]"
    match = re.search(tool_call_pattern, test_str1)
    assert match is not None, "测试用例1解析失败"
    assert match.group(1) == "generate_exercises", "工具名解析错误"
    print(f"测试用例1解析成功: 工具={match.group(1)}, 参数={match.group(2)}")
    
    # 测试用例2
    test_str2 = "调用工具[get_resource_details]参数[resource_id=res_001]"
    match = re.search(tool_call_pattern, test_str2)
    assert match is not None, "测试用例2解析失败"
    assert match.group(1) == "get_resource_details", "工具名解析错误"
    print(f"测试用例2解析成功: 工具={match.group(1)}, 参数={match.group(2)}")
    
    print("✅ 工具调用模式解析测试通过！")

if __name__ == "__main__":
    print("开始工具调用功能测试...")
    
    try:
        test_tool_registration()
        test_resource_tools()
        test_exercise_tools()
        test_tool_call_pattern()
        
        print("\n🎉 所有测试通过！工具调用功能正常工作！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
