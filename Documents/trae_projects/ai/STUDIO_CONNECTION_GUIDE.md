# OpenAgents Studio 连接指南

## 连接到OpenAgents网络

1. **打开OpenAgents Studio界面**
   - 访问地址：http://192.168.4.179:8050

2. **选择连接方式**
   
   ### 方式一：手动连接（推荐）
   - 在"手动连接"部分，填写以下信息：
     - 主机：192.168.4.179（或输入localhost）
     - 端口：8700
   - 确保"通过SSL连接"选项未勾选
   - 点击"连接"按钮

   ### 方式二：本地网络连接
   - 在"本地网络"部分，点击"连接"按钮
   - 这将自动连接到运行在同一台机器上的OpenAgents网络

3. **验证连接**
   - 连接成功后，界面将显示网络状态为"已连接"
   - 您将看到可用的智能体列表和网络拓扑图

## 开始使用智能体系统

### 1. 查看智能体列表
- 连接成功后，在"智能体"标签页中可以看到所有可用的智能体
- 您的系统中部署了以下智能体：
  - diagnosis_agent（诊断智能体）
  - planning_agent（规划智能体）
  - tutoring_agent（辅导智能体）
  - review_agent（复盘智能体）
  - custom_agent（自定义智能体）
  - custom_agent_v2（自定义智能体v2）
  - simple_agent（简单智能体）

### 2. 与智能体交互
- 点击任意智能体卡片，进入智能体交互界面
- 在消息输入框中输入您的问题或指令
- 点击"发送"按钮，与智能体进行对话

### 3. 监控智能体通信
- 在"消息"标签页中，可以查看智能体之间的通信历史
- 您可以跟踪智能体之间的协作过程

### 4. 查看网络拓扑
- 在"拓扑"标签页中，可以查看智能体网络的结构
- 您可以直观地看到智能体之间的连接关系

## 常见问题

### 连接失败怎么办？
1. 检查OpenAgents网络服务是否正在运行：
   ```bash
   openagents network status my_first_network
   ```
2. 检查端口8700是否被占用：
   ```bash
   netstat -an | findstr 8700
   ```
3. 确保防火墙允许端口8700的访问

### 智能体不响应怎么办？
1. 检查智能体是否正在运行：
   ```bash
   ps aux | grep agent.py
   ```
2. 重启不响应的智能体：
   ```bash
   python .\my_first_network\agents\[agent_name].py
   ```
3. 查看智能体日志文件：
   ```bash
   cd my_first_network/logs
   dir
   ```

## 学习资源

- [OpenAgents 官方文档](https://openagents.org/docs/)
- [智能体开发指南](https://openagents.org/docs/developers/)
- [网络配置教程](https://openagents.org/docs/network/)

祝您使用OpenAgents Studio愉快！