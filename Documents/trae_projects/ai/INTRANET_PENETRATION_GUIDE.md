# OpenAgents 内网穿透配置指南

## 网络配置信息

### 本地 OpenAgents 网络配置

从您的 `network.yaml` 文件中，我获取到以下信息：

- **HTTP 服务**: 运行在 `0.0.0.0:8700` 端口
- **gRPC 服务**: 运行在 `localhost:8600` 端口
- **认证类型**: `none` (无需认证)

### 本地 IP 地址

从您的网络配置中，我检测到您的本地 IPv4 地址为：**192.168.91.179**

## 内网穿透配置步骤

根据您提供的内网穿透界面截图，您已经有一个内网穿透服务在运行。现在需要为 OpenAgents 网络添加新的映射。

### 1. 添加新的映射

在您的内网穿透界面中，点击"添加映射"按钮：

### 2. 配置映射信息

根据您的 OpenAgents 网络配置，填写以下信息：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **映射名称** | `OpenAgents` | 用于标识这个映射 |
| **映射类型** | `HTTP` | 选择 HTTP 协议 |
| **内网地址** | `192.168.91.179` | 您的本地 IP 地址 |
| **内网端口** | `8700` | OpenAgents HTTP 服务端口 |
| **外网地址** | 系统自动分配 | 或选择您现有的域名 |

### 3. 确认映射配置

配置完成后，您的映射应该类似于：

```
映射名称: OpenAgents
映射类型: HTTP
外网地址: http://您的域名.vicp.fun
内网地址: 192.168.91.179:8700
```

## 验证内网穿透连接

### 1. 检查映射状态

在内网穿透界面中，确认新添加的 OpenAgents 映射状态为"在线"或"已连接"。

### 2. 测试连接

在浏览器中访问分配的外网地址（例如：http://您的域名.vicp.fun），您应该能够看到 OpenAgents 网络的界面。

### 3. 使用 OpenAgents Studio 连接

在 OpenAgents Studio 中，您可以使用分配的外网地址连接到您的网络：

1. 打开 OpenAgents Studio
2. 点击"连接到网络"
3. 输入您的外网地址（例如：http://您的域名.vicp.fun）
4. 点击"连接"

## 注意事项

1. **端口冲突**: 确保本地 8700 端口没有被其他程序占用
2. **防火墙设置**: 确保 Windows 防火墙允许 8700 端口的入站连接
3. **网络稳定性**: 内网穿透依赖于您的网络稳定性，如果遇到连接问题，可以尝试重启内网穿透服务
4. **HTTPS 配置**: 如果需要使用 HTTPS，可以在内网穿透配置中启用 HTTPS 选项

## 故障排除

### 问题：无法访问外网地址

1. 检查内网穿透服务是否正常运行
2. 确认映射状态为"在线"
3. 检查本地 OpenAgents 网络是否正常运行：
   ```bash
   # 在终端中运行
   openagents network status ./my_first_network
   ```

### 问题：OpenAgents Studio 无法连接

1. 确认外网地址格式正确（包含完整的 URL，例如：http://您的域名.vicp.fun）
2. 检查网络防火墙设置
3. 尝试重启 OpenAgents 网络：
   ```bash
   # 停止网络
   openagents network stop ./my_first_network
   
   # 启动网络
   openagents network start ./my_first_network
   ```

## 更新 OpenAgents 网络配置

如果您需要更新 OpenAgents 网络配置以使用内网穿透地址，可以修改 `network.yaml` 文件中的 `network_profile` 部分：

```yaml
network_profile:
  # ...
  host: "您的外网域名.vicp.fun"
  port: 80  # 或您的外网端口
```

修改后，重启 OpenAgents 网络：

```bash
openagents network restart ./my_first_network
```

---

完成配置后，您的 OpenAgents 网络将可以通过内网穿透服务从外部访问。如果您在配置过程中遇到任何问题，请随时向我咨询！