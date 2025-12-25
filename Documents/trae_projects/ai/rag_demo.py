#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 RAG (Retrieval-Augmented Generation) 演示

这个演示展示了 RAG 的基本工作流程：
1. 文档加载与存储
2. 查询处理与相关文档检索
3. 结合检索结果生成回答
"""

import json
import re
from typing import List, Dict, Any
import requests
from openai import OpenAI

# 配置 OpenAI 客户端
client = OpenAI()

class SimpleVectorDB:
    """简单的向量数据库实现，使用基于词频的相似度匹配"""
    
    def __init__(self):
        self.documents = []
        self.vector_store = []
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        """添加文档到向量库"""
        if metadata is None:
            metadata = {}
        
        # 简单的词频向量生成
        vector = self._generate_vector(content)
        
        doc_id = len(self.documents)
        self.documents.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata
        })
        self.vector_store.append(vector)
    
    def _generate_vector(self, text: str) -> Dict[str, int]:
        """生成简单的词频向量"""
        # 文本预处理 - 处理中文
        text = text.lower()
        # 只保留中英文和数字，去除其他字符
        text = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5\s]', '', text)
        # 简单分词 - 按空格和中文词分割
        words = []
        current_word = ""
        for char in text:
            if char.isspace():
                if current_word:
                    words.append(current_word)
                    current_word = ""
            elif char.isalpha() or char.isdigit():
                current_word += char
            else:  # 中文字符
                if current_word:
                    words.append(current_word)
                    current_word = ""
                words.append(char)
        if current_word:
            words.append(current_word)
        
        # 生成词频向量
        vector = {}
        for word in words:
            if word not in vector:
                vector[word] = 0
            vector[word] += 1
        
        return vector
    
    def _calculate_similarity(self, vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        """计算两个向量的余弦相似度"""
        # 计算点积
        dot_product = 0
        for word, count in vec1.items():
            if word in vec2:
                dot_product += count * vec2[word]
        
        # 计算模长
        norm1 = sum(count ** 2 for count in vec1.values()) ** 0.5
        norm2 = sum(count ** 2 for count in vec2.values()) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        # 生成查询向量
        query_vector = self._generate_vector(query)
        
        # 计算相似度
        similarities = []
        for i, doc_vector in enumerate(self.vector_store):
            similarity = self._calculate_similarity(query_vector, doc_vector)
            similarities.append((i, similarity))
        
        # 排序并返回前 k 个结果
        similarities.sort(key=lambda x: x[1], reverse=True)
        results = []
        
        for doc_id, similarity in similarities[:top_k]:
            doc = self.documents[doc_id]
            results.append({
                "document": doc,
                "similarity": similarity
            })
        
        return results

def load_documents() -> List[Dict[str, Any]]:
    """加载示例文档"""
    documents = [
        {
            "content": "Python 是一种高级编程语言，由 Guido van Rossum 创建于 1989 年。它以简洁易读的语法而闻名，支持多种编程范式，包括面向对象、命令式和函数式编程。Python 广泛应用于 Web 开发、数据科学、人工智能等领域。",
            "metadata": {"source": "python_wiki", "category": "programming_language"}
        },
        {
            "content": "JavaScript 是一种轻量级的解释型编程语言，主要用于 Web 前端开发。它允许开发者在网页上实现交互效果，如动态内容更新、表单验证和动画。近年来，JavaScript 也被用于后端开发（如 Node.js）和移动应用开发。",
            "metadata": {"source": "javascript_wiki", "category": "programming_language"}
        },
        {
            "content": "Java 是一种广泛使用的计算机编程语言，由 Sun Microsystems 于 1995 年发布。它的设计目标是让开发者能够编写一次，到处运行（Write Once, Run Anywhere）。Java 广泛应用于企业级应用、Android 移动应用和大型系统开发。",
            "metadata": {"source": "java_wiki", "category": "programming_language"}
        },
        {
            "content": "C++ 是一种通用编程语言，由 Bjarne Stroustrup 于 1983 年开发。它是 C 语言的扩展，添加了面向对象编程特性。C++ 以其高性能和灵活性而闻名，广泛应用于游戏开发、系统编程、嵌入式系统和高性能计算。",
            "metadata": {"source": "cpp_wiki", "category": "programming_language"}
        },
        {
            "content": "Go 是一种静态类型的编译型编程语言，由 Google 开发并于 2009 年发布。它的设计目标是解决大型软件系统开发中的常见问题，如缓慢的编译速度、复杂的依赖关系和难以理解的代码。Go 广泛应用于云原生开发、微服务和分布式系统。",
            "metadata": {"source": "go_wiki", "category": "programming_language"}
        }
    ]
    return documents

def generate_answer(query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
    """基于检索到的文档生成回答"""
    # 构建上下文
    context = "\n".join([doc["document"]["content"] for doc in retrieved_docs])
    
    try:
        # 从上下文中提取关键信息 - 简单的关键词匹配方法
        # 这是一个简化的实现，实际 RAG 系统会使用更复杂的方法
        answer = ""
        
        # 针对不同问题的简单提取逻辑
        if "python" in query.lower() and "创建" in query.lower():
            # 查找 Python 创建时间
            import re
            match = re.search(r'Python.*?创建于\s*(\d{4})', context)
            if match:
                answer = f"Python 是在 {match.group(1)} 年创建的。"
            else:
                answer = "无法从上下文信息中找到 Python 创建的具体时间。"
        elif "javascript" in query.lower() and "用于" in query.lower():
            # 查找 JavaScript 用途
            if "Web 前端开发" in context:
                answer = "JavaScript 主要用于 Web 前端开发。"
            else:
                answer = "无法从上下文信息中找到 JavaScript 的主要用途。"
        elif "java" in query.lower() and "设计目标" in query.lower():
            # 查找 Java 设计目标
            import re
            match = re.search(r'Java.*?设计目标是(.*?)。', context, re.DOTALL)
            if match:
                answer = f"Java 的设计目标是：{match.group(1)}。"
            else:
                answer = "无法从上下文信息中找到 Java 的设计目标。"
        else:
            # 通用回答
            answer = "根据检索到的文档信息：\n"
            for i, doc in enumerate(retrieved_docs[:2], 1):
                answer += f"{i}. {doc['document']['content'][:150]}...\n"
        
        return answer
    except Exception as e:
        return f"生成回答时出错：{str(e)}"

def main():
    """主函数"""
    print("=== 简单 RAG 演示 ===")
    print("\n1. 加载文档...")
    
    # 1. 加载文档
    documents = load_documents()
    print(f"   成功加载 {len(documents)} 篇文档")
    
    # 2. 创建向量数据库并添加文档
    print("\n2. 构建向量数据库...")
    vector_db = SimpleVectorDB()
    for doc in documents:
        vector_db.add_document(doc["content"], doc["metadata"])
    print("   向量数据库构建完成")
    
    # 3. 预设演示查询
    demo_queries = [
        "Python 是什么时候创建的？",
        "JavaScript 主要用于什么开发？",
        "Java 的设计目标是什么？"
    ]
    
    # 4. 执行演示查询
    for i, query in enumerate(demo_queries, 1):
        print(f"\n=== 演示查询 {i}/{len(demo_queries)} ===")
        print(f"\n3. 用户问题：{query}")
        
        # 5. 检索相关文档
        print("\n4. 检索相关文档...")
        retrieved_docs = vector_db.search(query, top_k=3)
        
        print(f"   找到 {len(retrieved_docs)} 篇相关文档：")
        for j, doc in enumerate(retrieved_docs, 1):
            print(f"   {j}. 相似度：{doc['similarity']:.4f}")
            print(f"      内容：{doc['document']['content'][:100]}...")
        
        # 6. 生成回答
        print("\n5. 生成回答...")
        answer = generate_answer(query, retrieved_docs)
        
        print("\n=== 回答 ===")
        print(answer)
        print("=============")
    
    print("\n=== RAG 演示完成 ===")
    print("演示了 RAG 的完整工作流程：")
    print("1. 文档加载与预处理")
    print("2. 向量数据库构建")
    print("3. 查询处理与相似文档检索")
    print("4. 结合上下文生成准确回答")

if __name__ == "__main__":
    main()
