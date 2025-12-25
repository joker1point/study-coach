# OpenAgents控制台发布问题解决方案

## 问题分析

从控制台截图和网络日志分析，发现健康检查失败的原因是：

### 错误的URL格式
日志显示请求的URL是：
```
GET /:8700/api/health HTTP/1.1 404
```

**这是错误的URL格式！** 正确的URL应该是：
```
GET /api/health HTTP/1.1 200
```

### 问题根源
从OpenAgents控制台截图可以看到，"**网络主持人**"字段中输入的域名包含了**尾部斜杠**：
```
1nz171374pe64.vicp.fun/
```

这导致OpenAgents控制台在构建健康检查URL时出现拼接错误：
```
# 错误的拼接结果
http://1nz171374pe64.vicp.fun/:8700/api/health

# 正确的拼接结果应该是
http://1nz171374pe64.vicp.fun:8700/api/health
```

## 解决方案

### 1. 修复控制台输入格式
在OpenAgents控制台中：

- **网络主持人**字段：删除尾部斜杠
  ✅ 正确：`1nz171374pe64.vicp.fun`
  ❌ 错误：`1nz171374pe64.vicp.fun/`

- **网络端口**字段：保持为`8700`

### 2. 确认花生壳配置
确保花生壳客户端的端口映射配置正确：
- 内网主机：本地IP地址（如192.168.x.x）
- 内网端口：8700
- 外网端口：8700
- 映射类型：HTTP

### 3. 验证修复

1. **检查本地服务**
```bash
curl.exe -s http://localhost:8700/api/health
# 应该返回健康状态
```

2. **重新发布网络**
在OpenAgents控制台中重新点击"发布"按钮。

## 其他可能的问题

### 花生壳域名访问超时
如果修复格式后仍然失败，可能是花生壳网络问题：

1. **测试花生壳连接**
```bash
# 测试TCP连接
telnet 1nz171374pe64.vicp.fun 8700

# 或者使用PowerShell测试
Test-NetConnection -ComputerName 1nz171374pe64.vicp.fun -Port 8700
```

2. **临时解决方案：使用ngrok**
```bash
# 安装并运行ngrok
ngrok http 8700

# 然后在控制台中使用ngrok提供的域名
# 例如：http://abc123.ngrok.io
```

## 总结

主要问题是OpenAgents控制台中"网络主持人"字段的格式错误（包含尾部斜杠）导致URL拼接失败。修复这个输入格式后，健康检查应该能够正常通过。