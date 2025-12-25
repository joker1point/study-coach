# 学生个性化伴学多智能体系统部署指南

## 系统概述

学生个性化伴学多智能体系统是一个基于OpenAgents框架开发的教育AI应用，包含多个智能体协同工作：

- **学情分析Agent**：分析学生作业和学习数据，识别知识盲点
- **任务规划Agent**：根据学情分析结果，生成个性化学习计划
- **答疑辅导Agent**：为学生提供实时答疑和针对性讲解
- **复盘总结Agent**：汇总学习数据，生成学习进度报告

## 部署前准备

### 硬件要求
- CPU：至少4核
- 内存：至少8GB
- 磁盘空间：至少20GB可用空间

### 软件要求
- Docker 20.10.0+ 及 Docker Compose 1.29.0+
- Python 3.10+ (仅用于手动部署)

## 环境变量配置

在部署前，需要配置以下环境变量：

| 环境变量名 | 描述 | 默认值 |
|------------|------|--------|
| OPENAGENTS_JWT_SECRET | JWT认证密钥 | default_secret_key_change_in_production |
| OPENAGENTS_HOST | 网络服务主机地址 | 0.0.0.0 |

## Docker 部署 (推荐)

### 1. 克隆项目

```bash
git clone <项目仓库地址>
cd <项目目录>
```

### 2. 构建Docker镜像

```bash
docker-compose build
```

### 3. 配置环境变量

创建 `.env` 文件，配置必要的环境变量：

```env
OPENAGENTS_JWT_SECRET=your_secure_jwt_secret_key_here
OPENAGENTS_HOST=network-server
```

### 4. 启动系统

```bash
docker-compose up -d
```

这将启动以下容器：
- openagents-network-server (网络服务)
- openagents-diagnosis-agent (学情分析Agent)
- openagents-planning-agent (任务规划Agent)
- openagents-tutoring-agent (答疑辅导Agent)
- openagents-review-agent (复盘总结Agent)
- openagents-custom-agent (自定义Agent)
- openagents-custom-agent-v2 (自定义Agent V2)
- openagents-simple-agent (简单Agent)

### 5. 验证部署

检查容器状态：

```bash
docker-compose ps
```

查看日志：

```bash
docker-compose logs -f
```

### 6. 停止系统

```bash
docker-compose down
```

## 手动部署

### 1. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置网络

修改 `my_first_network/network.yaml` 文件，配置网络参数：

```yaml
network:
  name: "ProductionNetwork"
  # 其他配置...

network_profile:
  # ...
  authentication:
    type: "jwt"
    config:
      secret_key: "your_secure_jwt_secret_key_here"
  host: "0.0.0.0"
  # ...
```

### 4. 启动网络服务

```bash
python -m openagents.network.server --network-config ./my_first_network/network.yaml
```

### 5. 启动各个智能体

在不同的终端窗口中分别启动：

```bash
# 学情分析Agent
python ./my_first_network/agents/diagnosis_agent.py

# 任务规划Agent
python ./my_first_network/agents/planning_agent.py

# 答疑辅导Agent
python ./my_first_network/agents/tutoring_agent.py

# 复盘总结Agent
python ./my_first_network/agents/review_agent.py
```

## 系统管理

### 查看智能体状态

使用 `openagents` 命令行工具查看智能体状态：

```bash
openagents network list-agents --host <host> --port <port>
```

### 发送消息到智能体

```bash
openagents agent send --agent <agent_id> --host <host> --port <port> --message "<your_message>"
```

## 故障排除

### 问题：网络服务无法启动

**可能原因**：端口被占用

**解决方案**：检查端口8600和8700是否被占用

```bash
# Linux/macOS
lsof -i :8600
lsof -i :8700

# Windows
netstat -ano | findstr :8600
netstat -ano | findstr :8700
```

### 问题：智能体无法连接到网络服务

**可能原因**：
1. 网络服务未完全启动
2. 环境变量配置错误
3. 网络连接问题

**解决方案**：
1. 检查网络服务日志
2. 确保环境变量 `OPENAGENTS_HOST` 配置正确
3. 检查容器间网络连接

### 问题：智能体响应缓慢

**可能原因**：
1. 系统资源不足
2. API调用延迟
3. 网络拥堵

**解决方案**：
1. 增加系统资源
2. 检查API密钥配置
3. 优化网络连接

## 系统监控

### Docker监控

```bash
# 查看系统资源使用情况
docker stats

# 查看容器日志
docker-compose logs -f <服务名>
```

### 网络服务监控

网络服务提供健康检查端点：

```
http://<host>:8700/health
```

## 更新系统

### Docker部署更新

```bash
docker-compose pull
# 或
docker-compose build --no-cache
docker-compose up -d
```

### 手动部署更新

```bash
# 拉取最新代码
git pull

# 安装新依赖
pip install -r requirements.txt

# 重启网络服务和智能体
```

## 安全建议

1. **生产环境中必须更改默认的JWT密钥**
2. **启用HTTPS**：在生产环境中使用反向代理（如Nginx）启用HTTPS
3. **限制访问**：配置防火墙规则，只允许必要的IP访问系统
4. **定期备份数据**：定期备份 `/var/data/openagents` 目录

## 联系我们

如果在部署过程中遇到问题，请联系技术支持团队。

---

**版本**: 1.0.0
**最后更新**: 2024年1月13日