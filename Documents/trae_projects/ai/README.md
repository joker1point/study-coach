# 智能学习助手网络 (Learning Assistant Network)

一个基于OpenAgents框架构建的智能学习系统，通过多智能体协作提供个性化、高效的学习体验。

## 🌟 核心功能

### 1. 多智能体协作系统
- **学习助手智能体**: 协调复杂学习任务，管理智能体间的协作流程
- **学习分析智能体**: 分析学习数据，识别知识缺口，提供个性化学习建议
- **资源匹配智能体**: 根据学习需求和偏好匹配最优学习资源
- **练习优化智能体**: 生成个性化练习，强化知识掌握

### 2. 个性化学习路径
- 基于学习风格、速度和表现动态生成学习路径
- 考虑知识点之间的依赖关系，确保学习逻辑连贯性
- 实时调整学习路径，适应学习进度和理解程度的变化

### 3. 智能资源管理
- 支持多种资源类型：视频、文档、练习、互动实验等
- 基于学习表现趋势选择最合适的资源类型
- 动态调整资源难度和呈现方式

### 4. 实时监控与可视化
- 学习进度实时追踪和可视化展示
- 表现趋势分析图表
- 资源使用统计
- 系统健康监控仪表盘

### 5. 任务管理与协作
- 支持复杂任务的分解和分配
- 任务依赖管理，确保正确的执行顺序
- 智能体间的异步协作机制

## 📦 项目结构

```
my_first_network/
├── agents/             # 智能体实现
│   ├── learning_assistant_agent.py      # 学习助手智能体
│   ├── learning_analysis_agent.py       # 学习分析智能体
│   ├── resource_matching_agent.py       # 资源匹配智能体
│   ├── exercise_optimization_agent.py   # 练习优化智能体
│   └── ...                               # 其他智能体
├── tools/              # 工具模块
│   ├── task_manager.py         # 任务管理工具
│   ├── visualization_tools.py  # 可视化工具
│   ├── resource_tools.py       # 资源管理工具
│   └── ...                     # 其他工具
├── mods/               # 核心模块
│   ├── openagents.mods.core.shared_cache/   # 共享缓存模块
│   ├── openagents.mods.workspace.messaging/ # 消息系统模块
│   └── ...                                   # 其他模块
├── events/             # 事件定义
├── network.yaml        # 网络配置
├── demo_*.py           # 演示脚本
├── sample_*.json       # 示例数据
├── start_network.bat   # 网络启动脚本
└── README.md           # 项目说明文档
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip包管理器

### 安装与启动

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **启动网络**
   ```bash
   # Windows
   start_network.bat
   
   # Linux/Mac
   python -m openagents.network start
   ```

3. **运行演示**
   ```bash
   python demo_simple.py          # 基础功能演示
   python demo_learning_path.py   # 学习路径生成演示
   python demo_enhanced_features.py # 增强功能演示
   ```

## 🎯 核心智能体

### 学习助手智能体 (Learning Assistant Agent)
作为系统的协调者，负责：
- 接收和解析用户请求
- 分解复杂任务为子任务
- 分配任务给专业智能体
- 整合和呈现最终结果

### 学习分析智能体 (Learning Analysis Agent)
负责学习数据的深度分析：
- 识别知识缺口和薄弱环节
- 分析学习表现趋势
- 计算学习风格和速度
- 提供个性化学习建议

### 资源匹配智能体 (Resource Matching Agent)
智能匹配学习资源：
- 基于学习需求选择资源类型
- 考虑学习风格和偏好
- 支持多种资源来源
- 动态调整资源推荐

### 练习优化智能体 (Exercise Optimization Agent)
生成个性化练习：
- 根据知识掌握程度调整难度
- 提供针对性的练习内容
- 支持多种练习形式
- 跟踪练习表现

## 🛠️ 工具模块

### 任务管理工具 (Task Manager)
提供任务创建、分配和跟踪功能：
- 支持任务优先级设置
- 管理任务依赖关系
- 实现任务重试机制
- 提供任务状态监控

### 可视化工具 (Visualization Tools)
生成学习相关的可视化内容：
- 学习路径图表
- 表现趋势分析
- 资源使用统计
- 实时监控仪表盘

## 📊 数据格式

系统使用JSON格式存储和交换数据：

### 学习数据示例
```json
{
  "student_id": "student_001",
  "knowledge_points": [
    {
      "id": "kp_001",
      "name": "一元一次方程",
      "mastery_level": 0.75,
      "practice_count": 25,
      "accuracy": 0.82
    }
  ],
  "learning_style": "visual",
  "learning_speed": "medium"
}
```

## 🎨 可视化界面

系统提供多种可视化界面：
- `learning_path_visualization.html`: 学习路径可视化
- `learning_progress_visualization.html`: 学习进度展示
- `knowledge_map_visualization.html`: 知识图谱可视化
- `index.html`: 主可视化仪表盘

## 📚 使用指南

### 1. 基本学习流程
1. 用户提出学习需求
2. 学习助手智能体接收并解析请求
3. 分配任务给专业智能体
4. 智能体协作完成任务
5. 返回整合的学习建议和资源

### 2. 个性化学习路径生成
```python
# 示例代码：生成个性化学习路径
from agents.learning_analysis_agent import LearningAnalysisAgent

analysis_agent = LearningAnalysisAgent()
learning_path = analysis_agent.generate_personalized_path(
    learning_data=student_data,
    target_knowledge_points=["kp_001", "kp_002"]
)
```

### 3. 资源匹配
```python
# 示例代码：匹配学习资源
from agents.resource_matching_agent import ResourceMatchingAgent

resource_agent = ResourceMatchingAgent()
resources = resource_agent.match_resources(
    topic="一元一次方程",
    learning_style="visual",
    knowledge_gaps=[{"id": "kp_001", "mastery_level": 0.6}]
)
```

## 🔧 配置说明

### 网络配置 (network.yaml)
- 设置网络名称、模式和节点ID
- 配置HTTP/GRPC通信端口
- 启用和配置核心模块
- 设置消息系统参数

### LLM配置 (llm_config.py)
- 配置语言模型提供商
- 设置API密钥和端点
- 调整模型参数

## 📈 性能优化

1. **异步处理**: 使用asyncio实现高效的并发任务处理
2. **缓存机制**: 缓存频繁访问的学习数据和资源
3. **任务优先级**: 基于优先级调度任务执行
4. **资源池**: 管理智能体实例，避免频繁创建销毁

## 🤝 贡献指南

我们欢迎社区贡献！请按照以下步骤：

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目邮箱: learning-assistant-network@example.com
- 问题反馈: [GitHub Issues](https://github.com/yourusername/learning-assistant-network/issues)

## 📋 更新日志

### v1.0.0 (2025-12-29)
- 初始版本发布
- 实现核心智能体系统
- 支持个性化学习路径生成
- 提供基础可视化功能
- 实现任务管理和协作机制

---

**智能学习助手网络** - 让学习更智能，更高效！ 🚀
