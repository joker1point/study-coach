"""
知识图谱Mod - 提供知识点管理、知识图谱生成和掌握程度评估功能
"""

from typing import Dict, List, Set, Any, Tuple
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class KnowledgePoint:
    """知识点数据结构"""
    id: str
    name: str
    category: str
    subject: str
    parent_id: str = None
    mastery_level: float = 0.0  # 0.0-1.0之间的掌握程度
    importance: int = 3  # 1-5，5最高


@dataclass
class KnowledgeGap:
    """知识盲点数据结构"""
    knowledge_point: KnowledgePoint
    gap_reason: str  # 产生盲点的原因
    error_count: int  # 相关错误次数
    priority: int  # 优先级，1-5，5最高
    related_questions: List[str] = None  # 相关题目ID列表


class KnowledgeGraphMod:
    """知识图谱Mod的核心实现"""
    
    def __init__(self):
        self.knowledge_base = {}  # 存储所有知识点
        self.student_mastery = {}  # 存储学生知识点掌握程度
        self._load_default_knowledge_base()
    
    def _load_default_knowledge_base(self):
        """加载默认的知识点库"""
        # 数学知识点
        math_knowledge = [
            KnowledgePoint("math_algebra", "代数", "数学", "数学"),
            KnowledgePoint("math_algebra_eq", "方程", "数学", "数学", "math_algebra"),
            KnowledgePoint("math_algebra_eq_linear", "一元一次方程", "数学", "数学", "math_algebra_eq", importance=4),
            KnowledgePoint("math_algebra_eq_quadratic", "一元二次方程", "数学", "数学", "math_algebra_eq", importance=5),
            KnowledgePoint("math_geometry", "几何", "数学", "数学"),
            KnowledgePoint("math_geometry_triangle", "三角形", "数学", "数学", "math_geometry"),
            KnowledgePoint("math_geometry_triangle_area", "三角形面积", "数学", "数学", "math_geometry_triangle", importance=4),
            KnowledgePoint("math_geometry_circle", "圆", "数学", "数学", "math_geometry", importance=5),
            KnowledgePoint("math_calculus", "微积分", "数学", "数学"),
            KnowledgePoint("math_calculus_derivative", "导数", "数学", "数学", "math_calculus", importance=5),
        ]
        
        # 物理知识点
        physics_knowledge = [
            KnowledgePoint("physics_mechanics", "力学", "物理", "物理"),
            KnowledgePoint("physics_mechanics_newton", "牛顿定律", "物理", "物理", "physics_mechanics", importance=5),
            KnowledgePoint("physics_mechanics_kinematics", "运动学", "物理", "物理", "physics_mechanics", importance=4),
            KnowledgePoint("physics_mechanics_work", "功和能", "物理", "物理", "physics_mechanics", importance=5),
            KnowledgePoint("physics_electricity", "电学", "物理", "物理"),
            KnowledgePoint("physics_electricity_circuit", "电路", "物理", "物理", "physics_electricity", importance=4),
            KnowledgePoint("physics_electricity_field", "电场", "物理", "物理", "physics_electricity", importance=5),
        ]
        
        # 英语知识点
        english_knowledge = [
            KnowledgePoint("english_grammar", "语法", "英语", "英语"),
            KnowledgePoint("english_grammar_tenses", "时态", "英语", "英语", "english_grammar", importance=5),
            KnowledgePoint("english_grammar_sentence", "句型", "英语", "英语", "english_grammar", importance=4),
            KnowledgePoint("english_vocabulary", "词汇", "英语", "英语"),
            KnowledgePoint("english_vocabulary_core", "核心词汇", "英语", "英语", "english_vocabulary", importance=5),
            KnowledgePoint("english_reading", "阅读", "英语", "英语"),
            KnowledgePoint("english_reading_comprehension", "阅读理解", "英语", "英语", "english_reading", importance=5),
        ]
        
        # 添加所有知识点到知识库
        all_knowledge = math_knowledge + physics_knowledge + english_knowledge
        for kp in all_knowledge:
            self.knowledge_base[kp.id] = kp
    
    def add_knowledge_point(self, kp: KnowledgePoint) -> bool:
        """添加知识点到知识库"""
        if kp.id in self.knowledge_base:
            return False
        self.knowledge_base[kp.id] = kp
        return True
    
    def update_knowledge_point(self, kp: KnowledgePoint) -> bool:
        """更新知识点"""
        if kp.id not in self.knowledge_base:
            return False
        self.knowledge_base[kp.id] = kp
        return True
    
    def get_knowledge_point(self, kp_id: str) -> KnowledgePoint:
        """获取知识点"""
        return self.knowledge_base.get(kp_id)
    
    def get_knowledge_points_by_subject(self, subject: str) -> List[KnowledgePoint]:
        """获取指定学科的所有知识点"""
        return [kp for kp in self.knowledge_base.values() if kp.subject == subject]
    
    def analyze_learning_data(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析学习数据，生成知识图谱和学情报告
        
        Args:
            learning_data: 学习数据，包含学生ID、学科、题目和答案信息
            格式示例: {
                "student_id": "student_001",
                "subject": "数学",
                "learning_duration": 3600,  # 学习时长（秒）
                "questions": [
                    {
                        "id": "q001",
                        "content": "解方程：2x + 3 = 7",
                        "knowledge_points": ["math_algebra_eq_linear"],
                        "user_answer": "x = 2",
                        "correct_answer": "x = 2",
                        "is_correct": True,
                        "error_type": None,
                        "answer_time": 60  # 答题时间（秒）
                    },
                    {
                        "id": "q002",
                        "content": "解方程：x² + 2x - 3 = 0",
                        "knowledge_points": ["math_algebra_eq_quadratic"],
                        "user_answer": "x = 1",
                        "correct_answer": "x = 1 或 x = -3",
                        "is_correct": False,
                        "error_type": "incomplete_solution",
                        "answer_time": 120
                    }
                ]
            }
        
        Returns:
            包含知识盲点和知识图谱的学情报告
        """
        student_id = learning_data.get("student_id", "unknown")
        subject = learning_data.get("subject", "general")
        questions = learning_data.get("questions", [])
        learning_duration = learning_data.get("learning_duration", 0)
        
        # 提取知识盲点
        knowledge_gaps = self.extract_knowledge_gaps(questions)
        
        # 生成知识图谱
        knowledge_map = self.generate_knowledge_map(knowledge_gaps, subject, student_id)
        
        # 更新学生掌握程度
        self._update_student_mastery(student_id, subject, questions)
        
        return {
            "student_id": student_id,
            "subject": subject,
            "learning_duration": learning_duration,
            "knowledge_gaps": [
                {
                    "knowledge_point_id": gap.knowledge_point.id,
                    "knowledge_point_name": gap.knowledge_point.name,
                    "gap_reason": gap.gap_reason,
                    "error_count": gap.error_count,
                    "priority": gap.priority,
                    "related_questions": gap.related_questions
                }
                for gap in knowledge_gaps
            ],
            "knowledge_map": knowledge_map,
            "mastery_overview": self._calculate_mastery_overview(student_id, subject),
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
        related_questions_by_kp = {}
        
        # 统计每个知识点的错误次数和相关题目
        for question in questions:
            if not question.get("is_correct", False):
                for kp_id in question.get("knowledge_points", []):
                    if kp_id in error_count_by_kp:
                        error_count_by_kp[kp_id] += 1
                        related_questions_by_kp[kp_id].append(question.get("id", "unknown"))
                    else:
                        error_count_by_kp[kp_id] = 1
                        related_questions_by_kp[kp_id] = [question.get("id", "unknown")]
        
        # 生成知识盲点
        for kp_id, error_count in error_count_by_kp.items():
            if kp_id in self.knowledge_base:
                knowledge_point = self.knowledge_base[kp_id]
                
                # 确定盲点原因
                gap_reason = self._determine_gap_reason(questions, kp_id)
                
                # 计算优先级（基于错误次数、知识点重要性和掌握程度）
                priority = min(5, error_count + (5 - int(knowledge_point.mastery_level * 5)) + (knowledge_point.importance // 2))
                priority = max(1, priority)
                
                knowledge_gaps.append(KnowledgeGap(
                    knowledge_point=knowledge_point,
                    gap_reason=gap_reason,
                    error_count=error_count,
                    priority=priority,
                    related_questions=related_questions_by_kp[kp_id]
                ))
        
        # 按优先级排序，优先级高的排在前面
        knowledge_gaps.sort(key=lambda x: x.priority, reverse=True)
        
        return knowledge_gaps
    
    def _determine_gap_reason(self, questions: List[Dict[str, Any]], kp_id: str) -> str:
        """
        确定产生知识盲点的原因
        """
        error_types = []
        answer_times = []
        
        for question in questions:
            if not question.get("is_correct", False) and kp_id in question.get("knowledge_points", []):
                error_type = question.get("error_type", "unknown")
                error_types.append(error_type)
                answer_time = question.get("answer_time", 0)
                answer_times.append(answer_time)
        
        # 根据错误类型确定原因
        if not error_types:
            return "未知原因"
        
        # 统计最常见的错误类型
        from collections import Counter
        error_counter = Counter(error_types)
        most_common_error = error_counter.most_common(1)[0][0]
        
        # 计算平均答题时间
        avg_answer_time = sum(answer_times) / len(answer_times) if answer_times else 0
        
        # 综合错误类型和答题时间确定原因
        reason_map = {
            "concept_error": "概念理解错误",
            "calculation_error": "计算错误",
            "application_error": "应用错误",
            "incomplete_solution": "答案不完整",
            "misinterpretation": "题意理解错误",
            "unknown": "未知原因"
        }
        
        base_reason = reason_map.get(most_common_error, "未知原因")
        
        # 如果答题时间过长，可能是知识不熟练
        if avg_answer_time > 180:  # 超过3分钟
            return f"{base_reason}（答题时间过长，知识掌握不熟练）"
        elif avg_answer_time < 30:  # 少于30秒，可能是粗心
            return f"{base_reason}（答题时间过短，可能存在粗心问题）"
        
        return base_reason
    
    def generate_knowledge_map(self, knowledge_gaps: List[KnowledgeGap], subject: str, student_id: str) -> Dict[str, Any]:
        """
        生成知识图谱
        
        Args:
            knowledge_gaps: 知识盲点列表
            subject: 学科
            student_id: 学生ID
        
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
        
        # 确保所有学科知识点都包含
        subject_kps = self.get_knowledge_points_by_subject(subject)
        for kp in subject_kps:
            all_kps.add(kp.id)
        
        # 构建知识图谱结构
        knowledge_map = {
            "subject": subject,
            "total_topics": len(all_kps),
            "gaps_count": len(gap_kps),
            "mastery_rate": self._calculate_mastery_rate(student_id, subject),
            "priority_gaps": [
                gap.knowledge_point.name for gap in knowledge_gaps if gap.priority >= 4
            ],
            "knowledge_tree": self._build_knowledge_tree(list(all_kps), gap_kps, student_id)
        }
        
        return knowledge_map
    
    def _build_knowledge_tree(self, all_kp_ids: List[str], gap_kp_ids: Set[str], student_id: str) -> List[Dict[str, Any]]:
        """
        构建知识树结构
        
        Args:
            all_kp_ids: 所有相关知识点ID
            gap_kp_ids: 知识盲点ID集合
            student_id: 学生ID
        
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
        
        # 获取学生对各个知识点的掌握程度
        student_mastery = self.student_mastery.get(student_id, {})
        
        # 递归构建树
        def build_tree_node(kp: KnowledgePoint) -> Dict[str, Any]:
            """构建单个树节点"""
            # 获取学生掌握程度
            mastery_level = student_mastery.get(kp.id, kp.mastery_level)
            
            node = {
                "id": kp.id,
                "name": kp.name,
                "category": kp.category,
                "subject": kp.subject,
                "is_gap": kp.id in gap_kp_ids,
                "mastery_level": mastery_level,
                "importance": kp.importance,
                "children": []
            }
            
            # 添加子节点
            if kp.id in parent_map:
                for child_kp in parent_map[kp.id]:
                    node["children"].append(build_tree_node(child_kp))
            
            return node
        
        return [build_tree_node(kp) for kp in root_kps]
    
    def update_student_mastery(self, student_id: str, subject: str, mastery_data: Dict[str, float]):
        """
        更新学生知识点掌握程度
        
        Args:
            student_id: 学生ID
            subject: 学科
            mastery_data: 知识点掌握程度数据，格式为 {"知识点ID": 掌握程度(0.0-1.0)}
        """
        if student_id not in self.student_mastery:
            self.student_mastery[student_id] = {}
        
        for kp_id, mastery_level in mastery_data.items():
            # 确保掌握程度在0.0-1.0之间
            clamped_mastery = max(0.0, min(1.0, mastery_level))
            self.student_mastery[student_id][kp_id] = clamped_mastery
    
    def _calculate_mastery_rate(self, student_id: str, subject: str) -> float:
        """
        计算学生对某一学科的总体掌握率
        """
        student_mastery = self.student_mastery.get(student_id, {})
        subject_kps = self.get_knowledge_points_by_subject(subject)
        
        if not subject_kps:
            return 0.0
        
        total_mastery = 0.0
        for kp in subject_kps:
            total_mastery += student_mastery.get(kp.id, kp.mastery_level)
        
        return total_mastery / len(subject_kps)
    
    def _calculate_mastery_overview(self, student_id: str, subject: str) -> Dict[str, Any]:
        """
        计算掌握程度概览
        """
        student_mastery = self.student_mastery.get(student_id, {})
        subject_kps = self.get_knowledge_points_by_subject(subject)
        
        if not subject_kps:
            return {
                "excellent_count": 0,
                "good_count": 0,
                "average_count": 0,
                "poor_count": 0,
                "total_count": 0
            }
        
        excellent_count = 0  # 掌握程度 >= 0.8
        good_count = 0       # 0.6 <= 掌握程度 < 0.8
        average_count = 0    # 0.4 <= 掌握程度 < 0.6
        poor_count = 0       # 掌握程度 < 0.4
        
        for kp in subject_kps:
            mastery = student_mastery.get(kp.id, kp.mastery_level)
            if mastery >= 0.8:
                excellent_count += 1
            elif mastery >= 0.6:
                good_count += 1
            elif mastery >= 0.4:
                average_count += 1
            else:
                poor_count += 1
        
        return {
            "excellent_count": excellent_count,
            "good_count": good_count,
            "average_count": average_count,
            "poor_count": poor_count,
            "total_count": len(subject_kps)
        }
    
    def _update_student_mastery(self, student_id: str, subject: str, questions: List[Dict[str, Any]]):
        """
        根据答题情况更新学生掌握程度
        """
        if student_id not in self.student_mastery:
            self.student_mastery[student_id] = {}
        
        # 计算每个知识点的掌握程度变化
        mastery_changes = {}
        for question in questions:
            is_correct = question.get("is_correct", False)
            for kp_id in question.get("knowledge_points", []):
                if kp_id not in mastery_changes:
                    mastery_changes[kp_id] = []
                mastery_changes[kp_id].append(1.0 if is_correct else 0.0)
        
        # 更新掌握程度
        for kp_id, scores in mastery_changes.items():
            if kp_id in self.knowledge_base:
                # 计算平均得分
                avg_score = sum(scores) / len(scores)
                
                # 计算新的掌握程度（使用加权平均，当前掌握程度占70%，新得分占30%）
                current_mastery = self.student_mastery[student_id].get(kp_id, 0.5)
                new_mastery = current_mastery * 0.7 + avg_score * 0.3
                
                # 确保在0.0-1.0之间
                clamped_mastery = max(0.0, min(1.0, new_mastery))
                self.student_mastery[student_id][kp_id] = clamped_mastery
    
    def get_related_knowledge_points(self, kp_id: str, depth: int = 2) -> List[KnowledgePoint]:
        """
        获取相关知识点（父节点、子节点等）
        
        Args:
            kp_id: 知识点ID
            depth: 搜索深度
        
        Returns:
            List[KnowledgePoint]: 相关知识点列表
        """
        if kp_id not in self.knowledge_base:
            return []
        
        related_kp_ids = set()
        
        # 获取当前知识点
        current_kp = self.knowledge_base[kp_id]
        related_kp_ids.add(current_kp.id)
        
        # 获取父节点链
        parent_kp = current_kp
        for _ in range(depth):
            if parent_kp.parent_id and parent_kp.parent_id in self.knowledge_base:
                parent_kp = self.knowledge_base[parent_kp.parent_id]
                related_kp_ids.add(parent_kp.id)
            else:
                break
        
        # 获取子节点树
        def get_children(kp, current_depth):
            if current_depth >= depth:
                return
            for child_kp in self.knowledge_base.values():
                if child_kp.parent_id == kp.id:
                    related_kp_ids.add(child_kp.id)
                    get_children(child_kp, current_depth + 1)
        
        get_children(current_kp, 0)
        
        # 将ID转换为知识点对象
        return [self.knowledge_base[kp_id] for kp_id in related_kp_ids]


# 创建Mod实例供外部使用
knowledge_graph_mod = KnowledgeGraphMod()


# 导出Mod的主要功能
def analyze_learning_data(learning_data: Dict[str, Any]) -> Dict[str, Any]:
    """分析学习数据，生成知识图谱和学情报告"""
    return knowledge_graph_mod.analyze_learning_data(learning_data)


def update_student_mastery(student_id: str, subject: str, mastery_data: Dict[str, float]):
    """更新学生知识点掌握程度"""
    return knowledge_graph_mod.update_student_mastery(student_id, subject, mastery_data)


def get_related_knowledge_points(kp_id: str, depth: int = 2) -> List[Dict[str, Any]]:
    """获取相关知识点"""
    related_kps = knowledge_graph_mod.get_related_knowledge_points(kp_id, depth)
    return [
        {
            "id": kp.id,
            "name": kp.name,
            "category": kp.category,
            "subject": kp.subject,
            "parent_id": kp.parent_id,
            "importance": kp.importance
        }
        for kp in related_kps
    ]


def get_knowledge_points_by_subject(subject: str) -> List[Dict[str, Any]]:
    """获取指定学科的所有知识点"""
    kps = knowledge_graph_mod.get_knowledge_points_by_subject(subject)
    return [
        {
            "id": kp.id,
            "name": kp.name,
            "category": kp.category,
            "subject": kp.subject,
            "parent_id": kp.parent_id,
            "importance": kp.importance
        }
        for kp in kps
    ]