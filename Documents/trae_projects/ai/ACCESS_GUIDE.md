# OpenAgents 智能体系统访问指南

## 系统状态概览

✅ **服务已成功配置为外部访问**

### 网络配置
- **服务IP地址**: `192.168.4.179`
- **HTTP端口**: `8700`
- **gRPC端口**: `8600`
- **网络模式**: 已配置为监听 `0.0.0.0` (支持外部访问)

### 端口状态
```
HTTP 端口 8700: ✅ 开放
gRPC 端口 8600: ✅ 开放
```

## 如何访问系统

### 1. Web前端界面（推荐）

OpenAgents提供了一个内置的Web可视化界面，可以轻松管理和监控智能体网络。

**访问地址：** `http://192.168.4.179:8050`

**连接步骤：**
1. 打开浏览器，访问上述地址
2. 在"手动连接"部分填写：
   - 主机：`192.168.4.179`（或`localhost`）
   - 端口：`8700`
3. 确保"通过SSL连接"选项未勾选
4. 点击"连接"按钮

**主要功能：**
- 智能体状态监控
- 消息历史查看
- 网络拓扑可视化
- 智能体交互界面
- 系统性能监控

**详细连接指南：** 请参考 `STUDIO_CONNECTION_GUIDE.md` 文件获取更详细的使用说明。

### 2. 智能体交互

#### 通过OpenAgents CLI工具访问
```bash
# 连接到网络
openagents network interact 192.168.4.179:8700

# 发送消息到特定智能体
exec --agent tutoring_agent --message "你好，我需要帮助学习Python"
```

#### 通过gRPC客户端访问
```bash
# 使用grpcurl（需安装）
grpcurl -plaintext 192.168.4.179:8600 list

# 发送请求示例
grpcurl -plaintext -d '{"agent_id":"tutoring_agent","message":"学习Python的基础知识"}' 192.168.4.179:8600 openagents.core.v1.AgentService/Execute
```

### 2. 系统监控

#### 查看运行中的智能体
```bash
# 在服务器端执行
openagents agent list
```

#### 查看网络状态
```bash
# 在服务器端执行
openagents network status
```

### 3. 防火墙配置（如果需要）

如果系统运行在有防火墙的环境中，需要开放以下端口：

**Windows防火墙配置**：
1. 打开「Windows Defender 防火墙」
2. 点击「高级设置」
3. 点击「入站规则」→「新建规则」
4. 选择「端口」→ 下一步
5. 选择「TCP」，输入「8600,8700」→ 下一步
6. 选择「允许连接」→ 下一步
7. 选择适用的网络类型 → 下一步
8. 命名规则（如「OpenAgents Services」）→ 完成

## 可用的智能体

系统已部署以下智能体，可通过上述方式访问：

| 智能体名称 | 功能描述 |
|-----------|---------|
| `tutoring_agent` | 个性化学习辅导智能体 |
| `diagnosis_agent` | 学习诊断智能体 |
| `planning_agent` | 学习计划制定智能体 |
| `review_agent` | 学习进度回顾智能体 |
| `simple_agent` | 简单对话智能体 |
| `custom_agent` | 自定义智能体 |
| `custom_agent_v2` | 自定义智能体v2 |
| `llm_agent` | 基础LLM智能体 |

## 测试工具

系统包含一个测试脚本，用于验证服务状态：

```bash
python test_grpc_service.py
```

## 多容器部署（备选方案）

如果需要使用Docker容器化部署，可通过以下命令启动：

```bash
docker-compose up -d
```

这将启动所有智能体和网络服务，端口映射与上述配置一致。

## 常见问题

### 问题：无法访问服务
**解决方案**：
1. 检查IP地址是否正确
2. 确认防火墙已开放相应端口
3. 验证服务是否正在运行：`openagents network status`

### 问题：智能体无响应
**解决方案**：
1. 检查智能体是否正在运行：`openagents agent list`
2. 重启无响应的智能体：`openagents agent restart <agent_id>`

### 问题：gRPC连接失败
**解决方案**：
1. 确认gRPC端口（8600）已开放
2. 检查客户端与服务器的网络连接
3. 验证gRPC服务状态：`python test_grpc_service.py`

## 技术支持

如需技术支持，请提供以下信息：
1. 操作系统版本
2. OpenAgents版本
3. 错误日志（可从 `openagents.log` 获取）
4. 测试结果（`python test_grpc_service.py` 的输出）

---

**系统已准备就绪，可以开始使用！** 🎉