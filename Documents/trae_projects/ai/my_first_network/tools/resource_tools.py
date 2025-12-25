# 资源匹配工具

from tool_manager import tool_manager
from typing import List, Dict, Any

# 添加mods目录到Python路径
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mods/openagents.mods.education.learning_resource')))
from __init__ import match_resources as match_learning_resources

@tool_manager.register_function(
    name="match_learning_resources",
    title="匹配学习资源",
    description="根据学情报告匹配个性化学习资源",
    input_schema={
        "student_id": {"type": "string", "description": "学生ID"},
        "subject": {"type": "string", "description": "学科"},
        "knowledge_points": {"type": "array", "items": {"type": "string"}, "description": "知识点列表"},
        "learning_level": {"type": "string", "description": "学习水平"}
    },
    output_schema={
        "resources": {"type": "array", "items": {"type": "object"}, "description": "匹配到的资源列表"}
    }
)
def match_learning_resources_tool(student_id: str, subject: str, knowledge_points: List[str], learning_level: str) -> Dict[str, Any]:
    """根据学情报告匹配个性化学习资源"""
    learning_report = {
        "student_id": student_id,
        "subject": subject,
        "knowledge_points": knowledge_points,
        "learning_level": learning_level
    }
    
    resources = match_learning_resources(learning_report)
    return {
        "resources": resources
    }

@tool_manager.register_function(
    name="get_resource_details",
    title="获取资源详情",
    description="根据资源ID获取资源详细信息",
    input_schema={
        "resource_id": {"type": "string", "description": "资源ID"}
    },
    output_schema={
        "resource": {"type": "object", "description": "资源详细信息"}
    }
)
def get_resource_details(resource_id: str) -> Dict[str, Any]:
    """根据资源ID获取资源详细信息"""
    # 模拟资源详情获取
    return {
        "resource": {
            "id": resource_id,
            "title": f"资源 {resource_id}",
            "description": f"这是资源 {resource_id} 的详细描述",
            "type": "article",
            "url": f"https://example.com/resources/{resource_id}"
        }
    }
