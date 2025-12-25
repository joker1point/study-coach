# 智能学习辅助系统

## 系统简介

智能学习辅助系统是一个基于本地大语言模型（Ollama）和多代理协作网络构建的智能教育辅助平台。该系统提供了丰富的学习分析、资源匹配、练习优化和学习指导功能，旨在帮助用户实现个性化、高效的学习体验。

## 系统架构

### 核心组件

1. **本地模型API服务**
   - 基于FastAPI构建的Ollama模型接口服务
   - 提供与OpenAI兼容的API接口
   - 支持普通调用和流式响应

2. **智能学习网络**
   - 多代理协作网络架构
   - 支持HTTP和gRPC通信协议
   - 内置消息传递和缓存机制

3. **学习辅助代理**
   - 学习分析代理：分析学习模式和进展
   - 练习优化代理：生成和优化学习练习
   - 资源匹配代理：匹配个性化学习资源
   - 学习辅导代理：提供个性化学习指导
   - 诊断代理：评估学习效果和知识掌握情况

### 目录结构

```
ai/
├── learning_assistant_network/   # 学习辅助网络主目录
│   ├── agents/                   # 网络代理定义
│   ├── mods/                     # 网络模块
│   └── network.yaml              # 网络配置
├── my_first_network/            # 示例网络
│   ├── agents/                  # 自定义代理
│   ├── llm_config.py            # LLM配置
│   └── network.yaml             # 网络配置
├── main.py                      # 本地模型API服务入口
├── model_router.py              # 模型路由定义
├── requirements.txt             # 依赖列表
└── ...                          # 其他配置和文档文件
```

## 核心功能

### 1. 本地模型服务

- 提供基于Ollama的本地大语言模型服务
- 兼容OpenAI API接口格式
- 支持多模型切换（默认使用qwen:7b）
- 提供实时健康检查功能

### 2. 学习分析功能

- 分析学习行为和模式
- 识别学习优势和不足
- 生成个性化学习报告
- 提供学习建议和优化方向

### 3. 资源匹配功能

- 根据学习需求匹配相关资源
- 支持多类型学习资源推荐
- 实现资源智能分类和筛选
- 提供资源质量评估

### 4. 练习优化功能

- 生成个性化练习题目
- 根据学习进度调整难度
- 提供即时反馈和解析
- 实现练习效果跟踪

### 5. 智能辅导功能

- 提供个性化学习指导
- 解答学习疑问
- 辅助解决学习难题
- 提供学习策略建议

## 安装与部署

### 环境要求

- Python 3.10+
- Ollama (本地大语言模型服务)
- FastAPI
- OpenAI Python SDK
- Uvicorn

### 安装步骤

1. **安装依赖**

```bash
pip install -r requirements.txt
```

2. **启动Ollama服务**

确保Ollama服务已在本地启动并监听11434端口：

```bash
ollama serve
```

3. **启动模型API服务**

```bash
python main.py
```

服务将在 `http://localhost:8700` 启动，API文档可通过 `http://localhost:8700/docs` 访问。

4. **启动智能学习网络**

```bash
cd my_first_network
# 使用网络启动脚本
```

## API接口

### 模型服务接口

#### 1. 聊天接口

```
POST /api/model/chat
```

**请求参数**：
- `prompt`: 聊天提示词
- `model`: 使用的模型（可选，默认qwen:7b）
- `max_tokens`: 最大输出token数（可选，默认1024）
- `temp`: 温度参数（可选，默认0.7）

**响应示例**：
```json
{
  "choices": [
    {
      "message": {
        "content": "这是模型的响应内容...",
        "role": "assistant"
      }
    }
  ]
}
```

#### 2. 流式聊天接口

```
POST /api/model/chat/stream
```

**请求参数**：同聊天接口

**响应**：流式文本响应

#### 3. 健康检查

```
GET /health
```

**响应示例**：
```json
{"status": "healthy"}
```

## 配置管理

### LLM配置

LLM配置文件位于 `my_first_network/llm_config.py`，可配置以下内容：

- CloseAI API密钥
- 模型选择
- 代理设置
- 其他LLM相关参数

### 网络配置

网络配置文件位于 `my_first_network/network.yaml`，可配置：

- 网络名称和模式
- 通信协议和端口
- 模块启用状态
- 消息通道设置

## 使用示例

### 1. 调用本地模型服务

```python
import requests

# 调用聊天接口
response = requests.post(
    "http://localhost:8700/api/model/chat",
    json={
        "prompt": "请解释一下深度学习的基本原理",
        "model": "qwen:7b",
        "max_tokens": 512
    }
)

print(response.json()['choices'][0]['message']['content'])
```

### 2. 启动学习辅助代理

```bash
# 启动学习辅助网络
python -m openagents.network run my_first_network/network.yaml
```

## 故障排除

### 常见问题

1. **Ollama服务未启动**
   - 错误信息：`Ollama服务未启动，请检查11434端口`
   - 解决方法：确保Ollama服务已启动并监听11434端口

2. **模型加载失败**
   - 错误信息：`模型加载失败`
   - 解决方法：确认指定的模型已在Ollama中下载

3. **网络连接问题**
   - 错误信息：`网络连接失败`
   - 解决方法：检查网络配置和端口是否正确

## 相关文档

- [部署指南](DEPLOYMENT.md)
- [服务器部署指南](DEPLOYMENT_TO_SERVER.md)
- [健康检查故障排除](HEALTH_CHECK_FAILURE_TROUBLESHOOTING.md)
- [内网连接故障排除](INTRANET_CONNECTION_TROUBLESHOOTING.md)
- [Windows SCP使用指南](WINDOWS_SCP_GUIDE.md)

## 开发与扩展

### 开发新代理

1. 在 `my_first_network/agents/` 目录下创建新的代理文件
2. 定义代理类，继承自基础代理类
3. 实现代理的核心功能方法
4. 在网络配置中注册新代理

### 扩展模型服务

1. 修改 `model_router.py` 添加新的API接口
2. 实现自定义模型调用逻辑
3. 更新依赖和配置文件

## 许可证

[MIT License](LICENSE)