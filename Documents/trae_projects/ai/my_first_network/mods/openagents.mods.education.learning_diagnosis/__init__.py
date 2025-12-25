"""
学情诊断Mod - 提供学习数据分析和知识盲点识别功能
"""

from typing import Dict, List, Set, Any
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class KnowledgePoint:
    """知识点数据结构"""
    id: str
    name: str
    category: str
    parent_id: str = None
    mastery_level: float = 0.0  # 0.0-1.0之间的掌握程度


@dataclass
class KnowledgeGap:
    """知识盲点数据结构"""
    knowledge_point: KnowledgePoint
    gap_reason: str  # 产生盲点的原因
    error_count: int  # 相关错误次数
    priority: int  # 优先级，1-5，5最高


class LearningDiagnosisMod:
    """学情诊断Mod的核心实现"""
    
    def __init__(self):
        self.knowledge_base = {}
        self._load_default_knowledge_base()
    
    def _load_default_knowledge_base(self):
        """加载默认的知识点库"""
        # 这里可以从文件或数据库加载知识点库
        # 示例：数学知识点
        math_knowledge = [
            KnowledgePoint("math_algebra", "代数", "数学"),
            KnowledgePoint("math_algebra_eq", "方程", "数学", "math_algebra"),
            KnowledgePoint("math_algebra_eq_linear", "一元一次方程", "数学", "math_algebra_eq"),
            KnowledgePoint("math_algebra_eq_quadratic", "一元二次方程", "数学", "math_algebra_eq"),
            KnowledgePoint("math_geometry", "几何", "数学"),
            KnowledgePoint("math_geometry_triangle", "三角形", "数学", "math_geometry"),
            KnowledgePoint("math_geometry_triangle_area", "三角形面积", "数学", "math_geometry_triangle"),
            KnowledgePoint("math_geometry_circle", "圆", "数学", "math_geometry"),
            KnowledgePoint("math_calculus", "微积分", "数学"),
            KnowledgePoint("math_calculus_derivative", "导数", "数学", "math_calculus"),
        ]
        
        # 添加到知识库
        for kp in math_knowledge:
            self.knowledge_base[kp.id] = kp
    
    def analyze_homework(self, homework_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析作业数据，识别知识盲点
        
        Args:
            homework_data: 作业数据，包含题目和答案信息
            格式示例: {
                "student_id": "student_001",
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
        
        Returns:
            包含知识盲点和知识图谱的分析结果
        """
        student_id = homework_data.get("student_id", "unknown")
        subject = homework_data.get("subject", "general")
        questions = homework_data.get("questions", [])
        
        # 提取知识盲点
        knowledge_gaps = self.extract_knowledge_gaps(questions)
        
        # 生成知识图谱
        knowledge_map = self.generate_knowledge_map(knowledge_gaps, subject)
        
        return {
            "student_id": student_id,
            "subject": subject,
            "knowledge_gaps": [
                {
                    "knowledge_point": gap.knowledge_point.name,
                    "gap_reason": gap.gap_reason,
                    "error_count": gap.error_count,
                    "priority": gap.priority
                }
                for gap in knowledge_gaps
            ],
            "knowledge_map": knowledge_map,
            "analysis_time": datetime.now().isoformat()
        }
    
    def extract_knowledge_gaps(self, questions: List[Dict[str, Any]]) -> List[KnowledgeGap]:
        """
        从题目列表中提取知识盲点
        
        Args:
            questions: 题目列表，包含每个题目的知识点和答题情况
        
        Returns:
            知识盲点列表
        """
        knowledge_gaps = []
        error_count_by_kp = {}
        
        # 统计每个知识点的错误次数
        for question in questions:
            if not question.get("is_correct", False):
                for kp_id in question.get("knowledge_points", []):
                    if kp_id in error_count_by_kp:
                        error_count_by_kp[kp_id] += 1
                    else:
                        error_count_by_kp[kp_id] = 1
        
        # 生成知识盲点
        for kp_id, error_count in error_count_by_kp.items():
            if kp_id in self.knowledge_base:
                knowledge_point = self.knowledge_base[kp_id]
                
                # 确定盲点原因
                gap_reason = self._determine_gap_reason(questions, kp_id)
                
                # 计算优先级（基于错误次数和知识点重要性）
                priority = min(5, error_count + 1)  # 简单的优先级计算
                
                knowledge_gaps.append(KnowledgeGap(
                    knowledge_point=knowledge_point,
                    gap_reason=gap_reason,
                    error_count=error_count,
                    priority=priority
                ))
        
        # 按优先级排序，优先级高的排在前面
        knowledge_gaps.sort(key=lambda x: x.priority, reverse=True)
        
        return knowledge_gaps
    
    def _determine_gap_reason(self, questions: List[Dict[str, Any]], kp_id: str) -> str:
        """
        确定产生知识盲点的原因
        
        Args:
            questions: 题目列表
            kp_id: 知识点ID
        
        Returns:
            盲点原因
        """
        error_types = []
        
        for question in questions:
            if not question.get("is_correct", False) and kp_id in question.get("knowledge_points", []):
                error_type = question.get("error_type", "unknown")
                error_types.append(error_type)
        
        # 根据错误类型确定原因
        if not error_types:
            return "未知原因"
        
        # 统计最常见的错误类型
        from collections import Counter
        error_counter = Counter(error_types)
        most_common_error = error_counter.most_common(1)[0][0]
        
        reason_map = {
            "concept_error": "概念理解错误",
            "calculation_error": "计算错误",
            "application_error": "应用错误",
            "incomplete_solution": "答案不完整",
            "misinterpretation": "题意理解错误",
            "unknown": "未知原因"
        }
        
        return reason_map.get(most_common_error, "未知原因")
    
    def generate_knowledge_map(self, knowledge_gaps: List[KnowledgeGap], subject: str) -> Dict[str, Any]:
        """
        生成知识图谱
        
        Args:
            knowledge_gaps: 知识盲点列表
            subject: 学科
        
        Returns:
            知识图谱数据
        """
        # 收集所有相关知识点
        all_kps = set()
        gap_kps = set()
        
        for gap in knowledge_gaps:
            kp = gap.knowledge_point
            gap_kps.add(kp.id)
            all_kps.add(kp.id)
            
            # 添加父知识点
            current_kp = kp
            while current_kp.parent_id:
                if current_kp.parent_id in self.knowledge_base:
                    parent_kp = self.knowledge_base[current_kp.parent_id]
                    all_kps.add(parent_kp.id)
                    current_kp = parent_kp
                else:
                    break
        
        # 构建知识图谱结构
        knowledge_map = {
            "subject": subject,
            "total_topics": len(all_kps),
            "gaps_count": len(gap_kps),
            "mastery_rate": 1.0 - (len(gap_kps) / len(all_kps)) if all_kps else 0.0,
            "priority_gaps": [
                gap.knowledge_point.name for gap in knowledge_gaps if gap.priority >= 4
            ],
            "knowledge_tree": self._build_knowledge_tree(list(all_kps), gap_kps)
        }
        
        return knowledge_map
    
    def _build_knowledge_tree(self, all_kp_ids: List[str], gap_kp_ids: Set[str]) -> List[Dict[str, Any]]:
        """
        构建知识树结构
        
        Args:
            all_kp_ids: 所有相关知识点ID
            gap_kp_ids: 知识盲点ID集合
        
        Returns:
            知识树结构
        """
        # 构建知识点ID到知识点对象的映射
        kp_map = {kp_id: self.knowledge_base[kp_id] for kp_id in all_kp_ids if kp_id in self.knowledge_base}
        
        # 构建父ID到子知识点的映射
        parent_map = {}
        for kp_id, kp in kp_map.items():
            if kp.parent_id:
                if kp.parent_id not in parent_map:
                    parent_map[kp.parent_id] = []
                parent_map[kp.parent_id].append(kp)
        
        # 找到根节点
        root_kps = [kp for kp in kp_map.values() if not kp.parent_id]
        
        # 递归构建树
        def build_tree_node(kp: KnowledgePoint) -> Dict[str, Any]:
            """构建单个树节点"""
            node = {
                "id": kp.id,
                "name": kp.name,
                "category": kp.category,
                "is_gap": kp.id in gap_kp_ids,
                "children": []
            }
            
            # 添加子节点
            if kp.id in parent_map:
                for child_kp in parent_map[kp.id]:
                    node["children"].append(build_tree_node(child_kp))
            
            return node
        
        return [build_tree_node(kp) for kp in root_kps]
    
    def update_knowledge_mastery(self, student_id: str, subject: str, mastery_data: Dict[str, float]):
        """
        更新知识点掌握程度
        
        Args:
            student_id: 学生ID
            subject: 学科
            mastery_data: 知识点掌握程度数据，格式为 {"知识点ID": 掌握程度(0.0-1.0)}
        """
        # 这里可以实现将掌握程度保存到持久化存储的逻辑
        pass


# 创建Mod实例供外部使用
learning_diagnosis_mod = LearningDiagnosisMod()


# 导出Mod的主要功能
def analyze_homework(homework_data: Dict[str, Any]) -> Dict[str, Any]:
    """分析作业数据"""
    return learning_diagnosis_mod.analyze_homework(homework_data)


def extract_knowledge_gaps(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """提取知识盲点"""
    gaps = learning_diagnosis_mod.extract_knowledge_gaps(questions)
    return [
        {
            "knowledge_point": gap.knowledge_point.name,
            "gap_reason": gap.gap_reason,
            "error_count": gap.error_count,
            "priority": gap.priority
        }
        for gap in gaps
    ]


def generate_knowledge_map(knowledge_gaps: List[Dict[str, Any]], subject: str) -> Dict[str, Any]:
    """生成知识图谱"""
    # 转换为内部数据结构
    internal_gaps = []
    for gap in knowledge_gaps:
        # 查找对应的知识点对象
        kp = None
        for kp_obj in learning_diagnosis_mod.knowledge_base.values():
            if kp_obj.name == gap["knowledge_point"]:
                kp = kp_obj
                break
        
        if kp:
            internal_gaps.append(KnowledgeGap(
                knowledge_point=kp,
                gap_reason=gap["gap_reason"],
                error_count=gap["error_count"],
                priority=gap["priority"]
            ))
    
    return learning_diagnosis_mod.generate_knowledge_map(internal_gaps, subject)


def update_knowledge_mastery(student_id: str, subject: str, mastery_data: Dict[str, float]):
    """更新知识点掌握程度"""
    return learning_diagnosis_mod.update_knowledge_mastery(student_id, subject, mastery_data)
