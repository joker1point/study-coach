"""
学习资源库Mod - 提供学习资源的管理、检索和匹配功能
"""

from typing import Dict, List, Set, Any, Tuple
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LearningResource:
    """学习资源数据结构"""
    id: str
    title: str
    type: str  # 资源类型：课件、微课、习题、文档等
    subject: str  # 学科
    difficulty: str  # 难度：简单、中等、困难
    knowledge_points: List[str]  # 关联的知识点ID列表
    url: str  # 资源URL或路径
    duration: int = 0  # 时长（秒），仅适用于视频/音频资源
    size: str = ""  # 文件大小，例如："10MB"
    description: str = ""  # 资源描述
    upload_time: str = None  # 上传时间
    usage_count: int = 0  # 使用次数
    rating: float = 0.0  # 评分（0.0-5.0）


class LearningResourceMod:
    """学习资源库Mod的核心实现"""
    
    def __init__(self):
        self.resource库 = {}  # 存储所有学习资源
        self.resource_by_knowledge_point = {}  # 按知识点索引资源
        self.resource_by_subject = {}  # 按学科索引资源
        self._load_default_resources()
    
    def _load_default_resources(self):
        """加载默认的学习资源"""
        # 数学资源
        math_resources = [
            LearningResource(
                id="math_res_001",
                title="一元一次方程详解",
                type="微课",
                subject="数学",
                difficulty="简单",
                knowledge_points=["math_algebra_eq_linear"],
                url="https://example.com/videos/math_algebra_eq_linear.mp4",
                duration=600,
                size="50MB",
                description="详细讲解一元一次方程的概念、解法和应用",
                upload_time="2025-01-15T10:00:00",
                usage_count=156,
                rating=4.8
            ),
            LearningResource(
                id="math_res_002",
                title="一元二次方程解法专题",
                type="课件",
                subject="数学",
                difficulty="中等",
                knowledge_points=["math_algebra_eq_quadratic"],
                url="https://example.com/docs/math_algebra_eq_quadratic.pdf",
                size="2MB",
                description="包含一元二次方程的多种解法：因式分解法、配方法、公式法",
                upload_time="2025-01-20T14:30:00",
                usage_count=234,
                rating=4.9
            ),
            LearningResource(
                id="math_res_003",
                title="三角形面积计算练习",
                type="习题",
                subject="数学",
                difficulty="中等",
                knowledge_points=["math_geometry_triangle_area"],
                url="https://example.com/exercises/math_geometry_triangle_area.html",
                description="包含20道三角形面积计算练习题，从基础到进阶",
                upload_time="2025-02-01T09:15:00",
                usage_count=189,
                rating=4.7
            ),
            LearningResource(
                id="math_res_004",
                title="圆的性质与应用",
                type="微课",
                subject="数学",
                difficulty="困难",
                knowledge_points=["math_geometry_circle"],
                url="https://example.com/videos/math_geometry_circle.mp4",
                duration=900,
                size="75MB",
                description="深入讲解圆的基本性质、定理及其在几何问题中的应用",
                upload_time="2025-02-10T16:45:00",
                usage_count=123,
                rating=4.6
            )
        ]
        
        # 物理资源
        physics_resources = [
            LearningResource(
                id="physics_res_001",
                title="牛顿三大定律入门",
                type="微课",
                subject="物理",
                difficulty="简单",
                knowledge_points=["physics_mechanics_newton"],
                url="https://example.com/videos/physics_mechanics_newton.mp4",
                duration=720,
                size="60MB",
                description="生动讲解牛顿三大定律的基本概念和应用实例",
                upload_time="2025-03-05T11:20:00",
                usage_count=198,
                rating=4.9
            ),
            LearningResource(
                id="physics_res_002",
                title="功和能知识点总结",
                type="文档",
                subject="物理",
                difficulty="中等",
                knowledge_points=["physics_mechanics_work"],
                url="https://example.com/docs/physics_mechanics_work.docx",
                size="1.5MB",
                description="功和能的知识点总结，包含公式推导和典型例题",
                upload_time="2025-03-15T13:50:00",
                usage_count=167,
                rating=4.7
            )
        ]
        
        # 英语资源
        english_resources = [
            LearningResource(
                id="english_res_001",
                title="英语时态详解",
                type="微课",
                subject="英语",
                difficulty="中等",
                knowledge_points=["english_grammar_tenses"],
                url="https://example.com/videos/english_grammar_tenses.mp4",
                duration=840,
                size="70MB",
                description="详细讲解英语16种时态的构成和用法",
                upload_time="2025-04-01T10:30:00",
                usage_count=256,
                rating=4.8
            ),
            LearningResource(
                id="english_res_002",
                title="核心词汇记忆技巧",
                type="课件",
                subject="英语",
                difficulty="简单",
                knowledge_points=["english_vocabulary_core"],
                url="https://example.com/docs/english_vocabulary_core.pdf",
                size="3MB",
                description="高效记忆英语核心词汇的方法和技巧",
                upload_time="2025-04-10T15:20:00",
                usage_count=312,
                rating=4.9
            )
        ]
        
        # 添加所有资源到资源库
        all_resources = math_resources + physics_resources + english_resources
        for resource in all_resources:
            self.add_resource(resource)
    
    def add_resource(self, resource: LearningResource) -> bool:
        """
        添加学习资源
        
        Args:
            resource: 学习资源对象
        
        Returns:
            bool: 添加成功返回True，否则返回False
        """
        if resource.id in self.resource库:
            return False
        
        # 添加到资源库
        self.resource库[resource.id] = resource
        
        # 更新知识点索引
        for kp_id in resource.knowledge_points:
            if kp_id not in self.resource_by_knowledge_point:
                self.resource_by_knowledge_point[kp_id] = []
            self.resource_by_knowledge_point[kp_id].append(resource.id)
        
        # 更新学科索引
        if resource.subject not in self.resource_by_subject:
            self.resource_by_subject[resource.subject] = []
        self.resource_by_subject[resource.subject].append(resource.id)
        
        return True
    
    def update_resource(self, resource: LearningResource) -> bool:
        """
        更新学习资源
        
        Args:
            resource: 学习资源对象
        
        Returns:
            bool: 更新成功返回True，否则返回False
        """
        if resource.id not in self.resource库:
            return False
        
        # 获取旧资源
        old_resource = self.resource库[resource.id]
        
        # 删除旧的知识点索引
        for kp_id in old_resource.knowledge_points:
            if kp_id in self.resource_by_knowledge_point:
                self.resource_by_knowledge_point[kp_id].remove(resource.id)
                if not self.resource_by_knowledge_point[kp_id]:
                    del self.resource_by_knowledge_point[kp_id]
        
        # 更新资源库
        self.resource库[resource.id] = resource
        
        # 更新知识点索引
        for kp_id in resource.knowledge_points:
            if kp_id not in self.resource_by_knowledge_point:
                self.resource_by_knowledge_point[kp_id] = []
            self.resource_by_knowledge_point[kp_id].append(resource.id)
        
        return True
    
    def delete_resource(self, resource_id: str) -> bool:
        """
        删除学习资源
        
        Args:
            resource_id: 资源ID
        
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        if resource_id not in self.resource库:
            return False
        
        # 获取资源
        resource = self.resource库[resource_id]
        
        # 删除知识点索引
        for kp_id in resource.knowledge_points:
            if kp_id in self.resource_by_knowledge_point:
                self.resource_by_knowledge_point[kp_id].remove(resource_id)
                if not self.resource_by_knowledge_point[kp_id]:
                    del self.resource_by_knowledge_point[kp_id]
        
        # 删除学科索引
        if resource.subject in self.resource_by_subject:
            self.resource_by_subject[resource.subject].remove(resource_id)
            if not self.resource_by_subject[resource.subject]:
                del self.resource_by_subject[resource.subject]
        
        # 删除资源库中的资源
        del self.resource库[resource_id]
        
        return True
    
    def get_resource(self, resource_id: str) -> LearningResource:
        """
        获取学习资源
        
        Args:
            resource_id: 资源ID
        
        Returns:
            LearningResource: 资源对象，不存在返回None
        """
        return self.resource库.get(resource_id)
    
    def search_resources(self, **kwargs) -> List[LearningResource]:
        """
        搜索学习资源
        
        Args:
            kwargs: 搜索条件，包括：
                knowledge_points: 知识点ID列表
                subject: 学科
                difficulty: 难度
                type: 资源类型
                keyword: 标题或描述中的关键词
        
        Returns:
            List[LearningResource]: 匹配的资源列表
        """
        results = []
        
        # 遍历所有资源，检查是否匹配搜索条件
        for resource in self.resource库.values():
            match = True
            
            # 检查知识点
            if 'knowledge_points' in kwargs and kwargs['knowledge_points']:
                kp_match = any(kp in resource.knowledge_points for kp in kwargs['knowledge_points'])
                if not kp_match:
                    match = False
            
            # 检查学科
            if 'subject' in kwargs and kwargs['subject'] and resource.subject != kwargs['subject']:
                match = False
            
            # 检查难度
            if 'difficulty' in kwargs and kwargs['difficulty'] and resource.difficulty != kwargs['difficulty']:
                match = False
            
            # 检查资源类型
            if 'type' in kwargs and kwargs['type'] and resource.type != kwargs['type']:
                match = False
            
            # 检查关键词
            if 'keyword' in kwargs and kwargs['keyword']:
                keyword = kwargs['keyword'].lower()
                if keyword not in resource.title.lower() and keyword not in resource.description.lower():
                    match = False
            
            if match:
                results.append(resource)
        
        return results
    
    def match_resources(self,学情报告: Dict[str, Any], resource_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        根据学情报告匹配合适的学习资源
        
        Args:
            学情报告: 包含知识盲点和掌握程度的学情报告
            resource_types: 希望匹配的资源类型列表，None表示匹配所有类型
        
        Returns:
            List[Dict[str, Any]]: 匹配的资源列表，包含资源信息和匹配度
        """
        matched_resources = []
        
        # 提取知识盲点
        knowledge_gaps = 学情报告.get('knowledge_gaps', [])
        subject = 学情报告.get('subject', '')
        
        if not knowledge_gaps:
            return []
        
        # 为每个知识盲点匹配资源
        for gap in knowledge_gaps:
            kp_id = gap.get('knowledge_point_id', '')
            priority = gap.get('priority', 1)
            
            # 获取该知识点相关的资源
            resources = self.search_resources(
                knowledge_points=[kp_id],
                subject=subject,
                type=resource_types[0] if resource_types else None
            )
            
            # 计算资源匹配度
            for resource in resources:
                # 匹配度基于优先级和资源难度
                difficulty_weights = {
                    '简单': 1.0,
                    '中等': 1.5,
                    '困难': 2.0
                }
                
                # 根据资源类型调整权重
                type_weights = {
                    '微课': 1.2,
                    '课件': 1.0,
                    '习题': 1.5,
                    '文档': 0.8
                }
                
                # 计算匹配度
                match_score = priority * 0.5
                match_score += difficulty_weights.get(resource.difficulty, 1.0) * 0.3
                match_score += type_weights.get(resource.type, 1.0) * 0.2
                
                # 添加到匹配结果
                matched_resources.append({
                    'resource': self._resource_to_dict(resource),
                    'knowledge_gap': gap,
                    'match_score': round(match_score, 2),
                    'priority': priority
                })
        
        # 按匹配度和优先级排序
        matched_resources.sort(key=lambda x: (x['priority'], x['match_score']), reverse=True)
        
        # 去重，每个资源只返回一次，保留匹配度最高的
        unique_resources = {}
        for item in matched_resources:
            res_id = item['resource']['id']
            if res_id not in unique_resources or item['match_score'] > unique_resources[res_id]['match_score']:
                unique_resources[res_id] = item
        
        # 返回结果
        return list(unique_resources.values())
    
    def recommend_resources(self, student_id: str, subject: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        推荐学习资源
        
        Args:
            student_id: 学生ID
            subject: 学科
            count: 推荐资源数量
        
        Returns:
            List[Dict[str, Any]]: 推荐的资源列表
        """
        # 这里可以实现基于学生历史学习数据的个性化推荐
        # 目前简化实现，返回该学科评分最高的资源
        
        resources = self.search_resources(subject=subject)
        # 按评分和使用次数排序
        resources.sort(key=lambda x: (x.rating, x.usage_count), reverse=True)
        
        return [self._resource_to_dict(res) for res in resources[:count]]
    
    def _resource_to_dict(self, resource: LearningResource) -> Dict[str, Any]:
        """
        将资源对象转换为字典
        
        Args:
            resource: 资源对象
        
        Returns:
            Dict[str, Any]: 资源字典
        """
        return {
            'id': resource.id,
            'title': resource.title,
            'type': resource.type,
            'subject': resource.subject,
            'difficulty': resource.difficulty,
            'knowledge_points': resource.knowledge_points,
            'url': resource.url,
            'duration': resource.duration,
            'size': resource.size,
            'description': resource.description,
            'upload_time': resource.upload_time,
            'usage_count': resource.usage_count,
            'rating': resource.rating
        }
    
    def get_resources_by_subject(self, subject: str, resource_type: str = None) -> List[Dict[str, Any]]:
        """
        获取指定学科的资源
        
        Args:
            subject: 学科
            resource_type: 资源类型，None表示所有类型
        
        Returns:
            List[Dict[str, Any]]: 资源列表
        """
        resources = self.search_resources(subject=subject, type=resource_type)
        return [self._resource_to_dict(res) for res in resources]
    
    def get_resources_by_knowledge_point(self, kp_id: str) -> List[Dict[str, Any]]:
        """
        获取指定知识点的资源
        
        Args:
            kp_id: 知识点ID
        
        Returns:
            List[Dict[str, Any]]: 资源列表
        """
        resources = self.search_resources(knowledge_points=[kp_id])
        return [self._resource_to_dict(res) for res in resources]
    
    def increment_resource_usage(self, resource_id: str) -> bool:
        """
        增加资源使用次数
        
        Args:
            resource_id: 资源ID
        
        Returns:
            bool: 成功返回True，否则返回False
        """
        if resource_id not in self.resource库:
            return False
        
        self.resource库[resource_id].usage_count += 1
        return True
    
    def update_resource_rating(self, resource_id: str, rating: float) -> bool:
        """
        更新资源评分
        
        Args:
            resource_id: 资源ID
            rating: 新评分（0.0-5.0）
        
        Returns:
            bool: 成功返回True，否则返回False
        """
        if resource_id not in self.resource库:
            return False
        
        # 这里可以实现更复杂的评分计算逻辑，比如加权平均
        # 目前简化实现，直接更新评分
        self.resource库[resource_id].rating = max(0.0, min(5.0, rating))
        return True


# 创建Mod实例供外部使用
learning_resource_mod = LearningResourceMod()


# 导出Mod的主要功能
def add_resource(resource_data: Dict[str, Any]) -> bool:
    """
    添加学习资源
    
    Args:
        resource_data: 资源数据字典
    
    Returns:
        bool: 添加成功返回True，否则返回False
    """
    resource = LearningResource(
        id=resource_data.get('id', ''),
        title=resource_data.get('title', ''),
        type=resource_data.get('type', ''),
        subject=resource_data.get('subject', ''),
        difficulty=resource_data.get('difficulty', '简单'),
        knowledge_points=resource_data.get('knowledge_points', []),
        url=resource_data.get('url', ''),
        duration=resource_data.get('duration', 0),
        size=resource_data.get('size', ''),
        description=resource_data.get('description', ''),
        upload_time=resource_data.get('upload_time', datetime.now().isoformat()),
        usage_count=resource_data.get('usage_count', 0),
        rating=resource_data.get('rating', 0.0)
    )
    return learning_resource_mod.add_resource(resource)


def match_resources(learning_analysis: Dict[str, Any], resource_types: List[str] = None) -> List[Dict[str, Any]]:
    """
    根据学情报告匹配学习资源
    
    Args:
        learning_analysis: 学情报告
        resource_types: 资源类型列表
    
    Returns:
        List[Dict[str, Any]]: 匹配的资源列表
    """
    return learning_resource_mod.match_resources(learning_analysis, resource_types)


def recommend_resources(student_id: str, subject: str, count: int = 5) -> List[Dict[str, Any]]:
    """
    推荐学习资源
    
    Args:
        student_id: 学生ID
        subject: 学科
        count: 推荐数量
    
    Returns:
        List[Dict[str, Any]]: 推荐资源列表
    """
    return learning_resource_mod.recommend_resources(student_id, subject, count)


def get_resources_by_knowledge_point(kp_id: str) -> List[Dict[str, Any]]:
    """
    获取指定知识点的资源
    
    Args:
        kp_id: 知识点ID
    
    Returns:
        List[Dict[str, Any]]: 资源列表
    """
    return learning_resource_mod.get_resources_by_knowledge_point(kp_id)


def get_resources_by_subject(subject: str, resource_type: str = None) -> List[Dict[str, Any]]:
    """
    获取指定学科的资源
    
    Args:
        subject: 学科
        resource_type: 资源类型
    
    Returns:
        List[Dict[str, Any]]: 资源列表
    """
    return learning_resource_mod.get_resources_by_subject(subject, resource_type)
